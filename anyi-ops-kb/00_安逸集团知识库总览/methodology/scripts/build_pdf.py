# -*- coding: utf-8 -*-
"""
build_pdf.py - 报告 PDF 构建（骨架）
历史：methodology/sop-region-analysis.md 引用。v1.0 骨架 — reportlab 实现。
"""
import sys
from pathlib import Path

def build_pdf(markdown_path: str, charts_dir: str = None, output_pdf: str = None) -> str:
    """
    输入: markdown + charts/ 目录
    输出: PDF 路径
    """
    try:
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        return f'Error: reportlab 未安装。请 pip install reportlab'

    md = Path(markdown_path).read_text(encoding='utf-8')
    out = output_pdf or str(Path(markdown_path).with_suffix('.pdf'))

    doc = SimpleDocTemplate(out)
    styles = getSampleStyleSheet()
    story = []
    for line in md.split('\n'):
        if line.startswith('# '):
            story.append(Paragraph(f'<b>{line[2:]}</b>', styles['Title']))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:], styles['Heading2']))
        elif line.strip():
            story.append(Paragraph(line, styles['BodyText']))
    doc.build(story)
    return out

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python build_pdf.py <report.md> [charts_dir] [output.pdf]')
        sys.exit(1)
    args = sys.argv[1:]
    print(build_pdf(args[0], args[1] if len(args) > 1 else None, args[2] if len(args) > 2 else None))