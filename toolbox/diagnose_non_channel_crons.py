#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diagnose_non_channel_crons.py
Eric 2026-09-08 15:09 指令：非 channel 任务失败，具体解决
策略：1) 重启用 5 个非 channel 关键任务 2) 逐个 run 一次 3) 收集具体错误
"""
import sqlite3
import subprocess
import time

DB = r'C:\Users\ericz\.openclaw\state\openclaw.sqlite'

# 选出 5 个非 channel 任务（纯本地任务，不依赖推送）
TARGETS = [
    '01679313-75d4-4ffa-8c99-ad1543869bc7',  # B166ER-每日本地备份-02点
    '26fa75f0-186e-4ccb-80df-d27180bd3b4d',  # B166ER-每周全量备份-周日03点
    'ea9005ef-6805-40c0-b84f-b02144a971aa',  # WAL compaction (preventive)
    '9e176754-55aa-4017-bea0-51f62d4b70b6',  # heartbeat-main
    '5a830cba-e9b8-4681-9d93-1f2df34edae0',  # Memory Dreaming Promotion
]

CLI = r'C:\Users\ericz\.openclaw\tmp\agent-cli\openclaw.cmd'
WORKDIR = r'C:\Users\ericz\.openclaw\state'

# 1. 重新启用
print('=' * 60)
print('[1/3] 重新启用 5 个非 channel 关键任务')
print('=' * 60)
conn = sqlite3.connect(DB, timeout=10)
cur = conn.cursor()
enabled_count = 0
for job_id in TARGETS:
    cur.execute('UPDATE cron_jobs SET enabled=1 WHERE job_id=?', (job_id,))
    if cur.rowcount > 0:
        enabled_count += 1
        cur.execute('SELECT name FROM cron_jobs WHERE job_id=?', (job_id,))
        name = cur.fetchone()[0]
        print(f'  [OK] {name}')
conn.commit()
conn.close()
print(f'Enabled: {enabled_count}/{len(TARGETS)}')

# 2. 逐个 run 看错误
print('\n' + '=' * 60)
print('[2/3] 逐个 run 看实际错误')
print('=' * 60)

results = []
for job_id in TARGETS:
    print(f'\n--- run {job_id} ---')
    try:
        result = subprocess.run(
            [CLI, 'automations', 'run', job_id],
            capture_output=True, text=True, timeout=120,
            cwd=WORKDIR
        )
        out = (result.stdout + result.stderr).strip()
        # 找 runId
        run_id = ''
        if 'runId' in out:
            import re
            m = re.search(r'"runId"\s*:\s*"([^"]+)"', out)
            if m:
                run_id = m.group(1)
        print(f'  returncode: {result.returncode}')
        print(f'  runId: {run_id}')
        print(f'  output: {out[:300]}')
        results.append({'job_id': job_id, 'run_id': run_id, 'returncode': result.returncode, 'output': out})
    except subprocess.TimeoutExpired:
        print(f'  TIMEOUT (>120s)')
        results.append({'job_id': job_id, 'error': 'timeout'})
    except Exception as e:
        print(f'  EXC: {e}')
        results.append({'job_id': job_id, 'error': str(e)})

# 3. 等 60 秒后查每个任务的最近 1 次 run 状态
print('\n' + '=' * 60)
print('[3/3] 等 60s 后查每个任务的最近 1 次 run 状态')
print('=' * 60)

time.sleep(60)

conn = sqlite3.connect(DB, timeout=10)
cur = conn.cursor()

# 查 cron_job_scratch 或 cron_job_runtime_authorities 表
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
all_tables = [r[0] for r in cur.fetchall()]
print(f'所有相关表: {[t for t in all_tables if "cron" in t or "run" in t]}')

# 找运行历史表
run_history_table = None
for t in all_tables:
    if 'run' in t.lower() and 'history' in t.lower():
        run_history_table = t
        break
    if t == 'cron_job_runs':
        run_history_table = t
        break

if run_history_table:
    print(f'使用表: {run_history_table}')
    cur.execute(f'SELECT job_id, status, error, completed_at FROM "{run_history_table}" WHERE job_id IN ({",".join("?"*len(TARGETS))}) ORDER BY completed_at DESC LIMIT 10', TARGETS)
    for r in cur.fetchall():
        print(f'  {r[0][:8]} | {r[1]} | err={str(r[2])[:100] if r[2] else None}')
else:
    print('未找到运行历史表')

conn.close()

# 总结
print('\n' + '=' * 60)
print('总结')
print('=' * 60)
for r in results:
    print(f'  {r.get("job_id", "?")[:8]}: returncode={r.get("returncode", r.get("error", "?"))}')

# 写诊断结果
with open(r'D:\B166ER-OpenClaw\workspace\toolbox\non_channel_diagnose_v1.0.md', 'w', encoding='utf-8') as f:
    f.write('# 非 channel 任务失败诊断 (Eric 2026-09-08 15:09)\n\n')
    f.write('## 重启用的 5 个非 channel 任务\n\n')
    for j in TARGETS:
        f.write(f'- `{j}`\n')
    f.write('\n## 逐个 run 结果\n\n')
    for r in results:
        f.write(f'### {r.get("job_id", "?")[:8]}\n')
        f.write(f'- returncode: {r.get("returncode", r.get("error", "?"))}\n')
        f.write(f'- runId: {r.get("run_id", "N/A")}\n')
        f.write(f'- output: `{r.get("output", "")[:500]}`\n\n')

print('\n诊断报告: toolbox/non_channel_diagnose_v1.0.md')
