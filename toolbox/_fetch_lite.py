# -*- coding: utf-8 -*-
import io, sys, os, re, gzip, urllib.request, urllib.parse, html, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

def fetch(url, timeout=18):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'zh-CN,zh;q=0.9'})
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

def so_links(q):
    h = fetch('https://www.so.com/s?q=' + urllib.parse.quote(q))
    out = []
    for b in re.split(r'<li class="res-list"', h)[1:8]:
        m = re.search(r'<h3[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', b, re.S)
        if m:
            out.append((m.group(1), clean(m.group(2))))
    return out

qs = ['存量酒店改造 轻重缓急 不是所有翻新都要大拆大建', '酒店装修翻新成本核算 不同星级 改造单价 回收周期 测算']
for q in qs:
    print('=' * 88)
    print('Q: ' + q)
    try:
        ls = so_links(q)
    except Exception as e:
        print('  搜索失败:', str(e)[:70]); continue
    n = 0
    for url, title in ls:
        if not url.startswith('http'):
            continue
        print('  * ' + title[:76])
        print('    ' + url[:120])
        try:
            body = clean(fetch(url))
            print('    正文节选: ' + body[:1400])
        except Exception as e:
            print('    抓取失败:', str(e)[:60])
        n += 1
        if n >= 2:
            break
        time.sleep(0.5)
