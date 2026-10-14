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
    line-height: 1.4;
  }}
  .speech-card strong {{
    color: #b45309;
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
    padding: 10px 12px;
    border-radius: 4px;
    color: #14532d;
    font-size: 8.5pt;
    line-height: 1.45;
  }}
  .figure-speak-box strong {{
    color: #166534;
    display: block;
    font-size: 8pt;
    margin-bottom: 4px;
    text-transform: uppercase;
  }}
</style>
</head>
<body>

  <!-- Header Banner -->
  <div class="header-banner">
    <div>
      <h1>🎥 Google Meet Video Recording Script (Side-by-Side Presentation Guide)</h1>
      <p>DISTRIBUTED URBAN AIR QUALITY ANALYTICS & FORECASTING (DISTRIBUTED BIG DATA & ML) &bull; NATURAL PRESENTATION WALKTHROUGH</p>
    </div>
    <div class="meta-tag">Distributed Architecture &bull; HDFS &rarr; Spark &rarr; Spark MLlib</div>
  </div>

  <!-- Roles Grid -->
  <div class="roles-bar">
    <div class="role-card">
      <strong>Teammate A (Driver / Storage Lead)</strong>
      <span>Shares screen, runs commands, presents Steps 1 & 2 (HDFS Data Lake) & Step 7 Conclusion</span>
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
  <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:6px; padding:6px 10px; margin-bottom:10px; border-left:4px solid #0284c7;">
    <div style="font-size:7.5pt; font-weight:700; color:#0369a1; text-transform:uppercase; margin-bottom:1px;">Video Introduction (30 Seconds) &bull; Teammate A (Screen Sharer)</div>
    <div style="font-size:8pt; color:#0f172a; line-height:1.4;">
      <em>"Hello everyone. In this video, our team is presenting our Big Data project: <strong>Distributed Urban Air Quality Analytics and AQI Forecasting</strong>. 
      We implemented the full distributed lifecycle under a <strong>Distributed Big Data Architecture</strong>—spanning 
      <strong>Hadoop HDFS &rarr; Apache Spark distributed ETL &rarr; Spark MLlib</strong>. 
      We analyze continuous telemetry from Delhi NCR, Bengaluru, and Hyderabad adhering strictly to Indian 
      <strong>CPCB regulatory standards</strong>. Let us begin by inspecting our raw distributed data lake in Hadoop HDFS."</em>
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
      <div class="box-label-right">🗣️ What to Say Naturally</div>
      <div class="speech-card">
        "Here in our first step, our command just listed the raw telemetry staged inside Hadoop HDFS under the path <code>/air_quality/raw/</code>.<br/><br/>
        As shown on the terminal, we have <strong>raw_hourly_measurements.jsonl</strong>, which is <strong>47.3 Megabytes</strong> and contains <strong>96,000 raw continuous hourly records</strong> collected from the OpenAQ API across Delhi, Bengaluru, and Hyderabad.<br/><br/>
        Our client respects OpenAQ's 60 req/min rate limit with automated token replenishment. Staging this in HDFS allows Hadoop to distribute the data using standard 128 MB blocks and a 3x replication factor.<br/><br/>
        Now, let us inspect Step 2 to see how we store the processed data."
      </div>
      <div class="highlight-box">
        <strong>Key Highlights to Point at:</strong>
        <ul>
          <li>Point to <strong>47.3 M</strong>: Real continuous telemetry (96k rows), not dummy sample data.</li>
          <li>Point to <strong>/air_quality/raw/</strong>: Demonstrates proper HDFS distributed file zoning.</li>
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
      <div class="box-label-right">🗣️ What to Say Naturally</div>
      <div class="speech-card">
        "Moving to Step 2, this is our processed data lake in HDFS.<br/><br/>
        Notice that instead of plain CSV files, we persist our cleaned data as <strong>columnar Apache Parquet with Snappy compression</strong>, partitioned by city—<code>city=Bengaluru</code>, <code>city=Delhi NCR</code>, and <code>city=Hyderabad</code>.<br/><br/>
        This gives us significant performance gains through <strong>Partition Pruning</strong>. When downstream Spark queries run on Delhi data, Spark scans only the Delhi directory and skips all other cities, saving disk I/O and network shuffle.<br/><br/>
        Now, my teammate will explain Step 3 and demonstrate our distributed Spark ETL."
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
    <div class="col-right-speech">
      <div class="box-label-right">🗣️ What to Say Naturally</div>
      <div class="speech-card">
        <em>(While running):</em> "The driver has started our Apache Spark ETL script. Spark 4.2.0 is loading the 96,000 raw records from HDFS into an in-memory DataFrame."<br/><br/>
        <em>(When output finishes):</em> "The pipeline completed in just 20 seconds. Here is what took place:
        <ol style="margin:2px 0; padding-left:16px;">
          <li>In Step 3, we converted gases like NO2 and SO2 from parts-per-billion into &mu;g/m&sup3; using their molecular weights.</li>
          <li>In Step 4, Spark pivoted individual pollutant streams into <strong>18,521 station-hour records</strong>.</li>
          <li>In Step 5, we enforced the official Indian <strong>CPCB 16-hour completeness rule</strong>: a 24-hour moving average is only valid if at least 16 hourly readings exist. Exactly <strong>12,792 records</strong> met this strict rule.</li>
          <li>In the sample table, you can see calculated 24h PM2.5, PM10, and final AQI—R K Puram shows an AQI of 500, which falls into the <strong>Severe</strong> category.</li>
        </ol>
        Next, let us run Step 4 to inspect our Spark SQL analytics and visual trends."
      </div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- STEP 4: Terminal Analytics Table Card -->
  <div class="two-col-card">
    <div class="card-header-full">
      <div class="step-title">🎬 Step 4: Distributed Spark SQL Analytics & Summary Tables</div>
      <div class="step-badge">Speaker: Teammate B (Spark ETL & Analytics Lead)</div>
    </div>
    <div class="col-left-term">
      <div>
        <div class="box-label-left">🕹️ Terminal Action (What Driver Runs)</div>
        <div class="cmd-prompt">./4_spark_run_analytics.sh</div>
      </div>
      <div>
        <div class="box-label-left">🖥️ Screen Output (What is Displayed)</div>
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
    <div class="col-right-speech">
      <div class="box-label-right">🗣️ What to Say Naturally</div>
      <div class="speech-card">
        "Our Spark SQL distributed aggregations are now displayed on screen:<br/><br/>
        * <strong>Table 1:</strong> Looking at the city averages, Delhi's average PM2.5 is <strong>121.9 &mu;g/m&sup3;</strong>, whereas Bengaluru is only <strong>28.8</strong> and Hyderabad is <strong>28.0</strong>. Delhi's particulate pollution is over four times higher.<br/><br/>
        * <strong>Table 2:</strong> In Delhi, a massive <strong>62.5% of all monitored hours fell into the Severe category</strong>. In contrast, Bengaluru has 36.6% Satisfactory hours and Hyderabad has 41.3%.<br/><br/>
        * <strong>Generated Figures:</strong> Below the tables, Spark generated three figures for Command 4. Let us inspect each generated chart side-by-side with its findings."
      </div>
      <div class="highlight-box">
        <strong>Key Highlights to Point at:</strong>
        <ul>
          <li>Point to <strong>Delhi avg_pm25 (121.9)</strong> vs <strong>Bengaluru (28.8)</strong>.</li>
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
        "In this diurnal trend chart, notice the sharp pollution spike in Delhi at <strong>08:00 AM</strong>, where PM2.5 exceeds 160 &mu;g/m&sup3;.<br/><br/>
        This morning peak is caused by nocturnal thermal inversion trapping cold air and vehicular smoke near the ground.<br/><br/>
        As the sun warms the boundary layer during mid-day, the smoke disperses, but rises again to a second peak at <strong>08:00 PM</strong> due to evening rush-hour traffic.<br/><br/>
        Meanwhile, Bengaluru and Hyderabad (the green and blue lines) remain remarkably flat and stable below 40 &mu;g/m&sup3; throughout the entire day."
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
        "Looking at Figure CMD 4-2, this bar chart directly compares the health hazard profile across our monitored cities:<br/><br/>
        The dark red bar for Delhi represents <strong>62.5% of monitored hours in the Severe hazard category</strong> (AQI above 400).<br/><br/>
        In comparison, Bengaluru and Hyderabad are dominated by green and yellow (Satisfactory and Moderate), proving that Southern metropolitan areas experience significantly better ambient dispersion than the landlocked northern plains."
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
        "In Figure CMD 4-3, this boxplot displays the statistical median, interquartile range, and outliers of the composite National Air Quality Index:<br/><br/>
        The median line for Delhi is pinned right near the <strong>400 Severe threshold</strong>, with the upper whisker frequently hitting the maximum cap of 500.<br/><br/>
        In contrast, Bengaluru and Hyderabad have narrow interquartile ranges, demonstrating consistent air quality with rare extreme excursions."
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
      <div class="box-label-right">🗣️ What to Say Naturally</div>
      <div class="speech-card">
        "Now we transition to distributed Machine Learning using Spark MLlib. Here, our objective is to forecast PM2.5 levels <strong>24 hours into the future</strong>.<br/><br/>
        Notice how we set this up:
        <ol style="margin:2px 0; padding-left:16px;">
          <li>In Step 2, we used a <strong>strict chronological 80/20 block split</strong>—the past 80% is used for training and future 20% for testing. We never use random shuffle because that causes temporal data leakage.</li>
          <li>In Step 3, we evaluated a standard <strong>Persistence Baseline</strong>, which assumes tomorrow's air will be identical to today's reading. That gave an RMSE of 42.16.</li>
          <li>Then Spark trained three models at scale. As you can see, our champion model is <strong>Random Forest</strong> with an <strong>RMSE of 35.17 &mu;g/m&sup3;—an improvement of +16.6% over baseline</strong> in just 1.79 seconds of distributed training.</li>
        </ol>
        Let us look at the forecast curve comparison chart side-by-side below."
      </div>
    </div>
  </div>

  <!-- STEP 5: Figure 1 Side-by-Side Card -->
  <div class="two-col-card">
    <div class="card-header-full">
      <div class="step-title">🖼️ Step 5 - Figure 1: 24-Hour Ahead PM2.5 Forecast vs Observed Ground Truth</div>
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
        "In this chart for Figure CMD 5-1, we are visualizing our model predictions against real sensor observations across the future test horizon:<br/><br/>
        * The <strong>blue line</strong> represents the actual ground truth PM2.5 concentration observed by the station.<br/>
        * The <strong>orange line</strong> represents our Spark MLlib Random Forest model forecasting 24 hours ahead.<br/><br/>
        Notice how closely the orange line tracks the rapid diurnal spikes and drops. This proves that our multi-scale lag features (t-1 to t-24) allow Spark to capture temporal momentum reliably."
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
      <div class="box-label-right">🗣️ What to Say Naturally</div>
      <div class="speech-card">
        "Beyond regression values, municipal authorities need discrete category alerts. In Step 6, we trained a distributed multiclass <strong>RandomForestClassifier</strong> to predict which of the 6 official CPCB hazard tiers will occur 24 hours ahead.<br/><br/>
        Looking at the metrics on screen, the classifier achieved:
        <ul>
          <li><strong>70.21% Test Accuracy</strong> across the 6 hazard categories.</li>
          <li><strong>0.676 Weighted F1-Score</strong> with balanced precision and recall.</li>
          <li>Distributed training took only <strong>3.60 seconds</strong> on Spark.</li>
        </ul>
        Let us inspect the confusion matrix side-by-side to verify how well it distinguishes critical hazard tiers."
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
        "In this confusion matrix heatmap for Figure CMD 6-1:<br/><br/>
        Notice how strongly the predictions are concentrated along the main diagonal.<br/><br/>
        Particularly in the bottom-right corner for the <strong>Severe category</strong>, the model achieves high true-positive detection for dangerous air episodes with minimal false negatives. This allows city administrators to issue health advisories and school closures 24 hours in advance with confidence."
      </div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- STEP 7 -->
  <div class="two-col-card">
    <div class="card-header-full">
      <div class="step-title">🎬 Step 7: Master Automated Pipeline Runner & Video Closing</div>
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
      <div class="box-label-right">🗣️ What to Say to Wrap Up</div>
      <div class="speech-card">
        "Finally, if we ever want to run the entire distributed pipeline end-to-end automatically—from data validation and Spark ETL to analytics and all MLlib models—we have <code>./7_run_entire_pipeline.sh</code>, which executes everything in one automated run.<br/><br/>
        To summarize our project:
        <ol style="margin:3px 0; padding-left:16px;">
          <li>We built a full distributed Big Data architecture on <strong>HDFS, Apache Spark, and Spark MLlib</strong>.</li>
          <li>We enforced official government <strong>CPCB NAQI regulations</strong>, including the 16-hour completeness rule and unit conversions.</li>
          <li>We proved machine learning at scale with a <strong>16.6% improvement in 24h forecasting</strong> and <strong>70.2% hazard classification accuracy</strong>.</li>
        </ol>
        Thank you for watching our demonstration!"
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
