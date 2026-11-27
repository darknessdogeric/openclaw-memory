# -*- coding: utf-8 -*-
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = r'D:\B166ER-openclaw\workspace'
print('=== 1. KB: 安逸 峨眉山 / 乐山 嘉州 物业 ===')
files = glob.glob(os.path.join(ROOT, 'anyi-ops-kb', '**', '*.md'), recursive=True)
files += glob.glob(os.path.join(ROOT, 'memory', '*.md'))
seen = 0
for p in files:
    try: t = open(p, encoding='utf-8', errors='replace').read()
    except Exception: continue
    if ('峨眉' in t) and ('嘉州' in t or '安逸' in t):
        for l in t.split(chr(10)):
            s = l.strip()
            if ('峨眉' in s) and len(s) > 12 and len(s) < 300:
                print('   [%s] %s' % (os.path.basename(p)[:34], re.sub(r'\s+',' ',s)[:190]))
                seen += 1
                break
        if seen >= 12: break
print()
print('=== 2. web: 梅里泊度 归属 + 松赞关系 ===')
import requests
tv = open(os.path.join(ROOT, 'tools', 'tavily_search.py'), encoding='utf-8').read()
m = re.search(r'tvly-prod-[A-Za-z0-9\-]{20,}', tv)
print('   tavily key found:', bool(m))
if m:
    def ts(q):
        try:
            r = requests.post('https://api.tavily.com/search',
                headers={'Authorization': 'Bearer ' + m.group(0), 'Content-Type': 'application/json'},
                json={'query': q, 'max_results': 4, 'include_answer': True}, timeout=40)
            if r.status_code != 200: return 'HTTP ' + str(r.status_code)
            d = r.json()
            return str(d.get('answer',''))[:400] + ' || ' + ' ; '.join(str(x.get('title',''))[:50] for x in d.get('results',[])[:3])
        except Exception as e:
            return 'ERR ' + str(e)[:70]
    for q in ['德钦 梅里泊度 MEILI LODGE 业主 松赞 Songtsam 运营',
              '外滩设计酒店大赏 第18届 生活家评委 人数 权威评审团 投票 2026']:
        print('#### ' + q)
        print('   ' + ts(q).replace(chr(10), ' ')[:460])