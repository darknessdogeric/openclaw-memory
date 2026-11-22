# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SRC = r'C:\Users\ericz\Desktop\中共四川省旅投集团第一届委员会第188次（2026年第23次）会议纪要-传达议题.pdf'
OUT = r'D:\B166ER-openclaw\workspace\tmp\_lst_188.txt'
os.makedirs(os.path.dirname(OUT), exist_ok=True)

text = None
lib = None

try:
    import fitz
    d = fitz.open(SRC)
    parts = []
    for i, pg in enumerate(d):
        parts.append('=== PAGE %d ===' % (i + 1))
        parts.append(pg.get_text())
    text = '\n'.join(parts)
    lib = 'PyMuPDF'
    print('pages: %d' % d.page_count)
except Exception as e:
    print('fitz fail: %s' % e)

if not text:
    try:
        from pypdf import PdfReader
        r = PdfReader(SRC)
        parts = []
        for i, pg in enumerate(r.pages):
            parts.append('=== PAGE %d ===' % (i + 1))
            parts.append(pg.extract_text() or '')
        text = '\n'.join(parts)
        lib = 'pypdf'
        print('pages: %d' % len(r.pages))
    except Exception as e:
        print('pypdf fail: %s' % e)

if not text:
    try:
        import pdfplumber
        parts = []
        with pdfplumber.open(SRC) as pdf:
            for i, pg in enumerate(pdf.pages):
                parts.append('=== PAGE %d ===' % (i + 1))
                parts.append(pg.extract_text() or '')
        text = '\n'.join(parts)
        lib = 'pdfplumber'
        print('pages: %d' % len(parts))
    except Exception as e:
        print('pdfplumber fail: %s' % e)

if text is None:
    print('NO_PDF_LIB')
    sys.exit(2)

open(OUT, 'w', encoding='utf-8').write(text)
print('LIB %s  chars %d -> %s' % (lib, len(text), OUT))
print('--- head ---')
print(text[:900])
