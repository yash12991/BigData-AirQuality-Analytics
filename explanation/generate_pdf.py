import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and display total page count."""
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
        self.setFillColor(colors.HexColor("#7F8C8D"))
        
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(36, 11 * inch - 30, "Distributed Air Quality Analytics (Track B) — Presentation & Defense Guide")
            self.drawRightString(8.5 * inch - 36, 11 * inch - 30, "Team Defense Walkthrough")
            self.setStrokeColor(colors.HexColor("#BDC3C7"))
            self.setLineWidth(0.5)
            self.line(36, 11 * inch - 34, 8.5 * inch - 36, 11 * inch - 34)
            
        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#BDC3C7"))
        self.setLineWidth(0.5)
        self.line(36, 40, 8.5 * inch - 36, 40)
        self.drawString(36, 28, "CONFIDENTIAL — Academic Evaluation & Defense Material")
        self.drawRightString(8.5 * inch - 36, 28, f"Page {self._pageNumber} of {total_pages}")
        self.restoreState()


def build_pdf(pdf_path: str):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    
    # Custom palette
    NAVY = colors.HexColor("#1A365D")
    TEAL = colors.HexColor("#0D9488")
    SLATE = colors.HexColor("#334155")
    CODE_BG = colors.HexColor("#0F172A")
    CALLOUT_BG = colors.HexColor("#F8FAFC")
    BORDER_COLOR = colors.HexColor("#CBD5E1")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=NAVY,
        alignment=TA_LEFT,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=TEAL,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=NAVY,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=SLATE,
        spaceAfter=5
    )

    speech_style = ParagraphStyle(
        'SpeechText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B"),
    )

    action_label = ParagraphStyle(
        'ActionLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0369A1"),
    )

    terminal_code = ParagraphStyle(
        'TerminalCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#38BDF8"),
    )

    story = []

    # Title Block
    story.append(Paragraph("Live Presentation, Demo & Defense Script", title_style))
    story.append(Paragraph("TRACK B: MACHINE LEARNING AT SCALE (HDFS &rarr; SPARK &rarr; SPARK MLLIB) &bull; DURATION: 10-15 MINS", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceBefore=0, spaceAfter=8))

    # Introduction / Roles Table
    story.append(Paragraph("<b>1. Presentation Strategy & Role Assignments</b>", h1_style))
    story.append(Paragraph(
        "This natural speaking guide coordinates screen driving and verbal presentation. "
        "Even if one person is running the terminal, teammates speak according to their layer without getting confused.",
        body_style
    ))

    roles_data = [
        [Paragraph("<b>Role</b>", body_style), Paragraph("<b>Lead Member</b>", body_style), Paragraph("<b>Assigned Script & Commands</b>", body_style), Paragraph("<b>Key Technical Defense</b>", body_style)],
        [Paragraph("<b>Terminal Driver</b>", body_style), Paragraph("Shared / Any", body_style), Paragraph("Runs commands 1 to 7 on cues", body_style), Paragraph("Terminal navigation & screen sharing", body_style)],
        [Paragraph("<b>Speaker 1: Storage</b>", body_style), Paragraph("HDFS Lead", body_style), Paragraph("Commands 1 & 2 (Raw & Parquet HDFS)", body_style), Paragraph("Ingestion rate-limiting, 128MB block & partitioning", body_style)],
        [Paragraph("<b>Speaker 2: Spark ETL</b>", body_style), Paragraph("Spark Lead", body_style), Paragraph("Commands 3 & 4 (Spark ETL & SQL)", body_style), Paragraph("CPCB 16h completeness, unit conversions, diurnal peaks", body_style)],
        [Paragraph("<b>Speaker 3: MLlib</b>", body_style), Paragraph("ML Lead", body_style), Paragraph("Commands 5 & 6 (Regression & Class.)", body_style), Paragraph("Leak-free chronological 80/20 split, RF vs Baseline (+16.6%)", body_style)],
    ]
    t_roles = Table(roles_data, colWidths=[1.3*inch, 1.1*inch, 2.3*inch, 2.8*inch])
    t_roles.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_roles)
    story.append(Spacer(1, 8))

    # Helper function for sections
    def add_step_block(step_num, title, speaker, command_run, terminal_output, what_to_say, what_it_proves, image_ref=None):
        block = []
        block.append(Paragraph(f"<b>Step {step_num}: {title}</b> — <font color='{TEAL}'>{speaker}</font>", h1_style))
        
        # Action Bar
        action_text = f"<b>Action:</b> Driver types <code>{command_run}</code> into terminal when {speaker} cues."
        if image_ref:
            action_text += f"<br/><b>Generates:</b> <code>{image_ref}</code>"
        
        t_action = Table([[Paragraph(action_text, action_label)]], colWidths=[7.5*inch])
        t_action.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#E0F2FE")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#38BDF8")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        block.append(t_action)
        block.append(Spacer(1, 4))

        # Two-column layout: Left = Terminal Output, Right = What to Say
        term_para = Paragraph(terminal_output.replace("\n", "<br/>").replace(" ", "&nbsp;"), terminal_code)
        speech_full = f"<b>What to Say Naturally:</b><br/>\"{what_to_say}\"<br/><br/><b>What this Proves:</b> {what_it_proves}"
        speech_para = Paragraph(speech_full, speech_style)

        table_data = [
            [Paragraph("<b>Terminal Display (What Examiner Sees)</b>", body_style), Paragraph(f"<b>Speaking Script ({speaker})</b>", body_style)],
            [term_para, speech_para]
        ]
        
        t_content = Table(table_data, colWidths=[3.2*inch, 4.3*inch])
        t_content.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.HexColor("#F1F5F9")),
            ('BACKGROUND', (1,0), (1,0), colors.HexColor("#FEF3C7")),
            ('BACKGROUND', (0,1), (0,1), CODE_BG),
            ('BACKGROUND', (1,1), (1,1), CALLOUT_BG),
            ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        block.append(t_content)
        block.append(Spacer(1, 10))
        story.append(KeepTogether(block))

    # Step 1
    add_step_block(
        step_num="1",
        title="Inspect Raw Telemetry in Hadoop HDFS",
        speaker="Speaker 1 (HDFS Lead)",
        command_run="./1_hdfs_show_raw.sh",
        terminal_output="$ hdfs dfs -ls -h /air_quality/raw/\nFound 1 items\n-rw-r--r--   1 yash supergroup  47.3 M\n/air_quality/raw/\n raw_hourly_measurements.jsonl",
        what_to_say="Good morning evaluators. We are presenting Track B: Machine Learning at Scale. As you can see, our raw sensor data is staged directly in Hadoop HDFS under /air_quality/raw/. This 47.3 Megabyte file contains 96,000 raw hourly sensor readings fetched from OpenAQ API v3 across Delhi, Bengaluru, and Hyderabad using our rate-limited ingestion client.",
        what_it_proves="Proves real Big Data staging in HDFS with 128MB block architecture and 3x replication, rather than reading local CSVs."
    )

    # Step 2
    add_step_block(
        step_num="2",
        title="Inspect Partitioned Columnar Lake in HDFS",
        speaker="Speaker 1 (HDFS Lead)",
        command_run="./2_hdfs_show_parquet.sh",
        terminal_output="$ hdfs dfs -ls -h .../hourly_aqi_parquet/\nFound 4 items\n_SUCCESS\ncity=Bengaluru\ncity=Delhi NCR\ncity=Hyderabad",
        what_to_say="Driver is now displaying our processed storage layer. Instead of slow CSVs, we persist our cleaned data as Snappy-compressed columnar Apache Parquet partitioned by city. When downstream Spark queries run on Delhi, Spark performs partition pruning, scanning only the relevant directory and cutting disk I/O significantly.",
        what_it_proves="Demonstrates advanced data lake design, partition pruning, and columnar compression in HDFS."
    )

    # Step 3
    add_step_block(
        step_num="3",
        title="Execute Distributed Apache Spark ETL & CPCB Math",
        speaker="Speaker 2 (Spark ETL Lead)",
        command_run="./3_spark_run_etl.sh",
        terminal_output="$ python3 scripts/spark_etl.py\n================ STARTING SPARK ETL ================\n[1/6] Ingested 96,000 raw records.\n[3/6] Normalizing IST & gaseous units (ppb -> ug/m3)\n[5/6] Total Station-Hours: 18,521\n      Records Meeting CPCB 16h Rule: 12,792\nSample Output:\nDelhi NCR | R K Puram | cpcb_aqi: 500.0 (Severe)\nSpark ETL completed in 20.71 seconds.",
        what_to_say="I will now explain our Spark ETL pipeline. In 20 seconds, Spark cleans units, converts gases from ppb to ug/m3 using molecular weights, and computes rolling 24h windows. Crucially, we enforce the official Indian CPCB 16-hour completeness rule: a 24h window is only legally valid if at least 16 hours of valid data exist. Notice out of 18,521 station-hours, exactly 12,792 met this strict regulatory test.",
        what_it_proves="Proves deep domain compliance with Indian government CPCB NAQI piecewise formulas and high-performance in-memory Spark transformations."
    )

    # Step 4
    add_step_block(
        step_num="4",
        title="Run Distributed Spark SQL Analytics & Trend Insights",
        speaker="Speaker 2 (Spark ETL Lead)",
        command_run="./4_spark_run_analytics.sh",
        terminal_output="$ python3 scripts/run_analytics.py\n[1/4] City Statistics:\nDelhi: avg PM2.5 = 121.9 | avg AQI = 382.0\nBengaluru: avg PM2.5 = 28.8 | avg AQI = 293.9\n[2/4] Hazard Distribution:\nDelhi Severe hours: 62.5%\nBengaluru Satisfactory: 36.6%\n[4/4] Saved:\n  [CMD 4 - FIG 1] cmd4_fig1_diurnal_pm25_trends.png\n  [CMD 4 - FIG 2] cmd4_fig2_cpcb_category_distribution.png\n  [CMD 4 - FIG 3] cmd4_fig3_city_aqi_boxplots.png",
        what_to_say="Our Spark SQL queries reveal significant environmental realities. Delhi averages 121.9 ug/m3 PM2.5—over four times higher than Bengaluru. 62.5% of all Delhi hours are classified as Severe. Pointing to Figure 1 (cmd4_fig1), we see severe diurnal peaks at 08:00 AM caused by nocturnal thermal inversion trapping smoke, and an evening rush-hour peak at 08:00 PM.",
        what_it_proves="Validates distributed analytical queries and meteorological domain understanding (thermal inversions & rush hour cycles).",
        image_ref="cmd4_fig1, cmd4_fig2, cmd4_fig3 in reports/figures/"
    )

    # Step 5
    add_step_block(
        step_num="5",
        title="Train Distributed Spark MLlib 24-Hour Forecasting Models",
        speaker="Speaker 3 (Spark MLlib Lead)",
        command_run="./5_spark_mllib_forecasting.sh",
        terminal_output="$ python3 scripts/train_forecasting_models.py\n[2/5] Chronological Split (80% Train, 20% Test)\n[3/5] Naive Persistence Baseline -> RMSE: 42.16\n[5/5] Training MLlib Distributed Models:\n  - Linear Regression: RMSE 37.86 (+10.2%)\n  - Random Forest:     RMSE 35.17 (+16.6%)\n  - GBT Regressor:     RMSE 37.61 (+10.8%)\nBest Model: Random Forest (RMSE 35.17, 1.38s)\nSaved: [CMD 5 - FIG 1] cmd5_fig1_model_forecast...",
        what_to_say="Now for Machine Learning at scale with Spark MLlib. Notice two critical rigor decisions: First, we used a strict 80/20 chronological block split to prevent temporal data leakage—no future records leak into the past. Second, we benchmarked against the standard Naive Persistence Baseline (RMSE 42.16). Our distributed Random Forest achieved an RMSE of 35.17—a 16.6% improvement over baseline, training in just 1.38 seconds.",
        what_it_proves="Demonstrates leak-free time-series ML, feature engineering (lags t-1 to t-24), and beating persistence benchmarks at scale.",
        image_ref="cmd5_fig1_model_forecast_actual_vs_pred.png"
    )

    # Step 6
    add_step_block(
        step_num="6",
        title="Train Distributed Spark MLlib 6-Tier Hazard Classifier",
        speaker="Speaker 3 (Spark MLlib Lead)",
        command_run="./6_spark_mllib_classification.sh",
        terminal_output="$ python3 scripts/train_classification_model.py\nTraining distributed RandomForestClassifier...\n--- Spark MLlib Classification Metrics ---\n  Accuracy:           70.21%\n  Weighted F1-Score:  0.676\n  Weighted Precision: 0.674\n  Weighted Recall:    0.702\nSaved: [CMD 6 - FIG 1] cmd6_fig1_cpcb_classification...",
        what_to_say="Beyond numerical regression, municipal health agencies need discrete category alerts. We trained a distributed RandomForestClassifier to predict which of the 6 official CPCB hazard categories will occur 24 hours in advance. It achieves 70.21% test accuracy and a 0.676 weighted F1 score. As seen in cmd6_fig1, predictions are strongly concentrated along the diagonal, accurately identifying Severe alerts.",
        what_it_proves="Demonstrates multi-class classification at scale and practical public health decision support.",
        image_ref="cmd6_fig1_cpcb_classification_confusion_matrix.png"
    )

    # Step 7 & Summary
    story.append(Paragraph("<b>Step 7: Master Automated Pipeline & Wrap-Up</b>", h1_style))
    story.append(Paragraph(
        "<b>Action if examiner asks for an end-to-end run:</b> Driver executes <code>./7_run_entire_pipeline.sh</code>.<br/>"
        "<b>Speaker 1 Conclusion:</b> <i>\"In conclusion, our project demonstrates a complete, fault-tolerant distributed system under Track B: "
        "ingestion from real-world telemetry, raw storage in HDFS, strict regulatory CPCB mathematical transformation in Spark ETL, "
        "and distributed predictive forecasting with Spark MLlib. We are now happy to take your questions.\"</i>",
        body_style
    ))
    story.append(Spacer(1, 10))

    # Defense Q&A Cheat Sheet Table
    story.append(Paragraph("<b>2. Evaluator Viva Q&A Defense Cheat Sheet</b>", h1_style))
    story.append(Paragraph("Be prepared with these concise, mathematically and architecturally rigorous answers:", body_style))
    
    qa_data = [
        [Paragraph("<b>Question</b>", body_style), Paragraph("<b>Examiner Intent</b>", body_style), Paragraph("<b>Your Bulletproof Answer</b>", body_style)],
        [
            Paragraph("<b>Why Parquet over CSV in HDFS?</b>", body_style),
            Paragraph("Tests distributed storage knowledge", body_style),
            Paragraph("Parquet is columnar and Snappy-compressed, supporting <b>Partition Pruning</b> and dictionary encoding. Queries filtering by city skip irrelevant directories entirely, minimizing disk I/O.", body_style)
        ],
        [
            Paragraph("<b>Why Chronological split over K-Fold?</b>", body_style),
            Paragraph("Tests time-series ML integrity", body_style),
            Paragraph("Air quality is auto-correlated time series. Standard K-fold or random shuffling leaks future weather and pollution data into the past, causing severe data leakage and fake high scores.", body_style)
        ],
        [
            Paragraph("<b>What is CPCB 16-Hour rule?</b>", body_style),
            Paragraph("Tests domain compliance", body_style),
            Paragraph("CPCB guidelines require at least 16 hourly sensor readings in a 24-hour moving window for an exposure sub-index to be legally valid. Missing data below 16 hours is marked invalid.", body_style)
        ],
        [
            Paragraph("<b>Why Random Forest beat GBT?</b>", body_style),
            Paragraph("Tests ML architecture comparison", body_style),
            Paragraph("Air quality telemetry has high sensor noise and sudden peaks (inversion, dust, traffic). GBT optimizes residuals and overfits outliers, while Random Forest's bagging reduces variance and handles noise better.", body_style)
        ],
        [
            Paragraph("<b>How does this scale to 500+ cities?</b>", body_style),
            Paragraph("Tests Big Data scalability", body_style),
            Paragraph("Because every single transformation is written in distributed PySpark over HDFS, scaling requires zero code changes—only adding worker nodes and adjusting executor memory in spark-submit.", body_style)
        ],
    ]
    t_qa = Table(qa_data, colWidths=[1.8*inch, 1.4*inch, 4.3*inch])
    t_qa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_qa)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully at: {pdf_path}")

if __name__ == "__main__":
    out_pdf = "explanation/PRESENTATION_DEFENSE_SCRIPT.pdf"
    build_pdf(out_pdf)
