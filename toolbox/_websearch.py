# -*- coding: utf-8 -*-
import io, sys, os, re, gzip, urllib.request, urllib.parse, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                                               'Accept': 'text/html,application/xhtml+xml'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
        if r.headers.get('Content-Encoding') == 'gzip':
            try:
                data = gzip.decompress(data)
            except Exception:
                pass
    for enc in ('utf-8', 'gbk', 'latin-1'):
        try:
            return data.decode(enc)
        except Exception:
            continue
    return data.decode('utf-8', 'replace')


def clean(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def ddg(q):
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q)
    h = fetch(url)
    out = []
    blocks = re.split(r'class="result__body"', h)
    for b in blocks[1:9]:
        tm = re.search(r'result__a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', b, re.S)
        if not tm:
            tm = re.search(r'class="result__a"[^>]*>(.*?)</a>', b, re.S)
            if not tm:
                continue
            href, title = '', tm.group(1)
        else:
            href, title = tm.group(1), tm.group(2)
        sn = re.search(r'result__snippet[^>]*>(.*?)</a>', b, re.S)
        out.append((clean(title), clean(sn.group(1)) if sn else '', href[:120]))
    return out


def bing(q):
    url = 'https://www.bing.com/search?q=' + urllib.parse.quote(q) + '&setlang=zh-CN&count=10'
    h = fetch(url)
    out = []
    for b in re.split(r'<li class="b_algo"', h)[1:9]:
        tm = re.search(r'<h2[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', b, re.S)
        if not tm:
            continue
        sn = re.search(r'<p[^>]*>(.*?)</p>', b, re.S)
        out.append((clean(tm.group(2)), clean(sn.group(1)) if sn else '', tm.group(1)[:120]))
    return out


qs = sys.argv[1:]
for q in qs:
    print('=' * 78)
    print('Q: ' + q)
    res = []
    for fn in (ddg, bing):
        try:
            res = fn(q)
            if res:
                break
        except Exception as e:
            print('  [%s fail] %s' % (fn.__name__, str(e)[:90]))
    if not res:
        print('  NO RESULTS')
    for i, (t, s, u) in enumerate(res[:6], 1):
        print('  %d. %s' % (i, t[:90]))
        if s:
            print('     %s' % s[:260])
    print()
