"""Distributed Spark ETL Pipeline for Urban Air Quality Analytics.

Loads raw OpenAQ hourly observations from HDFS, applies schema validation,
unit harmonization, 24-hour / 8-hour rolling window calculations, CPCB NAQI
sub-index and composite AQI calculation, and persists partitioned Parquet
to HDFS /air_quality/processed/.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# Ensure Java 17 for Spark 4.2.0 compatibility
os.environ["JAVA_HOME"] = "/opt/homebrew/Cellar/openjdk@17/17.0.20.1/libexec/openjdk.jdk/Contents/Home"
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession, Window
import pyspark.sql.functions as F
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(WORKSPACE_ROOT))

from scripts.cpcb_aqi import calculate_cpcb_aqi, calculate_sub_index

HDFS_RAW_PATH = "hdfs://localhost:9000/air_quality/raw/raw_hourly_measurements.jsonl"
LOCAL_RAW_PATH = str(WORKSPACE_ROOT / "data" / "raw" / "raw_hourly_measurements.jsonl")
HDFS_PROCESSED_PATH = "hdfs://localhost:9000/air_quality/processed/hourly_aqi_parquet"
LOCAL_PROCESSED_PATH = str(WORKSPACE_ROOT / "data" / "processed" / "hourly_aqi_parquet")


def create_spark_session() -> SparkSession:
    """Create and configure optimized PySpark session."""
    return (
        SparkSession.builder.appName("UrbanAirQualityDistributedETL")
        .master("local[*]")
        .config("spark.driver.memory", "4g")
        .config("spark.executor.memory", "4g")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.default.parallelism", "8")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )


def define_raw_schema() -> StructType:
    """Define explicit schema for raw JSON ingestion."""
    return StructType([
        StructField("location_id", IntegerType(), True),
        StructField("station_name", StringType(), True),
        StructField("city", StringType(), True),
        StructField("sensor_id", IntegerType(), True),
        StructField("parameter", StringType(), True),
        StructField("units", StringType(), True),
        StructField("datetime_from_utc", StringType(), True),
        StructField("datetime_to_utc", StringType(), True),
        StructField("datetime_local", StringType(), True),
        StructField("value", DoubleType(), True),
        StructField("avg_value", DoubleType(), True),
        StructField("min_value", DoubleType(), True),
        StructField("max_value", DoubleType(), True),
        StructField("std_dev", DoubleType(), True),
        StructField("percent_complete", DoubleType(), True),
        StructField("observed_count", IntegerType(), True),
        StructField("expected_count", IntegerType(), True),
        StructField("ingested_at", StringType(), True),
    ])


def run_etl(use_hdfs: bool = True) -> None:
    """Execute end-to-end distributed ETL pipeline."""
    start_time = time.time()
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    print("\n================ STARTING DISTRIBUTED SPARK ETL ================")
    print(f"Apache Spark Version: {spark.version}")

    # 1. Distributed Ingestion
    raw_source = HDFS_RAW_PATH if use_hdfs else LOCAL_RAW_PATH
    print(f"[1/6] Ingesting raw dataset from: {raw_source}")
    try:
        raw_df = spark.read.schema(define_raw_schema()).json(raw_source)
        raw_count = raw_df.count()
        print(f"  Ingested {raw_count:,} raw records.")
    except Exception as e:
        print(f"  HDFS read failed ({e}), falling back to local dataset: {LOCAL_RAW_PATH}")
        raw_df = spark.read.schema(define_raw_schema()).json(LOCAL_RAW_PATH)
        raw_count = raw_df.count()
        print(f"  Ingested {raw_count:,} raw records from local storage.")

    # 2. Schema Validation & Data Cleansing
    print("\n[2/6] Cleaning data and enforcing validity constraints...")
    # Deduplicate on location, sensor, timestamp
    dedup_df = raw_df.dropDuplicates(["location_id", "sensor_id", "datetime_from_utc"])
    dedup_count = dedup_df.count()
    print(f"  Records after deduplication: {dedup_count:,} (Removed {raw_count - dedup_count:,} duplicates)")

    # Filter invalid physical concentrations (< 0 or extreme equipment errors)
    cleaned_df = dedup_df.filter(
        (F.col("value").isNotNull()) &
        (F.col("value") >= 0.0) &
        (F.col("value") < 5000.0)  # Filter extreme hardware glitches
    )

    # 3. Timestamp Normalization & Unit Harmonization
    print("\n[3/6] Normalizing timestamps to IST and harmonizing pollutant units...")
    # OpenAQ timestamp to TimestampType
    normalized_df = cleaned_df.withColumn(
        "ts_utc", F.to_timestamp("datetime_from_utc", "yyyy-MM-dd'T'HH:mm:ss'Z'")
    ).withColumn(
        # Convert UTC to IST (+5:30)
        "ts_ist", F.from_utc_timestamp("ts_utc", "Asia/Kolkata")
    ).withColumn(
        "year", F.year("ts_ist")
    ).withColumn(
        "month", F.month("ts_ist")
    ).withColumn(
        "day", F.dayofmonth("ts_ist")
    ).withColumn(
        "hour", F.hour("ts_ist")
    ).withColumn(
        "day_of_week", F.dayofweek("ts_ist")
    )

    # Convert volume units (ppb, ppm) to mass concentrations (µg/m³, mg/m³) for CPCB calculation
    # Standard ambient conversions at 25°C, 1 atm:
    # NO2 (µg/m³) = ppb * 1.88
    # SO2 (µg/m³) = ppb * 2.62
    # CO  (mg/m³) = ppb * 0.001145 (or ppm * 1.145)
    # O3  (µg/m³) = ppb * 1.96
    harmonized_df = normalized_df.withColumn(
        "harmonized_val",
        F.when((F.col("parameter") == "no2") & (F.col("units") == "ppb"), F.col("value") * 1.88)
        .when((F.col("parameter") == "so2") & (F.col("units") == "ppb"), F.col("value") * 2.62)
        .when((F.col("parameter") == "co") & (F.col("units") == "ppb"), F.col("value") * 0.001145)
        .when((F.col("parameter") == "co") & (F.col("units") == "ppm"), F.col("value") * 1.145)
        .when((F.col("parameter") == "o3") & (F.col("units") == "ppb"), F.col("value") * 1.96)
        .otherwise(F.col("value")),
    )

    # 4. Multi-Pollutant Station-Hour Pivot
    print("\n[4/6] Reshaping and pivoting pollutants into hourly station records...")
    pivoted_df = (
        harmonized_df.groupBy("location_id", "station_name", "city", "ts_ist", "year", "month", "day", "hour", "day_of_week")
        .pivot("parameter", ["pm25", "pm10", "no2", "so2", "co", "o3", "temperature", "relativehumidity"])
        .agg(F.avg("harmonized_val"))
    )

    # 5. CPCB Rolling Windows & NAQI Calculation
    print("\n[5/6] Calculating rolling exposure windows and CPCB NAQI...")
    # Time-series window per station ordered chronologically
    win_24h = (
        Window.partitionBy("location_id")
        .orderBy(F.col("ts_ist").cast("long"))
        .rangeBetween(-23 * 3600, 0)
    )
    win_8h = (
        Window.partitionBy("location_id")
        .orderBy(F.col("ts_ist").cast("long"))
        .rangeBetween(-7 * 3600, 0)
    )

    # Calculate 24-hr averages for PM2.5, PM10, NO2, SO2 and 8-hr for CO, O3
    # Also count valid non-null hourly observations in the 24h window (CPCB requires >= 16 hrs)
    windowed_df = (
        pivoted_df.withColumn("pm25_24h", F.avg("pm25").over(win_24h))
        .withColumn("pm25_count_24h", F.count("pm25").over(win_24h))
        .withColumn("pm10_24h", F.avg("pm10").over(win_24h))
        .withColumn("pm10_count_24h", F.count("pm10").over(win_24h))
        .withColumn("no2_24h", F.avg("no2").over(win_24h))
        .withColumn("so2_24h", F.avg("so2").over(win_24h))
        .withColumn("co_8h", F.avg("co").over(win_8h))
        .withColumn("o3_8h", F.avg("o3").over(win_8h))
    )

    # Filter windows with at least 16 valid hours of particulate data per CPCB rule
    valid_windowed_df = windowed_df.withColumn(
        "is_window_valid_16h",
        (F.col("pm25_count_24h") >= 16) | (F.col("pm10_count_24h") >= 16)
    )

    # Vectorized UDF for CPCB calculation
    aqi_schema = StructType([
        StructField("aqi", DoubleType(), True),
        StructField("health_category", StringType(), True),
        StructField("prominent_pollutant", StringType(), True),
        StructField("category_code", IntegerType(), True),
        StructField("sub_index_pm25", DoubleType(), True),
        StructField("sub_index_pm10", DoubleType(), True),
        StructField("sub_index_no2", DoubleType(), True),
        StructField("sub_index_so2", DoubleType(), True),
        StructField("sub_index_co", DoubleType(), True),
        StructField("sub_index_o3", DoubleType(), True),
    ])

    @F.udf(returnType=aqi_schema)
    def compute_cpcb_udf(pm25, pm10, no2, so2, co, o3, is_valid_16h):
        if not is_valid_16h:
            return (None, None, None, None, None, None, None, None, None, None)
        conc_dict = {
            "pm25": pm25,
            "pm10": pm10,
            "no2": no2,
            "so2": so2,
            "co": co,
            "o3": o3,
        }
        aqi, cat, prom, code, sub_indices = calculate_cpcb_aqi(conc_dict)
        return (
            aqi,
            cat,
            prom,
            code,
            sub_indices.get("pm25"),
            sub_indices.get("pm10"),
            sub_indices.get("no2"),
            sub_indices.get("so2"),
            sub_indices.get("co"),
            sub_indices.get("o3"),
        )

    enriched_df = valid_windowed_df.withColumn(
        "cpcb_result",
        compute_cpcb_udf(
            F.col("pm25_24h"),
            F.col("pm10_24h"),
            F.col("no2_24h"),
            F.col("so2_24h"),
            F.col("co_8h"),
            F.col("o3_8h"),
            F.col("is_window_valid_16h"),
        ),
    ).select(
        "location_id",
        "station_name",
        "city",
        "ts_ist",
        "year",
        "month",
        "day",
        "hour",
        "day_of_week",
        "pm25",
        "pm10",
        "no2",
        "so2",
        "co",
        "o3",
        "temperature",
        "relativehumidity",
        "pm25_24h",
        "pm10_24h",
        "no2_24h",
        "so2_24h",
        "co_8h",
        "o3_8h",
        "is_window_valid_16h",
        F.col("cpcb_result.aqi").alias("cpcb_aqi"),
        F.col("cpcb_result.health_category").alias("health_category"),
        F.col("cpcb_result.prominent_pollutant").alias("prominent_pollutant"),
        F.col("cpcb_result.category_code").alias("category_code"),
        F.col("cpcb_result.sub_index_pm25").alias("sub_index_pm25"),
        F.col("cpcb_result.sub_index_pm10").alias("sub_index_pm10"),
    )

    enriched_df.cache()
    total_hourly_records = enriched_df.count()
    valid_aqi_records = enriched_df.filter(F.col("cpcb_aqi").isNotNull()).count()

    print(f"  Total Station-Hour Records Processed: {total_hourly_records:,}")
    print(f"  Records Meeting Strict CPCB 16h NAQI Validity: {valid_aqi_records:,}")

    # Display sample output
    print("\n--- Sample Processed Station Records with CPCB AQI ---")
    enriched_df.filter(F.col("cpcb_aqi").isNotNull()).select(
        "city", "station_name", "ts_ist", "pm25_24h", "pm10_24h", "cpcb_aqi", "health_category", "prominent_pollutant"
    ).show(5, truncate=False)

    # 6. Parquet Output Storage
    print("\n[6/6] Persisting partitioned Parquet dataset to storage...")
    # Write to local processed dir
    Path(LOCAL_PROCESSED_PATH).parent.mkdir(parents=True, exist_ok=True)
    enriched_df.write.mode("overwrite").partitionBy("city", "year").parquet(LOCAL_PROCESSED_PATH)
    print(f"  Local Parquet saved to: {LOCAL_PROCESSED_PATH}")

    # Also persist directly into HDFS if available
    if use_hdfs:
        try:
            enriched_df.write.mode("overwrite").partitionBy("city", "year").parquet(HDFS_PROCESSED_PATH)
            print(f"  HDFS Partitioned Parquet saved to: {HDFS_PROCESSED_PATH}")
        except Exception as ex:
            print(f"  Notice: Direct HDFS write skipped: {ex}")

    elapsed = time.time() - start_time
    print(f"\nSpark ETL Pipeline completed successfully in {elapsed:.2f} seconds.")
    spark.stop()


if __name__ == "__main__":
    run_etl(use_hdfs=True)
