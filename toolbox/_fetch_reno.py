# -*- coding: utf-8 -*-
import io, sys, os, re, gzip, urllib.request, urllib.parse, html, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'zh-CN,zh;q=0.9'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = r.read()
        if r.headers.get('Content-Encoding') == 'gzip':
            try:
                d = gzip.decompress(d)
            except Exception:
                pass
    for e in ('utf-8', 'gbk', 'gb18030'):
        try:
            return d.decode(e)
        except Exception:
            continue
    return d.decode('utf-8', 'replace')


def clean(h):
    h = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', h)
    h = re.sub(r'(?s)<[^>]+>', ' ', h)
    return re.sub(r'\s+', ' ', html.unescape(h)).strip()


def so_links(q):
    h = fetch('https://www.so.com/s?q=' + urllib.parse.quote(q))
    out = []
    for b in re.split(r'<li class="res-list"', h)[1:10]:
        m = re.search(r'<h3[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', b, re.S)
        if m:
            out.append((m.group(1), clean(m.group(2))))
    return out


QS = [
 ('君亭朱晓东 中高端酒店 破局 存量 改造', ['改造', '存量', '旧', '翻', '步骤', '周期', '投入', '单房']),
 ('悦榕庄 峨眉山 开业 度假村 改造 存量 酒店', ['悦榕', '峨眉', '改造', '存量', '物业', '度假', '康养', '汤']),
 ('酒店改造 施工顺序 机电 管线 吊顶 装修 先做 还是 后做', ['机电', '管线', '吊顶', '隐蔽', '装修', '顺序', '施工', '改造']),
 ('酒店 改造 样板房 mock-up 试点 验证 分批 施工', ['样板', '试点', '分批', '验证', '改造', '周期', '爬坡']),
]

for q, kws in QS:
    print('=' * 96)
    print('Q: ' + q)
    try:
        ls = so_links(q)
    except Exception as e:
        print('  搜索失败:', str(e)[:70])
        continue
    n = 0
    for url, title in ls:
        if not url.startswith('http'):
            continue
        print('  * ' + title[:76])
        try:
            body = clean(fetch(url))
            hits = []
            for seg in re.split(r'[。！？；]', body):
                s = seg.strip()
                if 12 < len(s) < 160 and any(k in s for k in kws):
                    hits.append(s)
            for h in hits[:6]:
                print('      · ' + h)
            if not hits:
                print('      ' + body[:400])
        except Exception as e:
            print('      抓取失败:', str(e)[:50])
        n += 1
        if n >= 3:
            break
        time.sleep(0.4)
