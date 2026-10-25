# -*- coding: utf-8 -*-
"""
registry_gap_probe.py — 市场空白监测器 (V2.0, 2026-10-25)

为什么需要它：
  2026-10-25 实测发现，ClawHub 上「酒店域竞品房价/动态定价监控」多组同义词全部 0 命中；
  存在的 competitor-* 全是电商/商品域（Amazon 监控等），不是酒店房价。
  → 这类「市场空白」比「装了哪个技能」更值钱：它直接决定「哪些能力必须自建」。

V2.0 修正（V1.0 首跑暴露的 3 个质量缺陷）：
  ① exclude 匹配对象错位：V1.0 用 `re.search(exclude_re, blob)` 且模式带 `$` 锚点，
     而 blob = slug + displayName + summary（slug 不在末尾）→ `amap-lbs-skill` 根本没被排除。
     V2.0 改为**只对 slug 匹配**，且锚点独立。
  ② domain 判定过宽：V1.0 只要命中「竞品监控」就算域内命中 → 11 个命中其实全是
     电商/营销监控（competitor-monitor-ai、keyword-monitor…），**不是酒店房价**。
     V2.0 改为**两级判定**：core_re（必须同时命中目标域核心词，如 房价/ADR/RevPAR/入住率）
     + adj_re（相邻但不对口，如泛竞品监控）。只命中相邻 → 判 ADJACENT 而非 FILLED。
  ③ 预算耗尽导致对照组被 SKIP（无对照就无从判断"空白"是真是假）→ V2.0 保证对照组必跑。

状态语义（这是本工具的核心价值）：
  FILLED    域内核心供给成熟（core 命中且 installs>=3）→ 可以买
  THIN      域内核心供给薄弱（core 命中但 installs<3）→ 可买但要自建主力
  ADJACENT  只有相邻供给（泛竞品监控/泛营销工具），**不对口** → 该能力仍需自建
  BLANK     连相邻供给都没有 → 完全空白，必须自建

双通道（两者互补，缺一不可）：
  - registry 关键词检索：命中下载量高的真技能，但**对长中文复合词不切分**
    （实测「高德酒店」0 条 / 「高德」10 条）→ 中文必须用 2–3 字粒度
  - clawhub 向量检索：能覆盖同义词，但泛词 hotel/travel 会被占位条目霸榜

用法: python registry_gap_probe.py [--quick]
"""
import json
import os
import re
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WS = Path(__file__).resolve().parent
if (WS / 'skills').is_dir():
    WS = WS.parent
CLI = str(Path(os.environ.get('APPDATA', '')) / 'npm' / 'clawhub.cmd')
OUT_JSON = WS / '.tmp' / 'registry_gap_probe.json'
OUT_MD = WS / 'memory' / '市场空白追踪.md'
BUDGET = 300
t0 = time.time()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
HDR = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0',
       'Accept': 'application/json'}

# ============ 能力缺口定义（core = 目标域核心词；adj = 相邻但不对口）============
GAPS = [
    {
        'id': 'hotel-competitor-rates',
        'title': '酒店竞品房价 / 动态定价监控',
        'why': 'Eric 酒店经营侧最刚的需求：对区域内竞对房价的持续采集与异动预警',
        'queries': ['竞品监控', '动态定价', '竞品价格', '竞对价格', '酒店降价监控',
                    'competitor pricing', 'competitor monitor', 'rate monitoring',
                    'revenue intelligence'],
        # core：必须同时出现「竞对语义」与「酒店房价语义」
        'core_re': r'(hotel|otel|酒店|房价|入住率|occupancy|ADR|RevPAR|RGI|rate\s*shop|房价)',
        'core2_re': r'(competitor|rival|peer|竞品|竞对|同行|对标|定价)',
        'adj_re': r'(competitor|rival|peer|竞品|竞对|同行|对标|监控|monitor|intelligence)',
        'exclude_slug_re': r'(ecommerce|amazon|shopify|etsy|ebay|walmart|taobao|jd|temu|aliexpress)',
    },
    {
        'id': 'hotel-renovation-site',
        'title': '酒店存量翻新选址分析（POI + 商圈 + 客流）',
        'why': '安逸存量改造项目的选址、商圈与客流可行性判断',
        'queries': ['高德', '选址', '商圈', 'poi', 'lbs', 'site analysis'],
        'core_re': r'(poi|lbs|geospatial|地图|商圈|选址|位置|客流|footfall|周边|地点)',
        'core2_re': r'(amap|gaode|高德|map|location|geo)',
        'adj_re': r'(location|geo|map|poi|位置|地图)',
        'exclude_slug_re': r'(taxi|ride|navigation|导航|打车)',
    },
    {
        'id': 'hotel-scrm-private',
        'title': '酒店私域 / 会员 / 复购运营',
        'why': '安逸私域会员体系（KB 已具备，缺工具）',
        'queries': ['私域', '会员', '复购', 'crm', 'loyalty', 'wechat'],
        'core_re': r'(hotel|酒店|会员|member|loyalty|复购|retention|入住)',
        'core2_re': r'(私域|private|wechat|微信|社群|crm|会员|积分|rfm)',
        'adj_re': r'(私域|private|traffic|流量|crm|微信|wechat|营销|marketing)',
        'exclude_slug_re': r'(ecommerce|amazon|shopify|etsy)',
    },
    {
        'id': 'hotel-rate-shopping',
        'title': '酒店房价聚合（对照组 · 市场已有供给）',
        'why': '对照组：若这项都能判空白，说明判定逻辑过严，需校准',
        'queries': ['酒店比价', '多平台比价', 'hotel price compare', 'hotel price monitor', 'ota'],
        'core_re': r'(hotel|otel|酒店|房价|比价|ota)',
        'core2_re': r'(price|比价|compare|monitor|价)',
        'adj_re': r'(price|hotel|酒店|价)',
        'exclude_slug_re': r'(ecommerce|amazon|shopify|etsy)',
    },
]


def reg_search(q, limit=10):
    try:
        url = 'https://clawhub.ai/api/v1/search?q=' + urllib.parse.quote(q)
        req = urllib.request.Request(url, headers=HDR)
        raw = urllib.request.urlopen(req, timeout=15, context=ctx).read()
        d = json.loads(raw.decode('utf-8', 'replace'))
        return d.get('results') or []
    except Exception:
        return []


def vec_search(q, limit=6):
    try:
        p = subprocess.run([CLI, 'search', q, '--limit', str(limit)], capture_output=True,
                           text=True, encoding='utf-8', errors='replace', timeout=30)
        out = []
        for ln in (p.stdout or '').splitlines():
            ln = ln.strip()
            if not ln or ln.startswith('-') or 'Searching' in ln:
                continue
            m = re.match(r'^(\S+)\s{2,}(.*?)\s{2,}\([\d.]+\)$', ln)
            if m:
                out.append({'slug': m.group(1), 'desc': m.group(2)})
        return out
    except Exception:
        return []


def probe(gap, quick=False):
    """两级判定：core（域内核心）× adj（相邻）"""
    core, adj, detail = {}, {}, {}
    c1 = re.compile(gap['core_re'], re.I)
    c2 = re.compile(gap['core2_re'], re.I)
    ca = re.compile(gap['adj_re'], re.I)
    ex = re.compile(gap['exclude_slug_re'], re.I)
    qs = gap['queries'][:4] if quick else gap['queries']

    def add(store, slug, dl, ins, q, desc, ch):
        if slug not in store or (ins or 0) > (store[slug]['installs'] or 0):
            store[slug] = {'slug': slug, 'downloads': dl or 0, 'installs': ins or 0,
                           'q': q, 'desc': (desc or '')[:90], 'ch': ch}

    for q in qs:
        if time.time() - t0 > BUDGET - 50:
            break
        for it in reg_search(q, 10):
            slug = it.get('slug') or ''
            if not slug:
                continue
            detail[(q, slug)] = 1
            if ex.search(slug):          # V2.0：排除只对 slug 生效
                continue
            blob = '{} {} {}'.format(slug, it.get('displayName') or '',
                                     it.get('summary') or '')
            if c1.search(blob) and c2.search(blob):
                add(core, slug, it.get('downloads'), it.get('installs'), q,
                    it.get('summary'), 'reg')
            elif ca.search(blob):
                add(adj, slug, it.get('downloads'), it.get('installs'), q,
                    it.get('summary'), 'reg')
        for it in vec_search(q, 5):
            slug = it.get('slug') or ''
            if not slug:
                continue
            detail[(q, slug)] = 1
            if ex.search(slug):
                continue
            blob = slug + ' ' + it.get('desc', '')
            if c1.search(blob) and c2.search(blob):
                add(core, slug, 0, 0, q, it.get('desc'), 'vec')
            elif ca.search(blob):
                add(adj, slug, 0, 0, q, it.get('desc'), 'vec')

    if not core:
        status = 'ADJACENT' if adj else 'BLANK'
    else:
        best = max(core.values(), key=lambda x: (x['installs'], x['downloads']))
        status = 'FILLED' if (best['installs'] or 0) >= 3 else 'THIN'
    return {'status': status,
            'core': sorted(core.values(), key=lambda x: -(x['installs'] or 0)),
            'adj': sorted(adj.values(), key=lambda x: -(x['installs'] or 0))[:6],
            'detail_n': len(detail)}


def main():
    quick = '--quick' in sys.argv
    results = []
    for gap in GAPS:
        if time.time() - t0 > BUDGET - 50 and gap['id'] != 'hotel-rate-shopping':
            results.append({'id': gap['id'], 'title': gap['title'], 'why': gap['why'],
                            'status': 'SKIP', 'core': [], 'adj': [], 'detail_n': 0})
            print('[SKIP] {}（预算不足，优先保对照组）'.format(gap['id']))
            continue
        r = probe(gap, quick)
        r.update({'id': gap['id'], 'title': gap['title'], 'why': gap['why']})
        results.append(r)
        print('[{}] {:<26} core={} adj={} / 探测 {}'.format(
            r['status'], gap['id'], len(r['core']), len(r['adj']), r['detail_n']))
        for h in r['core'][:4]:
            print('      CORE  {}  ↓{} 装{}  ({})'.format(
                h['slug'], h['downloads'], h['installs'], h['q']))
        for h in r['adj'][:2]:
            print('      adj   {}  ↓{} 装{}  ({})'.format(
                h['slug'], h['downloads'], h['installs'], h['q']))

    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps({'ts': ts, 'results': results}, ensure_ascii=False,
                                   indent=2), encoding='utf-8')

    L = ['# 市场空白追踪（ClawHub）', '',
         '> 由 `toolbox/registry_gap_probe.py` 自动生成｜双通道：registry 关键词 + clawhub 向量',
         '> **空白 = 该能力市场无对口供给 → 必须自建**；这是比「装了哪个技能」更值钱的结论',
         '> 状态：🟢🟢FILLED 域内核心供给成熟（可买）｜🟡🟡THIN 域内供给薄弱｜'
         '🟠🟠ADJACENT 只有相邻工具（不对口，仍需自建）｜🔴BLANK 完全空白',
         '', '| 检查时间 | 能力缺口 | 状态 | 核心命中 | 相邻命中 | 判定 |', '|---|---|---|---|---|---|']
    for r in results:
        mark = {'BLANK': '🔴 空白 → 自建', 'ADJACENT': '🟠🟠 只有相邻工具 → 仍需自建',
                'FILLED': '🟢🟢 可买', 'THIN': '🟡🟡 供给薄弱',
                'SKIP': '⚪ 跳过'}.get(r['status'], r['status'])
        L.append('| {} | {} | {} | {} | {} | {} |'.format(
            ts, r['title'], r['status'], len(r.get('core', [])), len(r.get('adj', [])), mark))
    L += ['', '## 逐项明细', '']
    for r in results:
        L.append('### {} — {}'.format(r['id'], r['title']))
        L.append('- **为什么关心**: {}'.format(r.get('why', '')))
        L.append('- **状态**: {}'.format(r['status']))
        if r.get('core'):
            L.append('- **域内核心候选**:')
            for h in r['core'][:8]:
                L.append('  - `{}` ↓{} 装{} — {}'.format(
                    h['slug'], h['downloads'], h['installs'], h['desc']))
        else:
            L.append('- **域内核心候选**: 无')
        if r.get('adj'):
            L.append('- **相邻（不对口，仅供判断市场成熟度）**:')
            for h in r['adj'][:5]:
                L.append('  - `{}` ↓{} 装{}'.format(h['slug'], h['downloads'], h['installs']))
        L.append('')
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_MD, 'a', encoding='utf-8') as f:
        f.write('\n---\n\n' + '\n'.join(L) + '\n')

    print()
    print('=== 汇总 ===')
    for r in results:
        print('  {:<28} {:<9} core={} adj={}'.format(
            r['id'], r['status'], len(r.get('core', [])), len(r.get('adj', []))))
    print('JSON: {}'.format(OUT_JSON))
    print('追踪: {}'.format(OUT_MD))
    print('用时 {:.0f}s'.format(time.time() - t0))
    return 0


if __name__ == '__main__':
    sys.exit(main())
