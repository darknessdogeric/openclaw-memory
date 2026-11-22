# -*- coding: utf-8 -*-
"""
MD → HTML → PDF 转换器（使用 Edge headless）
B166ER · 2026-08-01 13:15 GMT+8
"""
import sys
import subprocess
from pathlib import Path
import markdown

WORKSPACE = Path(r'D:\B166ER-OpenClaw\workspace')

# 中文字体 fallback（CSS 用）
CSS = """
@page {
    size: A4;
    margin: 2.5cm 2cm 2.5cm 2cm;
}

body {
    font-family: "Microsoft YaHei", "PingFang SC", "Hiragino Sans GB", "WenQuanYi Micro Hei", sans-serif;
    font-size: 11pt;
    line-height: 1.7;
    color: #1a1a1a;
    max-width: 100%;
}

h1 {
    font-size: 22pt;
    font-weight: bold;
    color: #003366;
    border-bottom: 3px solid #003366;
    padding-bottom: 8pt;
    margin-top: 24pt;
    margin-bottom: 16pt;
    page-break-before: always;
}

h1:first-of-type {
    page-break-before: avoid;
}

h2 {
    font-size: 16pt;
    font-weight: bold;
    color: #003366;
    margin-top: 20pt;
    margin-bottom: 12pt;
    border-left: 4px solid #003366;
    padding-left: 10pt;
}

h3 {
    font-size: 13pt;
    font-weight: bold;
    color: #2a4d6e;
    margin-top: 16pt;
    margin-bottom: 8pt;
}

h4 {
    font-size: 12pt;
    font-weight: bold;
    color: #4a6d8e;
    margin-top: 12pt;
    margin-bottom: 6pt;
}

p {
    margin: 8pt 0;
    text-align: justify;
}

blockquote {
    border-left: 4px solid #ccc;
    margin: 12pt 0;
    padding: 8pt 12pt;
    color: #555;
    background-color: #f9f9f9;
    font-style: italic;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 12pt 0;
    font-size: 10pt;
}

th {
    background-color: #003366;
    color: white;
    padding: 8pt;
    border: 1px solid #ddd;
    text-align: left;
    font-weight: bold;
}

td {
    padding: 6pt 8pt;
    border: 1px solid #ddd;
    vertical-align: top;
}

tr:nth-child(even) {
    background-color: #f5f5f5;
}

code {
    background-color: #f4f4f4;
    padding: 2pt 4pt;
    border-radius: 2pt;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 10pt;
    color: #c7254e;
}

pre {
    background-color: #f4f4f4;
    padding: 12pt;
    border-radius: 4pt;
    overflow-x: auto;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 10pt;
    line-height: 1.4;
}

ul, ol {
    margin: 8pt 0;
    padding-left: 24pt;
}

li {
    margin: 4pt 0;
}

hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 16pt 0;
}

strong {
    color: #003366;
    font-weight: bold;
}

em {
    color: #555;
}

.cover {
    page-break-after: always;
    text-align: center;
    padding-top: 30%;
}

.cover h1 {
    border: none;
    font-size: 28pt;
    color: #003366;
    margin-bottom: 24pt;
}

.cover .subtitle {
    font-size: 16pt;
    color: #555;
    margin: 12pt 0;
}

.cover .meta {
    margin-top: 48pt;
    font-size: 11pt;
    color: #888;
}

@media print {
    h1 { page-break-before: always; }
    h1:first-of-type { page-break-before: avoid; }
    h2, h3 { page-break-after: avoid; }
    table, figure { page-break-inside: avoid; }
}
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""


def md_to_html(md_path: Path, html_path: Path):
    """MD → HTML"""
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    md_engine = markdown.Markdown(
        extensions=[
            'extra',         # tables, fenced_code, etc.
            'tables',
            'fenced_code',
            'toc',
            'sane_lists',
            'codehilite',
        ],
        extension_configs={
            'toc': {'permalink': False}
        }
    )

    html_body = md_engine.convert(md_content)

    title = md_path.stem
    html_content = HTML_TEMPLATE.format(title=title, css=CSS, body=html_body)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"  [HTML] {html_path} ({len(html_content)} chars)")


def html_to_pdf(html_path: Path, pdf_path: Path):
    """HTML → PDF (Edge headless)"""
    edge = Path(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')

    if not edge.exists():
        raise FileNotFoundError(f"Edge not found at {edge}")

    # 使用 Edge headless 打印 PDF
    cmd = [
        str(edge),
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        '--disable-extensions',
        '--disable-software-rasterizer',
        '--no-pdf-header-footer',  # 移除默认页眉页脚
        '--print-to-pdf=' + str(pdf_path),
        '--force-device-scale-factor=2',  # Retina 高清 (Eric 2026-05-21 明确要求)
        'file:///' + str(html_path).replace('\\', '/'),
    ]

    print(f"  [Edge] cmd: {' '.join(cmd[:5])}...")
    result = subprocess.run(
        cmd,
        timeout=120,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"  [Edge stderr] {result.stderr[:500]}")
        raise RuntimeError(f"Edge failed with code {result.returncode}")

    if not pdf_path.exists():
        raise RuntimeError(f"PDF not generated at {pdf_path}")

    pdf_size = pdf_path.stat().st_size
    print(f"  [PDF] {pdf_path} ({pdf_size:,} bytes)")


def main():
    if len(sys.argv) < 2:
        # 默认模式：处理今日 DeepSeek 生成的评估报告
        md_file = WORKSPACE / 'anyi-ops-kb' / '02_项目' / '总府四川宾馆' / '评估报告_DeepSeek_2026-08-01.md'
    else:
        md_file = Path(sys.argv[1])

    if not md_file.exists():
        print(f"ERROR: MD file not found: {md_file}")
        sys.exit(1)

    pdf_file = md_file.with_suffix('.pdf')
    html_file = md_file.with_suffix('.html')

    print("=" * 80)
    print(f"  MD → PDF 转换")
    print(f"  Source: {md_file.name}")
    print(f"  Target: {pdf_file.name}")
    print("=" * 80)

    # Step 1: MD → HTML
    print("\n[1] MD → HTML")
    md_to_html(md_file, html_file)

    # Step 2: HTML → PDF
    print("\n[2] HTML → PDF (Edge headless)")
    html_to_pdf(html_file, pdf_file)

    print(f"\n[完成] PDF: {pdf_file}")
    print(f"      Size: {pdf_file.stat().st_size:,} bytes")


if __name__ == '__main__':
    main()