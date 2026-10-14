import re
import base64
import subprocess
from pathlib import Path
import markdown

WORKSPACE_ROOT = Path(".").resolve()
md_file = WORKSPACE_ROOT / "explanation" / "PRESENTATION_SCRIPT.md"
md_text = md_file.read_text(encoding="utf-8")

# Convert relative image paths to base64 data URIs so Chrome embeds them seamlessly
def embed_images(match):
    alt_text = match.group(1)
    img_rel = match.group(2)
    # resolve image path
    img_path = (md_file.parent / img_rel).resolve()
    if img_path.exists():
        b64 = base64.b64encode(img_path.read_bytes()).decode('utf-8')
        return f'<div class="img-container"><img src="data:image/png;base64,{b64}" alt="{alt_text}"/><div class="img-caption">{alt_text}</div></div>'
    return f'<p><em>[Image not found: {img_rel}]</em></p>'

# Replace ![alt](path) with embedded html
img_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
md_text = img_pattern.sub(embed_images, md_text)

html_body = markdown.markdown(
    md_text,
    extensions=['tables', 'fenced_code', 'nl2br']
)

full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Google Meet Video Recording Script & Defense Guide</title>
<style>
  @page {{
    size: A4;
    margin: 16mm 14mm 16mm 14mm;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    line-height: 1.5;
    font-size: 10pt;
    margin: 0;
    padding: 0;
  }}
  h1 {{
    color: #0f172a;
    font-size: 18pt;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 6px;
    margin-top: 0;
    margin-bottom: 6px;
  }}
  h2 {{
    color: #0369a1;
    font-size: 13pt;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    margin-top: 18px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }}
  h3 {{
    color: #334155;
    font-size: 11pt;
    margin-top: 12px;
    margin-bottom: 4px;
    page-break-after: avoid;
  }}
  blockquote {{
    background-color: #fefce8;
    border-left: 4px solid #f59e0b;
    margin: 6px 0;
    padding: 8px 12px;
    color: #0f172a;
    font-size: 10pt;
    border-radius: 4px;
    page-break-inside: avoid;
  }}
  blockquote p {{
    margin: 3px 0;
  }}
  pre {{
    background-color: #0f172a;
    color: #38bdf8;
    padding: 10px 12px;
    border-radius: 6px;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
    font-size: 8.5pt;
    line-height: 1.35;
    overflow-x: auto;
    margin: 6px 0;
    page-break-inside: avoid;
  }}
  code {{
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
    font-size: 9pt;
    background-color: #f1f5f9;
    color: #0369a1;
    padding: 2px 4px;
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
    margin: 10px 0;
    font-size: 9pt;
    page-break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #cbd5e1;
    padding: 6px 8px;
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
    margin: 14px 0;
  }}
  .img-container {{
    text-align: center;
    margin: 10px 0;
    page-break-inside: avoid;
  }}
  img {{
    max-width: 90%;
    max-height: 340px;
    border-radius: 6px;
    border: 1px solid #cbd5e1;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    margin: 0 auto;
    display: block;
  }}
  .img-caption {{
    font-size: 8.5pt;
    color: #64748b;
    font-style: italic;
    margin-top: 4px;
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

html_file = WORKSPACE_ROOT / "explanation" / "presentation_print.html"
html_file.write_text(full_html, encoding="utf-8")

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
print("Chrome compilation finished with code:", res.returncode)
print("PDF output file size:", pdf_file.stat().st_size if pdf_file.exists() else "Missing")
