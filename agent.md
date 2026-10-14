## Phase 0: Analyze the Reference Material

Reference website provided by the project team:
https://explore.openaq.org/#1.2/20/40

Before implementing the project:

1. Inspect the OpenAQ Explorer to understand the available monitoring locations, pollutants, and geographic coverage.
2. Read the official OpenAQ API v3 documentation to determine the correct endpoints, authentication method, pagination, and historical measurement access.
3. Explain how OpenAQ can support the project titled "Distributed Urban Air Quality Analytics and AQI Forecasting."
4. Identify the difference between raw pollutant concentrations and AQI calculated under India's CPCB methodology.
5. Identify relevant published research papers on distributed air-quality analytics, Spark-based processing, and air-quality forecasting. Prefer credible research publications and provide their actual links.
6. Summarize the methodology, algorithms, datasets, evaluation metrics, and limitations of relevant papers.
7. Compare our planned implementation against the literature and identify a defensible project contribution.
8. Do not invent paper titles, authors, results, or citations. Clearly distinguish the OpenAQ Explorer, official technical documentation, and peer-reviewed research papers.

Produce a reference-analysis report before finalizing the project architecture.

# Project: Distributed Urban Air Quality Analytics and AQI Forecasting

Act as a senior Big Data engineer and machine-learning engineer. Build and verify this project incrementally in the current workspace.

## Technology stack
- OpenAQ API v3 for air-quality measurements
- Python for ingestion
- Hadoop HDFS for distributed storage
- Apache Spark for distributed ETL and analytics
- Spark MLlib for forecasting
- Python plotting libraries for visualizations

## Phase 1: Inspect and audit
1. Inspect the existing workspace before changing files.
2. Check whether the OpenAQ API key is configured. Read it only from an environment variable or a locally stored secret file; never print it, expose it in logs, or commit it.
3. Test authentication with OpenAQ API v3.
4. Inspect the official API documentation and determine the correct endpoints and parameters.
5. Discover Indian monitoring locations, sensors, pollutant types, units, measurement frequency, and available historical coverage.
6. Produce a data-audit report with coverage, missing values, data quality issues, and recommended cities.
7. Do not assume data availability before testing the API.

## Phase 2: Ingestion
1. Implement robust API pagination, retries, rate-limit handling, timeouts, and error logging.
2. Retrieve location metadata, sensor metadata, and historical measurements for suitable Indian stations.
3. Save original responses in a raw-data directory.
4. Make ingestion resumable and avoid duplicate records.
5. Store credentials outside source code and add secret files to .gitignore.
6. Begin with a small sample, validate it, and only then expand collection.

## Phase 3: HDFS and Spark
1. Inspect the installed Java, Hadoop, and Spark versions and their configuration.
2. Do not overwrite existing configurations or install system packages without approval.
3. Create raw, processed, and analytics data zones in HDFS.
4. Implement Spark transformations for schema validation, deduplication, timestamp normalization, unit checks, missing-value analysis, and hourly/daily aggregation.
5. Store cleaned datasets in Parquet with sensible partitioning.
6. Provide scripts and commands to run the pipeline reproducibly.

## Phase 4: Analytics
Generate:
- City-wise and station-wise pollutant statistics.
- Daily and monthly pollution trends.
- Pollutant distributions and comparisons.
- Missing-data and station-coverage reports.
- Evidence that Spark transformations execute successfully.

## Phase 5: AQI and forecasting
1. Use the official CPCB AQI methodology for India and document all required breakpoints, units, averaging periods, and data-validity rules.
2. Never treat pollutant concentration as AQI or replace missing values with zero.
3. Calculate AQI only where required observations are valid.
4. If valid AQI cannot be calculated, clearly report the limitation and consider a separate PM2.5 forecasting target.
5. Build a naive forecasting baseline and an appropriate Spark MLlib regression model using historical lag features.
6. Use chronological train, validation, and test splits to avoid temporal leakage.
7. Report MAE and RMSE and compare the model against the baseline.
8. Document limitations and avoid unsupported claims about accuracy.

## Phase 6: Deliverables
Create:
- A clean, modular project structure.
- A requirements file and setup instructions.
- An environment-variable example without real credentials.
- API ingestion, HDFS, Spark ETL, analytics, training, and evaluation scripts.
- A data-audit report.
- Architecture documentation.
- Reproducible commands and sample outputs.
- Visualizations and a final project report.

## Execution rules
Work in small phases. Run tests after each phase and fix errors before proceeding. Ask for approval before destructive operations, external system changes, or expensive large-scale data collection. Do not fabricate results or claim commands succeeded unless you verified them. First report the workspace state, API test result, and data-audit plan, then proceed with Phase 1.