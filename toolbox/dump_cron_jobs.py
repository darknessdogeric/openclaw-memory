import sqlite3, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB = r'C:\Users\ericz\.openclaw\state\openclaw.sqlite'
conn = sqlite3.connect(DB, timeout=10)
cur = conn.cursor()

# 1. heartbeat
cur.execute("SELECT job_json FROM cron_jobs WHERE job_id='9e176754-55aa-4017-bea0-51f62d4b70b6'")
d = json.loads(cur.fetchone()[0])
print('=== heartbeat-main ===')
print(json.dumps(d, ensure_ascii=False, indent=2))

# 2. 每日本地备份
cur.execute("SELECT job_json FROM cron_jobs WHERE job_id='01679313-75d4-4ffa-8c99-ad1543869bc7'")
d = json.loads(cur.fetchone()[0])
print('\n=== 每日本地备份 ===')
print(json.dumps(d, ensure_ascii=False, indent=2))

conn.close()
