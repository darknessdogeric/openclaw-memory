# -*- coding: utf-8 -*-
"""抓取 Mandai Rainforest Resort by Banyan Tree 官方页 + 辅助信源"""
import io, sys, os, re, gzip, urllib.request, urllib.parse, html, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'en,zh;q=0.8'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = r.read()
        if r.headers.get('Content-Encoding') == 'gzip':
            try:
                d = gzip.decompress(d)
            except Exception:
                pass
        final = r.geturl()
    for e in ('utf-8', 'gbk', 'gb18030'):
        try:
            return d.decode(e), final
        except Exception:
            continue
    return d.decode('utf-8', 'replace'), final


def clean(h):
    h = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', h)
    h = re.sub(r'(?s)<[^>]+>', ' ', h)
    return re.sub(r'\s+', ' ', html.unescape(h)).strip()


def so_links(q):
    h, _ = fetch('https://www.so.com/s?q=' + urllib.parse.quote(q))
    out = []
    for b in re.split(r'<li class="res-list"', h)[1:10]:
        m = re.search(r'<h3[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', b, re.S)
        if m:
            out.append((m.group(1), clean(m.group(2))))
    return out


def resolve(u):
    try:
        if 'so.com/link' in u:
            _, f = fetch(u, timeout=15)
            return f
    except Exception:
        pass
    return u


print('=' * 90)
print('【官方页】https://www.banyantree.com/singapore/mandai-rainforest-resort-by-banyan-tree')
U = 'https://www.banyantree.com/singapore/mandai-rainforest-resort-by-banyan-tree'
try:
    body, final = fetch(U)
    print('跳转后:', final, ' 长度:', len(body))
    txt = clean(body)
    print('纯文本:', len(txt))
    # 抓关键段落
    KEY = ['Mandai', 'rainforest', 'Rainforest', 'Singapore', 'villa', 'Villa', 'treehouse', 'Treehouse',
           'wildlife', 'Wildlife', 'conservation', 'skunk', 'ibis', 'opening', '2025', 'keys', 'room',
           'Mandai Wildlife Reserve', 'park', 'nature', 'sustainability', 'wayang', 'guest']
    segs = [s.strip() for s in re.split(r'[.!?]\s+|\n', txt) if 25 < len(s.strip()) < 300]
    hit = []
    for s in segs:
        if any(k in s for k in KEY):
            hit.append(s)
    seen = set()
    for h in hit[:40]:
        if h in seen:
            continue
        seen.add(h)
        print('  · ' + h)
    if len(hit) < 4:
        print('  [全文节选] ' + txt[:2500])
except Exception as e:
    print('  抓取失败:', str(e)[:180])

print('')
print('=' * 90)
print('【检索补充】')
for q in ['Mandai Rainforest Resort by Banyan Tree Singapore opening 2025 villas',
          'Banyan Tree Mandai Rainforest Resort rainforest experience conservation Singapore']:
    print('--- ' + q)
    try:
        ls = so_links(q)
    except Exception as e:
        print('  搜索失败:', str(e)[:70])
        continue
    n = 0
    for url, title in ls:
        if not url.startswith('http'):
            continue
        real = resolve(url)
        print('  * ' + title[:78])
        print('    ' + real[:110])
        try:
            b, _ = fetch(real)
            t2 = clean(b)
            segs = [s.strip() for s in re.split(r'[.!?]\s+', t2) if 30 < len(s.strip()) < 260
                    and any(k in s for k in ['Mandai', 'rainforest', 'Rainforest', 'villa', 'Villa', 'treehouse',
                                             'wildlife', 'Wildlife', 'conservation', 'Singapore', 'resort',
                                             ' Banyan', 'rooms', 'night safari', 'zoo', 'habitat'])]
            for s in segs[:5]:
                print('      · ' + s)
            if not segs and len(t2) > 200:
                print('      ' + t2[:350])
        except Exception as e:
            print('      抓取失败:', str(e)[:50])
        n += 1
        if n >= 2:
            break
        time.sleep(0.4)
