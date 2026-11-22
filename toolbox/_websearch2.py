# -*- coding: utf-8 -*-
import io, sys, re, gzip, urllib.request, urllib.parse, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'zh-CN,zh;q=0.9',
                                               'Accept': 'text/html,application/xhtml+xml,*/*'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
        if r.headers.get('Content-Encoding') == 'gzip':
            try:
                data = gzip.decompress(data)
            except Exception:
                pass
    for enc in ('utf-8', 'gbk', 'gb18030', 'latin-1'):
        try:
            return data.decode(enc)
        except Exception:
            continue
    return data.decode('utf-8', 'replace')


def clean(s):
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def eng_sogou(q):
    h = fetch('https://www.sogou.com/web?query=' + urllib.parse.quote(q))
    out = []
    for b in re.split(r'<div class="vrwrap"', h)[1:8]:
        tm = re.search(r'<h3[^>]*>.*?<a[^>]*>(.*?)</a>', b, re.S)
        sn = re.search(r'<p class="str_info"[^>]*>(.*?)</p>', b, re.S) or re.search(r'<div class="text-layout"[^>]*>(.*?)</div>', b, re.S)
        if tm:
            out.append((clean(tm.group(1)), clean(sn.group(1)) if sn else ''))
    return out


def eng_baidu(q):
    h = fetch('https://www.baidu.com/s?wd=' + urllib.parse.quote(q))
    out = []
    for b in re.split(r'<div class="result', h)[1:9]:
        tm = re.search(r'<h3[^>]*>.*?<a[^>]*>(.*?)</a>', b, re.S)
        sn = re.search(r'<div class="c-abstract"[^>]*>(.*?)</div>', b, re.S) or re.search(r'class="content-right_[^"]*"[^>]*>(.*?)</span>', b, re.S)
        if tm:
            out.append((clean(tm.group(1)), clean(sn.group(1)) if sn else ''))
    return out


def eng_bing(q):
    h = fetch('https://cn.bing.com/search?q=' + urllib.parse.quote(q) + '&ensearch=0&FORM=BESBTB')
    out = []
    for b in re.split(r'<li class="b_algo"', h)[1:9]:
        tm = re.search(r'<h2[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', b, re.S)
        sn = re.search(r'<p[^>]*>(.*?)</p>', b, re.S)
        if tm:
            out.append((clean(tm.group(2)), clean(sn.group(1)) if sn else ''))
    return out


def eng_so(q):
    h = fetch('https://www.so.com/s?q=' + urllib.parse.quote(q))
    out = []
    for b in re.split(r'<li class="res-list"', h)[1:9]:
        tm = re.search(r'<h3[^>]*>.*?<a[^>]*>(.*?)</a>', b, re.S)
        sn = re.search(r'<p class="res-desc"[^>]*>(.*?)</p>', b, re.S)
        if tm:
            out.append((clean(tm.group(1)), clean(sn.group(1)) if sn else ''))
    return out


def hit_ok(q, res):
    if not res:
        return False
    kws = [k for k in re.split(r'[\s,，]+', q) if len(k) >= 2]
    blob = ' '.join(t + s for t, s in res)
    return sum(1 for k in kws if k in blob) >= 1


qs = sys.argv[1:]
for q in qs:
    print('=' * 78)
    print('Q: ' + q)
    best = None
    for fn in (eng_sogou, eng_baidu, eng_bing, eng_so):
        try:
            res = fn(q)
            if res and hit_ok(q, res):
                print('  [engine: %s  relevant]' % fn.__name__)
                best = res
                break
            else:
                print('  [%s: %d 条%s]' % (fn.__name__, len(res), '，不相关' if res else ''))
        except Exception as e:
            print('  [%s fail] %s' % (fn.__name__, str(e)[:80]))
    if not best:
        print('  >>> 无可用结果')
    else:
        for i, (t, s) in enumerate(best[:6], 1):
            print('  %d. %s' % (i, t[:88]))
            if s:
                print('     %s' % s[:250])
    print()
