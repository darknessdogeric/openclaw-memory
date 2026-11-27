# -*- coding: utf-8 -*-
import io, sys, os, re, urllib.parse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = r'D:\B166ER-openclaw\workspace'
SRC = r'D:\B166ER-openclaw\workspace\media\inbound\openclaw-staged-ebdea283-4b35-4097-8dec-2a642a2a9045\input-image---1b1867e8-83f2-444a-9521-5d7babc81278.png'
OUT = os.path.join(ROOT, 'output', 'award_form')
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
engine = RapidOCR()
im = Image.open(SRC).convert('RGB')
W, H = im.size
print('=== A. 顶部单选区 6x OCR ===')
for tag, x0, x1, y0, y1 in [('radios', 0, W, 930, 1075), ('radioL', 0, 760, 930, 1075), ('radioR', 600, W, 930, 1075)]:
    c = im.crop((x0, y0, x1, y1)).resize(((x1-x0)*6, (y1-y0)*6), Image.LANCZOS)
    p = os.path.join(OUT, 'r6_%s.png' % tag)
    c.save(p)
    res, el = engine(p)
    print('--- %s ---' % tag)
    if res:
        for box, txt, conf in sorted(res, key=lambda r: (r[0][0][1], r[0][0][0])):
            print('   c=%.2f  %s' % (float(conf), txt))
    else:
        print('   (none)')
print()
print('=== B. 可疑候选名 web 核验 ===')
import requests
from concurrent.futures import ThreadPoolExecutor
tv = open(os.path.join(ROOT, 'tools', 'tavily_search.py'), encoding='utf-8').read()
tok = re.search(r'tvly-prod-[A-Za-z0-9\-]+', tv)
tok = tok.group(0) if tok else None
def ts(q):
    if not tok: return 'NO_TOK'
    try:
        r = requests.post('https://api.tavily.com/search',
            headers={'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json'},
            json={'query': q, 'max_results': 4, 'include_answer': True}, timeout=40)
        if r.status_code != 200: return 'HTTP ' + str(r.status_code)
        d = r.json()
        ans = str(d.get('answer',''))[:300]
        its = ['- ' + str(x.get('title',''))[:60] for x in d.get('results',[])[:3]]
        return ans + ' || ' + ' ; '.join(its)
    except Exception as e:
        return 'ERR ' + str(e)[:80]
QS = ['雁柏山庄 酒店 设计 中国', '七礁石酒店 中国 设计酒店', '既象 崇庆 SONYATA 度假酒店 成都', '大理 与归 民宿 设计', '外滩设计酒店大赏 第十八届 2027 平衡之道 候选']
def job(q): return q, ts(q)
with ThreadPoolExecutor(max_workers=5) as ex:
    for q, ans in ex.map(job, QS):
        print('#### ' + q)
        print('   ' + ans.replace(chr(10), ' ')[:420])