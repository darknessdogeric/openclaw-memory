# -*- coding: utf-8 -*-
"""
pdf_extract.py —— PDF 文本 + 表格双通道抽取（参数化能力工具）

用法：
    python pdf_extract.py <pdf路径> [输出txt路径] [--no-tables] [--pages N-M]

背景（2026-11-20 工具层治理）：
    toolbox 曾并存 5 个一次性脚本 dump_pdf.py / dump_pdf_hy.py / dump_pdf_lb.py /
    dump_pdf_str.py / dump_pdf_xz.py —— 逻辑完全相同，唯一差别是写死的 SRC 路径。
    每遇一份新 PDF 就复制一份，正是「重复造轮子」在工具层的真实形态。
    本工具为该族的正本：路径由参数传入，一次抽取任意 PDF。
    原 5 件已归档至 toolbox/_archive/pdf_dump_family_2026-11-20/（移动非删除，可回滚）。

能力：
    - 文本通道：pdfplumber 优先，失败退回 PyMuPDF，再退回 pypdf
    - 表格通道：pdfplumber extract_tables，行内单元格以 " | " 连接，空行丢弃
    - 输出 UTF-8，页码分节，附 PAGE 与 size 信息
"""
import io
import os
import sys


def _emit_header(out, total_pages, lib):
    out.append("PAGES: %d" % total_pages)
    out.append("EXTRACTOR: %s" % lib)


def extract_with_pdfplumber(src):
    import pdfplumber
    out = []
    with pdfplumber.open(src) as pdf:
        _emit_header(out, len(pdf.pages), "pdfplumber")
        for i, page in enumerate(pdf.pages, 1):
            out.append("")
            out.append("=" * 90)
            out.append("PAGE %d  size=%s" % (i, page.width))
            out.append("=" * 90)
            out.append(page.extract_text() or "")
            for ti, tb in enumerate(page.extract_tables(), 1):
                out.append("[TABLE %d]" % ti)
                for row in tb:
                    cells = ["" if c is None else str(c).replace("\n", " ") for c in row]
                    if any(c.strip() for c in cells):
                        out.append(" | ".join(cells))
    return out


def extract_with_fitz(src):
    import fitz
    doc = fitz.open(src)
    out = []
    _emit_header(out, doc.page_count, "PyMuPDF")
    for i, pg in enumerate(doc, 1):
        out.append("")
        out.append("=" * 90)
        out.append("PAGE %d" % i)
        out.append("=" * 90)
        out.append(pg.get_text())
    doc.close()
    return out


def extract_with_pypdf(src):
    from pypdf import PdfReader
    reader = PdfReader(src)
    out = []
    _emit_header(out, len(reader.pages), "pypdf")
    for i, page in enumerate(reader.pages, 1):
        out.append("")
        out.append("=" * 90)
        out.append("PAGE %d" % i)
        out.append("=" * 90)
        out.append(page.extract_text() or "")
    return out


def extract(src, want_tables=True):
    """按 pdfplumber -> PyMuPDF -> pypdf 顺序回退抽取，返回文本行列表。"""
    errors = []
    if want_tables:
        for fn in (extract_with_pdfplumber,):
            try:
                return fn(src)
            except Exception as e:
                errors.append("pdfplumber: %s" % e)
    for fn in (extract_with_fitz, extract_with_pypdf):
        try:
            return fn(src)
        except Exception as e:
            errors.append("%s: %s" % (fn.__name__, e))
    raise RuntimeError(" | ".join(errors))


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = {a for a in argv[1:] if a.startswith("--")}
    if not args:
        print(__doc__)
        return 2
    src = args[0]
    if not os.path.exists(src):
        print("NOT FOUND: %s" % src)
        return 1
    out_path = args[1] if len(args) > 1 else os.path.splitext(src)[0] + ".extract.txt"
    out = extract(src, want_tables="--no-tables" not in flags)
    d = os.path.dirname(out_path)
    if d:
        os.makedirs(d, exist_ok=True)
    with io.open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    print("OK chars=%d pages_hdr=%s -> %s" % (
        sum(len(x) for x in out),
        out[0] if out else "?", out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
