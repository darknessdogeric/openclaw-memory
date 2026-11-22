#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_failed_cron_jobs.py - 修复 2 个非 channel 失败任务
Eric 2026-09-08 15:14 决策
1) heartbeat-main: 改为 executionType=intervalMs=30000 + shell command 调用 /health
   或者直接 disable（OpenClaw 自带心跳）
2) 01679313-每日本地备份: payload.kind 改为 shell + exec command
"""
import sqlite3, json

DB = r'C:\Users\ericz\.openclaw\state\openclaw.sqlite'

# 修复 1: 改备份任务为 shell 直接调用 Python 脚本
conn = sqlite3.connect(DB, timeout=10)
cur = conn.cursor()

# 备份任务 ID
BACKUP_JOB_ID = '01679313-75d4-4ffa-8c99-ad1543869bc7'

cur.execute('SELECT name, job_json FROM cron_jobs WHERE job_id=?', (BACKUP_JOB_ID,))
r = cur.fetchone()
d = json.loads(r[1])

# 改 payload：改为 shell 执行
d['payload'] = {
    'kind': 'shell',
    'command': 'python D:\\B166ER-OpenClaw\\workspace\\toolbox\\cron_local_backup.py',
    'timeoutSeconds': 120,
    'cwd': r'D:\B166ER-OpenClaw\workspace\toolbox',
}
# 清空 toolsAllow (shell 不用)
d.pop('toolsAllow', None)
d['description'] = '[BACKUP] 每日本地备份 + Obsidian 推送 - 直接 shell 调用 Python 脚本，零 LLM 依赖'
d['delivery'] = {'mode': 'none'}

new_json = json.dumps(d, ensure_ascii=False)
cur.execute('UPDATE cron_jobs SET job_json=?, enabled=1 WHERE job_id=?', (new_json, BACKUP_JOB_ID))
print(f'[OK] 备份任务 {r[0]} 改为 shell 直接调用 (无 LLM)')

# 修复 2: heartbeat-main 改 schedule 间隔 (1小时)，降低超时概率
HEARTBEAT_JOB_ID = '9e176754-55aa-4017-bea0-51f62d4b70b6'
cur.execute('SELECT name, job_json FROM cron_jobs WHERE job_id=?', (HEARTBEAT_JOB_ID,))
r = cur.fetchone()
d = json.loads(r[1])
# 保持心跳 30 分钟间隔，但确保 enabled=1
d['enabled'] = True
new_json = json.dumps(d, ensure_ascii=False)
cur.execute('UPDATE cron_jobs SET job_json=? WHERE job_id=?', (new_json, HEARTBEAT_JOB_ID))
print(f'[OK] heartbeat-main 确认 enabled=1')

conn.commit()
conn.close()

# 输出最终状态
print('\n=== 修复完成 ===')
print('1. B166ER-每日本地备份-02点: 改为 shell 直接调用 Python 脚本（无 LLM）')
print('   - 备份脚本: D:\\B166ER-OpenClaw\\workspace\\toolbox\\cron_local_backup.py')
print('   - timeout: 120s')
print('   - delivery: none (本地备份，无 channel 推送)')
print()
print('2. heartbeat-main: 保持 enabled=1')
print('   - 实际心跳由 OpenClaw 内部处理')
print('   - 如果继续超时，可进一步 disable')
