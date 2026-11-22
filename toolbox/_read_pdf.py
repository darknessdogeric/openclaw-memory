# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = 'C:\\Users\\ericz\\Desktop\\安逸酒店集团大运营体系建设实施方案20261104.pdf'
print('存在:', os.path.exists(P), ' 大小:', os.path.getsize(P) // 1024 if os.path.exists(P) else 0, 'KB')
text = ''
try:
    import pypdf
    r = pypdf.PdfReader(P)
    print('pypdf 页数:', len(r.pages))
    parts = []
    for i, pg in enumerate(r.pages):
        parts.append('\n===== PAGE %d =====\n' % (i + 1) + (pg.extract_text() or ''))
    text = '\n'.join(parts)
except Exception as e:
    print('pypdf 失败:', str(e)[:120])
    try:
        import fitz
        doc = fitz.open(P)
        print('fitz 页数:', doc.page_count)
        text = '\n'.join('\n===== PAGE %d =====\n%s' % (i + 1, doc[i].get_text()) for i in range(doc.page_count))
    except Exception as e2:
        print('fitz 失败:', str(e2)[:120])
if text:
    print('提取字符数:', len(text))
    print('可打印占比: %.1f%%' % (100.0 * sum(1 for c in text if c.strip() and c.isprintable()) / max(1, len(text))))
    open('D:\\B166ER-openclaw\\workspace\\tmp\\_dyun_text.txt', 'w', encoding='utf-8').write(text)
    print('已存 tmp/_dyun_text.txt')
    print('')
    print('===== 正文全文 =====')
    print(text[:22000])
else:
    print('!! 无法提取文本，可能是扫描件')