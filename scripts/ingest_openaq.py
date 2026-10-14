"""Production-grade Ingestion Engine for OpenAQ API v3.

Fetches location metadata, sensor metadata, and hourly historical measurements
for Indian CAAQMS ambient monitoring stations.
Supports:
- Checkpointed and resumable ingestion
- Strict rate-limit compliance (60 req/min)
- Exponential backoff and retry handling
- Raw JSON response persistence for data lineage
- Deduplicated JSONL / Parquet staging for HDFS ingestion
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
import requests

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
KEY_PATH = WORKSPACE_ROOT / "apikey.md"
DATA_RAW_DIR = WORKSPACE_ROOT / "data" / "raw"
LOGS_DIR = WORKSPACE_ROOT / "logs"

BASE_URL = "https://api.openaq.org/v3"

# Core Indian CAAQMS stations covering North, South, and Deccan plateau
TARGET_STATIONS = [
    {"id": 17, "city": "Delhi NCR", "name": "R K Puram, Delhi - DPCC"},
    {"id": 5509, "city": "Delhi NCR", "name": "Anand Vihar, Delhi - DPCC"},
    {"id": 5548, "city": "Bengaluru", "name": "BTM Layout, Bengaluru - CPCB"},
    {"id": 5623, "city": "Hyderabad", "name": "Central University, Hyderabad - TSPCB"},
]

CORE_PARAMETERS = {"pm25", "pm10", "no2", "so2", "co", "o3", "temperature", "relativehumidity"}


def setup_logger() -> logging.Logger:
    """Configure structured logger."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("openaq_ingestion")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        fh = logging.FileHandler(LOGS_DIR / "ingestion.log", encoding="utf-8")
        ch = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        fh.setFormatter(fmt)
        ch.setFormatter(fmt)
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger


logger = setup_logger()


def get_api_key() -> str:
    """Retrieve API key securely from env or apikey.md without exposing in logs."""
    key = os.getenv("OPENAQ_API_KEY")
    if key and key.strip():
        return key.strip()
    if KEY_PATH.exists():
        with open(KEY_PATH, "r", encoding="utf-8") as f:
            key = f.read().strip()
            if key:
                return key
    raise RuntimeError("OpenAQ API key not found. Store in apikey.md or set OPENAQ_API_KEY.")


class OpenAQClient:
    """HTTP Client with rate limiting and exponential backoff."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Accept": "application/json",
            "User-Agent": "UrbanAirQualityDistributedETL/1.0",
        })

    def request(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None, max_retries: int = 5
    ) -> Dict[str, Any]:
        url = f"{BASE_URL}/{endpoint.lstrip('/')}"
        delay = 1.0

        for attempt in range(max_retries):
            try:
                resp = self.session.get(url, params=params, timeout=25)

                # Inspect rate limit headers
                remaining = int(resp.headers.get("X-Ratelimit-Remaining", 60))
                reset_sec = int(resp.headers.get("X-Ratelimit-Reset", 10))

                if remaining < 3:
                    sleep_time = max(1.5, float(reset_sec))
                    logger.debug(f"Rate limit nearly exhausted ({remaining} left). Throttling {sleep_time:.1f}s")
                    time.sleep(sleep_time)

                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code == 429:
                    retry_after = int(resp.headers.get("Retry-After", reset_sec or 5))
                    logger.warning(f"Rate limit hit (429). Pausing for {retry_after} seconds (attempt {attempt+1}/{max_retries})")
                    time.sleep(retry_after + 1)
                    continue
                elif resp.status_code >= 500:
                    logger.warning(f"Server error {resp.status_code}. Retrying in {delay}s...")
                    time.sleep(delay)
                    delay *= 2
                    continue
                else:
                    logger.error(f"HTTP request failed with status {resp.status_code}: {resp.text[:200]}")
                    resp.raise_for_status()

            except (requests.RequestException, ValueError) as ex:
                if attempt == max_retries - 1:
                    logger.error(f"Request failed permanently for {endpoint}: {ex}")
                    raise
                logger.warning(f"Network error: {ex}. Retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2

        return {}


class IngestionPipeline:
    """Manages the full lifecycle of data extraction and checkpointing."""

    def __init__(self, client: OpenAQClient, sample_mode: bool = False, max_pages_per_sensor: int = 10):
        self.client = client
        self.sample_mode = sample_mode
        self.max_pages = 2 if sample_mode else max_pages_per_sensor

        # Output paths
        self.raw_responses_dir = DATA_RAW_DIR / "responses"
        self.raw_locations_dir = DATA_RAW_DIR / "locations"
        self.raw_sensors_dir = DATA_RAW_DIR / "sensors"
        self.checkpoint_file = DATA_RAW_DIR / ".checkpoint.json"
        self.output_jsonl = DATA_RAW_DIR / "raw_hourly_measurements.jsonl"

        for p in [self.raw_responses_dir, self.raw_locations_dir, self.raw_sensors_dir]:
            p.mkdir(parents=True, exist_ok=True)

        self.checkpoint = self._load_checkpoint()
        self.seen_record_keys: Set[str] = set()
        self._load_existing_keys()

    def _load_checkpoint(self) -> Dict[str, Any]:
        if self.checkpoint_file.exists():
            try:
                with open(self.checkpoint_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_checkpoint(self) -> None:
        with open(self.checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(self.checkpoint, f, indent=2)

    def _load_existing_keys(self) -> None:
        if self.output_jsonl.exists():
            with open(self.output_jsonl, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            rec = json.loads(line)
                            k = f"{rec.get('sensor_id')}_{rec.get('datetime_from_utc')}"
                            self.seen_record_keys.add(k)
                        except Exception:
                            pass
            logger.info(f"Loaded {len(self.seen_record_keys)} existing unique records into memory.")

    def run(self) -> Dict[str, Any]:
        logger.info(f"Starting ingestion pipeline (sample_mode={self.sample_mode}, max_pages={self.max_pages})")
        total_records_ingested = 0

        for station_info in TARGET_STATIONS:
            loc_id = station_info["id"]
            city = station_info["city"]
            st_name = station_info["name"]

            logger.info(f"--- Ingesting Station {loc_id}: {st_name} ({city}) ---")

            # 1. Fetch Location Metadata
            loc_data = self._ingest_location_metadata(loc_id, city, st_name)

            # 2. Fetch Sensor Metadata
            sensors = self._ingest_sensors_metadata(loc_id)
            logger.info(f"Discovered {len(sensors)} sensors for location {loc_id}")

            # 3. Ingest Hourly Measurements for target parameters
            for s in sensors:
                p_info = s.get("parameter", {})
                param_name = p_info.get("name")
                sensor_id = s.get("id")

                if param_name not in CORE_PARAMETERS:
                    continue

                rec_count = self._ingest_sensor_hours(
                    sensor_id=sensor_id,
                    location_id=loc_id,
                    city=city,
                    station_name=st_name,
                    param_name=param_name,
                    param_unit=p_info.get("units", ""),
                )
                total_records_ingested += rec_count

        logger.info(f"Ingestion complete. Total new records saved: {total_records_ingested}")
        logger.info(f"Master output: {self.output_jsonl} (Total unique keys: {len(self.seen_record_keys)})")

        return {
            "total_new_records": total_records_ingested,
            "total_unique_records": len(self.seen_record_keys),
            "output_path": str(self.output_jsonl),
        }

    def _ingest_location_metadata(self, loc_id: int, city: str, st_name: str) -> Dict[str, Any]:
        dest_file = self.raw_locations_dir / f"location_{loc_id}.json"
        if dest_file.exists():
            with open(dest_file, "r", encoding="utf-8") as f:
                return json.load(f)

        data = self.client.request(f"locations/{loc_id}")
        results = data.get("results", [])
        loc_record = results[0] if results else {"id": loc_id, "name": st_name, "city": city}
        loc_record["city"] = city

        with open(dest_file, "w", encoding="utf-8") as f:
            json.dump(loc_record, f, indent=2)

        return loc_record

    def _ingest_sensors_metadata(self, loc_id: int) -> List[Dict[str, Any]]:
        dest_file = self.raw_sensors_dir / f"sensors_loc_{loc_id}.json"
        if dest_file.exists():
            with open(dest_file, "r", encoding="utf-8") as f:
                return json.load(f)

        data = self.client.request(f"locations/{loc_id}/sensors")
        sensors = data.get("results", [])

        with open(dest_file, "w", encoding="utf-8") as f:
            json.dump(sensors, f, indent=2)

        return sensors

    def _ingest_sensor_hours(
        self,
        sensor_id: int,
        location_id: int,
        city: str,
        station_name: str,
        param_name: str,
        param_unit: str,
    ) -> int:
        sensor_key = str(sensor_id)
        last_page = self.checkpoint.get(sensor_key, {}).get("last_page", 0)

        # In sample mode, stop if already reached max pages
        if self.sample_mode and last_page >= self.max_pages:
            logger.debug(f"Sensor {sensor_id} ({param_name}) already sampled ({last_page} pages).")
            return 0

        current_page = last_page + 1
        sensor_records_added = 0

        while current_page <= self.max_pages:
            logger.info(f"Fetching Sensor {sensor_id} ({param_name}) Page {current_page}...")

            params = {"limit": 1000, "page": current_page}
            resp_data = self.client.request(f"sensors/{sensor_id}/hours", params=params)

            results = resp_data.get("results", [])
            if not results:
                logger.info(f"No further records for sensor {sensor_id} at page {current_page}.")
                self.checkpoint[sensor_key] = {"last_page": current_page - 1, "completed": True}
                self._save_checkpoint()
                break

            # Save raw API response for data lineage
            raw_resp_path = self.raw_responses_dir / f"sensor_{sensor_id}_page_{current_page}.json"
            with open(raw_resp_path, "w", encoding="utf-8") as f:
                json.dump(resp_data, f)

            # Transform into standardized records and append to JSONL
            records_to_append = []
            for item in results:
                period = item.get("period", {})
                dt_from = period.get("datetimeFrom", {})
                dt_to = period.get("datetimeTo", {})
                dt_from_utc = dt_from.get("utc")
                dt_from_local = dt_from.get("local")

                rec_key = f"{sensor_id}_{dt_from_utc}"
                if rec_key in self.seen_record_keys:
                    continue

                summary = item.get("summary") or {}
                coverage = item.get("coverage") or {}

                clean_record = {
                    "location_id": location_id,
                    "station_name": station_name,
                    "city": city,
                    "sensor_id": sensor_id,
                    "parameter": param_name,
                    "units": param_unit,
                    "datetime_from_utc": dt_from_utc,
                    "datetime_to_utc": dt_to.get("utc"),
                    "datetime_local": dt_from_local,
                    "value": item.get("value"),
                    "avg_value": summary.get("avg"),
                    "min_value": summary.get("min"),
                    "max_value": summary.get("max"),
                    "std_dev": summary.get("sd"),
                    "percent_complete": coverage.get("percentComplete"),
                    "observed_count": coverage.get("observedCount"),
                    "expected_count": coverage.get("expectedCount"),
                    "ingested_at": datetime.now(timezone.utc).isoformat(),
                }
                self.seen_record_keys.add(rec_key)
                records_to_append.append(clean_record)

            if records_to_append:
                with open(self.output_jsonl, "a", encoding="utf-8") as f:
                    for r in records_to_append:
                        f.write(json.dumps(r) + "\n")
                sensor_records_added += len(records_to_append)

            # Update checkpoint
            self.checkpoint[sensor_key] = {"last_page": current_page, "completed": len(results) < 1000}
            self._save_checkpoint()

            if len(results) < 1000:
                # Last available page reached
                break

            current_page += 1
            time.sleep(0.3)  # Gentle spacing

        return sensor_records_added


def main():
    parser = argparse.ArgumentParser(description="OpenAQ API v3 Ingestion Engine")
    parser.add_argument("--sample", action="store_true", help="Run in small sample mode to validate pipeline")
    parser.add_argument("--pages", type=int, default=10, help="Max pages per sensor (1 page = up to 1000 hours)")
    args = parser.parse_args()

    api_key = get_api_key()
    client = OpenAQClient(api_key=api_key)
    pipeline = IngestionPipeline(client, sample_mode=args.sample, max_pages_per_sensor=args.pages)
    summary = pipeline.run()

    print("\n================ INGESTION SUMMARY ================")
    print(f"Sample Mode: {args.sample}")
    print(f"New Records Ingested: {summary['total_new_records']}")
    print(f"Total Unique Records: {summary['total_unique_records']}")
    print(f"Output File: {summary['output_path']}")
    print("===================================================\n")


if __name__ == "__main__":
    main()
