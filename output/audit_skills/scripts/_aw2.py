# -*- coding: utf-8 -*-
import io, sys, os, re, importlib.util
from concurrent.futures import ThreadPoolExecutor
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = r'D:\B166ER-openclaw\workspace'
spec = importlib.util.spec_from_file_location('fa', os.path.join(ROOT,'tools','fetch_any.py'))
fa = importlib.util.module_from_spec(spec); spec.loader.exec_module(fa)
URLS = [
 ('netease_award', 'https://www.163.com/dy/article/L2U4I0DL0524BERB.html'),
 ('qq_award', 'https://news.qq.com/rain/a/20260814A06HG600'),
 ('netease_g2', 'https://www.163.com/dy/article/KG3LASKT051285HS.html'),
 ('bund_official', 'https://www.thebundhotelawards.com/'),
 ('bund_alt', 'https://www.bunddesignhotelawards.com/'),
]
def clean(h):
    h = re.sub(r'(?is)<script.*?</script>|<style.*?</style>', ' ', h)
    return re.sub(r'(?s)<[^>]+>', chr(10), h)
def job(t):
    tag, u = t
    h, how = fa.fetch_html(u, ms=40000)
    if not h: return tag, u, how, ''
    txt = chr(10).join(x.strip() for x in clean(h).split(chr(10)) if len(x.strip()) > 10)
    return tag, u, how, txt
PAT = r'(Design|Art|Reborn|Next|设计|艺术|焕新|新生|平衡|避世|时髦|奖项|评审|评委|投票|候选|报名|入选|提名|2026|2027|12月|类目|年度|提名权|终审|颁奖|入围|候选名单)'
with ThreadPoolExecutor(max_workers=5) as ex:
    for tag, u, how, txt in ex.map(job, URLS):
        print()
        print('-' * 92)
        print('### %s | %s | %s' % (tag, how, u))
        print('-' * 92)
        seen = set(); n = 0
        for l in txt.split(chr(10)):
            k = re.sub(r'\s+',' ',l)[:46]
            if k in seen: continue
            seen.add(k)
            if re.search(PAT, l):
                print('   ' + re.sub(r'\s+',' ', l)[:240]); n += 1
                if n >= 26: break