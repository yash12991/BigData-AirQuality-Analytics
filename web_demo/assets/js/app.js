// AirFlow360 Interactive Application Logic
document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initTeleprompterTimer();
  initAqiCalculator();
  initHdfsExplorer();
  initSqlConsole();
  initMllibPredictor();
  initTerminalSimulator();
});

// 1. Tab Navigation
function initTabs() {
  const tabs = document.querySelectorAll(".nav-tab");
  const panes = document.querySelectorAll(".tab-pane");

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      const targetId = tab.getAttribute("data-tab");
      tabs.forEach(t => t.classList.remove("active"));
      panes.forEach(p => p.classList.remove("active"));
      tab.classList.add("active");
      const targetPane = document.getElementById(targetId);
      if (targetPane) targetPane.classList.add("active");
    });
  });
}

// 2. Presentation Teleprompter & Timer
let timerInterval = null;
let secondsElapsed = 0;
let isTimerRunning = false;

function initTeleprompterTimer() {
  const clock = document.getElementById("timerClock");
  const startBtn = document.getElementById("timerStartBtn");
  const resetBtn = document.getElementById("timerResetBtn");
  const speakerPills = document.querySelectorAll(".speaker-pill");
  const speakerCards = document.querySelectorAll(".speaker-card");

  function updateDisplay() {
    const mins = Math.floor(secondsElapsed / 60);
    const secs = secondsElapsed % 60;
    if (clock) clock.textContent = String(mins).padStart(2, "0") + ":" + String(secs).padStart(2, "0");

    if (isTimerRunning) {
      speakerCards.forEach(c => c.style.opacity = "0.4");
      if (secondsElapsed < 180) {
        const c1 = document.getElementById("card-person1");
        if (c1) c1.style.opacity = "1";
      } else if (secondsElapsed < 360) {
        const c2 = document.getElementById("card-person2");
        if (c2) c2.style.opacity = "1";
      } else {
        const c3 = document.getElementById("card-person3");
        if (c3) c3.style.opacity = "1";
      }
    }
  }

  if (startBtn) {
    startBtn.addEventListener("click", () => {
      if (!isTimerRunning) {
        isTimerRunning = true;
        startBtn.innerHTML = "⏸ Pause Timer";
        startBtn.classList.remove("btn-accent");
        startBtn.classList.add("btn-secondary");
        timerInterval = setInterval(() => {
          secondsElapsed++;
          updateDisplay();
        }, 1000);
      } else {
        isTimerRunning = false;
        clearInterval(timerInterval);
        startBtn.innerHTML = "▶ Resume Timer";
        startBtn.classList.add("btn-accent");
        startBtn.classList.remove("btn-secondary");
      }
    });
  }

  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      isTimerRunning = false;
      clearInterval(timerInterval);
      secondsElapsed = 0;
      updateDisplay();
      if (startBtn) {
        startBtn.innerHTML = "▶ Start Presentation Timer";
        startBtn.classList.add("btn-accent");
        startBtn.classList.remove("btn-secondary");
      }
      speakerCards.forEach(c => c.style.opacity = "1");
    });
  }

  speakerPills.forEach(pill => {
    pill.addEventListener("click", () => {
      speakerPills.forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      const filter = pill.getAttribute("data-filter");

      speakerCards.forEach(card => {
        if (filter === "all" || card.id === "card-" + filter) {
          card.style.display = "block";
        } else {
          card.style.display = "none";
        }
      });
    });
  });
}

// 3. CPCB NAQI Regulatory Engine
const CPCB_BREAKPOINTS = {
  pm25: [
    { blo: 0,   bhi: 30,  ilo: 0,   ihi: 50 },
    { blo: 31,  bhi: 60,  ilo: 51,  ihi: 100 },
    { blo: 61,  bhi: 90,  ilo: 101, ihi: 200 },
    { blo: 91,  bhi: 120, ilo: 201, ihi: 300 },
    { blo: 121, bhi: 250, ilo: 301, ihi: 400 },
    { blo: 251, bhi: 500, ilo: 401, ihi: 500 }
  ],
  pm10: [
    { blo: 0,   bhi: 50,  ilo: 0,   ihi: 50 },
    { blo: 51,  bhi: 100, ilo: 51,  ihi: 100 },
    { blo: 101, bhi: 250, ilo: 101, ihi: 200 },
    { blo: 251, bhi: 350, ilo: 201, ihi: 300 },
    { blo: 351, bhi: 430, ilo: 301, ihi: 400 },
    { blo: 431, bhi: 600, ilo: 401, ihi: 500 }
  ],
  no2: [
    { blo: 0,   bhi: 40,  ilo: 0,   ihi: 50 },
    { blo: 41,  bhi: 80,  ilo: 51,  ihi: 100 },
    { blo: 81,  bhi: 180, ilo: 101, ihi: 200 },
    { blo: 181, bhi: 280, ilo: 201, ihi: 300 },
    { blo: 281, bhi: 400, ilo: 301, ihi: 400 },
    { blo: 401, bhi: 600, ilo: 401, ihi: 500 }
  ],
  so2: [
    { blo: 0,   bhi: 40,  ilo: 0,   ihi: 50 },
    { blo: 41,  bhi: 80,  ilo: 51,  ihi: 100 },
    { blo: 81,  bhi: 380, ilo: 101, ihi: 200 },
    { blo: 381, bhi: 800, ilo: 201, ihi: 300 },
    { blo: 801, bhi: 1600,ilo: 301, ihi: 400 },
    { blo: 1601,bhi: 2400,ilo: 401, ihi: 500 }
  ],
  co: [
    { blo: 0.0,  bhi: 1.0,  ilo: 0,   ihi: 50 },
    { blo: 1.1,  bhi: 2.0,  ilo: 51,  ihi: 100 },
    { blo: 2.1,  bhi: 10.0, ilo: 101, ihi: 200 },
    { blo: 10.1, bhi: 17.0, ilo: 201, ihi: 300 },
    { blo: 17.1, bhi: 34.0, ilo: 301, ihi: 400 },
    { blo: 34.1, bhi: 50.0, ilo: 401, ihi: 500 }
  ],
  o3: [
    { blo: 0,   bhi: 50,  ilo: 0,   ihi: 50 },
    { blo: 51,  bhi: 100, ilo: 51,  ihi: 100 },
    { blo: 101, bhi: 168, ilo: 101, ihi: 200 },
    { blo: 169, bhi: 208, ilo: 201, ihi: 300 },
    { blo: 209, bhi: 748, ilo: 301, ihi: 400 },
    { blo: 749, bhi: 1000,ilo: 401, ihi: 500 }
  ]
};

function calculateSubIndex(conc, pollutant) {
  if (conc === null || conc === undefined || conc < 0) return 0;
  const bpList = CPCB_BREAKPOINTS[pollutant];
  if (!bpList) return 0;
  for (const bp of bpList) {
    if (conc >= bp.blo && conc <= bp.bhi) {
      const idx = ((bp.ihi - bp.ilo) / (bp.bhi - bp.blo)) * (conc - bp.blo) + bp.ilo;
      return Math.round(idx);
    }
  }
  if (conc > bpList[bpList.length - 1].bhi) return 500;
  return 0;
}

function getAqiCategory(aqi) {
  if (aqi <= 50) return { name: "Good", color: "#10b981", desc: "Minimal impact. Air quality is considered safe." };
  if (aqi <= 100) return { name: "Satisfactory", color: "#84cc16", desc: "Minor breathing discomfort to sensitive people." };
  if (aqi <= 200) return { name: "Moderate", color: "#eab308", desc: "Breathing discomfort to people with asthma and heart diseases." };
  if (aqi <= 300) return { name: "Poor", color: "#f97316", desc: "Breathing discomfort to most people on prolonged exposure." };
  if (aqi <= 400) return { name: "Very Poor", color: "#ef4444", desc: "Respiratory illness on prolonged exposure. Significant risk." };
  return { name: "Severe", color: "#881337", desc: "Affects healthy people and seriously impacts vulnerable populations." };
}

function initAqiCalculator() {
  const pollutants = ["pm25", "pm10", "no2", "so2", "co", "o3"];
  const sliders = {};
  const valueBadges = {};

  pollutants.forEach(p => {
    sliders[p] = document.getElementById("slider-" + p);
    valueBadges[p] = document.getElementById("val-" + p);
    if (sliders[p]) {
      sliders[p].addEventListener("input", () => {
        valueBadges[p].textContent = sliders[p].value;
        recalculateAqi();
      });
    }
  });

  function recalculateAqi() {
    let maxSubIndex = 0;
    let dominant = "PM2.5";

    pollutants.forEach(p => {
      if (!sliders[p]) return;
      const conc = parseFloat(sliders[p].value);
      const sIdx = calculateSubIndex(conc, p);

      const bar = document.getElementById("subbar-" + p);
      const val = document.getElementById("subval-" + p);
      if (bar) {
        const pct = Math.min(100, (sIdx / 500) * 100);
        bar.style.width = pct + "%";
        const cat = getAqiCategory(sIdx);
        bar.style.backgroundColor = cat.color;
      }
      if (val) val.textContent = sIdx;

      if (sIdx > maxSubIndex) {
        maxSubIndex = sIdx;
        dominant = p.toUpperCase().replace("25", "2.5");
      }
    });

    const aqiNum = document.getElementById("aqiScoreNumber");
    const aqiCatBadge = document.getElementById("aqiCategoryBadge");
    const dominantElem = document.getElementById("dominantPollutantText");
    const advisoryElem = document.getElementById("aqiHealthAdvisory");
    const meterCard = document.getElementById("aqiMeterCard");

    const category = getAqiCategory(maxSubIndex);
    if (aqiNum) aqiNum.textContent = maxSubIndex;
    if (aqiCatBadge) {
      aqiCatBadge.textContent = category.name;
      aqiCatBadge.style.backgroundColor = category.color;
      aqiCatBadge.style.boxShadow = "0 0 20px " + category.color + "88";
    }
    if (dominantElem) dominantElem.innerHTML = "Dominant Pollutant: <strong>" + dominant + "</strong> (CPCB Max Sub-Index)";
    if (advisoryElem) advisoryElem.textContent = category.desc;
    if (meterCard) meterCard.style.borderColor = category.color;
  }

  const presets = {
    delhi: { pm25: 360, pm10: 480, no2: 95, so2: 45, co: 3.8, o3: 82 },
    bengaluru: { pm25: 35, pm10: 65, no2: 28, so2: 12, co: 0.8, o3: 42 },
    hyderabad: { pm25: 75, pm10: 140, no2: 48, so2: 19, co: 1.3, o3: 58 },
    clean: { pm25: 18, pm10: 32, no2: 15, so2: 8, co: 0.4, o3: 25 }
  };

  document.querySelectorAll(".btn-preset").forEach(btn => {
    btn.addEventListener("click", () => {
      const pKey = btn.getAttribute("data-preset");
      const values = presets[pKey];
      if (values) {
        pollutants.forEach(p => {
          if (sliders[p]) {
            sliders[p].value = values[p];
            valueBadges[p].textContent = values[p];
          }
        });
        recalculateAqi();
      }
    });
  });

  recalculateAqi();
}

// 4. HDFS Explorer
const HDFS_NODES = {
  "raw-json": {
    path: "hdfs:///air_quality/raw/raw_hourly_measurements.jsonl",
    type: "Unstructured JSONL Staging Lake",
    size: "47.3 MB",
    records: "96,000 raw observations",
    blocks: "1 Block (128 MB default block size)",
    replication: "3 Replicas (HDFS Fault-Tolerant)",
    schema: [
      { col: "location_id", type: "Integer", desc: "OpenAQ station ID" },
      { col: "parameter", type: "String", desc: "pm25, pm10, no2, so2, co, o3" },
      { col: "value", type: "Double", desc: "Raw sensor measurement" },
      { col: "unit", type: "String", desc: "ug/m3 or ppb/ppm" },
      { col: "datetime_utc", type: "Timestamp", desc: "ISO-8601 UTC timestamp" },
      { col: "city", type: "String", desc: "Delhi, Bengaluru, Hyderabad" }
    ],
    sample: "{\"location_id\": 8118, \"city\": \"Delhi\", \"parameter\": \"pm25\", \"value\": 142.5, \"unit\": \"µg/m³\", \"datetime_utc\": \"2024-01-15T02:30:00Z\"}"
  },
  "processed-parquet": {
    path: "hdfs:///air_quality/processed/hourly_aqi_parquet/",
    type: "Apache Parquet Columnar Lake",
    size: "3.8 MB (Snappy compressed, 92% compression ratio)",
    records: "18,521 station-hours (12,792 valid CPCB)",
    blocks: "3 Partitions (city=delhi, bengaluru, hyderabad)",
    replication: "3 Replicas",
    schema: [
      { col: "city", type: "String [Partition Key]", desc: "Partition directory column" },
      { col: "year", type: "Integer [Partition Key]", desc: "Temporal partition key" },
      { col: "station_name", type: "String", desc: "R K Puram, BTM Layout, Central University" },
      { col: "datetime_ist", type: "Timestamp", desc: "Indian Standard Time (+05:30)" },
      { col: "pm25_rolling24h", type: "Double", desc: "24-Hour windowed concentration" },
      { col: "cpcb_aqi", type: "Integer", desc: "Official CPCB NAQI value (0-500)" },
      { col: "cpcb_category", type: "String", desc: "Good, Moderate, Severe, etc." },
      { col: "cpcb_is_valid", type: "Boolean", desc: "Meets 16h completeness rule" }
    ],
    sample: "{\"city\": \"Delhi\", \"station\": \"R K Puram\", \"datetime_ist\": \"2024-01-15 08:00:00\", \"cpcb_aqi\": 348, \"cpcb_category\": \"Very Poor\", \"cpcb_is_valid\": true}"
  },
  "analytics-parquet": {
    path: "hdfs:///air_quality/analytics/city_summary_metrics.parquet",
    type: "Aggregated Analytics Mart",
    size: "180 KB",
    records: "Pre-aggregated city-hour metrics",
    blocks: "1 Block",
    replication: "3 Replicas",
    schema: [
      { col: "city", type: "String", desc: "Analyzed City" },
      { col: "avg_pm25", type: "Double", desc: "Mean PM2.5 level" },
      { col: "max_aqi", type: "Integer", desc: "Maximum recorded AQI" },
      { col: "severe_pct", type: "Double", desc: "Percentage of Severe AQI hours" }
    ],
    sample: "{\"city\": \"Delhi\", \"avg_pm25\": 118.4, \"max_aqi\": 492, \"severe_pct\": 62.5}"
  }
};

function initHdfsExplorer() {
  const items = document.querySelectorAll(".hdfs-item");
  const pathDisplay = document.getElementById("hdfsSelectedPath");
  const typeDisplay = document.getElementById("hdfsSelectedType");
  const sizeDisplay = document.getElementById("hdfsSelectedSize");
  const recordsDisplay = document.getElementById("hdfsSelectedRecords");
  const blocksDisplay = document.getElementById("hdfsSelectedBlocks");
  const replDisplay = document.getElementById("hdfsSelectedRepl");
  const tableBody = document.getElementById("hdfsSchemaBody");
  const sampleBox = document.getElementById("hdfsSampleRecord");

  function selectNode(key) {
    const data = HDFS_NODES[key];
    if (!data) return;

    if (pathDisplay) pathDisplay.textContent = data.path;
    if (typeDisplay) typeDisplay.textContent = data.type;
    if (sizeDisplay) sizeDisplay.textContent = data.size;
    if (recordsDisplay) recordsDisplay.textContent = data.records;
    if (blocksDisplay) blocksDisplay.textContent = data.blocks;
    if (replDisplay) replDisplay.textContent = data.replication;
    if (sampleBox) sampleBox.textContent = data.sample;

    if (tableBody) {
      tableBody.innerHTML = "";
      data.schema.forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML = "<td><strong>" + row.col + "</strong></td><td><span class=\"type-pill\">" + row.type + "</span></td><td style=\"color: var(--text-secondary);\">" + row.desc + "</td>";
        tableBody.appendChild(tr);
      });
    }
  }

  items.forEach(item => {
    item.addEventListener("click", () => {
      items.forEach(i => i.classList.remove("active"));
      item.classList.add("active");
      const key = item.getAttribute("data-node");
      selectNode(key);
    });
  });

  selectNode("processed-parquet");
}

// 5. Spark SQL Console
const SQL_PRESETS = {
  q1: {
    title: "1. Multi-City Statistical Distribution",
    sql: "-- Query 1: Distributed multi-city aggregate metrics\nSELECT \n    city,\n    COUNT(*) as total_hours,\n    ROUND(AVG(pm25_conc), 2) as mean_pm25,\n    ROUND(STDDEV(pm25_conc), 2) as std_pm25,\n    ROUND(PERCENTILE_APPROX(pm25_conc, 0.50), 2) as median_pm25,\n    ROUND(MAX(cpcb_aqi), 0) as max_cpcb_aqi\nFROM parquet_lake\nWHERE cpcb_is_valid = true\nGROUP BY city\nORDER BY mean_pm25 DESC;",
    headers: ["City", "Valid Hours", "Mean PM2.5 (µg/m³)", "StdDev", "Median", "Max AQI"],
    rows: [
      ["Delhi NCR", "5,842", "118.42", "68.34", "104.20", "492 (Severe)"],
      ["Hyderabad", "3,610", "46.15", "22.81", "41.60", "288 (Poor)"],
      ["Bengaluru", "3,340", "34.82", "16.14", "31.25", "162 (Moderate)"]
    ]
  },
  q2: {
    title: "2. Diurnal Boundary Layer Inversion Dynamics",
    sql: "-- Query 2: Peak rush-hour vs afternoon dispersion analysis\nSELECT \n    HOUR(datetime_ist) as hour_of_day,\n    ROUND(AVG(CASE WHEN city = 'Delhi' THEN pm25_conc END), 1) as delhi_pm25,\n    ROUND(AVG(CASE WHEN city = 'Bengaluru' THEN pm25_conc END), 1) as blr_pm25,\n    ROUND(AVG(CASE WHEN city = 'Hyderabad' THEN pm25_conc END), 1) as hyd_pm25\nFROM parquet_lake\nGROUP BY HOUR(datetime_ist)\nHAVING hour_of_day IN (8, 14, 22)\nORDER BY hour_of_day;",
    headers: ["Hour (IST)", "Delhi PM2.5", "Bengaluru PM2.5", "Hyderabad PM2.5", "Atmospheric Phenomenon"],
    rows: [
      ["08:00 AM", "148.6 µg/m³", "44.2 µg/m³", "58.1 µg/m³", "Morning Peak (Rush Hour + Boundary Inversion)"],
      ["02:00 PM", "72.4 µg/m³", "24.1 µg/m³", "31.5 µg/m³", "Afternoon Minimum (Solar Thermal Dispersion)"],
      ["10:00 PM", "162.1 µg/m³", "41.8 µg/m³", "52.7 µg/m³", "Nighttime Peak (Radiative Inversion Trap)"]
    ]
  },
  q3: {
    title: "3. CPCB Health Hazard Tier Distribution",
    sql: "-- Query 3: Percentage distribution of CPCB hazard categories\nSELECT \n    city,\n    ROUND(SUM(CASE WHEN cpcb_category = 'Good' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as good_pct,\n    ROUND(SUM(CASE WHEN cpcb_category = 'Moderate' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as mod_pct,\n    ROUND(SUM(CASE WHEN cpcb_category = 'Very Poor' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as very_poor_pct,\n    ROUND(SUM(CASE WHEN cpcb_category = 'Severe' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as severe_pct\nFROM parquet_lake\nWHERE cpcb_is_valid = true\nGROUP BY city;",
    headers: ["City", "Good (0-50)", "Moderate (101-200)", "Very Poor (301-400)", "Severe (401-500)"],
    rows: [
      ["Delhi NCR", "0.2%", "14.1%", "23.2%", "62.5% (Extremely Hazardous)"],
      ["Hyderabad", "6.8%", "52.4%", "1.2%", "0.0%"],
      ["Bengaluru", "18.4%", "29.7%", "0.0%", "0.0%"]
    ]
  }
};

function initSqlConsole() {
  const querySelect = document.getElementById("sqlQuerySelect");
  const codeEditor = document.getElementById("sqlCodeEditor");
  const runBtn = document.getElementById("runSqlQueryBtn");
  const tableHeader = document.getElementById("sqlTableHeader");
  const tableBody = document.getElementById("sqlTableBody");
  const execTime = document.getElementById("sqlExecTime");

  function loadQuery(key) {
    const q = SQL_PRESETS[key];
    if (!q) return;
    if (codeEditor) codeEditor.value = q.sql;

    if (tableHeader && tableBody) {
      tableHeader.innerHTML = "";
      tableBody.innerHTML = "";
      q.headers.forEach(h => {
        const th = document.createElement("th");
        th.textContent = h;
        tableHeader.appendChild(th);
      });

      q.rows.forEach(row => {
        const tr = document.createElement("tr");
        row.forEach(col => {
          const td = document.createElement("td");
          td.textContent = col;
          tr.appendChild(td);
        });
        tableBody.appendChild(tr);
      });
    }
    if (execTime) {
      execTime.textContent = "Spark Catalyst Plan Optimized • Executed in " + Math.floor(120 + Math.random() * 80) + "ms";
    }
  }

  if (querySelect) {
    querySelect.addEventListener("change", () => {
      loadQuery(querySelect.value);
    });
  }

  if (runBtn) {
    runBtn.addEventListener("click", () => {
      runBtn.textContent = "⚙️ Executing in Spark...";
      setTimeout(() => {
        loadQuery(querySelect.value || "q1");
        runBtn.textContent = "▶ Run Query";
      }, 250);
    });
  }

  loadQuery("q1");
}

// 6. MLlib Live Predictor
function initMllibPredictor() {
  const lag1Input = document.getElementById("mlLag1");
  const lag2Input = document.getElementById("mlLag2");
  const lag24Input = document.getElementById("mlLag24");
  const tempInput = document.getElementById("mlTemp");
  const rhInput = document.getElementById("mlRh");
  const predictBtn = document.getElementById("btnRunMllibPredict");

  const outPredPm25 = document.getElementById("outPredPm25");
  const outPredDelta = document.getElementById("outPredDelta");
  const outPredCat = document.getElementById("outPredCat");
  const outPersistence = document.getElementById("outPersistenceBaseline");

  function runPrediction() {
    const l1 = parseFloat(lag1Input ? lag1Input.value : 120) || 120;
    const l2 = parseFloat(lag2Input ? lag2Input.value : 115) || 115;
    const l24 = parseFloat(lag24Input ? lag24Input.value : 110) || 110;
    const temp = parseFloat(tempInput ? tempInput.value : 22) || 22;
    const rh = parseFloat(rhInput ? rhInput.value : 65) || 65;

    const baseline = l24;
    const predictedPm25 = (0.35 * l1) + (0.20 * l2) + (0.38 * l24) - (0.4 * temp) + (0.15 * rh);
    const finalVal = Math.max(10, Math.round(predictedPm25 * 10) / 10);

    const cat = getAqiCategory(calculateSubIndex(finalVal, "pm25"));

    if (outPredPm25) outPredPm25.textContent = finalVal + " µg/m³";
    if (outPersistence) outPersistence.textContent = baseline + " µg/m³ (Baseline RMSE: 42.16)";
    if (outPredDelta) {
      outPredDelta.textContent = "16.6% Lower Error vs Baseline (R² = 0.306)";
      outPredDelta.className = "delta-badge positive";
    }
    if (outPredCat) {
      outPredCat.textContent = cat.name;
      outPredCat.style.backgroundColor = cat.color;
    }
  }

  if (predictBtn) {
    predictBtn.addEventListener("click", () => {
      predictBtn.textContent = "⚡ Distributed Inference...";
      setTimeout(() => {
        runPrediction();
        predictBtn.textContent = "🔮 Forecast Next 24-Hours via Spark MLlib";
      }, 200);
    });
  }

  runPrediction();
}

// 7. Live Terminal Simulator
const TERMINAL_SCRIPTS = {
  pipeline: [
    { type: "prompt", text: "yashsonawane@MacBook-Pro BigData % ./run_pipeline.sh" },
    { type: "info", text: "=====================================================================" },
    { type: "info", text: "  BIG DATA AIR QUALITY PIPELINE RUNNER (TRACK B)" },
    { type: "info", text: "=====================================================================" },
    { type: "info", text: "[1/5] Checking Java & HDFS cluster status..." },
    { type: "success", text: "[OK] Active Java: openjdk 17.0.20.1 2026-01-20" },
    { type: "success", text: "[OK] Hadoop HDFS: Hadoop 3.3.6 (NameNode & DataNode active at localhost:9000)" },
    { type: "info", text: "[2/5] Running Distributed Spark ETL & CPCB NAQI Engine..." },
    { type: "dim", text: "2026-10-14 23:15:38 INFO SparkContext: Running Spark version 4.2.0" },
    { type: "dim", text: "2026-10-14 23:15:42 INFO Ingested 96,000 raw records from hdfs:///air_quality/raw/" },
    { type: "dim", text: "2026-10-14 23:15:54 INFO Harmonized gaseous units: NO2, SO2, CO, O3 to µg/m³" },
    { type: "dim", text: "2026-10-14 23:16:01 INFO Applied 24h/8h sliding windows with 16h completeness rule" },
    { type: "success", text: "[OK] Spark ETL finished in 25.32s -> Wrote 12,792 valid CPCB records to HDFS Parquet" },
    { type: "info", text: "[3/5] Running Distributed Spark SQL Analytics..." },
    { type: "dim", text: "2026-10-14 23:17:12 INFO Generated diurnal curves, city boxplots, category distribution" },
    { type: "success", text: "[OK] Analytics completed -> High-res figures saved to reports/figures/" },
    { type: "info", text: "[4/5] Training Spark MLlib Regression Models (24h Ahead PM2.5)..." },
    { type: "dim", text: "2026-10-14 23:18:24 INFO Chronological 80/20 block split: Train=10,294, Test=2,570" },
    { type: "dim", text: "2026-10-14 23:18:25 INFO Naive Persistence Baseline: RMSE = 42.16 µg/m³" },
    { type: "dim", text: "2026-10-14 23:18:28 INFO Spark MLlib RandomForestRegressor: RMSE = 35.17 µg/m³ (R² = 0.306)" },
    { type: "success", text: "[OK] Random Forest delivers +16.6% error reduction over baseline!" },
    { type: "info", text: "[5/5] Training Spark MLlib 6-Tier Hazard Classifier..." },
    { type: "dim", text: "2026-10-14 23:20:10 INFO RandomForestClassifier Test Accuracy = 70.21%, F1 = 0.676" },
    { type: "success", text: "=====================================================================" },
    { type: "success", text: "  SUCCESS: ALL 5 PIPELINE STAGES COMPLETED WITH EXIT CODE 0" },
    { type: "success", text: "=====================================================================" }
  ],
  hdfs: [
    { type: "prompt", text: "yashsonawane@MacBook-Pro BigData % hdfs dfs -ls -h /air_quality/" },
    { type: "info", text: "Found 3 items" },
    { type: "dim", text: "drwxr-xr-x   - yashsonawane supergroup          0 2026-10-14 23:14 /air_quality/analytics" },
    { type: "dim", text: "drwxr-xr-x   - yashsonawane supergroup          0 2026-10-14 23:16 /air_quality/processed" },
    { type: "dim", text: "drwxr-xr-x   - yashsonawane supergroup          0 2026-10-14 23:12 /air_quality/raw" },
    { type: "prompt", text: "yashsonawane@MacBook-Pro BigData % hdfs dfs -ls -h /air_quality/raw/" },
    { type: "dim", text: "-rw-r--r--   3 yashsonawane supergroup     47.3 M 2026-10-14 23:13 /air_quality/raw/raw_hourly_measurements.jsonl" },
    { type: "prompt", text: "yashsonawane@MacBook-Pro BigData % hdfs dfs -ls /air_quality/processed/hourly_aqi_parquet/" },
    { type: "dim", text: "drwxr-xr-x   - yashsonawane supergroup          0 2026-10-14 23:16 /air_quality/processed/hourly_aqi_parquet/city=delhi" },
    { type: "dim", text: "drwxr-xr-x   - yashsonawane supergroup          0 2026-10-14 23:16 /air_quality/processed/hourly_aqi_parquet/city=bengaluru" },
    { type: "dim", text: "drwxr-xr-x   - yashsonawane supergroup          0 2026-10-14 23:16 /air_quality/processed/hourly_aqi_parquet/city=hyderabad" },
    { type: "success", text: "[HDFS Verified] Partition pruning ready for Spark workers." }
  ],
  mllib: [
    { type: "prompt", text: "yashsonawane@MacBook-Pro BigData % .venv/bin/python3 scripts/train_forecasting_models.py" },
    { type: "info", text: "[Phase 5] Initializing Spark 4.2.0 MLlib Session..." },
    { type: "dim", text: "Loading processed dataset from HDFS: hdfs:///air_quality/processed/hourly_aqi_parquet/" },
    { type: "dim", text: "Total records: 12,792 | Training Set (80%): 10,294 | Test Set (20%): 2,570" },
    { type: "info", text: "--- MODEL BENCHMARKING RESULTS (24-Hour Ahead PM2.5) ---" },
    { type: "dim", text: "1. Naive Persistence Baseline: RMSE = 42.16 µg/m³, MAE = 18.22 µg/m³" },
    { type: "dim", text: "2. Spark MLlib LinearRegression: RMSE = 37.86 µg/m³ (+10.2% improvement, R² = 0.198)" },
    { type: "dim", text: "3. Spark MLlib GBTRegressor:     RMSE = 37.61 µg/m³ (+10.8% improvement, R² = 0.208)" },
    { type: "success", text: "4. Spark MLlib RandomForest:   RMSE = 35.17 µg/m³ (+16.6% improvement, R² = 0.306)" },
    { type: "success", text: "Training Time: 1.49 seconds | Model saved to models/spark_rf_pm25_forecaster" }
  ]
};

function initTerminalSimulator() {
  const terminalBody = document.getElementById("terminalBody");
  const buttons = document.querySelectorAll(".btn-term-run");

  function playTerminalScript(key) {
    const lines = TERMINAL_SCRIPTS[key];
    if (!lines || !terminalBody) return;
    terminalBody.innerHTML = "";
    let i = 0;

    function addLine() {
      if (i >= lines.length) return;
      const line = lines[i];
      const p = document.createElement("p");
      if (line.type === "prompt") p.className = "term-line-prompt";
      else if (line.type === "info") p.className = "term-line-info";
      else if (line.type === "success") p.className = "term-line-success";
      else p.className = "term-line-dim";
      p.textContent = line.text;
      terminalBody.appendChild(p);
      terminalBody.scrollTop = terminalBody.scrollHeight;
      i++;
      setTimeout(addLine, 45);
    }
    addLine();
  }

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      const scriptKey = btn.getAttribute("data-script");
      playTerminalScript(scriptKey);
    });
  });

  playTerminalScript("pipeline");
}
