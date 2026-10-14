"""Distributed CPCB Health Hazard Classification Pipeline using Spark MLlib.

Predicts the CPCB categorical hazard tier (Good through Severe) 24 hours ahead
using distributed Spark MLlib RandomForestClassifier and MulticlassClassificationEvaluator.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

os.environ["JAVA_HOME"] = "/opt/homebrew/Cellar/openjdk@17/17.0.20.1/libexec/openjdk.jdk/Contents/Home"
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession, Window
import pyspark.sql.functions as F
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import StandardScaler, VectorAssembler

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_PATH = str(WORKSPACE_ROOT / "data" / "processed" / "hourly_aqi_parquet")
FIGURES_DIR = WORKSPACE_ROOT / "reports" / "figures"
DOCS_DIR = WORKSPACE_ROOT / "docs"


def create_spark() -> SparkSession:
    return (
        SparkSession.builder.appName("UrbanAirQualityMLlibClassification")
        .master("local[*]")
        .config("spark.driver.memory", "4g")
        .config("spark.sql.shuffle.partitions", "8")
        .getOrCreate()
    )


def run_classification():
    spark = create_spark()
    spark.sparkContext.setLogLevel("WARN")

    print("\n================ STARTING SPARK MLLIB CLASSIFICATION PIPELINE ================")
    df = spark.read.parquet(PROCESSED_PATH)

    # Time-series window for target lag
    win_station = Window.partitionBy("location_id").orderBy(F.col("ts_ist").cast("long"))

    # Lead 24h category code (0: Good, 1: Satisfactory, 2: Moderate, 3: Poor, 4: Very Poor, 5: Severe)
    feat_df = (
        df.withColumn("target_cat_code_24h", F.lead("category_code", 24).over(win_station))
        .withColumn("pm25_lag_1", F.lag("pm25", 1).over(win_station))
        .withColumn("pm25_lag_24", F.lag("pm25", 24).over(win_station))
        .withColumn("pm10_lag_1", F.lag("pm10", 1).over(win_station))
        .withColumn("pm10_lag_24", F.lag("pm10", 24).over(win_station))
        .withColumn("no2_lag_1", F.lag("no2", 1).over(win_station))
        .withColumn("is_weekend", F.when(F.col("day_of_week").isin([1, 7]), 1.0).otherwise(0.0))
    )

    clean_df = feat_df.filter(
        F.col("target_cat_code_24h").isNotNull() &
        F.col("category_code").isNotNull() &
        F.col("pm25_lag_1").isNotNull() &
        F.col("pm25_lag_24").isNotNull()
    ).fillna({
        "temperature": 25.0,
        "relativehumidity": 50.0,
        "pm10_lag_1": 60.0,
        "pm10_lag_24": 60.0,
        "no2_lag_1": 30.0,
    })

    total_samples = clean_df.count()
    print(f"Total usable classified samples: {total_samples:,}")

    # Chronological 80/20 train/test split
    sorted_df = clean_df.orderBy("ts_ist")
    split_idx = int(total_samples * 0.8)
    split_ts = sorted_df.select("ts_ist").collect()[split_idx]["ts_ist"]

    train_df = sorted_df.filter(F.col("ts_ist") <= split_ts).cache()
    test_df = sorted_df.filter(F.col("ts_ist") > split_ts).cache()

    feature_cols = [
        "pm25",
        "pm10",
        "no2",
        "so2",
        "co",
        "o3",
        "pm25_lag_1",
        "pm25_lag_24",
        "pm10_lag_1",
        "pm10_lag_24",
        "no2_lag_1",
        "temperature",
        "relativehumidity",
        "hour",
        "day_of_week",
        "is_weekend",
    ]

    assembler = VectorAssembler(inputCols=feature_cols, outputCol="raw_features", handleInvalid="skip")
    scaler = StandardScaler(inputCol="raw_features", outputCol="features", withMean=True, withStd=True)

    rf = RandomForestClassifier(
        featuresCol="features",
        labelCol="target_cat_code_24h",
        numTrees=50,
        maxDepth=8,
        seed=42,
    )

    pipeline = Pipeline(stages=[assembler, scaler, rf])

    print("Training distributed RandomForestClassifier...")
    t0 = time.time()
    model = pipeline.fit(train_df)
    train_duration = time.time() - t0

    pred_df = model.transform(test_df).cache()

    acc_eval = MulticlassClassificationEvaluator(labelCol="target_cat_code_24h", predictionCol="prediction", metricName="accuracy")
    f1_eval = MulticlassClassificationEvaluator(labelCol="target_cat_code_24h", predictionCol="prediction", metricName="f1")
    precision_eval = MulticlassClassificationEvaluator(labelCol="target_cat_code_24h", predictionCol="prediction", metricName="weightedPrecision")
    recall_eval = MulticlassClassificationEvaluator(labelCol="target_cat_code_24h", predictionCol="prediction", metricName="weightedRecall")

    accuracy = acc_eval.evaluate(pred_df)
    f1_score = f1_eval.evaluate(pred_df)
    precision = precision_eval.evaluate(pred_df)
    recall = recall_eval.evaluate(pred_df)

    print("\n--- Spark MLlib Classification Metrics ---")
    print(f"  Accuracy:           {accuracy*100:.2f}%")
    print(f"  Weighted F1-Score:  {f1_score:.3f}")
    print(f"  Weighted Precision: {precision:.3f}")
    print(f"  Weighted Recall:    {recall:.3f}")
    print(f"  Training Duration:  {train_duration:.2f}s")

    # Generate Confusion Matrix
    cm_rows = (
        pred_df.groupBy("target_cat_code_24h", "prediction")
        .count()
        .toPandas()
    )

    labels = ["Good (0)", "Satisfactory (1)", "Moderate (2)", "Poor (3)", "Very Poor (4)", "Severe (5)"]
    num_classes = 6
    cm_matrix = np.zeros((num_classes, num_classes), dtype=int)

    for _, row in cm_rows.iterrows():
        r = int(row["target_cat_code_24h"])
        c = int(row["prediction"])
        if 0 <= r < num_classes and 0 <= c < num_classes:
            cm_matrix[r, c] = int(row["count"])

    # Plot Confusion Matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm_matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=labels,
        yticklabels=labels,
    )
    plt.title("Spark MLlib CPCB Hazard Tier Classification Confusion Matrix", fontsize=12, fontweight="bold")
    plt.xlabel("Predicted Health Category", fontsize=11)
    plt.ylabel("True Observed Health Category", fontsize=11)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()

    cm_path = FIGURES_DIR / "cpcb_classification_confusion_matrix.png"
    plt.savefig(cm_path, dpi=200)
    plt.close()
    print(f"  Saved confusion matrix plot: {cm_path}")

    # Write report
    write_classification_report(accuracy, f1_score, precision, recall, train_duration, cm_matrix, labels)

    spark.stop()


def write_classification_report(acc, f1, prec, rec, duration, cm, labels):
    rep_path = DOCS_DIR / "CLASSIFICATION_EVALUATION_REPORT.md"
    md = []
    md.append("# Phase 5: CPCB Health Hazard Classification Report\n")
    md.append("**Model:** Spark MLlib `RandomForestClassifier` (50 trees, maxDepth=8)  ")
    md.append("**Target:** Future 24-Hour CPCB Air Quality Tier (0: Good to 5: Severe)  \n")
    md.append("---\n")
    md.append("## 1. Classification Performance Metrics\n")
    md.append(f"- **Test Accuracy:** `{acc*100:.2f}%`")
    md.append(f"- **Weighted F1-Score:** `{f1:.3f}`")
    md.append(f"- **Weighted Precision:** `{prec:.3f}`")
    md.append(f"- **Weighted Recall:** `{rec:.3f}`")
    md.append(f"- **Spark Cluster Training Time:** `{duration:.2f} seconds`\n")
    md.append("---\n")
    md.append("## 2. Confusion Matrix (True vs Predicted Counts)\n")
    md.append("| True Category \\ Pred | " + " | ".join(labels) + " |")
    md.append("| :--- | " + " | ".join([":---:"] * len(labels)) + " |")
    for idx, true_label in enumerate(labels):
        row_vals = " | ".join([str(cm[idx, c]) for c in range(len(labels))])
        md.append(f"| **{true_label}** | {row_vals} |")

    with open(rep_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print(f"Classification report written to: {rep_path}")


if __name__ == "__main__":
    run_classification()
