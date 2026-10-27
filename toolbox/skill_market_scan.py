# -*- coding: utf-8 -*-
r"""
B166ER-技能市场扫描 v1.3 —— 确定性扫描器（替代 agentTurn，根治 timeout）

根因与修复对照：
  A. clawhub 是 .ps1 → 用 npm 的 clawhub.cmd shim
  B. clawhub search 输出是纯文本（非 JSON）→ 正则解析 "name  desc  (score)"
  C. 泛查询词 + 大 limit → 向量检索卡 20s+ → 只用 2 个精准词 / limit 5 / 15s 硬超时
  D. 任务原 cd 到 C 盘空壳目录 → 写死真实工作区 D:\B166ER-OpenClaw\workspace
  E. **Windows 管道死锁**：.cmd→cmd.exe→node.exe 孙进程持有 stdout 管道，
     subprocess.communicate() 超时后仍永久阻塞 → 改用「临时文件承接 stdout +
     taskkill /T 杀整棵进程树」，保证调用必然在 timeout 内返回
"""
import sys, os, re, json, subprocess, tempfile, time, datetime
from pathlib import Path

# 复用「市场空白监测器」的能力缺口定义（避免两份正则规则漂移）
try:
    from registry_gap_probe import GAPS as _CAPABILITY_GAPS
except Exception:
    _CAPABILITY_GAPS = []

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WS = Path(r'D:\B166ER-OpenClaw\workspace')
SKILLS = WS / 'skills'
MEMO = WS / 'memory' / 'B166ER-skill-upgrade-checklist.md'
SHIM = Path(os.environ.get('APPDATA', '')) / 'npm' / 'clawhub.cmd'
LOG = WS / '.tmp' / 'skill_scan_last.json'
POOL = WS / 'memory' / 'skill_market_seen_pool.json'

TOTAL_BUDGET = 280   # 2026-10-27：检索面补 8 个英文词后实测 170.7s，200s 太挤
CLAWHUB_TIMEOUT = 15
REG_TIMEOUT = 12
GIT_TIMEOUT = 30
MAX_GIT = 8
QUERIES = ['hotel', 'travel']
# 2026-10-25 追加：向量检索连续 4 轮返回同一批占位条目（hotel/travel/travel-rule-check…），
# 而 registry 关键词检索能翻到 hotel-price-monitor / hotel-price-finder / meituan-hotel-deals
# 等真正有价值的技能（1304/1355/965 次下载）→ 增加关键词通道（互补，不替代向量通道）
REG_QUERIES = [
               'hotel price comparison', 'hotel rate comparison', 'hotel price monitoring',
               'competitive pricing analysis', 'hotel competitor pricing',
               'hotel revenue management', 'hotel rate shopping', 'dynamic pricing hotel',
               '酒店比价', '降价监控', '多平台比价', '采购价格', '美团', '高德',
               'OTA', '竞品监控', '动态定价', '会员', '私域', '选址', '商圈',
               'hotel price compare', 'hotel price monitor',
               'competitor pricing', 'revenue intelligence']
# 2026-10-25 实测修正：registry 关键词检索对**长中文复合词不切分**
#   「高德 酒店」0 条 /「高德酒店」0 条 /「高德」10 条 → 中文必须用 2–3 字粒度
# 新增「竞品监控/动态定价/会员/私域/选址/商圈」用于**监测市场空白是否被填补**
# （配套工具：toolbox/registry_gap_probe.py）

t0 = time.time()
def left():
    return TOTAL_BUDGET - (time.time() - t0)

NEWPROC = getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 0)

def kill_tree(pid):
    subprocess.run(['taskkill', '/PID', str(pid), '/T', '/F'],
                   capture_output=True, shell=False)

def run(cmd, timeout):
    """文件承接 stdout + 超时杀整棵进程树 —— 绝不因孙进程持句柄而死锁"""
    try:
        with tempfile.TemporaryFile('w+b') as tf:
            try:
                p = subprocess.Popen(cmd, stdout=tf, stderr=subprocess.STDOUT,
                                     stdin=subprocess.DEVNULL,
                                     creationflags=NEWPROC)
            except Exception as e:
                return -2, '', str(e)
            try:
                p.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                kill_tree(p.pid)
                try:
                    p.wait(timeout=8)
                except Exception:
                    pass
                return -1, '', 'TIMEOUT'
            tf.seek(0)
            out = tf.read().decode('utf-8', 'replace')
            return p.returncode, out, ''
    except Exception as e:
        return -2, '', str(e)



INSTALLS_CACHE = Path(__file__).resolve().parent.parent / 'memory' / 'skill_installs_cache.json'


def _cache_load():
    """官方 manifest 权威 installs 缓存（search API 不提供安装数 -> 判据只能取 manifest）。
    现场逐个抓会因网络抖动让同一份事实给出不同结论（实测 FILLED<->THIN 翻转）-> 判定只读缓存。"""
    try:
        if INSTALLS_CACHE.exists():
            return json.loads(INSTALLS_CACHE.read_text(encoding='utf-8', errors='replace'))
    except Exception:
        pass
    return {}


def _cache_lookup(cache, slug, owner=''):
    """按 slug 查缓存；同名多 owner 时要求 owner 一致（取不到就返回 None = 未知）。"""
    c = cache.get(slug)
    if not c or c.get('installs') is None:
        return None
    co = (c.get('owner') or '').lower()
    if co and owner and co != owner.lower():
        return None
    return c


def _disp_inst(r):
    """报告显示用：未知 installs 显示 ?（缺数要标未取得，不显示负数）"""
    v = r.get('installs')
    if v is None or (isinstance(v, int) and v < 0):
        return '?'
    return v



_CACHE = _cache_load()


def registry_search(query, limit=12):
    """只读查 ClawHub registry 关键词检索（不安装）
    返回 [{'slug','ref'(owner/slug),'desc','score','downloads','installs','version','owner'}]
    注意：同名 slug 可能有多 owner（安装会报 AMBIGUOUS_SKILL_SLUG），
          故用 install.reference = owner/slug 作为唯一安装引用。"""
    import json as _json
    import ssl as _ssl
    import urllib.parse
    import urllib.request
    out = []
    try:
        ctx = _ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = _ssl.CERT_NONE
        url = 'https://clawhub.ai/api/v1/search?q=' + urllib.parse.quote(query)
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0',
            'Accept': 'application/json'})
        raw = urllib.request.urlopen(req, timeout=REG_TIMEOUT, context=ctx).read()
        d = _json.loads(raw.decode('utf-8', 'replace'))
        for it in (d.get('results') or [])[:limit]:
            slug = it.get('slug') or ''
            if not slug:
                continue
            owner = it.get('ownerHandle') or (it.get('install') or {}).get('reference', '').split('/')[0]
            ref = (it.get('install') or {}).get('reference') or (
                (owner + '/' + slug) if owner else slug)
            out.append({
                'slug': slug,
                'ref': ref,
                'name': slug,
                'desc': (it.get('summary') or it.get('displayName') or '')[:110],
                'score': str(it.get('score') or 0),
                'downloads': it.get('downloads') or 0,
                # 2026-10-27 修正：ClawHub search API **不返回 installs 字段**
                #   （真实安装数藏在 install / metrics 对象里）-> 旧代码 it.get('installs')
                #   恒为 0 -> THIN->FILLED 门槛(installs>=3) 永远判不出来。
                #   抽不出时返回 -1 表示「未知」，与「真的是 0 次」区分开。
                # 2026-10-27 修正：ClawHub search API **不提供安装数**
                #   （install 对象只有 kind/reference/sourceUrl；metrics 只有 bookmarks/rolling60DayInstalls）
                #   -> 旧代码 it.get('installs') 恒为 0，THIN->FILLED 门槛(installs>=3) 永远判不出。
                #   search 阶段一律记 -1（未知，区别于真实的 0 次），由 manifest_enrich() 补权威值。
                'installs': -1,
                'version': it.get('version') or (it.get('tags') or {}).get('latest') or '',
                'owner': owner,
                'src': 'registry',
            })
    except Exception:
        return []
    return out


LINE_RE = re.compile(r'^(?P<name>[^\s]+)\s{2,}(?P<desc>.*?)\s{2,}\((?P<score>[\d.]+)\)\s*$')

def parse_market(text):
    out, seen = [], set()
    for line in (text or '').splitlines():
        line = line.rstrip()
        if not line or line.startswith('-'):
            continue
        m = LINE_RE.match(line)
        if m and m.group('name') not in seen:
            seen.add(m.group('name'))
            out.append({'name': m.group('name'),
                        'desc': m.group('desc').strip()[:100],
                        'score': m.group('score')})
    return out

# ---------- 1. 市场扫描 ----------
market, cli_ok, q_stat = [], False, []
vec_failed = []
if SHIM.exists():
    for q in QUERIES:
        if left() < 45:
            break
        st = time.time()
        rc, o, e = run([str(SHIM), 'search', q, '--limit', '5'], CLAWHUB_TIMEOUT)
        # 2026-10-25 20:22 轮：hotel 关键词 rc=-1（15.6s 超时）→ 本轮 hotel 侧候选覆盖度打折，
        #   而旧逻辑**超时即放弃、不重试、不告警** → 静默降覆盖。故：超时重试一次（更长超时），
        #   仍失败则显式记入 vec_failed 并在报告里输出覆盖度缺口告警。
        if rc == -1 and left() > 60:
            rc, o, e = run([str(SHIM), 'search', q, '--limit', '5'], CLAWHUB_TIMEOUT * 2)
        dt = round(time.time() - st, 1)
        q_stat.append({'q': q, 'rc': rc, 'sec': dt})
        if rc == 0:
            cli_ok = True
            for it in parse_market(o):
                if it['name'] not in {m['name'] for m in market}:
                    market.append(it)
        else:
            vec_failed.append(q)
    if vec_failed:
        print('[覆盖度告警] 向量检索以下关键词未取全: {}（该方向候选覆盖度打折，请以 registry 关键词结果为准）'.format(
            ', '.join(vec_failed)))
else:
    print('!! clawhub.cmd 不存在：', SHIM)

# ---------- 1b. registry 关键词检索（向量通道的互补）----------
# 2026-10-25 追加：向量检索连续 4 轮返回完全相同的 10 条占位条目（hotel/travel/…），
# 而 registry 关键词检索能翻到 hotel-price-finder(1355 下载) / hotel-price-monitor(1304) /
# meituan-hotel-deals(965) / hotel-procurement-price-check(748) 等真正有价值的技能。
# 原因：向量检索按语义相似度排序，泛词 hotel/travel 的 top 结果被占位条目占满。
reg_market, reg_stat = [], []
for q in REG_QUERIES:
    if left() < 90:
        break
    st = time.time()
    items = registry_search(q, limit=12)
    dt = round(time.time() - st, 1)
    reg_stat.append({'q': q, 'n': len(items), 'sec': dt})
    for it in items:
        if it['slug'] not in {r['slug'] for r in reg_market}:
            reg_market.append(it)

# ---------- 2. 本地清单 ----------
local_dirs, local_skill_md = [], set()
if SKILLS.exists():
    for d in SKILLS.iterdir():
        if d.is_dir() and not d.name.startswith('.'):
            local_dirs.append(d.name)
            if (d / 'SKILL.md').exists():
                local_skill_md.add(d.name)
local_dirs.sort()
local_names = set(local_dirs)
new_market = [m for m in market if m['name'] not in local_names]
# registry 候选：按 slug 判本地是否已有（同名多 owner 用 ref 区分）
reg_new = []
for r in reg_market:
    if r['slug'] in local_names:
        r['local'] = True
    else:
        r['local'] = False
        reg_new.append(r)
# 高价值排序：先看下载量，再看安装量（下载量高 = 被真实使用过）
reg_new.sort(key=lambda x: (-(x.get('downloads') or 0), -(x.get('installs') or 0)))


# ---------- 2b. 能力空白判定（零额外网络开销：复用已抓到的候选）----------
# 2026-10-25 追加：扫描每轮检出完全相同的 82 个候选 → 边际收益趋零；
# 真正该回答的是「我们的核心能力空白有没有被填补」。
# 判定规则与 registry_gap_probe.py 完全一致（复用同一份 GAPS 定义，避免规则漂移）。
def _classify_gaps(cands):
    """两级判定：core（域内核心）vs adj（相邻不对口）→ BLANK/ADJACENT/THIN/FILLED"""
    out = {}
    for g in _CAPABILITY_GAPS:
        try:
            c1 = re.compile(g['core_re'], re.I)
            c2 = re.compile(g['core2_re'], re.I)
            ca = re.compile(g['adj_re'], re.I)
            ex = re.compile(g['exclude_slug_re'], re.I)
        except Exception:
            continue
        core, adj = [], []
        for r in cands:
            slug = r.get('slug') or ''
            if ex.search(slug):
                continue
            blob = '{} {} {}'.format(slug, r.get('desc') or '', r.get('owner') or '')
            if c1.search(blob) and c2.search(blob):
                core.append(r)
            elif ca.search(blob):
                adj.append(r)
        if not core and not adj:
            status = 'BLANK'
        elif not core:
            status = 'ADJACENT'
        else:
            # 2026-10-27 修正：installs 未知(-1) 不能参与 max 比较当成 0 用
            #   -> 只用**已知**的 installs 判定；全未知时按 THIN 保守处理并标注
            # 已知 = installs 真的取到（>=0）。不能写 (x or -1)：真 0 会被当成未知。
            _known = [c for c in core if (c.get('installs') if c.get('installs') is not None else -1) >= 0]
            _best = max(_known, key=lambda x: ((x.get('installs') or 0), (x.get('downloads') or 0))) if _known else None
            status = 'FILLED' if (_best is not None and (_best.get('installs') or 0) >= 3) else 'THIN'
        out[g['id']] = {'title': g.get('title', g['id']), 'status': status,
                        'core': [c['slug'] for c in core][:6], 'adj': [a['slug'] for a in adj][:4],
                          'core_installs': {c['slug']: (c.get('installs') if c.get('installs') is not None else -1) for c in core[:12]},
                          'installs_known': len([c for c in core if (c.get('installs') if c.get('installs') is not None else -1) >= 0]),
                          'core_total': len(core)}
    return out




def _manifest_fetch(slug, ref='', timeout=8):
    """取 manifest 权威 stats.installs / stats.downloads。
    2026-10-27 实测三条关键事实：
      1. ClawHub search API **不提供安装数**（install 对象只有 kind/reference/sourceUrl；
         metrics 只有 bookmarks/rolling60DayInstalls）-> 判据只能用 manifest。
      2. 同名多 owner 的 slug -> /api/v1/skills/{slug} 返 409 AMBIGUOUS_SKILL_SLUG，
         响应体 matches[] 带 {ownerHandle, ref:"@owner/slug"}；
         可用形态：?ownerHandle=<owner>（实测有效）。
      3. **/api/v1/skills?slug=X 会忽略 slug 过滤**（返回无关技能）-> 必须校验返回的
         slug == 请求的 slug，否则会把别的技能的 installs 记到目标名下（串号）。
    返回 None = 取不到（调用方记 -1 未知，不得当 0）。
    """
    import json as _json
    import ssl as _ssl
    import urllib.error as _ue
    import urllib.request as _ur
    _ctx = _ssl.create_default_context()
    _ctx.check_hostname = False
    _ctx.verify_mode = _ssl.CERT_NONE
    _hdr = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}
    owner = (ref or '').split('/', 1)[0] if ref and '/' in ref else ''
    forms = ['https://clawhub.ai/api/v1/skills/' + slug]
    if owner:
        forms += ['https://clawhub.ai/api/v1/skills/' + slug + '?ownerHandle=' + owner,
                  'https://clawhub.ai/api/v1/skills/' + slug + '?owner=' + owner]
    tried = set()
    for _round in range(2):
        for u in forms:
            if u in tried:
                continue
            tried.add(u)
            try:
                raw = _ur.urlopen(_ur.Request(u, headers=_hdr), timeout=timeout, context=_ctx).read()
                j = _json.loads(raw.decode('utf-8', 'replace'))
                sk = j.get('skill') or (j.get('items') or [{}])[0] or {}
                # 护栏：返回的 slug 必须等于请求的 slug（list 端点忽略 slug 过滤 -> 会串号）
                if (sk.get('slug') or '').lower() != (slug or '').lower():
                    continue
                st = sk.get('stats') or {}
                if st.get('installs') is None:
                    continue
                return {'installs': st.get('installs'),
                        'downloads': st.get('downloads'),
                        'version': (sk.get('tags') or {}).get('latest') or sk.get('latestVersion') or ''}
            except _ue.HTTPError as ex:
                if ex.code == 409:
                    try:
                        j = _json.loads(ex.read().decode('utf-8', 'replace'))
                    except Exception:
                        j = {}
                    for m in (j.get('matches') or []):
                        ow = m.get('ownerHandle') or ''
                        if not ow or (owner and ow.lower() != owner.lower()):
                            continue
                        forms.append('https://clawhub.ai/api/v1/skills/' + slug + '?ownerHandle=' + ow)
                continue
            except Exception:
                continue
    return None


def manifest_enrich(reg_market, gaps, top_n=10, budget_s=50, workers=10):
    """给候选补权威 installs/downloads/version（search API 不提供安装数 -> 只能用 manifest）。
    只补两类（控制请求数）：(1) 各 gap 的 core 候选（决定 THIN/FILLED，必须准）
                           (2) downloads 最高的 top_n（报告要显示真实热度与版本）
    取不到的记 -1（未知），**不得当 0**（把未知当 0 会把 FILLED 误判成 THIN）。
    预算只限制**发起**新请求；已返回的结果一律采纳
    （2026-10-27 修：旧版把预算检查放在结果到达之后 -> 55s 后完成的补数被整批丢弃
      -> 出现 FILLED->THIN 假翻转）。
    """
    import re as _re
    import concurrent.futures as _cf
    need = {}
    for g in gaps:
        try:
            c1 = _re.compile(g['core_re'], _re.I)
            c2 = _re.compile(g['core2_re'], _re.I)
            ex = _re.compile(g['exclude_slug_re'], _re.I)
        except Exception:
            continue
        for r in reg_market:
            slug = r.get('slug') or ''
            blob = '%s %s %s' % (slug, r.get('desc') or '', r.get('owner') or '')
            if ex.search(slug):
                continue
            if c1.search(blob) and c2.search(blob):
                need[slug] = r
    for r in sorted(reg_market, key=lambda x: -(x.get('downloads') or 0))[:top_n]:
        need.setdefault(r.get('slug') or '', r)
    # 2026-10-27 权威缓存优先：缓存命中直接用并**移出待抓列表**（避免被现场结果覆盖）
    _cache_hit = 0
    for _slug in list(need.keys()):
        _c = _cache_lookup(_CACHE, _slug, need[_slug].get('owner') or '')
        if not _c:
            continue
        _r = need[_slug]
        _r['installs'] = _c['installs']
        if _c.get('downloads') is not None:
            _r['downloads'] = _c['downloads']
        if _c.get('version'):
            _r['version'] = _c['version']
        del need[_slug]
        _cache_hit += 1
    print('[manifest] cache hit %d / live-miss %d' % (_cache_hit, len(need)))
    items = [(slug, r) for slug, r in need.items() if slug]
    t0 = time.time()
    ok = 0
    unknown = 0
    if items:
        with _cf.ThreadPoolExecutor(max_workers=workers) as _pool:
            futs = {}
            for slug, r in items:
                if time.time() - t0 > budget_s:
                    break
                futs[_pool.submit(_manifest_fetch, slug, r.get('ref') or '')] = (slug, r)
            for fut in _cf.as_completed(futs):
                slug, r = futs[fut]
                try:
                    info = fut.result()
                except Exception:
                    info = None
                if info:
                    r['installs'] = info['installs'] if info['installs'] is not None else -1
                    if info['downloads'] is not None:
                        r['downloads'] = info['downloads']
                    if info['version']:
                        r['version'] = info['version']
                    ok += 1
                else:
                    r['installs'] = -1
                    unknown += 1
    print('[manifest] authoritative installs: %d known / %d unknown (of %d candidates, %.1fs)' % (
        ok, unknown, len(items), time.time() - t0))
    return ok, len(items)

manifest_enrich(reg_market, _CAPABILITY_GAPS)
gap_status = _classify_gaps(reg_market)
# 与上一轮对比 → 空白是否被填补（本扫描器最有价值的信号）
gap_delta = []
# 2026-10-26 16:41 修正：单轮差分把「回流」误报为「新增」
#   实测：registry 关键词检索结果集在轮间波动（82 → 69 → 75），
#   候选掉出检索集、下轮再回来 → 单轮差分 (_cur - _prev) 把它当成全新候选 → 假新增。
#   16:41 那轮 13 条「新增」里绝大多数是 12:40 已出现过的旧候选回流。
#   改为：**累计见过的 slug 池**判定真新增（首次出现才算新增），并单独报「回流」数量。
_prev = {}
_prev_slugs = set()
_prev_vec = set()
if LOG.exists():
    try:
        _pd = json.loads(LOG.read_text(encoding='utf-8', errors='replace'))
        _prev = _pd.get('gap_status') or {}
        _prev_slugs = {r.get('slug') for r in (_pd.get('reg_new') or []) if r.get('slug')}
        _prev_vec = {m.get('name') for m in (_pd.get('new') or []) if m.get('name')}
    except Exception:
        _prev = {}
_pool = {'slugs': [], 'vec': []}
if POOL.exists():
    try:
        _pd2 = json.loads(POOL.read_text(encoding='utf-8', errors='replace'))
        _pool = {'slugs': list(_pd2.get('slugs') or []), 'vec': list(_pd2.get('vec') or [])}
    except Exception:
        _pool = {'slugs': [], 'vec': []}
if not _pool.get('slugs') and not _pool.get('vec'):
    # 首次启用：无池文件 → 以「上一轮」为种子，避免把整库 75 条一次性误报为新增
    _pool = {'slugs': sorted(_prev_slugs), 'vec': sorted(_prev_vec)}
    print('[累计池] 首次启用 → 以上一轮为种子（{} 个 slug），避免全量误报新增'.format(len(_pool['slugs'])))
_pool_slugs = set(_pool.get('slugs') or [])
_pool_vec = set(_pool.get('vec') or [])
for gid, g in gap_status.items():
    old = (_prev.get(gid) or {}).get('status')
    if old and old != g['status']:
        gap_delta.append('{}：{} → {}'.format(g['title'], old, g['status']))
if gap_delta:
    print('[能力空白变化] ' + '；'.join(gap_delta))
_cur_slugs = {r.get('slug') for r in reg_market if r.get('slug')}
_cur_vec = {m.get('name') for m in market if m.get('name')}
# 真新增 = 从未在累计池里出现过（回流不再误报为新增）
candidate_delta = sorted(_cur_slugs - _pool_slugs)
vector_delta = sorted(_cur_vec - _pool_vec)
# 回流 = 本轮出现、累计池里见过、但上一轮没出现 → 单轮差分会误判为新增
reflow = sorted((_cur_slugs - _prev_slugs) & _pool_slugs)
NO_CHANGE = (not candidate_delta) and (not vector_delta) and (not gap_delta)
if NO_CHANGE:
    print('[本轮无变化] 真新增候选 0 + 空白状态与上轮一致 → 建议不推送（仅记日志）')
else:
    print('[本轮有变化] 真新增 registry {}｜真新增向量 {}｜空白变化 {}'.format(
        len(candidate_delta), len(vector_delta), len(gap_delta)))
print('[回流识别] 本轮回流旧候选 {} 个（已在累计池中，单轮差分会误报为新增）: {}'.format(
    len(reflow), ', '.join(reflow[:12]) or '—'))
_pool_slugs |= _cur_slugs
_pool_vec |= _cur_vec
try:
    POOL.parent.mkdir(parents=True, exist_ok=True)
    POOL.write_text(json.dumps({'slugs': sorted(_pool_slugs), 'vec': sorted(_pool_vec),
                                 'updated': time.strftime('%Y-%m-%d %H:%M:%S')},
                                ensure_ascii=False, indent=2), encoding='utf-8')
    print('[累计池] 已更新：{} 个 slug / {} 个向量候选'.format(len(_pool_slugs), len(_pool_vec)))
except Exception as _pe:
    print('[累计池写入失败] {}'.format(_pe))

# ---- 与报告段/结果字段口径对齐（这两个定义曾被差分块整块替换覆盖，2026-10-26 修复）----
#   _seen    = 累积 slug 池（同一对象引用；下面的 union 会原地更新它 -> 总量自动同步）
#   true_new = 真新增（累积池口径：从未在池中出现过 -> 天然排除回流）
_seen = _pool_slugs
true_new = list(candidate_delta)

# 2026-10-26 18:22 修正：clawhub search 的纯文本输出**不含 version** → 真新增候选必须查 manifest
#   （R-HEAL-26：版本只认 manifest；用 search 结果说「无版本号」会误判安装门控）
#   18:22 那轮报告写 store-location-analysis「registry 未提供版本号（空）」，
#   实际 manifest: tags.latest=1.0.0 / downloads=501 / installs=0。
_MANIFEST_BASE = 'https://clawhub.ai/api/v1/skills/'


def manifest_version(slug, t=12):
    import ssl as _ssl
    import urllib.request as _ur
    ctx = _ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = _ssl.CERT_NONE
    try:
        req = _ur.Request(_MANIFEST_BASE + slug,
                          headers={'User-Agent': 'B166ER-scan', 'Accept': 'application/json'})
        r = _ur.urlopen(req, timeout=t, context=ctx)
        j = json.loads(r.read().decode('utf-8', 'replace'))
        sk = j.get('skill') or {}
        st = sk.get('stats') or {}
        return ((sk.get('tags') or {}).get('latest'),
                st.get('downloads'), st.get('installs'),
                (j.get('owner') or {}).get('handle'))
    except Exception:
        return None, None, None, None


_ver_map = {}
# 补版本范围 = 真新增 + 下载量最高的候选（安装闸门要看的就是这些）
_top = [r.get('slug') for r in sorted(reg_new, key=lambda x: -(x.get('downloads') or 0))[:6]]
_need = []
for _s in list(true_new) + _top:
    if _s and _s not in _need:
        _need.append(_s)
for _slug in _need:
    if left() < 45:
        print('[manifest 补版本] 预算不足，提前停止（已查 {} 个）'.format(len(_ver_map)))
        break
    _v, _dl, _ins, _ow = manifest_version(_slug)
    if _v:
        _ver_map[_slug] = _v
    for _r in reg_new:
        if _r.get('slug') == _slug:
            if _v:
                _r['version'] = _v
            if _dl is not None:
                _r['downloads'] = _dl
            if _ins is not None:
                _r['installs'] = _ins
            if _ow:
                _r['owner'] = _ow
print('[manifest 补版本] 应查 {} 个 → 查到版本 {}（其余仍为 ?）'.format(
    len(_need), _ver_map or '无'))

# ---------- 3. git 更新（三分类，失败也给出可行动原因）----------
# 2026-10-25 修正：旧版 `git pull --ff-only` 失败只报 err，无行动价值。
#   evolver: main...origin/main [ahead 115, behind 149]  → 分叉，--ff-only 必然失败
#   wewrite: fetching ref refs/tags/v3.6.1 failed: reference already exists → 标签冲突
# 新版：fetch --no-tags（绕开标签冲突）→ 读 ahead/behind → 分类
#   ① uptodate  已是最新
#   ② updated  远端有新提交且可快进 → merge --ff-only（安全自动完成）
#   ③ diverged 本地有未推提交且远端也有新提交 → 需人工 rebase/merge，脚本绝不自动改写
#   ④ failed   网络/权限/其它 → 留待下轮
git_updated, git_diverged, git_failed, git_uptodate = [], [], [], []
git_skipped = []
# 2026-10-25 修正：run() 用 stderr=subprocess.STDOUT，错误文本在【stdout】而非 stderr，
#   旧代码从 e 取原因 → 永远得到空串 → 报告显示无行动价值的 err。
#   另一修正：GitHub 临时不可达时，6 个仓各等 21s 超时 = 130s 白烧预算 → 加网络预检 + 熔断。
NET_MARKERS = ('Could not connect', 'Failed to connect', 'Connection was reset',
               'RPC failed', 'Connection timed out', 'early EOF', 'gnutls_handshake')


# 2026-10-26 19:2x 根因修复：**Windows 上 git 不读 WinINET 系统代理**（Python urllib 会读）。
#   实测：裸 TCP 直连 github.com 时通时不通（代理/TUN 路由抖动），
#   而走 127.0.0.1:7900 的 urllib 稳定返回 200 → git 必须**显式指定代理**才稳定。
#   症状：同一台机器、同一分钟，直连/git 结论互相矛盾（我 19:05 测「直连不通但 git 1.1s 成功」，
#   扫描器 19:1x 测「直连通但 git 探针不通」）→ 结论：唯一可靠路径 = 显式代理。
def detect_proxy():
    try:
        import urllib.request as _u
        _p = _u.getproxies()
        _px = (_p.get('https') or _p.get('http') or '').strip()
        return _px if _px.startswith('http') else ''
    except Exception:
        return ''


GIT_PROXY = detect_proxy()


def git_args(*rest):
    """所有 git 调用统一走检测到的系统代理（无代理时退化为原样）"""
    _a = ['git']
    if GIT_PROXY:
        _a += ['-c', 'http.proxy=%s' % GIT_PROXY, '-c', 'https.proxy=%s' % GIT_PROXY]
    return _a + list(rest)


def net_reachable(host='github.com', port=443, t=6):
    """TCP 直连探测（仅作诊断信息，不再作为「是否跳过 git 阶段」的判据）"""
    import socket
    try:
        s = socket.create_connection((host, port), timeout=t)
        s.close()
        return True
    except Exception:
        return False


def git_reachable(t=14):
    """2026-10-26 18:22 修正：**预检必须与实际动作同栈**。
       旧版用裸 socket 直连判「网络 OK」，但 git 走 libcurl（可走系统代理 / 不同 TLS 栈），
       实测出现过「预检 OK 但 6 个仓全部 neterr」（net_ok=True 与 git_fail 同时成立，自相矛盾）。
       现在改用 git 自己探：ls-remote 一个已知仓，14s 内返回即认为 git 通道可用。
       另外：Windows 上 git 不会自动读 WinINET 系统代理（urllib 会读），
       故直连失败 ≠ git 不可用（实测直连超时但 git 走代理 1.1s 成功）。"""
    rc, o, e = run(git_args('-c', 'http.version=HTTP/1.1', 'ls-remote', '--heads',
                            'https://github.com/EvoMap/evolver.git'), t)
    return rc == 0


cands = [d for d in (SKILLS.iterdir() if SKILLS.exists() else [])
         if d.is_dir() and (d / '.git').exists()][:MAX_GIT]
NET_DIRECT = net_reachable()          # 诊断用：裸 TCP 直连（不代表 git 能否走代理）
GIT_OK = git_reachable()               # 判据用：与实际 fetch 同栈的 git 探针
NET_OK = GIT_OK
print('[git] 通道探测：裸TCP直连={}｜git同栈探针={}（判据用后者）'.format(
    '通' if NET_DIRECT else '不通', '通' if GIT_OK else '不通'))
if not NET_OK:
    git_skipped = ['{}(git通道不可达)'.format(d.name) for d in cands]
    print('[git] git 通道不可达 → 本轮跳过 {} 个仓的更新（网络/代理问题，非脚本故障）'.format(len(cands)))
consec_net_fail = 0
for d in cands:
    if not NET_OK:
        break
    if left() < 30:
        git_skipped.append(d.name)
        continue
    if consec_net_fail >= 2:
        # 熔断：连续 2 个仓因网络失败 → 判定网络整体不通，剩余不再逐个试
        # 2026-10-26 修正：标注「因熔断连带」——否则报告读起来像这 4 个仓也坏了
        git_skipped.append('{}(因网络熔断连带，非该仓故障)'.format(d.name))
        continue
    # 3.0 清理陈旧 .lock（上次 fetch 被 timeout 强杀留下的残留，
    #     会让后续 fetch 报 "reference already exists"）
    #     只删 .lock 文件，不动任何 ref / 对象 / commit
    try:
        for _lk in (d / '.git').rglob('*.lock'):
            if _lk.is_file():
                _lk.unlink()
    except Exception:
        pass
    # 3.1 fetch（--no-tags 避免本地/远端同名标签冲突）
    rc, o, e = run(git_args('-C', str(d), 'fetch', '--prune', '--no-tags', 'origin'), GIT_TIMEOUT)
    # 错误文本在 stdout（stderr 已合并），必须从 o 取
    if rc != 0 and rc != -1 and 'already exists' in (o or ''):
        # 远程跟踪引用冲突（远端 force-push 或本地 ref 形态不同）：
        #   保守重试 —— --force 只重置 refs/remotes/* 远程跟踪引用，
        #   不动本地分支、不动工作区、不改写任何提交。
        rc, o, e = run(git_args('-C', str(d), 'fetch', '--prune', '--no-tags', '--force', 'origin'),
                       GIT_TIMEOUT)
    if rc != 0 and any(k in (o or '') for k in NET_MARKERS):
        # 2026-10-26 修正：实测 neterr 是**瞬时抖动**（同命令 1.1s 成功 / 21s 超时都出现过）→ 重试一次
        #   （与 clawhub 侧「超时重试一次」的既有做法一致），仍失败才计入熔断
        rc, o, e = run(git_args('-c', 'http.version=HTTP/1.1', '-C', str(d),
                                'fetch', '--prune', '--no-tags', 'origin'), GIT_TIMEOUT)
        if rc == 0:
            o = o or ''
            e = e or ''
    if rc == -1:
        # 超时也计入网络熔断计数（否则 timeout 型失败不触发熔断，会把 8 个仓逐个等一遍）
        consec_net_fail += 1
        git_failed.append('{}(timeout)'.format(d.name))
        continue
    if rc != 0:
        blob = o or ''
        is_net = any(k in blob for k in NET_MARKERS)
        if is_net:
            consec_net_fail += 1
            # 2026-10-26 修正：实测为**瞬时网络抖动**（同一命令 1.1s 成功 / 21s 超时都出现过），
            # 不是「该仓坏了」也不是「代理配置错误」→ 不该让 Eric 去人工排查代理/域名
            reason = 'neterr(瞬时抖动，下轮自动重试)'
        else:
            reason = 'timeout' if rc == -1 else ('missing' if rc == -2 else
                      (blob.strip().splitlines()[-1][:44] if blob.strip() else 'err'))
        git_failed.append('{}({})'.format(d.name, reason))
        continue
    # 3.2 读 ahead/behind
    rc2, o2, e2 = run(['git', '-C', str(d), 'rev-list', '--left-right', '--count', 'HEAD...@{u}'], 60)
    ahead = behind = None
    if rc2 == 0:
        parts = (o2 or '').split()
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            ahead, behind = int(parts[0]), int(parts[1])
    if ahead is None:
        git_failed.append('{}(no-upstream)'.format(d.name))
        continue
    if behind == 0:
        git_uptodate.append(d.name)
        continue
    if ahead > 0:
        # 分叉：本地有未推提交且远端也有新提交 → 需人工处理，脚本绝不自动改写历史
        git_diverged.append('{}(ahead {},behind {} → 需人工 rebase/merge)'.format(
            d.name, ahead, behind))
        continue
    # 3.3 仅在可快进时自动 merge
    rc3, o3, e3 = run(['git', '-C', str(d), 'merge', '--ff-only', '@{u}'], GIT_TIMEOUT)
    if rc3 == 0:
        git_updated.append(d.name)
    else:
        reason = 'timeout' if rc3 == -1 else (
            (e3.strip().splitlines()[-1][:40] if (e3 or '').strip() else 'err'))
        git_failed.append('{}({})'.format(d.name, reason))

# ---------- 4. 写清单 + 结构化日志 ----------
MEMO.parent.mkdir(parents=True, exist_ok=True)
ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
q_line = ', '.join('{}={}s(rc{})'.format(x['q'], x['sec'], x['rc']) for x in q_stat)
L = ['\n---\n\n## 技能市场扫描 · {}\n'.format(ts),
     '- 用时 {:.0f}s / 预算 {}s（clawhub CLI {}）\n'.format(
         time.time() - t0, TOTAL_BUDGET, '可用' if cli_ok else '不可用'),
     '- 检索词与耗时：' + q_line + '\n',
     '- 向量通道覆盖度缺口：{}\n'.format(
         ('、'.join(vec_failed) + '（未取全，该方向候选打折）') if vec_failed else '无'),
     '- 市场去重后 {} 条；本地技能 {} 个（SKILL.md {} 个）\n'.format(
         len(market), len(local_dirs), len(local_skill_md)),
     '- 市场有本地无：{} 个\n'.format(len(new_market)),
     '- registry 关键词检索: {} 条去重（{} 个可安装）\n'.format(
         len(reg_market), len(reg_new)),
     '\n### 能力空白状态（判定复用上方已抓候选，零额外请求）\n']
for gid, g in gap_status.items():
    L.append('- {}：**{}**（域内核心 {}｜相邻 {}）\n'.format(
        g['title'], g['status'],
        '、'.join(g['core']) if g['core'] else '无',
        '、'.join(g['adj']) if g['adj'] else '无'))
L.append('- 空白变化：{}\n'.format('；'.join(gap_delta) if gap_delta else '无（本轮无变化）'))
L.append('- 候选变化：新增 registry 候选 {}｜新增向量候选 {}｜**本轮是否有变化**: {}\n'.format(
    len(candidate_delta), len(vector_delta), '否（建议不推送）' if NO_CHANGE else '是'))
L.append('- 真新增（累积池口径，排除回流）：{} 个：{}\n'.format(
    len(true_new), '、'.join(true_new) if true_new else '无'))
L.append('- 累积 slug 池总量：{} 条\n'.format(len(_seen)))
L += ['\n### 新技能候选\n']
if new_market:
    for m in new_market:
        L.append('- **{}** (score {}) — {}\n'.format(m['name'], m['score'], m['desc']))
else:
    L.append('- 无（市场返回项均已安装）\n')
L.append('\n### registry 关键词检索 · 可安装候选（按下载量降序）\n')
if reg_new:
    for r in reg_new[:15]:
        L.append('- **{}**  v{}  ↓{}次/装{}次  owner: {}  ref: `{}`  — {}\n'.format(
            r['slug'], r['version'] or '?', r['downloads'], r['installs'],
            r['owner'] or '?', r['ref'], r['desc'][:90]))
else:
    L.append('- 无（全部已本地安装）\n')
L.append('\n### git 更新结果\n- 已更新 {} 个：{}\n'.format(
    len(git_updated), ', '.join(git_updated) if git_updated else '—'))
L.append('- 已是最新 {} 个：{}\n'.format(
    len(git_uptodate), ', '.join(git_uptodate) if git_uptodate else '—'))
L.append('- 需人工处理（分支分叉，脚本不自动改写）{} 个：{}\n'.format(
    len(git_diverged), ', '.join(git_diverged) if git_diverged else '—'))
L.append('- 失败（网络/权限等）{} 个：{}\n'.format(
    len(git_failed), ', '.join(git_failed) if git_failed else '—'))
L.append('- 跳过（网络不通/预算不足）{} 个：{}\n'.format(
    len(git_skipped), ', '.join(git_skipped) if git_skipped else '—'))
with open(MEMO, 'a', encoding='utf-8') as f:
    f.writelines(L)

result = {'ts': ts, 'sec': round(time.time() - t0, 1), 'cli_ok': cli_ok,
          'queries': q_stat, 'market_n': len(market), 'local_n': len(local_dirs),
          'vec_failed': vec_failed,
          'skill_md_n': len(local_skill_md), 'new': new_market,
          'reg_new': reg_new, 'reg_stat': reg_stat,
          'gap_status': gap_status, 'gap_delta': gap_delta,
          'candidate_delta': candidate_delta, 'vector_delta': vector_delta,
          'reflow': reflow, 'pool_n': len(_pool_slugs),
          'true_new': true_new, 'seen_pool_n': len(_seen),
          'no_change': NO_CHANGE,
          'git_ok': git_updated, 'git_uptodate': git_uptodate,
          'git_diverged': git_diverged, 'git_fail': git_failed,
          'git_skipped': git_skipped, 'net_ok': NET_OK}
LOG.parent.mkdir(parents=True, exist_ok=True)
LOG.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')

print('=== B166ER 技能市场扫描完成 ===')
print('用时 {}s / 预算 {}s｜clawhub CLI {}'.format(
    result['sec'], TOTAL_BUDGET, '可用' if cli_ok else '不可用'))
print('查询耗时：' + ' | '.join('{}={}s'.format(x['q'], x['sec']) for x in q_stat))
print('市场去重 {} 条｜本地技能 {} 个（SKILL.md {}）'.format(
    len(market), len(local_dirs), len(local_skill_md)))
print('新技能候选：' + (', '.join(m['name'] for m in new_market) if new_market else '无'))
print('registry 可安装候选 {} 个: {}'.format(
    len(reg_new), ', '.join(r['slug'] for r in reg_new[:8]) or '无'))
print('git 更新: 已更新 {}｜已最新 {}｜需人工(分叉) {}｜失败 {}｜跳过 {}'.format(
    len(git_updated), len(git_uptodate), len(git_diverged), len(git_failed),
    len(git_skipped)))
print('清单：{}｜日志：{}'.format(MEMO, LOG))
