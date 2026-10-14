import subprocess
from pathlib import Path
import markdown

md_file = Path("explanation/PRESENTATION_SCRIPT.md")
md_text = md_file.read_text(encoding="utf-8")

html_body = markdown.markdown(
    md_text,
    extensions=['tables', 'fenced_code', 'nl2br']
)

full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Google Meet Video Recording Script</title>
<style>
  @page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    line-height: 1.5;
    font-size: 11pt;
    margin: 0;
    padding: 0;
  }}
  h1 {{
    color: #0f172a;
    font-size: 20pt;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 6px;
    margin-top: 0;
    margin-bottom: 8px;
  }}
  h2 {{
    color: #0369a1;
    font-size: 14pt;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    margin-top: 22px;
    margin-bottom: 10px;
    page-break-after: avoid;
  }}
  h3 {{
    color: #334155;
    font-size: 11.5pt;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}
  blockquote {{
    background-color: #fefce8;
    border-left: 4px solid #f59e0b;
    margin: 8px 0;
    padding: 10px 14px;
    color: #0f172a;
    font-size: 10.5pt;
    border-radius: 4px;
  }}
  blockquote p {{
    margin: 4px 0;
  }}
  pre {{
    background-color: #0f172a;
    color: #38bdf8;
    padding: 12px 14px;
    border-radius: 6px;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
    font-size: 9pt;
    line-height: 1.35;
    overflow-x: auto;
    margin: 8px 0;
    page-break-inside: avoid;
  }}
  code {{
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
    font-size: 9.5pt;
    background-color: #f1f5f9;
    color: #0369a1;
    padding: 2px 5px;
    border-radius: 3px;
  }}
  pre code {{
    background-color: transparent;
    color: inherit;
    padding: 0;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #cbd5e1;
    padding: 8px 10px;
    text-align: left;
    vertical-align: top;
  }}
  th {{
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
  }}
  tr:nth-child(even) {{
    background-color: #f8fafc;
  }}
  hr {{
    border: 0;
    height: 1px;
    background: #e2e8f0;
    margin: 18px 0;
  }}
  ul, ol {{
    margin: 6px 0;
    padding-left: 22px;
  }}
  li {{
    margin-bottom: 4px;
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

html_file = Path("explanation/presentation_print.html")
html_file.write_text(full_html, encoding="utf-8")

pdf_file = Path("explanation/PRESENTATION_DEFENSE_SCRIPT.pdf").resolve()
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
print("Chrome exit code:", res.returncode)
print("PDF output size:", pdf_file.stat().st_size if pdf_file.exists() else "File not found")
