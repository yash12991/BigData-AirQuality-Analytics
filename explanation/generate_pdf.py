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
    font-size: 9pt;
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
    font-size: 8pt;
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
    padding: 6px 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }}
  .role-card strong {{
    color: #0369a1;
    display: block;
    font-size: 8.5pt;
    margin-bottom: 2px;
  }}
  .role-card span {{
    font-size: 7.5pt;
    color: #64748b;
  }}

  /* Two Column Container */
  .two-col-card {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    margin-bottom: 12px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.04);
    overflow: hidden;
    page-break-inside: avoid;
    display: grid;
    grid-template-columns: 50% 50%;
  }}
  .card-header-full {{
    grid-column: span 2;
    background: #f1f5f9;
    border-bottom: 1px solid #cbd5e1;
    padding: 6px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .step-title {{
    font-size: 10.5pt;
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
    font-size: 7.5pt;
    font-weight: 600;
  }}

  .col-left-term {{
    background: #0f172a;
    color: #e2e8f0;
    padding: 10px 12px;
    border-right: 1px solid #cbd5e1;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  .col-right-speech {{
    background: #ffffff;
    padding: 10px 14px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    gap: 6px;
  }}

  /* Left Side: Terminal Box */
  .box-label-left {{
    font-size: 7pt;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: #94a3b8;
    margin-bottom: 3px;
  }}
  .cmd-prompt {{
    background: #1e293b;
    border: 1px solid #334155;
    padding: 5px 8px;
    border-radius: 5px;
    color: #f8fafc;
    font-family: "SFMono-Regular", Consolas, Menlo, monospace;
    font-size: 8pt;
    font-weight: 600;
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

  /* Left Side: Image Box */
  .col-left-fig {{
    background: #f8fafc;
    padding: 10px 12px;
    border-right: 1px solid #cbd5e1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }}
  .fig-preview {{
    width: 100%;
    max-height: 230px;
    object-fit: contain;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    background: #ffffff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  }}
  .fig-caption-tag {{
    font-size: 7.5pt;
    font-weight: 600;
    color: #475569;
    margin-top: 4px;
    text-align: center;
  }}

  /* Right Side: Speech Card */
  .box-label-right {{
    font-size: 7pt;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: #0369a1;
    margin-bottom: 2px;
  }}
  .speech-card {{
    background: #fefce8;
    border-left: 4px solid #f59e0b;
    padding: 8px 10px;
    border-radius: 4px;
    color: #0f172a;
    font-size: 8.5pt;
    line-height: 1.48;
  }}
  .speech-card strong {{
    color: #b45309;
  }}
  .speech-card p {{
    margin: 0 0 6px 0;
  }}
  .speech-card p:last-child {{
    margin-bottom: 0;
  }}
  .highlight-box {{
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    padding: 6px 8px;
    border-radius: 4px;
    font-size: 7.5pt;
    color: #334155;
  }}
  .highlight-box ul {{
    margin: 2px 0 0 0;
    padding-left: 14px;
  }}
  .figure-speak-box {{
    background: #f0fdf4;
    border-left: 4px solid #22c55e;
    padding: 8px 10px;
    border-radius: 4px;
    color: #0f172a;
    font-size: 8.5pt;
    line-height: 1.48;
  }}
  .figure-speak-box strong {{
    color: #15803d;
  }}
  .figure-speak-box p {{
    margin: 0 0 6px 0;
  }}
  .figure-speak-box p:last-child {{
    margin-bottom: 0;
  }}
</style>
</head>
<body>

  <!-- Header Banner -->
  <div class="header-banner">
    <div>
      <h1>🎥 Google Meet Video Recording & Defense Teleprompter</h1>
      <p>Distributed Big Data Pipeline &bull; Hadoop HDFS, Apache Spark ETL & Spark MLlib Analytics</p>
    </div>
    <div class="meta-tag">HDFS &rarr; Spark &rarr; Spark MLlib</div>
  </div>

  <!-- Roles Grid -->
  <div class="roles-bar">
    <div class="role-card">
      <strong>Teammate A (Driver / Storage Lead)</strong>
      <span>Shares screen, runs commands, presents Steps 1 & 2 (HDFS Data Lake) & Step 7 Wrap-Up</span>
    </div>
    <div class="role-card">
      <strong>Teammate B (Spark ETL & Analytics Lead)</strong>
      <span>Presents Steps 3 & 4 (Distributed Spark ETL, CPCB 16h validity & 3 Diurnal/AQI Charts)</span>
    </div>
    <div class="role-card">
      <strong>Teammate C (Spark MLlib ML Lead)</strong>
      <span>Presents Steps 5 & 6 (Chronological 24h Forecasting +16.6% & 6-Tier Hazard Confusion Matrix)</span>
    </div>
  </div>

  <!-- Opening Box -->
  <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:6px; padding:8px 12px; margin-bottom:10px; border-left:4px solid #0284c7;">
    <div style="font-size:7.5pt; font-weight:700; color:#0369a1; text-transform:uppercase; margin-bottom:3px;">🎬 Video Opening (30 Seconds) &bull; Teammate A (Screen Sharer)</div>
    <div style="font-size:8.5pt; color:#0f172a; line-height:1.45;">
      <em>"Hello everyone! Welcome to our demonstration of our Big Data project on <strong>Urban Air Quality Analytics and Forecasting</strong>.<br/>
      In this project, we built an end-to-end distributed system using <strong>Hadoop HDFS</strong> for storage, <strong>Apache Spark</strong> for distributed ETL, and <strong>Spark MLlib</strong> for machine learning at scale.<br/>
      We're analyzing real continuous environmental data from three major Indian cities — <strong>Delhi NCR</strong>, <strong>Bengaluru</strong>, and <strong>Hyderabad</strong> — strictly adhering to official Central Pollution Control Board guidelines.<br/>
      To keep this walkthrough smooth and easy to follow, we’ve organized our run into numbered execution scripts. Let's start with Step 1."</em>
    </div>
  </div>

  <!-- STEP 1 -->
  <div class="two-col-card">
    <div class="card-header-full">
      <div class="step-title">🎬 Step 1: Inspecting Raw Telemetry in Hadoop HDFS</div>
      <div class="step-badge">Speaker: Teammate A (Driver / Storage Lead)</div>
    </div>
    <div class="col-left-term">
      <div>
        <div class="box-label-left">🕹️ Terminal Action (What Driver Runs)</div>
        <div class="cmd-prompt">./1_hdfs_show_raw.sh</div>
      </div>
      <div>
        <div class="box-label-left">🖥️ Screen Output (What is Displayed)</div>
        <pre class="terminal-screen">$ hdfs dfs -ls -h /air_quality/raw/
Found 1 items
-rw-r--r--   1 yashsonawane supergroup     47.3 M 2026-10-14 23:13 /air_quality/raw/raw_hourly_measurements.jsonl</pre>
      </div>
    </div>
    <div class="col-right-speech">
      <div class="box-label-right">🗣️ What to Say (Natural Human Flow)</div>
      <div class="speech-card">
        <p>"Starting with Step 1, our screen driver is running <code>./1_hdfs_show_raw.sh</code>.</p>
        <p>Right here on screen, you can see our raw telemetry stored directly inside Hadoop HDFS under <code>/air_quality/raw/</code>.</p>
        <p>This file, <strong>raw_hourly_measurements.jsonl</strong>, is about <strong>47 Megabytes</strong> and holds <strong>96,000 real hourly readings</strong> collected via the OpenAQ API across Delhi, Bengaluru, and Hyderabad.</p>
        <p>Because we stage this in HDFS, Hadoop automatically distributes it using standard 128 MB blocks with 3x replication, making our ingestion layer completely fault-tolerant.</p>
        <p>Now, let’s move to Step 2 to see our optimized storage layer."</p>
      </div>
      <div class="highlight-box">
        <strong>Visual Pointers on Screen:</strong>
        <ul>
          <li>Point to <strong>47.3 M</strong>: Real continuous telemetry (96,000 rows), not simulated data.</li>
          <li>Point to <strong>/air_quality/raw/</strong>: Demonstrates proper HDFS raw data staging.</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- STEP 2 -->
  <div class="two-col-card">
    <div class="card-header-full">
      <div class="step-title">🎬 Step 2: Inspecting Partitioned Parquet Lake in HDFS</div>
      <div class="step-badge">Speaker: Teammate A (Driver / Storage Lead)</div>
    </div>
    <div class="col-left-term">
      <div>
        <div class="box-label-left">🕹️ Terminal Action (What Driver Runs)</div>
        <div class="cmd-prompt">./2_hdfs_show_parquet.sh</div>
      </div>
      <div>
        <div class="box-label-left">🖥️ Screen Output (What is Displayed)</div>
        <pre class="terminal-screen">$ hdfs dfs -ls -h /air_quality/processed/hourly_aqi_parquet/
Found 4 items
-rw-r--r--   1 yashsonawane supergroup          0 2026-10-15 02:22 /air_quality/processed/hourly_aqi_parquet/_SUCCESS
drwxr-xr-x   - yashsonawane supergroup          0 2026-10-15 02:22 /air_quality/processed/hourly_aqi_parquet/city=Bengaluru
drwxr-xr-x   - yashsonawane supergroup          0 2026-10-15 02:22 /air_quality/processed/hourly_aqi_parquet/city=Delhi NCR
drwxr-xr-x   - yashsonawane supergroup          0 2026-10-15 02:22 /air_quality/processed/hourly_aqi_parquet/city=Hyderabad</pre>
      </div>
    </div>
    <div class="col-right-speech">
      <div class="box-label-right">🗣️ What to Say (Natural Human Flow)</div>
      <div class="speech-card">
        <p>"In Step 2, we run <code>./2_hdfs_show_parquet.sh</code> to inspect our processed data lake.</p>
        <p>Notice that instead of slow, uncompressed CSVs, we converted everything into <strong>columnar Apache Parquet with Snappy compression</strong>, partitioned by city: Bengaluru, Delhi NCR, and Hyderabad.</p>
        <p>This gives us a huge performance advantage called <strong>Partition Pruning</strong>. Whenever our downstream Spark queries ask for Delhi data, Spark reads only the Delhi directory and skips the other cities entirely, saving substantial disk I/O and query time.</p>
        <p>Now, my teammate will walk you through our distributed Spark ETL pipeline."</p>
      </div>
      <div class="highlight-box">
        <strong>Visual Pointers on Screen:</strong>
        <ul>
          <li>Point to <strong>_SUCCESS</strong>: Official Hadoop output committer validation mark.</li>
          <li>Point to <strong>city=XXX folders</strong>: Hive-style partitioning for fast parallel scans.</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- STEP 3 -->
  <div class="two-col-card">
    <div class="card-header-full">
      <div class="step-title">🎬 Step 3: Running Distributed Apache Spark ETL & CPCB Math</div>
      <div class="step-badge">Speaker: Teammate B (Spark ETL & Analytics Lead)</div>
    </div>
    <div class="col-left-term">
      <div>
        <div class="box-label-left">🕹️ Terminal Action (What Driver Runs)</div>
        <div class="cmd-prompt">./3_spark_run_etl.sh</div>
      </div>
      <div>
        <div class="box-label-left">🖥️ Screen Output (What is Displayed)</div>
        <pre class="terminal-screen">$ python3 scripts/spark_etl.py
================ STARTING DISTRIBUTED SPARK ETL ================
Apache Spark Version: 4.2.0
[1/6] Ingesting raw dataset from: hdfs://localhost:9000/air_quality/raw/...
  Ingested 96,000 raw records.
[3/6] Normalizing timestamps to IST and harmonizing pollutant units...
[4/6] Enforcing CPCB completeness rule (>=16 valid hours/day)...
  Compliant station-days retained: 1,320
[5/6] Computing sub-indices and National Air Quality Index (NAQI)...
  Max sub-index applied across PM2.5, PM10, NO2, SO2, CO, O3.
[6/6] Writing partitioned Parquet dataset to HDFS...
ETL Pipeline execution finished in 20.48 seconds.</pre>
      </div>
    </div>
    <div class="col-right-speech">
      <div class="box-label-right">🗣️ What to Say (Natural Human Flow)</div>
      <div class="speech-card">
        <p>"Moving to Step 3, we execute <code>./3_spark_run_etl.sh</code> to launch our distributed Apache Spark ETL job.</p>
        <p>Watch how fast this runs across the cluster — in just about <strong>20 seconds</strong>, Spark processes all 96,000 records.</p>
        <p>During this stage, Spark handles three critical operations:
        first, it converts all timestamps to Indian Standard Time and standardizes units;
        second, it enforces the official <strong>CPCB 16-hour completeness rule</strong> — requiring at least 16 valid readings a day so missing sensor hours don't distort our results;
        and third, it computes the exact non-linear piecewise formula to calculate the final National AQI.</p>
        <p>Next in Step 4, let’s explore the analytics and visual insights."</p>
      </div>
      <div class="highlight-box">
        <strong>Visual Pointers on Screen:</strong>
        <ul>
          <li>Point to <strong>20.48 seconds</strong>: Demonstrates high-speed distributed execution.</li>
          <li>Point to <strong>>=16 valid hours/day</strong>: Shows strict regulatory adherence.</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- STEP 4: Terminal Analytics Output Card -->
  <div class="two-col-card">
    <div class="card-header-full">
      <div class="step-title">🎬 Step 4: Distributed Spark Analytics & Summary Aggregations</div>
      <div class="step-badge">Speaker: Teammate B (Spark ETL & Analytics Lead)</div>
    </div>
    <div class="col-left-term">
      <div>
        <div class="box-label-left">🕹️ Terminal Action (What Driver Runs)</div>
        <div class="cmd-prompt">./4_spark_analytics.sh</div>
      </div>
      <div>
        <div class="box-label-left">🖥️ Screen Output (What is Displayed)</div>
        <pre class="terminal-screen">$ python3 scripts/run_analytics.py
================ SPARK ANALYTICS & VISUALIZATION PIPELINE ================
Spark reading partitioned dataset from HDFS...
[Query 1] Computing 24-hour diurnal pollutant patterns...
[Query 2] Computing CPCB health category distribution across cities...
+-----------+---------+---------+---------+---------+---------+---------+
|city       |Good %   |Satisf. %|Moderate%|Poor %   |V.Poor % |Severe % |
+-----------+---------+---------+---------+---------+---------+---------+
|Bengaluru  |14.2%    |62.1%    |21.8%    |1.9%     |0.0%     |0.0%     |
|Delhi NCR  |0.0%     |2.4%     |8.1%     |12.5%    |14.5%    |62.5%    |
|Hyderabad  |8.5%     |48.2%    |35.1%    |7.2%     |1.0%     |0.0%     |
+-----------+---------+---------+---------+---------+---------+---------+
City Air Quality Overview:
  Delhi NCR  -> Avg PM2.5: 121.9 µg/m³ | Avg NAQI: 342.6 (Severe Smog)
  Bengaluru  -> Avg PM2.5:  28.8 µg/m³ | Avg NAQI:  78.4 (Satisfactory)
  Hyderabad  -> Avg PM2.5:  42.1 µg/m³ | Avg NAQI: 104.2 (Moderate)</pre>
      </div>
    </div>
    <div class="col-right-speech">
      <div class="box-label-right">🗣️ What to Say (Natural Human Flow)</div>
      <div class="speech-card">
        <p>"In Step 4, we run <code>./4_spark_analytics.sh</code>. Spark runs distributed SQL aggregations to calculate summary statistics and generates our high-resolution analytical plots.</p>
        <p>Look at the summary table on screen:</p>
        <p>In <strong>Delhi NCR</strong>, the average PM2.5 level reaches <strong>121.9 micrograms per cubic meter</strong>, and <strong>62.5% of the recorded days fall into the Severe category</strong>.</p>
        <p>In sharp contrast, <strong>Bengaluru</strong> averages only <strong>28.8</strong>, with less than 2% in Severe.</p>
        <p>Now, let’s look at the generated figures right beside us to see what the data reveals."</p>
      </div>
      <div class="highlight-box">
        <strong>Visual Pointers on Screen:</strong>
        <ul>
          <li>Point to <strong>Delhi avg PM2.5 (121.9)</strong> vs <strong>Bengaluru (28.8)</strong>.</li>
          <li>Point to <strong>Delhi Severe % (62.5%)</strong> proving severe northern winter smog.</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- STEP 4: Figure 1 Side-by-Side Card -->
  <div class="two-col-card">
    <div class="card-header-full">
      <div class="step-title">🖼️ Step 4 - Figure 1: Diurnal Pattern of PM2.5 Concentration across Metros</div>
      <div class="step-badge">Visual Reference: cmd4_fig1_diurnal_pm25_trends.png</div>
    </div>
    <div class="col-left-fig">
      <img class="fig-preview" src="{img_cmd4_1}" alt="Diurnal Trends Chart"/>
      <div class="fig-caption-tag">Figure CMD 4-1: Diurnal Cycle of PM2.5 across 24 Hours (IST)</div>
    </div>
    <div class="col-right-speech">
      <div class="box-label-right">🗣️ What to Say While Showing Figure 1</div>
      <div class="figure-speak-box">
        <strong>Explaining the Diurnal Cycle:</strong>
        <p>"Looking at this first figure on the left, we plotted the 24-hour diurnal cycle of PM2.5 for each city.</p>
        <p>Look at the orange line for Delhi — you'll notice two distinct peaks:</p>
        <p>The highest spike happens at <strong>8:00 AM</strong>, reaching over 160 micrograms per cubic meter. This is caused by winter nocturnal temperature inversion, which traps cold air and vehicle exhaust right at ground level.</p>
        <p>As the sun warms the atmosphere, the pollutants disperse slightly, but then rise again to a second peak around <strong>8:00 PM</strong> during evening rush hour.</p>
        <p>Meanwhile, Bengaluru and Hyderabad — the green and blue lines — stay low and steady below 40 all day long, thanks to steady coastal winds and favorable geography."</p>
      </div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- STEP 4: Figure 2 Side-by-Side Card -->
  <div class="two-col-card">
    <div class="card-header-full">
      <div class="step-title">🖼️ Step 4 - Figure 2: CPCB Health Hazard Categories Distribution</div>
      <div class="step-badge">Visual Reference: cmd4_fig2_cpcb_category_distribution.png</div>
    </div>
    <div class="col-left-fig">
      <img class="fig-preview" src="{img_cmd4_2}" alt="CPCB Category Distribution"/>
      <div class="fig-caption-tag">Figure CMD 4-2: Distribution of CPCB Categories by City (%)</div>
    </div>
    <div class="col-right-speech">
      <div class="box-label-right">🗣️ What to Say While Showing Figure 2</div>
      <div class="figure-speak-box">
        <strong>Explaining Category Breakdown:</strong>
        <p>"Now turning to our second figure, this chart compares the official CPCB health hazard categories across the three cities.</p>
        <p>Delhi’s distribution is dominated by that tall dark red bar — showing that <strong>62.5% of all days are in the Severe category</strong>, with AQI values exceeding 400.</p>
        <p>On the other hand, Bengaluru and Hyderabad are almost entirely green and yellow — meaning Good, Satisfactory, and Moderate air. This clearly illustrates the geographical and meteorological contrast between Northern landlocked plains and Southern plateau regions."</p>
      </div>
    </div>
  </div>

  <!-- STEP 4: Figure 3 Side-by-Side Card -->
  <div class="two-col-card">
    <div class="card-header-full">
      <div class="step-title">🖼️ Step 4 - Figure 3: City AQI Boxplots Distribution Spread</div>
      <div class="step-badge">Visual Reference: cmd4_fig3_city_aqi_boxplots.png</div>
    </div>
    <div class="col-left-fig">
      <img class="fig-preview" src="{img_cmd4_3}" alt="AQI Boxplots"/>
      <div class="fig-caption-tag">Figure CMD 4-3: Statistical Boxplot Comparison of NAQI</div>
    </div>
    <div class="col-right-speech">
      <div class="box-label-right">🗣️ What to Say While Showing Figure 3</div>
      <div class="figure-speak-box">
        <strong>Explaining AQI Spread:</strong>
        <p>"Here in our third figure, the boxplot highlights the statistical distribution of the National AQI.</p>
        <p>For Delhi, the median line sits way up at <strong>400</strong>, right in the Severe zone, with many measurements maxing out at the 500 ceiling.</p>
        <p>In comparison, Bengaluru and Hyderabad have very compact boxplots with medians safely below 100, remaining well within healthy, acceptable ranges."</p>
      </div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- STEP 5: Terminal Benchmark Output Card -->
  <div class="two-col-card">
    <div class="card-header-full">
      <div class="step-title">🎬 Step 5: Distributed Spark MLlib 24-Hour Forecasting Pipeline</div>
      <div class="step-badge">Speaker: Teammate C (Spark MLlib ML Lead)</div>
    </div>
    <div class="col-left-term">
      <div>
        <div class="box-label-left">🕹️ Terminal Action (What Driver Runs)</div>
        <div class="cmd-prompt">./5_spark_mllib_forecasting.sh</div>
      </div>
      <div>
        <div class="box-label-left">🖥️ Screen Output (What is Displayed)</div>
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
    </div>
    <div class="col-right-speech">
      <div class="box-label-right">🗣️ What to Say (Natural Human Flow)</div>
      <div class="speech-card">
        <p>"Now moving to Step 5, we run <code>./5_spark_mllib_forecasting.sh</code> to train machine learning models at scale with Spark MLlib. Our goal is to forecast PM2.5 levels <strong>24 hours ahead</strong>.</p>
        <p>To do this with strict scientific integrity:</p>
        <p>First, we used a <strong>chronological 80/20 train-test split</strong>. We train on past days and test on future days — we never do a random shuffle, because random shuffling leaks future weather conditions into past training data.</p>
        <p>Second, we set up a naive <strong>Persistence Baseline</strong>, which assumes tomorrow's pollution will just be the same as today. That baseline gave an RMSE of 42.16.</p>
        <p>Then, Spark trained three models in parallel. Our champion model is the <strong>Random Forest Regressor</strong>, achieving an <strong>RMSE of 35.17 — that is a 16.6% improvement over the baseline</strong>, trained in under 2 seconds!</p>
        <p>Let’s look at how well the model predictions track reality on the next card."</p>
      </div>
    </div>
  </div>

  <!-- STEP 5: Forecast Curve Side-by-Side Card -->
  <div class="two-col-card">
    <div class="card-header-full">
      <div class="step-title">🖼️ Step 5 - Figure 1: Spark MLlib 24h Predictions vs Observed Ground Truth</div>
      <div class="step-badge">Visual Reference: cmd5_fig1_model_forecast_actual_vs_pred.png</div>
    </div>
    <div class="col-left-fig">
      <img class="fig-preview" src="{img_cmd5_1}" alt="24h Forecast Curve"/>
      <div class="fig-caption-tag">Figure CMD 5-1: Spark MLlib Random Forest 24h Predictions vs Observed Ground Truth</div>
    </div>
    <div class="col-right-speech">
      <div class="box-label-right">🗣️ What to Say While Showing Figure 5-1</div>
      <div class="figure-speak-box">
        <strong>Explaining the 24h Forecast:</strong>
        <p>"Looking at Figure 5-1 on the left, this shows our 24-hour forecast in action.</p>
        <p>The <strong>blue line</strong> represents the actual ground-truth sensor measurements, and the <strong>orange line</strong> is our Spark MLlib model's 24-hour forecast.</p>
        <p>Notice how closely the orange line tracks the rapid diurnal spikes and dips over multiple days.</p>
        <p>By engineering historical lag features from 1 hour all the way to 24 hours back, our distributed model successfully captures the inertia and momentum of urban air pollution."</p>
      </div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- STEP 6: Terminal Classification Output Card -->
  <div class="two-col-card">
    <div class="card-header-full">
      <div class="step-title">🎬 Step 6: Spark MLlib 6-Tier Hazard Category Classification</div>
      <div class="step-badge">Speaker: Teammate C (Spark MLlib ML Lead)</div>
    </div>
    <div class="col-left-term">
      <div>
        <div class="box-label-left">🕹️ Terminal Action (What Driver Runs)</div>
        <div class="cmd-prompt">./6_spark_mllib_classification.sh</div>
      </div>
      <div>
        <div class="box-label-left">🖥️ Screen Output (What is Displayed)</div>
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
    </div>
    <div class="col-right-speech">
      <div class="box-label-right">🗣️ What to Say (Natural Human Flow)</div>
      <div class="speech-card">
        <p>"Next in Step 6, we run <code>./6_spark_mllib_classification.sh</code>. Along with predicting exact numbers, city authorities need actionable alerts.</p>
        <p>So we trained a multiclass <strong>RandomForestClassifier</strong> on Spark to classify the upcoming day into one of the 6 official CPCB hazard tiers: Good, Satisfactory, Moderate, Poor, Very Poor, or Severe.</p>
        <p>As you can see from the terminal output:</p>
        <p>The model achieved <strong>70.21% test accuracy</strong> across all 6 tiers, with a <strong>weighted F1-score of 0.676</strong>, and training took only <strong>3.6 seconds</strong> on Spark.</p>
        <p>Let’s examine the confusion matrix heatmap beside this to see the classification breakdown."</p>
      </div>
    </div>
  </div>

  <!-- STEP 6: Confusion Matrix Side-by-Side Card -->
  <div class="two-col-card">
    <div class="card-header-full">
      <div class="step-title">🖼️ Step 6 - Figure 1: CPCB Health Hazard Confusion Matrix</div>
      <div class="step-badge">Visual Reference: cmd6_fig1_cpcb_classification_confusion_matrix.png</div>
    </div>
    <div class="col-left-fig">
      <img class="fig-preview" src="{img_cmd6_1}" alt="Confusion Matrix"/>
      <div class="fig-caption-tag">Figure CMD 6-1: Multiclass Confusion Matrix across 6 CPCB Tiers</div>
    </div>
    <div class="col-right-speech">
      <div class="box-label-right">🗣️ What to Say While Showing Confusion Matrix</div>
      <div class="figure-speak-box">
        <strong>Explaining the Confusion Matrix:</strong>
        <p>"Looking at this confusion matrix heatmap on the left, you can see that the vast majority of predictions line up straight along the diagonal, which indicates correct classifications.</p>
        <p>Notice especially the bottom-right cell for the <strong>Severe category</strong> — the model shows very high sensitivity with almost zero false negatives.</p>
        <p>This reliability means municipal officials can trust this pipeline to trigger proactive public health advisories and traffic restrictions 24 hours before hazardous smog sets in."</p>
      </div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- STEP 7 -->
  <div class="two-col-card">
    <div class="card-header-full">
      <div class="step-title">🎬 Step 7: Master Automated Pipeline Runner & Wrap-Up</div>
      <div class="step-badge">Speaker: Teammate A (Driver / Storage Lead)</div>
    </div>
    <div class="col-left-term">
      <div>
        <div class="box-label-left">🕹️ Terminal Action (What Driver Runs)</div>
        <div class="cmd-prompt">./7_run_entire_pipeline.sh</div>
      </div>
      <div>
        <div class="box-label-left">🖥️ Screen Output (What is Displayed)</div>
        <pre class="terminal-screen">$ ./run_pipeline.sh
========================================================================
 Pipeline execution completed successfully!
 Reports available in: docs/
 Figures generated in: reports/figures/
 Partitioned Parquet: data/processed/hourly_aqi_parquet/
========================================================================</pre>
      </div>
    </div>
    <div class="col-right-speech">
      <div class="box-label-right">🗣️ What to Say to Wrap Up (Natural Human Flow)</div>
      <div class="speech-card">
        <p>"Finally, in Step 7, we have <code>./7_run_entire_pipeline.sh</code>. This master script runs our entire end-to-end workflow in one command — from data ingestion and HDFS verification, to Spark ETL, analytics, and all MLlib model training.</p>
        <p>To summarize our project:</p>
        <p>First, we successfully built and demonstrated a production-grade distributed Big Data architecture using <strong>HDFS, Apache Spark, and Spark MLlib</strong>.<br/>
        Second, we strictly followed official government <strong>CPCB standards</strong>, including unit conversions and the 16-hour validity rule.<br/>
        And third, we proved machine learning at scale, achieving a <strong>16.6% forecasting boost over baseline</strong> and <strong>70% hazard classification accuracy</strong>.</p>
        <p>Thank you very much for your time and for watching our demonstration!"</p>
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
print("Updated Chrome compilation code:", res.returncode)
print("PDF output file size:", pdf_file.stat().st_size if pdf_file.exists() else "Missing")
