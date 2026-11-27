# -*- coding: utf-8 -*-
import io, sys, os, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
print('=== OCR 引擎可用性 ===')
for exe in ['tesseract']:
    p = shutil.which(exe)
    print('  %-12s %s' % (exe, p or 'NOT FOUND'))
for mod in ['paddleocr','easyocr','rapidocr_onnxruntime','pytesseract','cnocr']:
    try:
        __import__(mod); print('  %-24s OK' % mod)
    except Exception as e:
        print('  %-24s --' % mod)
print()
print('=== 是否有 Windows OCR 语言包 ===')
import glob
for p in glob.glob(r'C:\Windows\OCR\*'):
    print('  ', p)
try:
    langs = glob.glob(r'C:\Program Files\WindowsApps\*OCR*') + glob.glob(r'C:\Windows\System32\OCR\*')
    print('  System32 OCR:', glob.glob(r'C:\Windows\System32\OCR\*')[:5])
except Exception as e:
    print(e)