#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""find_cron_no_channel.py - 找出所有无 channel 的 cron 任务并批量 disable
Eric 2026-09-08 15:07 决策
"""
import sqlite3
import json
import subprocess
import sys

DB = r'C:\Users\ericz\.openclaw\state\openclaw.sqlite'

conn = sqlite3.connect(DB, timeout=10)
cur = conn.cursor()

# 找 cron job 表
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%job%'")
tables = [r[0] for r in cur.fetchall()]
print(f'Tables: {tables}')

if not tables:
    # Try another approach: look at all tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables_all = [r[0] for r in cur.fetchall()]
    print(f'All tables: {tables_all[:20]}')
    sys.exit(0)

t = tables[0]
cur.execute(f'SELECT COUNT(*) FROM "{t}"')
total = cur.fetchone()[0]
print(f'  {t} count: {total}')

# 查所有任务
cur.execute(f'SELECT id, name, delivery, enabled FROM "{t}" LIMIT 5')
samples = cur.fetchall()
for s in samples:
    print(f'  sample: id={s[0][:8]} name={s[1]} enabled={s[3]} delivery={s[2][:200] if s[2] else None}')

# 找 delivery = webchat 但无 channel 配置的任务
# 实际上 delivery 是 JSON 字符串
no_channel_jobs = []
cur.execute(f'SELECT id, name, delivery, enabled FROM "{t}" WHERE delivery LIKE "%webchat%" OR delivery LIKE "%last%"')
for r in cur.fetchall():
    if not r[2]:
        continue
    try:
        d = json.loads(r[2])
        # 检查 channel 配置
        intended = d.get('intended', {})
        channel = intended.get('channel', '')
        if not channel or channel == 'webchat':
            # 进一步检查 channel 配置
            resolved = d.get('resolved', {})
            err = resolved.get('error', '')
            if 'Channel is required' in err or 'no configured channels' in err:
                no_channel_jobs.append(r)
    except:
        pass

print(f'\n=== 找到 {len(no_channel_jobs)} 个无 channel 的 webchat 任务 ===\n')
for j in no_channel_jobs:
    print(f'  {j[0]} | {j[1]}')

conn.close()
