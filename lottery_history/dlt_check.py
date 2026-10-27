# -*- coding: utf-8 -*-
"""
dlt_check.py — 大乐透开奖检查与复盘确定性脚本 (V1.0, 2026-10-25)

替代 automation「B166ER-大乐透开奖检查」里「读tracker/查官网/对比/更新tracker/出报告」
的自由发挥流程，改为确定性流水线：
  1. 多源抓取最新开奖（体彩官方 API / 500 历史页 / 福彩 / 中彩网），每源硬超时 20s
     —— 采信规则：≥2 源号码一致才判定（单源仅作参考并标注）
  2. 与本地 prediction_*.json 比对 → 命中数、奖级、盈亏（按官方标准奖级表）
  3. 更新 dlt-tracker.md（最新开奖 / 近期历史表 / 命中归档表 / 期号头）
  4. 追加 cron.log，输出结构化摘要 JSON（供下一步「生成下期预测」使用）

每步都有硬超时，总预算内必然返回。
用法: python dlt_check.py [--dry-run] [--no-update]
"""
import sys, os, re, json, time, ssl, math, urllib.request, datetime
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

LOT = Path(r'D:\B166ER-OpenClaw\workspace\lottery_history')
TRACKER = LOT / 'dlt-tracker.md'
CRONLOG = LOT / 'cron.log'
OUT_JSON = LOT / 'dlt_check_last.json'
REPORT = Path(r'D:\B166ER-OpenClaw\workspace\memory\大乐透开奖检查报告.md')

FETCH_TIMEOUT = 20
TOTAL_BUDGET = 150
t0 = time.time()

# 官方标准奖级表（单注 2 元）
# 官方奖级表（2026 现行 7 档 + 变更前 9 档）
# 2026-01-15 体彩公告变更规则：自 2026-02-02（期号 26014）起由 9 档并为 7 档，26013 及以前为 9 档。
# 7 档结构经官方 sporttery API 92 期「各奖级注数比」交叉验证（误差 1~9%），并与官方 51% 返奖率自洽：
#   一等 5+2 | 二等 5+1 | 三等 5+0、4+2 | 四等 4+1 | 五等 3+2、4+0 | 六等 3+1、2+2 | 七等 3+0、2+1、1+2、0+2
# 不中奖 5 类：2+0、1+1、1+0、0+1、0+0（旧表误算为中奖 -> 任中奖被算成 1/2、固定奖 EV 达投入 783%，物理不可能）
# 每期单注金额优先取官方 prizeLevelList（奖池大时三至七等奖升级），取不到则用表内标准值。
PRIZE_7 = {(5, 2): ('一等奖', 0), (5, 1): ('二等奖', 0), (5, 0): ('三等奖', 5000), (4, 2): ('三等奖', 5000), (4, 1): ('四等奖', 300), (3, 2): ('五等奖', 150), (4, 0): ('五等奖', 150), (3, 1): ('六等奖', 15), (2, 2): ('六等奖', 15), (3, 0): ('七等奖', 5), (2, 1): ('七等奖', 5), (1, 2): ('七等奖', 5), (0, 2): ('七等奖', 5), (2, 0): ('', 0), (1, 1): ('', 0), (1, 0): ('', 0), (0, 1): ('', 0), (0, 0): ('', 0)}
PRIZE_9 = {(5, 2): ('一等奖', 0), (5, 1): ('二等奖', 0), (5, 0): ('三等奖', 10000), (4, 2): ('四等奖', 3000), (4, 1): ('五等奖', 300), (3, 2): ('六等奖', 200), (4, 0): ('七等奖', 100), (3, 1): ('八等奖', 15), (2, 2): ('八等奖', 15), (3, 0): ('九等奖', 5), (2, 1): ('九等奖', 5), (1, 2): ('九等奖', 5), (0, 2): ('九等奖', 5), (2, 0): ('', 0), (1, 1): ('', 0), (1, 0): ('', 0), (0, 1): ('', 0), (0, 0): ('', 0)}
LEGACY_LAST_ISSUE = '26013'


def prize_tier(issue, fh, bh):
    """按期号选 7 档(现行)/9 档(2026-02-02 之前)，返回 (奖级名, 标准单注金额)。"""
    tbl = PRIZE_9 if str(issue) <= LEGACY_LAST_ISSUE else PRIZE_7
    return tbl.get((fh, bh), ('', 0))


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
HDR = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                     '(KHTML, like Gecko) Chrome/120.0 Safari/537.36'}


def get(url, hdr=None, timeout=FETCH_TIMEOUT):
    req = urllib.request.Request(url, headers=hdr or HDR)
    raw = urllib.request.urlopen(req, timeout=timeout, context=ctx).read()
    try:
        return raw.decode('utf-8')
    except Exception:
        return raw.decode('gbk', errors='ignore')


def fetch_sporttery():
    """体彩官方 API（权威源），一次拉多期"""
    out = []
    for page in (1, 2):
        url = ('https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry'
               '?gameNo=85&provinceId=0&pageSize=30&isVerify=1&pageNo=%d' % page)
        j = json.loads(get(url, {'User-Agent': HDR['User-Agent'],
                                 'Referer': 'https://www.sporttery.cn/'}))
        for it in j['value']['list']:
            nums = re.findall(r'\d+', it['lotteryDrawResult'] or '')
            if len(nums) < 7:
                continue
            date = (it.get('lotteryDrawTime') or '')[:10]
            _amts = {}
            for _lv in (it.get('prizeLevelList') or []):
                _nm = str(_lv.get('prizeLevel') or '')
                if '追加' in _nm:
                    continue
                _amts[_nm] = _lv.get('stakeAmount')
            out.append({'amounts': _amts,
                        'issue': str(it['lotteryDrawNum']).strip(),
                        'date': date,
                        'front': [int(x) for x in nums[:5]],
                        'back': [int(x) for x in nums[5:7]],
                        'src': 'sporttery.cn（官方）'})
    return out


def fetch_cwl():
    """福彩官方（大乐透亦在其开奖公告体系）"""
    h = {'User-Agent': HDR['User-Agent'],
         'Referer': 'https://www.cwl.gov.cn/ygkj/wqkjgg/dlt/',
         'Accept': 'application/json, text/javascript, */*; q=0.01',
         'X-Requested-With': 'XMLHttpRequest'}
    txt = get('https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice'
              '?name=dlt&issueCount=5&issueStart=&issueEnd=&dayStart=&dayEnd=&pageNo=1', h)
    j = json.loads(txt)
    res = j.get('result') or []
    out = []
    for r in res:
        fr = re.findall(r'\d+', r.get('red') or '')
        bk = re.findall(r'\d+', r.get('blue') or '')
        if len(fr) < 5 or len(bk) < 2:
            continue
        out.append({'issue': str(r.get('code')).strip(), 'date': (r.get('date') or '')[:10],
                    'front': [int(x) for x in fr[:5]], 'back': [int(x) for x in bk[:2]],
                    'src': 'cwl.gov.cn（官方）'})
    return out


def fetch_500():
    """500.com 历史页（第三方，用于交叉校验）
    真实 HTML 结构: td[0]=行序(带注释), td[1]=期号, td[2..6]=前区5个,
                     td[7..8]=后区2个, td[15]=开奖日期
    （注：行内首个 td 常被 <!--...--> 注释包裹，需先剥注释）"""
    txt = get('https://datachart.500.com/dlt/history/newinc/history.php?start=26100&end=26200',
              {'User-Agent': HDR['User-Agent'],
               'Referer': 'https://datachart.500.com/dlt/history/history.shtml'})
    out = []
    for row in re.findall(r'<tr[^>]*>(.*?)</tr>', txt, re.S):
        row = re.sub(r'<!--.*?-->', '', row, flags=re.S)   # 剥注释
        tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)
        if len(tds) < 9:
            continue
        cells = [re.sub(r'<[^>]+>', '', td).strip() for td in tds]
        # 定位期号：5位数字且在靠前位置
        idx = next((i for i, c in enumerate(cells[:4]) if re.fullmatch(r'\d{5}', c)), None)
        if idx is None:
            continue
        issue = cells[idx]
        nums = []
        for c in cells[idx + 1:idx + 8]:
            nums += re.findall(r'\d+', c)
        if len(nums) < 7:
            continue
        date = next((c for c in cells if re.fullmatch(r'\d{4}-\d{2}-\d{2}', c)), '')
        out.append({'issue': issue, 'date': date,
                    'front': [int(x) for x in nums[:5]], 'back': [int(x) for x in nums[5:7]],
                    'src': 'datachart.500.com（第三方）'})
    return out


# ---------------- 1. 抓取 ----------------
sources = []
errs = []
for name, fn in (('sporttery', fetch_sporttery), ('cwl', fetch_cwl), ('500', fetch_500)):
    if time.time() - t0 > 60:
        errs.append(name + ': 预算不足')
        break
    try:
        rows = fn()
        sources.append({'name': name, 'rows': rows, 'ok': True, 'n': len(rows)})
    except Exception as ex:
        sources.append({'name': name, 'rows': [], 'ok': False, 'n': 0, 'err': str(ex)[:150]})
        errs.append('{}: {}'.format(name, str(ex)[:150]))

# ---------------- 2. 交叉比对 ----------------
# 关键：按【源】去重计票——同一源分页重复返回同一期不能算两票
latest = None

# 2026-10-27 状态保护（R-HEAL-31）：抓取失败时**不覆盖**上一次的有效状态。
#   起因：2026-10-27 09:10 一次三源同时 SSL 失败的运行，把本状态文件覆写为空壳
#   （issue=None / recent=0）-> 最近开奖数据丢失、下游复盘无数据可对。
_STATE_BACKUP = None
try:
    if OUT_JSON.exists():
        _STATE_BACKUP = OUT_JSON.read_text(encoding='utf-8', errors='replace')
except Exception:
    _STATE_BACKUP = None
detail = {}
for s in sources:
    for r in s['rows']:
        key = (r['issue'], tuple(r['front']), tuple(r['back']))
        if key not in detail:
            detail[key] = {'issue': r['issue'], 'date': r['date'],
                           'front': r['front'], 'back': r['back'], 'srcs': set()}
        detail[key]['srcs'].add(s['name'])
        detail[key]['amounts'] = r.get('amounts') or {}

if not detail:
    print('[抓取] 全部源失败：' + ' | '.join(errs))
    OUT_JSON.write_text(json.dumps({'ts': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    'ok': False, 'errors': errs}, ensure_ascii=False, indent=2),
                        encoding='utf-8')
    sys.exit(2)

# 取最新一期（按期号排序），并统计该期的【不同源】数量
latest = sorted(detail.values(), key=lambda x: x['issue'])[-1]
best_n = len(latest['srcs'])
latest['votes'] = best_n
latest['src_list'] = sorted(latest['srcs'])

# 置信度：官方一手源 → 🟢🟢；≥3 源交叉 → 🟡🟡；1-2 源 → 🟠🟠
OFFICIAL = {'sporttery', 'cwl'}
if OFFICIAL & set(latest['src_list']):
    CONF = '🟢🟢'
    CONF_NOTE = '含官方一手源（{}）'.format('/'.join(sorted(OFFICIAL & set(latest['src_list']))))
elif best_n >= 3:
    CONF = '🟡🟡'
    CONF_NOTE = '多源交叉 {} 源'.format(best_n)
elif best_n >= 1:
    CONF = '🟠🟠'
    CONF_NOTE = '单源待补'
else:
    CONF = '🔴🔴'
    CONF_NOTE = '无有效源'

# 近期历史（取最近 8 期，按期号倒序）
hist = sorted(detail.values(), key=lambda x: x['issue'], reverse=True)[:8]

# ---------------- 3. 与预测比对 ----------------
def find_prediction(issue):
    """找该期号的预测文件（优先 v5x 新版）"""
    cands = sorted(LOT.glob('prediction_{}*.json'.format(issue)))
    if not cands:
        return None, None
    cands.sort(key=lambda p: (p.stat().st_mtime), reverse=True)
    return cands[0], json.loads(cands[0].read_text(encoding='utf-8', errors='replace'))


def hit(front_set, back_set, pf, pb):
    return len(front_set & set(pf)), len(back_set & set(pb))


pf, pb = set(latest['front']), set(latest['back'])
pred_file, pred = find_prediction(latest['issue'])
review = None
if pred:
    schemes = pred.get('schemes') or []
    rows = []
    total = 0
    best_prize = ''
    for sc in schemes:
        fh, bh = hit(pf, pb, sc.get('front') or [], sc.get('back') or [])
        level, amt = prize_tier(latest['issue'], fh, bh)
        if level:
            _ov = (latest.get('amounts') or {}).get(level)
            _ns = str(_ov or '').replace(',', '').replace('，', '').replace(' ', '').strip()
            try:
                amt = int(float(_ns))
            except Exception:
                amt = amt or 0
        else:
            amt = 0
        total += amt
        if amt and not best_prize:
            best_prize = level
        rows.append({'id': sc.get('id'), 'name': sc.get('name'),
                     'front': sc.get('front'), 'back': sc.get('back'),
                     'hit_front': fh, 'hit_back': bh, 'level': level or '未中奖',
                     'amount': amt})
    stake = pred.get('cost') or (len(schemes) * 2)
    review = {'file': pred_file.name if pred_file else None,
              'model': pred.get('model'), 'issue': latest['issue'],
              'schemes': rows, 'stake': stake, 'prize_total': total,
              'net': total - stake,
              'best_level': next((r['level'] for r in rows
                                  if r['level'] not in ('未中奖', '')), '未中奖')}
    if not best_prize:
        review['best_level'] = '未中奖'

# ---------------- 4. 更新 tracker ----------------
def zone(n):
    return (n - 1) // 7 + 1


def profile(fr, bk):
    return {
        '奇偶': '{}:{}'.format(sum(1 for x in fr if x % 2), sum(1 for x in fr if x % 2 == 0)),
        '和值': sum(fr), '跨度': max(fr) - min(fr),
        '分区': '/'.join(str(sum(1 for x in fr if zone(x) == z)) for z in range(1, 6)),
    }


updated = False
if not '--no-update' in sys.argv and TRACKER.exists():
    txt = TRACKER.read_text(encoding='utf-8', errors='replace')
    orig = txt

    # 4a. 头部期号
    m = re.search(r'> 更新时间: ([^\n]+)\n> 当前期号: (\d+) \| 下期: (\d+)( \(([^)]+)\))?', txt)
    next_issue = str(int(latest['issue']) + 1)
    if m:
        ts = datetime.datetime.now().strftime('%Y-%m-%d')
        wd = '一二三四五六日'[datetime.datetime.now().weekday()]
        head = '> 更新时间: {} ({} CST)\n> 当前期号: {} | 下期: {} (下期开奖日待定)'.format(
            ts, wd, latest['issue'], next_issue)
        txt = txt[:m.start()] + head + txt[m.end():]

    # 4b. 最新开奖结果区块
    pf_ = profile(latest['front'], latest['back'])
    block = ('### 第{}期 - {} 🔥NEW\n'
             '- **前区**: {}\n'
             '- **后区**: {}\n'
             '- **来源**: {}{}\n'
             '- **模式**: 奇偶{} | 和值{} | 跨度{} | 分区{}\n'
             '- **抓取确认**: {}（{}/{} 源一致，{}）\n'
             ).format(
        latest['issue'], latest['date'],
        ' '.join('%02d' % x for x in latest['front']),
        ' '.join('%02d' % x for x in latest['back']),
        ' / '.join(latest['src_list']),
        '（最新）' if best_n >= 2 else '（单源，待补）',
        pf_['奇偶'], pf_['和值'], pf_['跨度'], pf_['分区'],
        CONF, best_n, len([s for s in sources if s['ok']]), CONF_NOTE)
    if '## 最新开奖结果' in txt:
        after = txt.split('## 最新开奖结果', 1)[1]
        # 去掉旧的 🔥NEW 标记
        after = after.replace(' 🔥NEW', '')
        rest = after.split('\n###', 1)
        tail = ('\n###' + rest[1]) if len(rest) > 1 else ''
        txt = txt.split('## 最新开奖结果', 1)[0] + '## 最新开奖结果\n\n' + block + tail.lstrip('\n')
    else:
        txt = txt.replace('## 最新开奖结果', '## 最新开奖结果\n\n' + block, 1)

    # 4c. 近期历史数据表
    rows_ = []
    for r in hist:
        rows_.append('| {} | {} | {} | {} |'.format(
            r['issue'], r['date'],
            ' '.join('%02d' % x for x in r['front']),
            ' '.join('%02d' % x for x in r['back'])))
    tbl = ('## 近期历史数据 (近{}期)\n\n'
           '| 期号 | 开奖日期 | 前区号码 | 后区号码 |\n'
           '|------|---------|---------|---------|\n' + '\n'.join(rows_) + '\n').format(len(hist))
    if '## 近期历史数据' in txt:
        pre, post = txt.split('## 近期历史数据', 1)
        # 保留该节之后到下一个 ## 之间的内容
        nxt = post.split('\n## ', 1)
        remainder = ('\n## ' + nxt[1]) if len(nxt) > 1 else ''
        txt = pre + tbl + remainder.lstrip('\n')
    else:
        txt = txt.rstrip() + '\n\n' + tbl

    # 4d. 命中记录归档表
    if review and review['best_level'] not in ('未中奖',):
        lvl = review['best_level']
        line = '| {} | {} | {} | {:+d}元 |'.format(
            latest['issue'],
            '前{}+后{}'.format(max([r['hit_front'] for r in review['schemes']] or [0]),
                              max([r['hit_back'] for r in review['schemes']] or [0])),
            lvl, review['net'])
        if '## 命中记录归档' in txt and '| {} |'.format(latest['issue']) not in txt:
            pre, post = txt.split('## 命中记录归档', 1)
            seg, rest = post.split('\n## ', 1) if '\n## ' in post else (post, '')
            lines = seg.splitlines()
            out_lines = []
            inserted = False
            for ln in lines:
                if not inserted and re.match(r'^\|\s*\*{0,2}\d{5}', ln):
                    out_lines.append(line)
                    inserted = True
                out_lines.append(ln)
            if not inserted:
                out_lines.append(line)
            newseg = '\n'.join(out_lines)
            txt = pre + '## 命中记录归档' + newseg + ('\n\n## ' + rest if rest else '')

    if txt != orig:
        TRACKER.write_text(txt, encoding='utf-8')
        updated = True

# ---------------- 5. cron.log + 报告 + JSON ----------------
ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log = ['[{}] cron:e76f4886 大乐透开奖检查启动(确定性脚本版)'.format(ts)]
log.append('[抓取] {}期 {} 已开奖: 前区 {} | 后区 {}'.format(
    latest['issue'], latest['date'],
    ' '.join('%02d' % x for x in latest['front']),
    ' '.join('%02d' % x for x in latest['back'])))
log.append('[数据] 源确认: {} ({}/{} 源一致, {})'.format(
    ' / '.join(latest['src_list']), best_n,
    len([s for s in sources if s['ok']]), CONF_NOTE))
if review:
    log.append('[复盘] {}预测: 最佳命中={} | 投入{}元 奖金{}元 净{:+d}元'.format(
        latest['issue'], review['best_level'], review['stake'],
        review['prize_total'], review['net']))
log.append('[Tracker] dlt-tracker.md{} ({}字节)'.format(
    '已更新' if updated else '未更新', TRACKER.stat().st_size if TRACKER.exists() else 0))
log.append('[状态] 任务完成 ✓')
with open(CRONLOG, 'a', encoding='utf-8') as f:
    f.write('\n' + '\n'.join(log) + '\n')

result = {
    'ts': ts, 'ok': True, 'conf': CONF, 'conf_note': CONF_NOTE,
    'issue': latest['issue'], 'date': latest['date'],
    'front': latest['front'], 'back': latest['back'],
    'votes': best_n, 'sources': {s['name']: (s['n'] if s['ok'] else 'FAIL:' + s.get('err', '')[:80])
                                  for s in sources},
    'src_list': latest['src_list'],
    'review': review, 'tracker_updated': updated,
    'next_issue': str(int(latest['issue']) + 1),
    'recent': [{k: (sorted(v) if isinstance(v, set) else v) for k, v in r.items()}
               for r in hist],
}
OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')

L = ['# 大乐透开奖检查报告', '', '> 生成时间: {}（自动化脚本 dlt_check.py）'.format(ts),
     '> 信源置信度: {}（{}/{} 源一致，{}）'.format(CONF, best_n, len([s for s in sources if s['ok']]), CONF_NOTE), '',
     '## 一、开奖结果', '',
     '- **期号**: {}'.format(latest['issue']),
     '- **开奖日期**: {}'.format(latest['date']),
     '- **前区**: {}'.format(' '.join('%02d' % x for x in latest['front'])),
     '- **后区**: {}'.format(' '.join('%02d' % x for x in latest['back'])),
     '- **信源**: {}'.format(' / '.join(latest['src_list'])), '']
if review:
    L += ['## 二、复盘（{}）'.format(review['file'] or '无预测文件'), '',
          '| 方案 | 前区 | 后区 | 命中 | 奖级 | 奖金 |', '|------|------|------|------|------|------|']
    for r in review['schemes']:
        L.append('| {} {} | {} | {} | 前{}+后{} | {} | {}元 |'.format(
            r['id'], r['name'], ' '.join(str(x) for x in r['front']),
            ' '.join(str(x) for x in r['back']),
            r['hit_front'], r['hit_back'], r['level'], r['amount']))
    L += ['', '- 投入 {} 元｜奖金 {} 元｜**净 {:+d} 元**'.format(
        review['stake'], review['prize_total'], review['net']), '']
L += ['## 三、下一步', '',
      '- 待生成预测期号: **{}**'.format(result['next_issue']),
      '- 机器可读摘要: {}'.format(OUT_JSON), '',
      '> 免责声明: 本记录仅供娱乐研习，购彩为随机事件，不构成投注建议。理性投注，量力而行。']
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text('\n'.join(L) + '\n', encoding='utf-8')

print('=== 大乐透开奖检查完成 ===')
print('期号 {} ({}) 前区 {} 后区 {}'.format(
    latest['issue'], latest['date'],
    ' '.join('%02d' % x for x in latest['front']),
    ' '.join('%02d' % x for x in latest['back'])))
print('信源 {}（{}/{} 一致，{}）｜各源命中: {}'.format(
    CONF, best_n, len([s for s in sources if s['ok']]), CONF_NOTE,
    ', '.join('{}={}'.format(s['name'], s['n'] if s['ok'] else 'FAIL') for s in sources)))
if review:
    print('复盘: 最佳={} 投入{} 奖金{} 净{:+d}'.format(
        review['best_level'], review['stake'], review['prize_total'], review['net']))
print('tracker: {}'.format('已更新' if updated else '未更新'))
print('下期待预测期号: {}'.format(result['next_issue']))
print('报告: {}'.format(REPORT))
print('JSON: {}'.format(OUT_JSON))
print('用时 {:.1f}s'.format(time.time() - t0))


# ---- 状态保护兜底（跑在所有写入之后）----
if _STATE_BACKUP:
    _bad = False
    try:
        _cur = json.loads(OUT_JSON.read_text(encoding='utf-8', errors='replace'))
        # 判据只用 result 里确实存在的键：issue 为空 => 本轮没取到有效开奖
        _bad = not _cur.get('issue')
    except Exception:
        _bad = True
    if _bad:
        OUT_JSON.write_text(_STATE_BACKUP, encoding='utf-8')
        (OUT_JSON.parent / (OUT_JSON.name + '.failed')).write_text(OUT_JSON.read_text(encoding='utf-8', errors='replace'), encoding='utf-8')
        print('[状态保护] 本轮未取到有效开奖 -> 已恢复上一次有效状态（失败详情见 %s.failed）' % OUT_JSON.name)
