# -*- coding: utf-8 -*-
"""
kb_weekly_run.py — KB 每周维护确定性 runner (V1.0, 2026-10-25)

替代 agentTurn「B166ER-KB-Weekly-Maintenance」的 6 步自由发挥，改为固定三段流水线：
  1. kb_scanner.py         —— 扫描 KB，产出 scan_report.json
  2. kb_maintenance.py     —— 基于报告修复（当前 0 字节文件 0 个 → 实际为空操作）
  3. kb_routing_table.py --apply —— 把新纳入的 KB 登记进 routing-index.md，闭环路由表

每段都有独立硬超时，总预算内必然返回。执行完打印精简摘要 + 结构化日志。

用法: python kb_weekly_run.py [--dry-run]
"""
import sys, os, json, time, tempfile, subprocess, datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WS = Path(r'D:\B166ER-OpenClaw\workspace')
KB = WS / 'toolbox' / 'kb_tools'
LOG = WS / '.tmp' / 'kb_weekly_last.json'
REPORT = WS / 'memory' / 'KB-Weekly-Maintenance-report.md'

SCAN_TIMEOUT = 180
MAINT_TIMEOUT = 120
ROUTE_TIMEOUT = 120
TOTAL_BUDGET = 480

t0 = time.time()
NEWPROC = getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 0)


def run(cmd, timeout, cwd=None):
    """临时文件承接 stdout + 超时杀整棵进程树（避免 Windows 管道死锁）"""
    with tempfile.TemporaryFile('w+b') as tf:
        try:
            p = subprocess.Popen(cmd, cwd=cwd, stdout=tf, stderr=subprocess.STDOUT,
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


STEPS = [
    ('扫描', [sys.executable, str(KB / 'kb_scanner.py')], SCAN_TIMEOUT),
    ('维护', [sys.executable, str(KB / 'kb_maintenance.py')], MAINT_TIMEOUT),
    ('路由', [sys.executable, str(WS / 'kb_routing_table.py'), '--apply'], ROUTE_TIMEOUT),
]

results = []
for name, cmd, to in STEPS:
    if time.time() - t0 > TOTAL_BUDGET - 60:
        results.append((name, 'SKIP', '', '预算不足'))
        continue
    st = time.time()
    rc, out, err = run(cmd, to, cwd=str(WS))
    dt = round(time.time() - st, 1)
    results.append((name, 'OK' if rc == 0 else 'FAIL', out, err))
    print('[{}] {} rc={} {:.1f}s'.format(name, 'OK' if rc == 0 else 'FAIL', rc, dt))

# ---------- 采集关键指标 ----------
scan_report = KB / 'scan_report.json'
metrics = {}
if scan_report.exists():
    try:
        sr = json.loads(scan_report.read_text(encoding='utf-8'))
        iss = sr.get('issues', {})
        metrics = {
            'scanned_files': len(sr.get('files', [])),
            'empty_files': len(iss.get('empty_files', [])),
            'multi_versions': len(iss.get('multi_versions', [])),
            'conflict_keywords': len(iss.get('conflict_keywords', [])),
            'todos': len(iss.get('todos', [])),
        }
    except Exception as e:
        metrics['parse_error'] = str(e)

route_json = WS / 'memory' / 'routing_update_needed.json'
if route_json.exists():
    try:
        rj = json.loads(route_json.read_text(encoding='utf-8'))
        metrics.update({'kb_candidates': rj.get('kb_candidates'),
                        'already_routed': rj.get('already_routed'),
                        'new_routes_needed': rj.get('new_routes_needed'),
                        'routing_status': rj.get('status')})
    except Exception:
        pass

moc = KB / 'KB_MOC.md'
if moc.exists():
    metrics['moc_bytes'] = moc.stat().st_size

# ---------- 写报告 ----------
ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
L = ['# KB 每周维护报告', '', '> 生成时间: {}（自动）'.format(ts),
     '> 执行方式: `python toolbox/kb_tools/kb_weekly_run.py`（确定性三段流水线）', '',
     '## 执行结果', '', '| 阶段 | 结果 | 耗时 |', '|------|------|------|']
for name, status, out, err in results:
    L.append('| {} | {} | |'.format(name, status))
L += ['', '## 关键指标', '']
for k, v in metrics.items():
    L.append('- {}: {}'.format(k, v))
L += ['', '## 结论', '']
if metrics.get('routing_status') == 'OK':
    L.append('- 路由表闭环完成，无待登记条目。')
else:
    L.append('- 路由表仍有 {} 条待登记，需检查 kb_routing_table.py --apply 是否执行成功。'.format(
        metrics.get('new_routes_needed', '?')))
if metrics.get('empty_files', 0) == 0:
    L.append('- 无 0 字节文件需要清理。')
if metrics.get('multi_versions', 0):
    L.append('- 有 {} 组多版本冲突需人工判定（脚本不自动合并）。'.format(metrics['multi_versions']))
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text('\n'.join(L) + '\n', encoding='utf-8')

payload = {'ts': ts, 'sec': round(time.time() - t0, 1),
           'steps': [(n, s) for n, s, _, _ in results], 'metrics': metrics,
           'report': str(REPORT)}
LOG.parent.mkdir(parents=True, exist_ok=True)
LOG.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')

print()
print('=== KB 周维护完成 ===')
print('总耗时 {:.1f}s / 预算 {}s'.format(payload['sec'], TOTAL_BUDGET))
print('阶段: ' + ' | '.join('{}={}'.format(n, s) for n, s, _, _ in results))
for k, v in metrics.items():
    print('  {}: {}'.format(k, v))
print('报告: {}'.format(REPORT))
print('日志: {}'.format(LOG))
