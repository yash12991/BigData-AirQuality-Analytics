import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and display running headers and total page count."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(36, 11 * inch - 30, "Air Quality Big Data Project (Track B) — Google Meet Recording Script")
            self.drawRightString(8.5 * inch - 36, 11 * inch - 30, "Live Video Walkthrough")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 11 * inch - 34, 8.5 * inch - 36, 11 * inch - 34)
            
        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 38, 8.5 * inch - 36, 38)
        self.drawString(36, 26, "Google Meet Video Recording Walkthrough & Speaking Script")
        self.drawRightString(8.5 * inch - 36, 26, f"Page {self._pageNumber} of {total_pages}")
        self.restoreState()


def build_pdf(pdf_path: str):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=44,
        bottomMargin=46
    )
    
    styles = getSampleStyleSheet()
    
    NAVY = colors.HexColor("#0F172A")
    ACCENT_BLUE = colors.HexColor("#0284C7")
    DARK_SLATE = colors.HexColor("#1E293B")
    TERMINAL_BG = colors.HexColor("#090D16")
    TERM_TEXT = colors.HexColor("#38BDF8")
    SPEECH_BG = colors.HexColor("#F8FAFC")
    BORDER = colors.HexColor("#E2E8F0")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=NAVY,
        spaceAfter=3
    )
    
    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=ACCENT_BLUE,
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'StepH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=14,
        textColor=NAVY,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyTxt',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=DARK_SLATE
    )

    driver_style = ParagraphStyle(
        'DriverPrompt',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0369A1")
    )

    terminal_code = ParagraphStyle(
        'TermCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9.5,
        textColor=TERM_TEXT
    )

    speech_style = ParagraphStyle(
        'SpeechTxt',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # Title Banner
    story.append(Paragraph("🎥 Google Meet Video Recording Script & Defense Guide", title_style))
    story.append(Paragraph("DISTRIBUTED AIR QUALITY ANALYTICS & FORECASTING (TRACK B) &bull; NATURAL SPEAKING FLOW FOR PROFESSOR / SIR", sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT_BLUE, spaceBefore=0, spaceAfter=6))

    # Recording Overview
    intro_txt = (
        "<b>How to Record on Google Meet:</b> One teammate shares their screen with the terminal open in the "
        "<code>commands/</code> folder. The driver runs each numbered script (<code>./1_hdfs_show_raw.sh</code>, etc.). "
        "When the command finishes and output appears on screen, the assigned teammate speaks naturally to Sir, "
        "explaining the exact numbers and figures displayed."
    )
    story.append(Paragraph(intro_txt, body_style))
    story.append(Spacer(1, 6))

    # Roles Table
    roles_table_data = [
        [Paragraph("<b>Speaker</b>", body_style), Paragraph("<b>Role / Layer</b>", body_style), Paragraph("<b>Assigned Commands</b>", body_style), Paragraph("<b>What They Cover in the Video</b>", body_style)],
        [Paragraph("<b>Teammate A</b>", body_style), Paragraph("Driver / HDFS Storage Lead", body_style), Paragraph("<code>./1_hdfs_show_raw.sh</code><br/><code>./2_hdfs_show_parquet.sh</code>", body_style), Paragraph("Video intro, 96k raw data in HDFS, Parquet lake & partition pruning", body_style)],
        [Paragraph("<b>Teammate B</b>", body_style), Paragraph("Spark ETL & Analytics Lead", body_style), Paragraph("<code>./3_spark_run_etl.sh</code><br/><code>./4_spark_run_analytics.sh</code>", body_style), Paragraph("Spark ETL, CPCB 16h completeness rule, Delhi vs Bengaluru, diurnal peaks", body_style)],
        [Paragraph("<b>Teammate C</b>", body_style), Paragraph("Spark MLlib Machine Learning Lead", body_style), Paragraph("<code>./5_spark_mllib_forecasting.sh</code><br/><code>./6_spark_mllib_classification.sh</code>", body_style), Paragraph("Chronological split, Random Forest 24h forecast (+16.6%), 70.2% hazard classifier", body_style)],
    ]
    t_roles = Table(roles_table_data, colWidths=[1.1*inch, 1.6*inch, 2.1*inch, 2.7*inch])
    t_roles.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_roles)
    story.append(Spacer(1, 8))

    # Opening speech box
    opening_txt = (
        "<b>Opening (30s) — Teammate A (Screen Sharer):</b><br/>"
        "<i>\"Hello Sir. In this video, our team is presenting our Big Data project: Distributed Urban Air Quality Analytics and AQI Forecasting. "
        "We are strictly following Track B (HDFS &rarr; Apache Spark &rarr; Spark MLlib) across Delhi NCR, Bengaluru, and Hyderabad, adhering to official "
        "CPCB regulatory standards. We have prepared numbered commands so we can run and demonstrate each stage cleanly. Let us begin with Step 1.\"</i>"
    )
    t_opening = Table([[Paragraph(opening_txt, speech_style)]], colWidths=[7.5*inch])
    t_opening.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#F59E0B")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_opening)
    story.append(Spacer(1, 8))

    def make_step(step_num, title, speaker, command_run, terminal_output, what_to_say, image_callout=None):
        card = []
        card.append(Paragraph(f"<b>Step {step_num}: {title}</b> — <font color='{ACCENT_BLUE}'>{speaker}</font>", h1_style))
        
        # Command Bar
        cmd_text = f"<b>Terminal Action:</b> Driver types <code>{command_run}</code> and hits Enter."
        if image_callout:
            cmd_text += f"<br/><b>Generated Visual Output:</b> {image_callout}"
            
        t_cmd = Table([[Paragraph(cmd_text, driver_style)]], colWidths=[7.5*inch])
        t_cmd.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#E0F2FE")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#38BDF8")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        card.append(t_cmd)
        card.append(Spacer(1, 4))

        # Two-column box: Left = Output on Screen, Right = What Speaker Says
        t_code = Paragraph(terminal_output.replace("\n", "<br/>").replace(" ", "&nbsp;"), terminal_code)
        
        say_html = f"<b>What {speaker} Says to Sir Naturally:</b><br/>\"{what_to_say}\""
        t_say = Paragraph(say_html, speech_style)

        table_data = [
            [Paragraph("<b>Exact Screen Output (What Sir Sees)</b>", body_style), Paragraph("<b>What to Say While Displaying This Output</b>", body_style)],
            [t_code, t_say]
        ]
        
        t_box = Table(table_data, colWidths=[3.2*inch, 4.3*inch])
        t_box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.HexColor("#F1F5F9")),
            ('BACKGROUND', (1,0), (1,0), colors.HexColor("#FEF9C3")),
            ('BACKGROUND', (0,1), (0,1), TERMINAL_BG),
            ('BACKGROUND', (1,1), (1,1), SPEECH_BG),
            ('GRID', (0,0), (-1,-1), 0.5, BORDER),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        card.append(t_box)
        card.append(Spacer(1, 8))
        story.append(KeepTogether(card))

    # Step 1
    make_step(
        step_num="1",
        title="Inspect Raw Telemetry in Hadoop HDFS",
        speaker="Teammate A (Driver / Storage Lead)",
        command_run="./1_hdfs_show_raw.sh",
        terminal_output="$ hdfs dfs -ls -h /air_quality/raw/\nFound 1 items\n-rw-r--r--  1 yash supergroup  47.3 M\n  /air_quality/raw/\n  raw_hourly_measurements.jsonl",
        what_to_say="Sir, as you can see on the screen, our command just listed our raw telemetry staged inside Hadoop HDFS under /air_quality/raw/. You can see this file is 47.3 Megabytes and contains 96,000 raw continuous hourly records collected from OpenAQ API for Delhi, Bengaluru, and Hyderabad. We built a resumable client that respects API rate limits. Staging it in HDFS allows Hadoop to distribute the data with a 128 MB block size and 3x replication factor. Now let us look at Step 2 to see the processed lake."
    )

    # Step 2
    make_step(
        step_num="2",
        title="Inspect Partitioned Parquet Lake in HDFS",
        speaker="Teammate A (Driver / Storage Lead)",
        command_run="./2_hdfs_show_parquet.sh",
        terminal_output="$ hdfs dfs -ls -h .../hourly_aqi_parquet/\nFound 4 items\n_SUCCESS\ncity=Bengaluru\ncity=Delhi NCR\ncity=Hyderabad",
        what_to_say="Sir, in Step 2, this is our processed data lake in HDFS. Notice that instead of plain CSV files, we are using columnar Apache Parquet with Snappy compression, partitioned by city—Bengaluru, Delhi NCR, and Hyderabad. This enables Partition Pruning: when our downstream Spark queries ask for Delhi data, Spark reads only the Delhi directory and completely skips the other cities, saving disk I/O. Now my teammate will run Step 3 for our Spark ETL."
    )

    # Step 3
    make_step(
        step_num="3",
        title="Execute Distributed Apache Spark ETL",
        speaker="Teammate B (Spark ETL & Analytics Lead)",
        command_run="./3_spark_run_etl.sh",
        terminal_output="$ python3 scripts/spark_etl.py\n================ STARTING SPARK ETL ================\n[1/6] Ingested 96,000 raw records.\n[3/6] Normalizing IST & units (ppb -> ug/m3)\n[4/6] Pivoting into hourly station records...\n[5/6] Total Station-Hours Processed: 18,521\n      Records Meeting CPCB 16h Rule: 12,792\nSample Processed Records:\nDelhi NCR | R K Puram | cpcb_aqi: 500.0 (Severe)\nSpark ETL completed in 20.71 seconds.",
        what_to_say="Sir, as you can see on screen, Spark 4.2.0 executed our ETL pipeline in 20 seconds. It loaded the 96,000 raw records and pivoted them into 18,521 station-hour records. Here in step 5, our code enforces the official Indian CPCB 16-hour completeness rule: a 24-hour moving window is only legally valid if at least 16 hourly readings exist. Exactly 12,792 records met this strict rule. In the sample table, you can see the calculated 24h PM2.5, PM10, and overall AQI—for example, R K Puram in Delhi has an AQI of 500, which falls into the Severe category. Now let us run Step 4."
    )

    # Step 4
    make_step(
        step_num="4",
        title="Run Distributed Spark SQL Analytics & Visual Trends",
        speaker="Teammate B (Spark ETL & Analytics Lead)",
        command_run="./4_spark_run_analytics.sh",
        terminal_output="$ python3 scripts/run_analytics.py\n[1/4] City Statistics:\nDelhi: avg PM2.5 = 121.9 | avg AQI = 382.0\nBengaluru: avg PM2.5 = 28.8 | avg AQI = 293.9\nHyderabad: avg PM2.5 = 28.0 | avg AQI = 265.1\n[2/4] Hazard Distribution:\nDelhi Severe hours: 62.5%\nBengaluru Satisfactory: 36.6%\n[4/4] Saved:\n  [CMD 4 - FIG 1] cmd4_fig1_diurnal_pm25_trends.png\n  [CMD 4 - FIG 2] cmd4_fig2_cpcb_category_distribution.png\n  [CMD 4 - FIG 3] cmd4_fig3_city_aqi_boxplots.png",
        what_to_say="Sir, our Spark SQL aggregation is now displayed on screen. Looking at Table 1, Delhi's average PM2.5 is 121.9 ug/m3—over four times higher than Bengaluru (28.8). In Table 2, 62.5% of all recorded hours in Delhi fell into the Severe category. Below the tables, Spark generated three labeled figures: Figure CMD 4-1 shows the diurnal cycle—there is a huge peak at 8:00 AM due to morning thermal inversion trapping smoke, and another peak at 8:00 PM during rush hour. Figures 4-2 and 4-3 show category distributions and AQI boxplots. Now my teammate will present Step 5 for MLlib."
    )

    # Step 5
    make_step(
        step_num="5",
        title="Train Distributed Spark MLlib 24-Hour Forecasting",
        speaker="Teammate C (Spark MLlib Machine Learning Lead)",
        command_run="./5_spark_mllib_forecasting.sh",
        terminal_output="$ python3 scripts/train_forecasting_models.py\n[2/5] Chronological Split (80% Train, 20% Test)\n[3/5] Naive Persistence Baseline -> RMSE: 42.16\n[5/5] Training MLlib Distributed Models:\n  - Linear Regression: RMSE 37.86 (+10.2%)\n  - Random Forest:     RMSE 35.17 (+16.6%)\n  - GBT Regressor:     RMSE 37.61 (+10.8%)\nBest Model: Random Forest Regressor (RMSE 35.17)\nSaved: [CMD 5 - FIG 1] cmd5_fig1_model_forecast...",
        what_to_say="Sir, now we move to distributed Machine Learning using Spark MLlib to forecast PM2.5 levels 24 hours in advance. In Step 2, we used a strict chronological 80/20 block split—the model trains strictly on the past and tests on the future so there is zero data leakage. In Step 3, our Persistence Baseline gave an RMSE of 42.16. Then Spark trained three models. Our champion model is Random Forest with an RMSE of 35.17—a 16.6% improvement over baseline in just 1.79s of training. It saved Figure CMD 5-1, where you can see the orange predicted curve closely tracking the actual observed values. Next is Step 6."
    )

    # Step 6
    make_step(
        step_num="6",
        title="Train Distributed Spark MLlib 6-Tier Hazard Classifier",
        speaker="Teammate C (Spark MLlib Machine Learning Lead)",
        command_run="./6_spark_mllib_classification.sh",
        terminal_output="$ python3 scripts/train_classification_model.py\nTraining distributed RandomForestClassifier...\n--- Spark MLlib Classification Metrics ---\n  Accuracy:           70.21%\n  Weighted F1-Score:  0.676\n  Weighted Precision: 0.674\n  Weighted Recall:    0.702\n  Training Duration:  3.60s\nSaved: [CMD 6 - FIG 1] cmd6_fig1_cpcb_classification...",
        what_to_say="Sir, this is our second ML model for classification. Instead of just numbers, it predicts the exact CPCB health category 24 hours ahead—Good, Satisfactory, Moderate, Poor, Very Poor, or Severe. Looking at the metrics on screen, the Random Forest Classifier achieved 70.21% test accuracy and a weighted F1-score of 0.676 in just 3.6 seconds. It saved the confusion matrix as CMD 6-1, showing how reliably it identifies Severe and Satisfactory days. Driver, please show Step 7."
    )

    # Step 7 & Wrap-Up
    wrap_block = []
    wrap_block.append(Paragraph("<b>Step 7: Master Automated Pipeline & Closing (1 Minute)</b>", h1_style))
    wrap_txt = (
        "<b>Terminal Action:</b> Driver mentions or runs <code>./7_run_entire_pipeline.sh</code>.<br/>"
        "<b>What Teammate A Says to Conclude the Video:</b><br/>"
        "<i>\"And Sir, if we ever want to run the entire distributed pipeline end-to-end automatically—from data validation and Spark ETL to analytics and all MLlib models—we have <code>./7_run_entire_pipeline.sh</code>, which executes everything in one automated run.<br/><br/>"
        "To summarize our project:<br/>"
        "1. We built a full Track B distributed architecture on HDFS, Apache Spark, and Spark MLlib.<br/>"
        "2. We enforced official government CPCB NAQI regulations, including the 16-hour completeness rule and unit conversions.<br/>"
        "3. We proved machine learning at scale with a 16.6% improvement in 24h forecasting and 70.2% hazard classification accuracy.<br/><br/>"
        "Thank you, Sir!\"</i>"
    )
    t_wrap = Table([[Paragraph(wrap_txt, speech_style)]], colWidths=[7.5*inch])
    t_wrap.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94A3B8")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    wrap_block.append(t_wrap)
    wrap_block.append(Spacer(1, 8))
    story.append(KeepTogether(wrap_block))

    # Image Reference Table
    img_block = []
    img_block.append(Paragraph("<b>🖼️ Quick Figure Guide for Video Screen Display</b>", h1_style))
    img_block.append(Paragraph("If you open the generated images in <code>reports/figures/</code> during the video, say this:", body_style))
    
    img_data = [
        [Paragraph("<b>Command</b>", body_style), Paragraph("<b>Generated Image File</b>", body_style), Paragraph("<b>Exact Sentence to Say to Sir while Showing Image</b>", body_style)],
        [
            Paragraph("<b>Command 4</b>", body_style),
            Paragraph("<code>cmd4_fig1_diurnal_pm25_trends.png</code>", body_style),
            Paragraph("\"Sir, look at this spike in Delhi at 8:00 AM due to winter thermal inversion trapping pollutants, and the evening spike at 8:00 PM from traffic.\"", body_style)
        ],
        [
            Paragraph("<b>Command 4</b>", body_style),
            Paragraph("<code>cmd4_fig2_cpcb_category_distribution.png</code>", body_style),
            Paragraph("\"Notice the tall dark red bar for Delhi showing 62.5% Severe hours, while Bengaluru is mostly green and orange.\"", body_style)
        ],
        [
            Paragraph("<b>Command 4</b>", body_style),
            Paragraph("<code>cmd4_fig3_city_aqi_boxplots.png</code>", body_style),
            Paragraph("\"This boxplot shows the median AQI in Delhi is right near the 400 Severe threshold, whereas Bengaluru and Hyderabad stay much lower.\"", body_style)
        ],
        [
            Paragraph("<b>Command 5</b>", body_style),
            Paragraph("<code>cmd5_fig1_model_forecast_actual_vs_pred.png</code>", body_style),
            Paragraph("\"Here the orange predicted line tracks the actual blue observed curve accurately across the 24-hour future test horizon.\"", body_style)
        ],
        [
            Paragraph("<b>Command 6</b>", body_style),
            Paragraph("<code>cmd6_fig1_cpcb_classification_confusion_matrix.png</code>", body_style),
            Paragraph("\"The heatmap diagonal is dark, proving the classifier reliably identifies Severe days without confusing them with cleaner categories.\"", body_style)
        ],
    ]
    t_img = Table(img_data, colWidths=[1.1*inch, 2.4*inch, 4.0*inch])
    t_img.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    img_block.append(t_img)
    story.append(KeepTogether(img_block))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Video Recording PDF generated successfully at: {pdf_path}")

if __name__ == "__main__":
    out_pdf = "explanation/PRESENTATION_DEFENSE_SCRIPT.pdf"
    build_pdf(out_pdf)
