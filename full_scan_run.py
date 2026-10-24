# -*- coding: utf-8 -*-
"""
full_scan_run.py — 全盘扫描与自动纳入确定性 runner (V1.0, 2026-10-25)

替代 automation「B166ER-Full-Scan-Auto-Ingest」里的 5 步自由发挥，改为固定五段流水线：
  1. scan_files.py             —— 全盘扫描建清单（memory/file_inventory.json + file_scan_report.json）
  2. batch_indexer.py --limit 200 —— 批量增量纳入索引
  3. kb_rag.py stats           —— 确认索引库增长（文件数 / 分块数 / 索引大小 / 向量引擎）
  4. kb_routing_table.py --apply —— 登记文件级路由（唯一事实源 skills/knowledge-base/routing-index.md）
  5. 生成报告 memory/YYYY-MM-DD_full-scan-report.md

每段都有独立硬超时 + 总预算，执行完打印精简摘要 + 结构化日志。
注意：kb_router.py 已于 2026-07-11 删除，不存在；路由登记统一走 routing-index.md，
      不要往 SKILL.md 追加表格（SKILL.md 每次会话加载，承载增长型索引会膨胀）。

用法: python full_scan_run.py [--limit 200]
"""
import sys, os, re, json, time, tempfile, subprocess, datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WS = Path(__file__).resolve().parent
LOG = WS / '.tmp' / 'full_scan_last.json'
REPORT_DIR = WS / 'memory'

SCAN_TIMEOUT = 300
INDEX_TIMEOUT = 600
STATS_TIMEOUT = 120
ROUTE_TIMEOUT = 120
TOTAL_BUDGET = 1200

LIMIT = 200
for i, a in enumerate(sys.argv):
    if a == '--limit' and i + 1 < len(sys.argv):
        try:
            LIMIT = int(sys.argv[i + 1])
        except ValueError:
            pass

t0 = time.time()
NEWPROC = getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 0)


def left():
    return TOTAL_BUDGET - (time.time() - t0)


def run(cmd, timeout):
    """临时文件承接 stdout + 超时杀整棵进程树（避免 Windows 管道死锁）"""
    with tempfile.TemporaryFile('w+b') as tf:
        try:
            p = subprocess.Popen(cmd, cwd=str(WS), stdout=tf, stderr=subprocess.STDOUT,
                                 stdin=subprocess.DEVNULL, creationflags=NEWPROC)
        except Exception as e:
            return -2, '', str(e)
        try:
            p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True)
            try:
                p.wait(timeout=8)
            except Exception:
                pass
            return -1, '', 'TIMEOUT'
        tf.seek(0)
        return p.returncode, tf.read().decode('utf-8', 'replace'), ''


def tail(text, n=8):
    lines = [l for l in (text or '').splitlines() if l.strip()]
    return lines[-n:]


PY = sys.executable
STAGES = [
    ('扫描', [PY, str(WS / 'scan_files.py')], SCAN_TIMEOUT),
    ('纳入', [PY, str(WS / 'batch_indexer.py'), '--limit', str(LIMIT)], INDEX_TIMEOUT),
    ('索引统计', [PY, str(WS / 'kb_rag.py'), 'stats'], STATS_TIMEOUT),
    ('路由登记', [PY, str(WS / 'kb_routing_table.py'), '--apply'], ROUTE_TIMEOUT),
]

results = []
for name, cmd, to in STAGES:
    if left() < 120:
        results.append({'stage': name, 'status': 'SKIP', 'sec': 0, 'tail': ['预算不足']})
        print('[{}] SKIP 预算不足'.format(name))
        continue
    st = time.time()
    rc, out, err = run(cmd, to)
    dt = round(time.time() - st, 1)
    status = 'OK' if rc == 0 else ('TIMEOUT' if rc == -1 else 'FAIL')
    results.append({'stage': name, 'status': status, 'sec': dt, 'rc': rc,
                    'tail': tail(out or err)})
    print('[{}] {} rc={} {:.1f}s'.format(name, status, rc, dt))

# ---------- 采集关键指标 ----------
metrics = {}

# 扫描
inv = WS / 'memory' / 'file_inventory.json'
rep = WS / 'memory' / 'file_scan_report.json'
if inv.exists():
    try:
        d = json.loads(inv.read_text(encoding='utf-8', errors='replace'))
        files = d if isinstance(d, list) else (d.get('files') or d.get('inventory') or [])
        metrics['scanned_files'] = len(files)
        if files and isinstance(files[0], dict):
            metrics['scanned_bytes'] = sum(f.get('size') or 0 for f in files)
    except Exception as e:
        metrics['inventory_parse_error'] = str(e)[:120]
if rep.exists():
    try:
        d = json.loads(rep.read_text(encoding='utf-8', errors='replace'))
        if isinstance(d, dict):
            for k in ('total_files', 'total_bytes', 'extensions', 'top_dirs'):
                if k in d:
                    metrics['scan_' + k] = d[k] if not isinstance(d[k], (list, dict)) else \
                        (len(d[k]) if isinstance(d[k], list) else list(d[k].keys())[:8])
    except Exception:
        pass

# 纳入
for r in results:
    if r['stage'] == '纳入':
        blob = '\n'.join(r['tail'])
        m = re.search(r'新增候选[:：]\s*(\d+)', blob) or re.search(r'成功\s*(\d+)\s*/', blob)
        if m:
            metrics['indexed_this_run'] = int(m.group(1))
        m = re.search(r'失败[:：]?\s*(\d+)', blob)
        if m:
            metrics['index_failed'] = int(m.group(1))
        m = re.search(r'新增分块[:：]\s*(\d+)', blob)
        if m:
            metrics['new_chunks'] = int(m.group(1))

# 索引库
for r in results:
    if r['stage'] == '索引统计':
        blob = '\n'.join(r['tail'])
        for pat, key in [(r'索引\s*文件数[:：]\s*(\d+)', 'index_files'),
                         (r'分块\s*总数[:：]\s*(\d+)', 'index_chunks'),
                         (r'索引\s*总大小[:：]\s*(\d+)KB', 'index_kb')]:
            m = re.search(pat, blob)
            if m:
                metrics[key] = int(m.group(1))
        m = re.search(r'最后\s*索引[:：]\s*(\S+)', blob)
        if m:
            metrics['last_indexed'] = m.group(1)
        m = re.search(r'向量\s*引擎[:：]\s*(.+)$', blob, re.M)
        if m:
            metrics['vector_engine'] = m.group(1).strip()
        metrics['kb_rag_ok'] = (r['status'] == 'OK')

# 路由
rj = WS / 'memory' / 'routing_update_needed.json'
if rj.exists():
    try:
        j = json.loads(rj.read_text(encoding='utf-8', errors='replace'))
        metrics['kb_candidates'] = j.get('kb_candidates')
        metrics['already_routed'] = j.get('already_routed')
        metrics['new_routes_needed'] = j.get('new_routes_needed')
        metrics['routing_status'] = j.get('status')
    except Exception:
        pass

# ---------- 写报告 ----------
ts = datetime.datetime.now()
day = ts.strftime('%Y-%m-%d')
REPORT = REPORT_DIR / '{}_full-scan-report.md'.format(day)
L = ['# B166ER 全盘扫描与自动纳入报告', '',
     '> 生成时间: {}（自动脚本 full_scan_run.py）'.format(ts.strftime('%Y-%m-%d %H:%M:%S')),
     '> 执行方式: `python full_scan_run.py`（确定性五段流水线）', '',
     '## 一、执行结果', '', '| 阶段 | 结果 | 耗时 |', '|------|------|------|']
for r in results:
    L.append('| {} | {} | {:.1f}s |'.format(r['stage'], r['status'], r['sec']))
L += ['', '## 二、关键指标', '']
for k, v in metrics.items():
    L.append('- {}: {}'.format(k, v))
L += ['', '## 三、结论', '']
if metrics.get('routing_status') == 'OK':
    L.append('- 路由表闭环完成，无待登记条目。')
else:
    L.append('- ⚠️ 路由表仍有 {} 条待登记。'.format(metrics.get('new_routes_needed', '?')))
if metrics.get('kb_rag_ok'):
    L.append('- 索引库可用（{} 文件 / {} 分块）。'.format(
        metrics.get('index_files', '?'), metrics.get('index_chunks', '?')))
L.append('- 向量引擎: {}'.format(metrics.get('vector_engine', '未知')))
L += ['', '---', '',
      '> 路由登记唯一事实源: `skills/knowledge-base/routing-index.md`（`kb_routing_table.py --apply` 生成）。',
      '> 注意：`kb_router.py` 已于 2026-07-11 删除，不存在。']
REPORT_DIR.mkdir(parents=True, exist_ok=True)
REPORT.write_text('\n'.join(L) + '\n', encoding='utf-8')

payload = {'ts': ts.strftime('%Y-%m-%d %H:%M:%S'), 'sec': round(time.time() - t0, 1),
           'limit': LIMIT, 'stages': results, 'metrics': metrics, 'report': str(REPORT)}
LOG.parent.mkdir(parents=True, exist_ok=True)
LOG.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')

print()
print('=== 全盘扫描与自动纳入完成 ===')
print('总耗时 {:.1f}s / 预算 {}s｜limit={}'.format(payload['sec'], TOTAL_BUDGET, LIMIT))
print('阶段: ' + ' | '.join('{}={}({:.1f}s)'.format(r['stage'], r['status'], r['sec'])
                             for r in results))
for k, v in metrics.items():
    print('  {}: {}'.format(k, v))
print('报告: {}'.format(REPORT))
print('日志: {}'.format(LOG))
