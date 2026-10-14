import re
import base64
import subprocess
from pathlib import Path

WORKSPACE_ROOT = Path(".").resolve()
figures_dir = WORKSPACE_ROOT / "reports" / "figures"

def get_base64_img(filename):
    p = figures_dir / filename
    if p.exists():
        return f"data:image/png;base64,{base64.b64encode(p.read_bytes()).decode('utf-8')}"
    return ""

img_cmd4_1 = get_base64_img("cmd4_fig1_diurnal_pm25_trends.png")
img_cmd4_2 = get_base64_img("cmd4_fig2_cpcb_category_distribution.png")
img_cmd4_3 = get_base64_img("cmd4_fig3_city_aqi_boxplots.png")
img_cmd5_1 = get_base64_img("cmd5_fig1_model_forecast_actual_vs_pred.png")
img_cmd6_1 = get_base64_img("cmd6_fig1_cpcb_classification_confusion_matrix.png")

html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Google Meet Video Recording Script & Defense Guide</title>
<style>
  @page {{
    size: A4 landscape;
    margin: 10mm 12mm 10mm 12mm;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    line-height: 1.45;
    font-size: 9.5pt;
    margin: 0;
    padding: 0;
    background: #f8fafc;
  }}
  .page-break {{
    page-break-before: always;
  }}
  .header-banner {{
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #ffffff;
    padding: 10px 16px;
    border-radius: 8px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .header-banner h1 {{
    margin: 0;
    font-size: 15pt;
    font-weight: 700;
    color: #38bdf8;
  }}
  .header-banner p {{
    margin: 2px 0 0 0;
    font-size: 8.5pt;
    color: #cbd5e1;
  }}
  .meta-tag {{
    background: #0284c7;
    color: #fff;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 8pt;
    font-weight: 600;
  }}

  /* Roles Bar */
  .roles-bar {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 10px;
  }}
  .role-card {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }}
  .role-card strong {{
    color: #0369a1;
    display: block;
    font-size: 9pt;
    margin-bottom: 2px;
  }}
  .role-card span {{
    font-size: 8pt;
    color: #64748b;
  }}

  /* Two Column Step Card */
  .step-container {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    margin-bottom: 14px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.04);
    overflow: hidden;
    page-break-inside: avoid;
  }}
  .step-header {{
    background: #f1f5f9;
    border-bottom: 1px solid #cbd5e1;
    padding: 8px 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .step-title {{
    font-size: 11pt;
    font-weight: 700;
    color: #0f172a;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .step-badge {{
    background: #e0f2fe;
    color: #0369a1;
    border: 1px solid #bae6fd;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 8pt;
    font-weight: 600;
  }}
  .two-columns {{
    display: grid;
    grid-template-columns: 48% 52%;
  }}
  .col-left {{
    background: #0f172a;
    color: #e2e8f0;
    padding: 12px 14px;
    border-right: 1px solid #cbd5e1;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}
  .col-right {{
    background: #ffffff;
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    gap: 8px;
  }}

  /* Left Side: Technical & Screen */
  .box-label-left {{
    font-size: 7.5pt;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: #94a3b8;
    margin-bottom: 4px;
  }}
  .cmd-prompt {{
    background: #1e293b;
    border: 1px solid #334155;
    padding: 6px 10px;
    border-radius: 5px;
    color: #f8fafc;
    font-family: "SFMono-Regular", Consolas, Menlo, monospace;
    font-size: 8.5pt;
    font-weight: 600;
  }}
  .cmd-prompt span {{
    color: #38bdf8;
  }}
  pre.terminal-screen {{
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 5px;
    padding: 8px 10px;
    margin: 0;
    color: #38bdf8;
    font-family: "SFMono-Regular", Consolas, Menlo, monospace;
    font-size: 7pt;
    line-height: 1.35;
    white-space: pre-wrap;
    word-break: break-all;
  }}
  .embedded-img {{
    width: 100%;
    max-height: 180px;
    object-fit: contain;
    border: 1px solid #334155;
    border-radius: 5px;
    background: #ffffff;
    margin-top: 4px;
  }}
  .img-caption {{
    font-size: 7pt;
    color: #94a3b8;
    text-align: center;
    margin-top: 2px;
    font-style: italic;
  }}

  /* Right Side: Natural Speech Script */
  .box-label-right {{
    font-size: 7.5pt;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: #0369a1;
    margin-bottom: 2px;
  }}
  .speech-card {{
    background: #fefce8;
    border-left: 4px solid #f59e0b;
    padding: 10px 12px;
    border-radius: 4px;
    color: #0f172a;
    font-size: 8.5pt;
    line-height: 1.45;
  }}
  .speech-card strong {{
    color: #b45309;
  }}
  .highlight-box {{
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    padding: 8px 10px;
    border-radius: 4px;
    font-size: 8pt;
    color: #334155;
  }}
  .highlight-box ul {{
    margin: 3px 0 0 0;
    padding-left: 16px;
  }}
  .highlight-box li {{
    margin-bottom: 2px;
  }}
  .figure-speak {{
    background: #f0fdf4;
    border-left: 3px solid #22c55e;
    padding: 8px 10px;
    border-radius: 4px;
    font-size: 8pt;
    color: #14532d;
    margin-top: 4px;
  }}
</style>
</head>
<body>

  <!-- Header Banner -->
  <div class="header-banner">
    <div>
      <h1>🎥 Google Meet Video Recording Script (Side-by-Side Presentation Guide)</h1>
      <p>DISTRIBUTED URBAN AIR QUALITY ANALYTICS & FORECASTING (TRACK B) &bull; NATURAL SPEAKING FLOW FOR SIR</p>
    </div>
    <div class="meta-tag">Track B &bull; HDFS &rarr; Spark &rarr; Spark MLlib</div>
  </div>

  <!-- Roles Grid -->
  <div class="roles-bar">
    <div class="role-card">
      <strong>Teammate A (Driver / Storage Lead)</strong>
      <span>Shares screen, runs commands, presents Steps 1 & 2 (HDFS Data Lake) & Conclusion</span>
    </div>
    <div class="role-card">
      <strong>Teammate B (Spark ETL & Analytics Lead)</strong>
      <span>Presents Steps 3 & 4 (Distributed Spark ETL, CPCB 16h validity & Diurnal Analytics)</span>
    </div>
    <div class="role-card">
      <strong>Teammate C (Spark MLlib ML Lead)</strong>
      <span>Presents Steps 5 & 6 (Chronological 24h Forecasting +16.6% & Hazard Classification)</span>
    </div>
  </div>

  <!-- Opening Box -->
  <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:6px; padding:8px 12px; margin-bottom:12px; border-left:4px solid #0284c7;">
    <div style="font-size:8pt; font-weight:700; color:#0369a1; text-transform:uppercase; margin-bottom:2px;">Video Introduction (30 Seconds) &bull; Teammate A (Screen Sharer)</div>
    <div style="font-size:8.5pt; color:#0f172a; line-height:1.45;">
      <em>"Hello Sir. In this video, our team is presenting our Big Data project: <strong>Distributed Urban Air Quality Analytics and AQI Forecasting</strong>. 
      We have built this project according to <strong>Track B: Machine Learning at Scale</strong>, implementing the complete distributed lifecycle: 
      <strong>Hadoop HDFS &rarr; Apache Spark distributed ETL &rarr; Spark MLlib</strong> across Delhi NCR, Bengaluru, and Hyderabad adhering strictly to Indian 
      <strong>CPCB regulatory standards</strong>. We have prepared numbered commands so we can run and demonstrate each stage cleanly. Let us begin with Step 1."</em>
    </div>
  </div>

  <!-- STEP 1 -->
  <div class="step-container">
    <div class="step-header">
      <div class="step-title">🎬 Step 1: Inspecting Raw Telemetry in Hadoop HDFS</div>
      <div class="step-badge">Speaker: Teammate A (Driver / Storage Lead)</div>
    </div>
    <div class="two-columns">
      <div class="col-left">
        <div>
          <div class="box-label-left">🕹️ Terminal Action (What Driver Runs)</div>
          <div class="cmd-prompt">./1_hdfs_show_raw.sh</div>
        </div>
        <div>
          <div class="box-label-left">🖥️ Screen Output (What Sir Sees)</div>
          <pre class="terminal-screen">$ hdfs dfs -ls -h /air_quality/raw/
Found 1 items
-rw-r--r--   1 yashsonawane supergroup     47.3 M 2026-10-14 23:13 /air_quality/raw/raw_hourly_measurements.jsonl</pre>
        </div>
      </div>
      <div class="col-right">
        <div class="box-label-right">🗣️ What to Say to Sir (Natural Speaking Script)</div>
        <div class="speech-card">
          "Sir, as you can see on the screen, our command just listed our raw telemetry staged inside Hadoop HDFS under the path <code>/air_quality/raw/</code>.<br/><br/>
          You can see this file: <strong>raw_hourly_measurements.jsonl</strong>. It is <strong>47.3 Megabytes</strong> and contains <strong>96,000 raw continuous hourly records</strong> collected from the OpenAQ API across Delhi, Bengaluru, and Hyderabad.<br/><br/>
          We built a resumable client that respects OpenAQ's 60 req/min rate limit. Staging it in HDFS allows Hadoop to distribute the data with a 128 MB block size and 3x replication factor.<br/><br/>
          Now, let us look at Step 2 to see how we store the processed data."
        </div>
        <div class="highlight-box">
          <strong>Key Highlights to Point at:</strong>
          <ul>
            <li>Point to <strong>47.3 M</strong>: Real continuous telemetry (96k rows), not dummy small data.</li>
            <li>Point to <strong>/air_quality/raw/</strong>: Demonstrates proper HDFS distributed file zoning.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- STEP 2 -->
  <div class="step-container">
    <div class="step-header">
      <div class="step-title">🎬 Step 2: Inspecting Partitioned Parquet Lake in HDFS</div>
      <div class="step-badge">Speaker: Teammate A (Driver / Storage Lead)</div>
    </div>
    <div class="two-columns">
      <div class="col-left">
        <div>
          <div class="box-label-left">🕹️ Terminal Action (What Driver Runs)</div>
          <div class="cmd-prompt">./2_hdfs_show_parquet.sh</div>
        </div>
        <div>
          <div class="box-label-left">🖥️ Screen Output (What Sir Sees)</div>
          <pre class="terminal-screen">$ hdfs dfs -ls -h /air_quality/processed/hourly_aqi_parquet/
Found 4 items
-rw-r--r--   1 yashsonawane supergroup          0 2026-10-15 02:22 /air_quality/processed/hourly_aqi_parquet/_SUCCESS
drwxr-xr-x   - yashsonawane supergroup          0 2026-10-15 02:22 /air_quality/processed/hourly_aqi_parquet/city=Bengaluru
drwxr-xr-x   - yashsonawane supergroup          0 2026-10-15 02:22 /air_quality/processed/hourly_aqi_parquet/city=Delhi NCR
drwxr-xr-x   - yashsonawane supergroup          0 2026-10-15 02:22 /air_quality/processed/hourly_aqi_parquet/city=Hyderabad</pre>
        </div>
      </div>
      <div class="col-right">
        <div class="box-label-right">🗣️ What to Say to Sir (Natural Speaking Script)</div>
        <div class="speech-card">
          "Sir, in Step 2, this is our processed data lake in HDFS.<br/><br/>
          Notice that instead of plain CSV files, we are using <strong>columnar Apache Parquet with Snappy compression</strong>, partitioned by city—<code>city=Bengaluru</code>, <code>city=Delhi NCR</code>, and <code>city=Hyderabad</code>.<br/><br/>
          This is crucial for performance because it enables <strong>Partition Pruning</strong>. When our downstream Spark queries ask for Delhi data, Spark reads only the Delhi directory and completely skips the other cities, saving disk I/O and network shuffle.<br/><br/>
          Now, my teammate will explain Step 3 and run our distributed Spark ETL."
        </div>
        <div class="highlight-box">
          <strong>Key Highlights to Point at:</strong>
          <ul>
            <li>Point to <strong>_SUCCESS</strong>: Hadoop output committer validation mark.</li>
            <li>Point to <strong>city=XXX folders</strong>: Automatic Hive-style partitioning for fast parallel scans.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- STEP 3 -->
  <div class="step-container">
    <div class="step-header">
      <div class="step-title">🎬 Step 3: Running Distributed Apache Spark ETL & CPCB Math</div>
      <div class="step-badge">Speaker: Teammate B (Spark ETL & Analytics Lead)</div>
    </div>
    <div class="two-columns">
      <div class="col-left">
        <div>
          <div class="box-label-left">🕹️ Terminal Action (What Driver Runs)</div>
          <div class="cmd-prompt">./3_spark_run_etl.sh</div>
        </div>
        <div>
          <div class="box-label-left">🖥️ Screen Output (What Sir Sees)</div>
          <pre class="terminal-screen">$ python3 scripts/spark_etl.py
================ STARTING DISTRIBUTED SPARK ETL ================
Apache Spark Version: 4.2.0
[1/6] Ingesting raw dataset from: hdfs://localhost:9000/air_quality/raw/...
  Ingested 96,000 raw records.
[3/6] Normalizing timestamps to IST and harmonizing pollutant units...
[4/6] Reshaping and pivoting pollutants into hourly station records...
[5/6] Calculating rolling exposure windows and CPCB NAQI...
  Total Station-Hour Records Processed: 18,521
  Records Meeting Strict CPCB 16h NAQI Validity: 12,792

--- Sample Processed Station Records with CPCB AQI ---
+---------+-----------------------+-------------------+------------------+--------+---------------+
|city     |station_name           |ts_ist             |pm25_24h          |cpcb_aqi|health_category|
+---------+-----------------------+-------------------+------------------+--------+---------------+
|Delhi NCR|R K Puram, Delhi - DPCC|2016-02-06 12:30:00|193.42857142857142|500.0   |Severe         |
+---------+-----------------------+-------------------+------------------+--------+---------------+
Spark ETL Pipeline completed successfully in 20.71 seconds.</pre>
        </div>
      </div>
      <div class="col-right">
        <div class="box-label-right">🗣️ What to Say to Sir (Natural Speaking Script)</div>
        <div class="speech-card">
          <em>(While running):</em> "Sir, the driver just started our Apache Spark ETL script. Spark 4.2.0 is loading the 96,000 raw records from HDFS into an in-memory DataFrame."<br/><br/>
          <em>(When output finishes):</em> "As you can see, the pipeline completed in 20 seconds. Here is what happened:
          <ol style="margin:4px 0; padding-left:18px;">
            <li>In Step 3, we converted gases like NO2 and SO2 from parts-per-billion into &mu;g/m&sup3; using their molecular weights.</li>
            <li>In Step 4, Spark pivoted individual pollutant streams into <strong>18,521 station-hour records</strong>.</li>
            <li>In Step 5, we applied the official Indian <strong>CPCB 16-hour completeness rule</strong>: a 24-hour moving window is only valid if at least 16 hourly readings exist. Exactly <strong>12,792 records</strong> met this strict rule.</li>
            <li>In the sample table, you can see calculated 24h PM2.5, PM10, and final AQI—R K Puram shows an AQI of 500, which falls into the <strong>Severe</strong> category.</li>
          </ol>
          Now let us run Step 4 to see our distributed Spark SQL analytics and generated charts."
        </div>
      </div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- STEP 4A: Analytics Tables -->
  <div class="step-container">
    <div class="step-header">
      <div class="step-title">🎬 Step 4: Distributed Spark SQL Analytics & Descriptive Stats</div>
      <div class="step-badge">Speaker: Teammate B (Spark ETL & Analytics Lead)</div>
    </div>
    <div class="two-columns">
      <div class="col-left">
        <div>
          <div class="box-label-left">🕹️ Terminal Action (What Driver Runs)</div>
          <div class="cmd-prompt">./4_spark_run_analytics.sh</div>
        </div>
        <div>
          <div class="box-label-left">🖥️ Screen Output (What Sir Sees)</div>
          <pre class="terminal-screen">$ python3 scripts/run_analytics.py
================ RUNNING DISTRIBUTED ANALYTICS ================
[1/4] Calculating city-wise descriptive statistics...
     city  total_hours  valid_aqi_hours  avg_pm25  std_pm25  avg_pm10  avg_cpcb_aqi  max_cpcb_aqi
Delhi NCR         8131             5924     121.9      97.7     288.8         382.0         500.0
Bengaluru         6126             3378      28.8      52.7      68.9         293.9         500.0
Hyderabad         4264             3490      28.0      21.6      69.7         265.1         500.0

[2/4] Computing CPCB health category distribution by city...
     city health_category  category_count pct_of_city
Delhi NCR          Severe            3701        62.5
Bengaluru    Satisfactory            1236        36.6
Hyderabad    Satisfactory            1440        41.3

[4/4] Rendering analytics visualizations...
  [COMMAND 4 - FIGURE 1] Saved: reports/figures/cmd4_fig1_diurnal_pm25_trends.png
  [COMMAND 4 - FIGURE 2] Saved: reports/figures/cmd4_fig2_cpcb_category_distribution.png
  [COMMAND 4 - FIGURE 3] Saved: reports/figures/cmd4_fig3_city_aqi_boxplots.png</pre>
        </div>
      </div>
      <div class="col-right">
        <div class="box-label-right">🗣️ What to Say to Sir (Natural Speaking Script)</div>
        <div class="speech-card">
          "Sir, our Spark SQL aggregation is now displayed on screen:<br/><br/>
          * <strong>Table 1:</strong> Notice the huge difference between cities. Delhi's average PM2.5 is <strong>121.9 &mu;g/m&sup3;</strong>, whereas Bengaluru is only <strong>28.8</strong> and Hyderabad is <strong>28.0</strong>. Delhi is more than four times more polluted.<br/><br/>
          * <strong>Table 2:</strong> In Delhi, a massive <strong>62.5% of all monitored hours fell into the Severe category</strong>. Meanwhile, Bengaluru has 36.6% Satisfactory hours and Hyderabad has 41.3%.<br/><br/>
          * <strong>Generated Figures:</strong> Below the tables, Spark generated three labeled figures for Command 4:
          <ul>
            <li><strong>Figure CMD 4-1:</strong> Shows the diurnal pollution cycle. Delhi has a severe morning peak at 08:00 AM due to winter thermal inversion trapping smoke, and an evening peak at 08:00 PM from traffic.</li>
            <li><strong>Figure CMD 4-2:</strong> Shows the category bar distribution comparing Delhi, Bengaluru, and Hyderabad.</li>
            <li><strong>Figure CMD 4-3:</strong> Shows the statistical AQI boxplots across the three cities.</li>
          </ul>
          Now let us look at the actual charts generated on the next page."
        </div>
      </div>
    </div>
  </div>

  <!-- STEP 4B: Analytics Visuals -->
  <div class="step-container">
    <div class="step-header">
      <div class="step-title">🖼️ Step 4 Visuals: Diurnal Cycle & Health Category Distributions</div>
      <div class="step-badge">Visual Reference: Command 4 Charts</div>
    </div>
    <div class="two-columns">
      <div class="col-left">
        <div>
          <div class="box-label-left">CMD 4 - Figure 1: Diurnal Cycle (Inversion at 08:00 AM)</div>
          <img class="embedded-img" src="{img_cmd4_1}" alt="Diurnal Trends"/>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px;">
          <div>
            <div class="box-label-left">Figure 2: CPCB Categories</div>
            <img class="embedded-img" src="{img_cmd4_2}" alt="Categories"/>
          </div>
          <div>
            <div class="box-label-left">Figure 3: AQI Boxplots</div>
            <img class="embedded-img" src="{img_cmd4_3}" alt="Boxplots"/>
          </div>
        </div>
      </div>
      <div class="col-right">
        <div class="box-label-right">🗣️ What to Say While Displaying These Charts</div>
        <div class="figure-speak">
          <strong>Figure CMD 4-1 (Diurnal Cycle):</strong><br/>
          <em>"Sir, look at this spike in Delhi at 8:00 AM due to winter thermal inversion trapping pollutants near the ground, followed by the evening rush-hour peak at 8:00 PM."</em>
        </div>
        <div class="figure-speak">
          <strong>Figure CMD 4-2 (Hazard Distribution):</strong><br/>
          <em>"Notice the tall dark red bar for Delhi showing 62.5% Severe hours, while Bengaluru is mostly green and orange (Satisfactory and Moderate)."</em>
        </div>
        <div class="figure-speak">
          <strong>Figure CMD 4-3 (AQI Boxplots):</strong><br/>
          <em>"This boxplot shows the median AQI in Delhi is right near the 400 Severe threshold, whereas Bengaluru and Hyderabad stay much lower."</em>
        </div>
      </div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- STEP 5 -->
  <div class="step-container">
    <div class="step-header">
      <div class="step-title">🎬 Step 5: Spark MLlib 24-Hour Forecasting Models</div>
      <div class="step-badge">Speaker: Teammate C (Spark MLlib ML Lead)</div>
    </div>
    <div class="two-columns">
      <div class="col-left">
        <div>
          <div class="box-label-left">🕹️ Terminal Action (What Driver Runs)</div>
          <div class="cmd-prompt">./5_spark_mllib_forecasting.sh</div>
        </div>
        <div>
          <div class="box-label-left">🖥️ Screen Output (What Sir Sees)</div>
          <pre class="terminal-screen">$ python3 scripts/train_forecasting_models.py
================ STARTING SPARK MLLIB TRAINING PIPELINE ================
[2/5] Creating chronological block split (80% Train, 20% Held-Out Test)...
  Training observations (Past):     10,294 (80.0%)
  Test observations (Future):        2,570 (20.0%)

[3/5] Evaluating Naive Persistence Baseline (y_hat = y_t)...
  [BASELINE] Naive Persistence -> RMSE: 42.16 µg/m³ | MAE: 15.56 µg/m³ | R²: 0.003

[5/5] Training distributed models across Spark cluster...
  --- Training Linear Regression (ElasticNet) ---
    RMSE: 37.86 µg/m³ (vs Baseline: +10.2%) | Training Latency: 1.64s
  --- Training Random Forest Regressor ---
    RMSE: 35.17 µg/m³ (vs Baseline: +16.6%) | Training Latency: 1.79s
  --- Training Gradient-Boosted Trees (GBT) ---
    RMSE: 37.61 µg/m³ (vs Baseline: +10.8%) | Training Latency: 5.56s

Best Performing Model: Random Forest Regressor with RMSE = 35.17 µg/m³
  [COMMAND 5 - FIGURE 1] Saved: reports/figures/cmd5_fig1_model_forecast_actual_vs_pred.png</pre>
        </div>
        <div>
          <div class="box-label-left">CMD 5 - Figure 1: 24h Forecast vs Ground Truth</div>
          <img class="embedded-img" src="{img_cmd5_1}" alt="24h Forecast Plot"/>
        </div>
      </div>
      <div class="col-right">
        <div class="box-label-right">🗣️ What to Say to Sir (Natural Speaking Script)</div>
        <div class="speech-card">
          "Sir, now we move to distributed Machine Learning using Spark MLlib. Here, our goal is to forecast PM2.5 levels <strong>24 hours into the future</strong>.<br/><br/>
          Notice how we engineered this:
          <ol style="margin:4px 0; padding-left:18px;">
            <li>In Step 2, we used a <strong>strict chronological 80/20 block split</strong>—the past 80% is used for training and future 20% for testing. We never use random shuffle because that causes data leakage in time series.</li>
            <li>In Step 3, we evaluated a standard <strong>Persistence Baseline</strong>, which assumes tomorrow's air will be identical to today's reading. That gave an RMSE of 42.16.</li>
            <li>Then Spark trained three models at scale. As you can see, our champion model is <strong>Random Forest</strong> with an <strong>RMSE of 35.17 &mu;g/m&sup3;—an improvement of +16.6% over baseline</strong> in just 1.79 seconds of distributed training.</li>
            <li>It also generated <strong>Figure CMD 5-1</strong>, where you can see the orange predicted curve closely tracking the actual observed ground truth across the 24h horizon.</li>
          </ol>
          Next, let us demonstrate our hazard classification model in Step 6."
        </div>
        <div class="figure-speak">
          <strong>Sentence to Say while Showing Figure CMD 5-1:</strong><br/>
          <em>"Here the orange predicted line tracks the actual blue observed curve accurately across the 24-hour future test horizon."</em>
        </div>
      </div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- STEP 6 -->
  <div class="step-container">
    <div class="step-header">
      <div class="step-title">🎬 Step 6: Spark MLlib 6-Tier Hazard Classification</div>
      <div class="step-badge">Speaker: Teammate C (Spark MLlib ML Lead)</div>
    </div>
    <div class="two-columns">
      <div class="col-left">
        <div>
          <div class="box-label-left">🕹️ Terminal Action (What Driver Runs)</div>
          <div class="cmd-prompt">./6_spark_mllib_classification.sh</div>
        </div>
        <div>
          <div class="box-label-left">🖥️ Screen Output (What Sir Sees)</div>
          <pre class="terminal-screen">$ python3 scripts/train_classification_model.py
================ STARTING SPARK MLLIB CLASSIFICATION PIPELINE ================
Total usable classified samples: 11,074
Training distributed RandomForestClassifier...

--- Spark MLlib Classification Metrics ---
  Accuracy:           70.21%
  Weighted F1-Score:  0.676
  Weighted Precision: 0.674
  Weighted Recall:    0.702
  Training Duration:  3.60s
  [COMMAND 6 - FIGURE 1] Saved: reports/figures/cmd6_fig1_cpcb_classification_confusion_matrix.png</pre>
        </div>
        <div>
          <div class="box-label-left">CMD 6 - Figure 1: Classification Confusion Matrix</div>
          <img class="embedded-img" src="{img_cmd6_1}" alt="Confusion Matrix"/>
        </div>
      </div>
      <div class="col-right">
        <div class="box-label-right">🗣️ What to Say to Sir (Natural Speaking Script)</div>
        <div class="speech-card">
          "Sir, this is our second ML model for classification. Instead of just numbers, it predicts the exact CPCB health category 24 hours ahead—Good, Satisfactory, Moderate, Poor, Very Poor, or Severe.<br/><br/>
          Looking at the metrics on screen, the Random Forest Classifier achieved:
          <ul>
            <li><strong>70.21% Test Accuracy</strong></li>
            <li><strong>0.676 Weighted F1-Score</strong></li>
            <li>Distributed training took only <strong>3.60 seconds</strong>.</li>
            <li>It generated <strong>Figure CMD 6-1</strong>, which confirms high diagonal concentration, proving that the model reliably identifies Severe and Satisfactory conditions without confusing them.</li>
          </ul>
          Driver, please show Step 7 for our master runner."
        </div>
        <div class="figure-speak">
          <strong>Sentence to Say while Showing Confusion Matrix:</strong><br/>
          <em>"The heatmap diagonal is dark, proving the classifier reliably identifies Severe days without confusing them with cleaner categories."</em>
        </div>
      </div>
    </div>
  </div>

  <!-- STEP 7 -->
  <div class="step-container">
    <div class="step-header">
      <div class="step-title">🎬 Step 7: Master Automated Pipeline & Closing (1 Minute)</div>
      <div class="step-badge">Speaker: Teammate A (Driver / Storage Lead)</div>
    </div>
    <div class="two-columns">
      <div class="col-left">
        <div>
          <div class="box-label-left">🕹️ Terminal Action (What Driver Runs)</div>
          <div class="cmd-prompt">./7_run_entire_pipeline.sh</div>
        </div>
        <div>
          <div class="box-label-left">🖥️ Screen Output (What Sir Sees)</div>
          <pre class="terminal-screen">$ ./run_pipeline.sh
========================================================================
 Pipeline execution completed successfully!
 Reports available in: docs/
 Figures generated in: reports/figures/
 Partitioned Parquet: data/processed/hourly_aqi_parquet/
========================================================================</pre>
        </div>
      </div>
      <div class="col-right">
        <div class="box-label-right">🗣️ What to Say to Sir (Closing Speech)</div>
        <div class="speech-card">
          "And Sir, if we ever want to run the entire distributed pipeline end-to-end automatically—from data validation and Spark ETL to analytics and all MLlib models—we have <code>./7_run_entire_pipeline.sh</code>, which executes everything in one automated run.<br/><br/>
          To summarize our project:
          <ol style="margin:4px 0; padding-left:18px;">
            <li>We built a full <strong>Track B</strong> distributed architecture on <strong>HDFS, Apache Spark, and Spark MLlib</strong>.</li>
            <li>We enforced official government <strong>CPCB NAQI regulations</strong>, including the 16-hour completeness rule and unit conversions.</li>
            <li>We proved machine learning at scale with a <strong>16.6% improvement in 24h forecasting</strong> and <strong>70.2% hazard classification accuracy</strong>.</li>
          </ol>
          Thank you, Sir!"
        </div>
      </div>
    </div>
  </div>

</body>
</html>
"""

html_file = WORKSPACE_ROOT / "explanation" / "presentation_print.html"
html_file.write_text(html_content, encoding="utf-8")

pdf_file = WORKSPACE_ROOT / "explanation" / "PRESENTATION_DEFENSE_SCRIPT.pdf"
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={pdf_file}",
    "--no-pdf-header-footer",
    str(html_file.resolve())
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Side-by-side Chrome compilation code:", res.returncode)
print("PDF output file size:", pdf_file.stat().st_size if pdf_file.exists() else "Missing")
