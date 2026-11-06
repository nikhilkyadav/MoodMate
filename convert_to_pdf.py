"""
convert_to_pdf.py - Converts experiment_design.md to publication-quality PDF.
Uses Markdown + KaTeX + Mermaid.js + Headless Edge/Chrome printing.
"""

import os
import re
import subprocess
import markdown

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = r"C:\Users\Nikhil Yadav\.gemini\antigravity\brain\759f85db-6584-4670-9db3-e394b904e51c\experiment_design.md"
HTML_PATH = os.path.join(BASE_DIR, "experiment_design.html")
PDF_PATH = os.path.join(BASE_DIR, "experiment_design.pdf")

def main():
    if not os.path.exists(MD_PATH):
        raise FileNotFoundError(f"Markdown file not found: {MD_PATH}")

    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Pre-process Mermaid blocks so markdown doesn't mess with them
    mermaid_blocks = []
    def save_mermaid(match):
        code = match.group(1).strip()
        idx = len(mermaid_blocks)
        mermaid_blocks.append(code)
        return f"<!--MERMAID_{idx}-->"

    processed_md = re.sub(r"```mermaid\s*([\s\S]*?)```", save_mermaid, md_text)

    # Convert markdown to HTML
    html_content = markdown.markdown(
        processed_md,
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"]
    )

    # Re-insert Mermaid blocks
    for idx, code in enumerate(mermaid_blocks):
        clean_code = code.strip()
        mermaid_html = f'<div class="mermaid-container"><div class="mermaid">{clean_code}</div></div>'
        html_content = html_content.replace(f"<!--MERMAID_{idx}-->", mermaid_html)

    # Full HTML template with KaTeX, Mermaid, and Academic CSS
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>MoodMate - Experiment Design & Evaluation Framework</title>
  
  <!-- KaTeX for LaTeX Math -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
          onload="renderMathInElement(document.body, {{
            delimiters: [
              {{left: '$$', right: '$$', display: true}},
              {{left: '$', right: '$', display: false}}
            ]
          }});"></script>

  <!-- Mermaid.js for Diagrams -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({{
      startOnLoad: true,
      theme: 'neutral',
      fontFamily: 'Inter, system-ui, sans-serif',
      securityLevel: 'loose',
      flowchart: {{ useMaxWidth: false, htmlLabels: true }},
      sequence: {{ useMaxWidth: false, showSequenceNumbers: true }}
    }});
  </script>

  <style>
    @page {{
      size: A4 portrait;
      margin: 18mm 16mm 18mm 16mm;
    }}

    *, *::before, *::after {{
      box-sizing: border-box;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-size: 10.5pt;
      line-height: 1.55;
      color: #1e293b;
      background: #ffffff;
      margin: 0;
      padding: 0;
    }}

    h1, h2, h3, h4, h5, h6 {{
      color: #0f172a;
      font-weight: 700;
      line-height: 1.25;
      margin-top: 1.4em;
      margin-bottom: 0.5em;
      page-break-after: avoid;
    }}

    h1 {{
      font-size: 20pt;
      border-bottom: 2px solid #3b82f6;
      padding-bottom: 8px;
      margin-top: 0;
      color: #1d4ed8;
    }}

    h2 {{
      font-size: 14pt;
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 4px;
      margin-top: 1.6em;
      color: #0f172a;
    }}

    h3 {{
      font-size: 11.5pt;
      margin-top: 1.2em;
      color: #334155;
    }}

    p {{
      margin: 0.6em 0;
    }}

    blockquote {{
      margin: 1em 0;
      padding: 10px 16px;
      background-color: #f8fafc;
      border-left: 4px solid #3b82f6;
      border-radius: 0 6px 6px 0;
      color: #334155;
      font-size: 9.5pt;
    }}

    blockquote p {{
      margin: 0.3em 0;
    }}

    /* Tables */
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.2em 0;
      font-size: 9pt;
      page-break-inside: avoid;
    }}

    th, td {{
      padding: 8px 10px;
      border: 1px solid #cbd5e1;
      text-align: left;
      vertical-align: top;
    }}

    th {{
      background-color: #f1f5f9;
      font-weight: 600;
      color: #0f172a;
    }}

    tr:nth-child(even) td {{
      background-color: #f8fafc;
    }}

    /* Lists */
    ul, ol {{
      margin: 0.5em 0;
      padding-left: 24px;
    }}

    li {{
      margin-bottom: 0.3em;
    }}

    /* Code & Pre */
    code {{
      font-family: "JetBrains Mono", Consolas, Monaco, "Courier New", monospace;
      font-size: 8.8pt;
      background-color: #f1f5f9;
      padding: 2px 5px;
      border-radius: 4px;
      color: #0f172a;
      border: 1px solid #e2e8f0;
    }}

    pre {{
      background-color: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 12px;
      overflow-x: auto;
      font-size: 8.5pt;
      line-height: 1.4;
      page-break-inside: avoid;
    }}

    pre code {{
      background: none;
      border: none;
      padding: 0;
    }}

    /* Mermaid Diagrams */
    .mermaid-container {{
      margin: 1.4em 0;
      text-align: center;
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 16px;
      page-break-inside: avoid;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }}

    .mermaid svg {{
      max-width: 100% !important;
      height: auto !important;
    }}

    /* Horizontal Rule */
    hr {{
      border: none;
      border-top: 1px solid #e2e8f0;
      margin: 1.8em 0;
    }}

    /* Print Optimizations */
    @media print {{
      body {{
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }}
      .mermaid-container, table, blockquote {{
        page-break-inside: avoid;
      }}
      h1, h2, h3 {{
        page-break-after: avoid;
      }}
    }}
  </style>
</head>
<body>
  {html_content}
</body>
</html>
"""

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Generated HTML file: {HTML_PATH}")

    # Browser executable selection (Edge or Chrome)
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    browser_exe = edge_path if os.path.exists(edge_path) else chrome_path

    if not os.path.exists(browser_exe):
        raise RuntimeError("Neither Microsoft Edge nor Google Chrome executable found!")

    print(f"Using browser renderer: {browser_exe}")

    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=6000",
        f"--print-to-pdf={PDF_PATH}",
        "--no-pdf-header-footer",
        HTML_PATH
    ]

    print("Executing headless browser print to PDF...")
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)

    if os.path.exists(PDF_PATH) and os.path.getsize(PDF_PATH) > 0:
        size_kb = os.path.getsize(PDF_PATH) / 1024
        print(f"[SUCCESS] PDF created successfully at: {PDF_PATH} ({size_kb:.1f} KB)")
        
        # Mirror to artifact directory
        artifact_pdf = r"C:\Users\Nikhil Yadav\.gemini\antigravity\brain\759f85db-6584-4670-9db3-e394b904e51c\experiment_design.pdf"
        try:
            import shutil
            shutil.copy2(PDF_PATH, artifact_pdf)
            print(f"[SUCCESS] Mirrored PDF to artifact directory: {artifact_pdf}")
        except Exception as e:
            print(f"[WARN] Could not mirror to artifact dir: {e}")
    else:
        print(f"[ERROR] Failed to generate PDF. Stderr: {res.stderr}")
        raise RuntimeError(f"PDF creation failed: {res.stderr}")

if __name__ == "__main__":
    main()

