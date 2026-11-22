# -*- coding: utf-8 -*-
import io, sys, os, re, gzip, urllib.request, urllib.parse, html, time, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def fetch(url, timeout=20, head=False):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'zh-CN,zh;q=0.9'})
    if head:
        req.get_method = lambda: 'HEAD'
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
    h = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', h)
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
            _, final = fetch(u, timeout=15)
            return final
    except Exception:
        pass
    return u


TASKS = [
 ('悦榕庄峨眉山开业', '世界级 酒店 峨眉山 悦榕庄 今日 开业',
  ['悦榕', '峨眉', '开业', '客房', '汤', '泡池', '康养', '度假', '二期', '投资', '占地', '改造']),
 ('装修与机电时序', '酒店装修施工顺序 机电 管线 吊顶 饰面 先做',
  ['机电', '管线', '吊顶', '隐蔽', '饰面', '装修', '顺序', '空调', '消防', '水电', '中央空调']),
 ('样板间 Mock-Up 制度', '酒店 改建 样板间 Mock-Up Room 检查表 规范',
  ['Mock-Up', '样板', '样板间', '封样', '检查', '确认', '批量', '大面', '施工']),
]

for tag, q, kws in TASKS:
    print('=' * 96)
    print('【' + tag + '】Q: ' + q)
    try:
        ls = so_links(q)
    except Exception as e:
        print('  搜索失败:', str(e)[:70]); continue
    n = 0
    for url, title in ls:
        if not url.startswith('http'):
            continue
        real = resolve(url)
        print('  * ' + title[:72])
        print('    ' + real[:110])
        try:
            body, _ = fetch(real)
            txt = clean(body)
            hits = []
            for seg in re.split(r'[。！？；\n]', txt):
                s = seg.strip()
                if 12 < len(s) < 170 and any(k in s for k in kws):
                    hits.append(s)
            for h in hits[:8]:
                print('      · ' + h)
            if not hits and len(txt) > 200:
                print('      ' + txt[:700])
        except Exception as e:
            print('      抓取失败:', str(e)[:60])
        n += 1
        if n >= 3:
            break
        time.sleep(0.4)
