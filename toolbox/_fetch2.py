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
    for b in re.split(r'<li class="res-list"', h)[1:9]:
        m = re.search(r'<h3[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', b, re.S)
        if m:
            out.append((m.group(1), clean(m.group(2))))
    return out

QS = [
 '酒店 改造 分阶段 不停业 客房 分批 收益 案例',
 '酒店集团 存量改造 分级 投资限额 授权 管理办法',
 '在地文化 酒店 前台 后台 双层架构 标准化 复制',
 '酒店 有限服务 全服务 收入结构 客房占比 非房占比 对比',
]
for q in QS:
    print('=' * 92)
    print('Q: ' + q)
    try:
        ls = so_links(q)
    except Exception as e:
        print('  搜索失败:', str(e)[:70]); continue
    n = 0
    for url, title in ls:
        if not url.startswith('http'):
            continue
        print('  * ' + title[:74])
        print('    ' + url[:118])
        try:
            body = clean(fetch(url))
            print('    ' + body[:1100])
        except Exception as e:
            print('    抓取失败:', str(e)[:50])
        n += 1
        if n >= 2:
            break
        time.sleep(0.4)
