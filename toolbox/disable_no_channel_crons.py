#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""disable_no_channel_crons.py v2 - 用直接 SQL 改 enabled=0 (避免 subprocess 路径问题)
Eric 2026-09-08 15:07 决策
"""
import sqlite3
import json

DB = r'C:\Users\ericz\.openclaw\state\openclaw.sqlite'

conn = sqlite3.connect(DB, timeout=10)
cur = conn.cursor()

cur.execute("""
    SELECT store_key, job_id, name, job_json
    FROM cron_jobs
    WHERE enabled = 1
""")

rows = cur.fetchall()
no_channel = []

for r in rows:
    job_json = r[3]
    if not job_json:
        continue
    try:
        d = json.loads(job_json)
    except:
        continue
    delivery = d.get('delivery', {})
    intended = delivery.get('intended', {}) if isinstance(delivery, dict) else {}
    channel = intended.get('channel', '') if isinstance(intended, dict) else ''
    if not channel or channel == 'webchat' or channel == 'last':
        no_channel.append(r)

print(f'总启用任务: {len(rows)}')
print(f'无 channel 任务: {len(no_channel)}')

# 直接 SQL 改 enabled=0
disabled = 0
for j in no_channel:
    job_id = j[1]
    try:
        cur.execute('UPDATE cron_jobs SET enabled=0 WHERE job_id=?', (job_id,))
        disabled += 1
    except Exception as e:
        print(f'  ! ERR {j[2]}: {e}')

conn.commit()
conn.close()

print(f'\nDisabled (直接 SQL): {disabled}')

# 写清单
out = []
out.append('# Cron 任务清单 v1.0 (R296 修复 2026-09-08)\n\n')
out.append(f'- 总启用: {len(rows)}\n')
out.append(f'- 无 channel: {len(no_channel)} (已 disable)\n')
out.append(f'- 成功 disable: {disabled}\n\n')
out.append('## 33 个无 channel 任务列表 (已 disable)\n\n')
for j in no_channel:
    out.append(f'- {j[2]}\n')

with open(r'D:\B166ER-OpenClaw\workspace\toolbox\no_channel_crons_v1.0.md', 'w', encoding='utf-8') as f:
    f.writelines(out)
print(f'清单已保存到 toolbox/no_channel_crons_v1.0.md')
