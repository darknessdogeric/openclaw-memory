#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inspect_failed_cron_jobs.py - 看 2 个失败任务的具体定义
Eric 2026-09-08 15:09 决策
"""
import sqlite3, json

DB = r'C:\Users\ericz\.openclaw\state\openclaw.sqlite'

conn = sqlite3.connect(DB, timeout=10)
cur = conn.cursor()

failed_jobs = [
    ('9e176754-55aa-4017-bea0-51f62d4b70b6', 'heartbeat-main'),
    ('01679313-75d4-4ffa-8c99-ad1543869bc7', 'B166ER-每日本地备份-02点'),
]

for jid, expected_name in failed_jobs:
    cur.execute('SELECT name, job_json FROM cron_jobs WHERE job_id=?', (jid,))
    r = cur.fetchone()
    if not r:
        print(f'{jid[:8]}: NOT FOUND')
        continue
    name, j = r
    print(f'\n=== {name} ({jid[:8]}) ===')
    d = json.loads(j)
    # schedule
    print(f'  schedule: {d.get("schedule")}')
    # payload
    p = d.get('payload', {})
    print(f'  payload_kind: {d.get("payload_kind")}')
    print(f'  payload keys: {list(p.keys())}')
    for k, v in p.items():
        if isinstance(v, str) and len(v) > 300:
            v = v[:300] + '...'
        try:
            print(f'    {k}: {v}')
        except UnicodeEncodeError:
            print(f'    {k}: {repr(v)[:300]}')
    # timeout
    print(f'  timeout_ms: {d.get("timeout_ms")}')

conn.close()
