# -*- coding: utf-8 -*-
import io, sys, os, re, glob, gzip, urllib.request, urllib.parse, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document

def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = r.read()
        if r.headers.get('Content-Encoding') == 'gzip':
            try: d = gzip.decompress(d)
            except Exception: pass
    for e in ('utf-8', 'gbk', 'gb18030'):
        try: return d.decode(e)
        except Exception: continue
    return d.decode('utf-8', 'replace')

def clean(h):
    h = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', h)
    h = re.sub(r'(?s)<[^>]+>', ' ', h)
    return re.sub(r'\s+', ' ', html.unescape(h)).strip()

# ---------- 1. 定位述职报告 ----------
print('=== 1. 述职报告定位与口径 ===')
cands = glob.glob(r'C:\Users\ericz\Desktop\**\*述职报告*.docx', recursive=True)
print('候选:', [os.path.basename(c) for c in cands][:5])
for c in cands[:1]:
    d = Document(c)
    ks = ['5.2亿', '考核口径', '旅行社', '2026年度核心经营目标']
    for i, x in enumerate(d.paragraphs):
        t = x.text.strip()
        if t and any(k in t for k in ks):
            print('  P%d: %s' % (i, t[:300]))

# ---------- 2. 检索并抓取关键文章 ----------
print()
print('=== 2. 轻改造关键文献 ===')
qs = ['旧酒店改造不用大拆大建 低成本焕新 RevPAR 提升 20%', '存量酒店改造 轻重缓急 不是所有翻新都要大拆大建', '酒店装修翻新成本 不同星级 改造单价 回收周期']
for q in qs:
    print('-' * 84)
    print('Q: ' + q)
    try:
        h = fetch('https://www.sogou.com/web?query=' + urllib.parse.quote(q))
    except Exception as e:
        print('  fetch fail', str(e)[:60]); continue
    links = re.findall(r'<h3[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', h, re.S)
    seen = 0
    for url, title in links[:4]:
        t = clean(title)
        if not t or len(t) < 6:
            continue
        print('  * ' + t[:70])
        print('    ' + url[:110])
        seen += 1
        if seen >= 2:
            break
