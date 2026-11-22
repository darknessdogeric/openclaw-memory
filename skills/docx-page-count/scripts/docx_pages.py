# -*- coding: utf-8 -*-
"""docx 实测页数：md -> docx -> pdf -> 页数（含每页字符分布）

用法：
    python docx_pages.py <md> <docx> "<标题>" "<副标题>"     # 全流程
    python docx_pages.py --pages-only <docx>                 # 只数已有 docx

依赖：LibreOffice(soffice.com) + PyMuPDF
"""
import io, os, sys, subprocess, glob, shutil
sys.stdout.reconfigure(encoding='utf-8')

SOFFICE = r'C:\Program Files\LibreOffice\program\soffice.com'
MD2DOCX = r'D:\B166ER-openclaw\workspace\toolbox\md2docx.py'
PY = r'C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe'
TMP = r'C:\Users\ericz\AppData\Local\Temp\lopdf'


def build(md, docx, title, subtitle):
    r = subprocess.run([PY, MD2DOCX, md, docx, '--title', title, '--subtitle', subtitle],
                       capture_output=True)
    out = (r.stdout or b'') + (r.stderr or b'')
    print(out.decode('utf-8', 'replace').strip()[:300])


def pages(docx):
    if not os.path.exists(SOFFICE):
        print('ERROR: 未找到 LibreOffice，请先安装。见 TOOLS.md')
        return None, []
    shutil.rmtree(TMP, ignore_errors=True)
    os.makedirs(TMP, exist_ok=True)
    subprocess.run([SOFFICE, '--headless', '--norestore', '--convert-to', 'pdf',
                    '--outdir', TMP, docx], capture_output=True, timeout=300)
    f = glob.glob(os.path.join(TMP, '*.pdf'))
    if not f:
        print('ERROR: 转换失败，未生成 PDF')
        return None, []
    try:
        import pymupdf as fitz
    except Exception:
        import fitz
    d = fitz.open(f[0])
    n = d.page_count
    info = [(i + 1, len(d[i].get_text().strip())) for i in range(n)]
    d.close()
    return n, info


def report(n, info):
    if n is None:
        return
    print('PAGES =', n)
    for p, c in info:
        flag = ''
        if n > 1 and p == n and c < 0.45 * max(x for _, x in info[:-1] or [1]):
            flag = '   <-- 尾页溢出：削这一段可收回上一页'
        print('   p%d: %d chars%s' % (p, c, flag))


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        sys.exit(1)
    if a[0] == '--pages-only':
        n, info = pages(a[1])
        report(n, info)
    else:
        md, docx = a[0], a[1]
        title = a[2] if len(a) > 2 else ''
        sub = a[3] if len(a) > 3 else ''
        build(md, docx, title, sub)
        n, info = pages(docx)
        report(n, info)
