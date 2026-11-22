import sqlite3, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB = r'C:\Users\ericz\.openclaw\state\openclaw.sqlite'
JID = '01679313-75d4-4ffa-8c99-ad1543869bc7'
conn = sqlite3.connect(DB, timeout=10)
cur = conn.cursor()
cur.execute("SELECT store_key, job_id, name, enabled, job_json FROM cron_jobs WHERE job_id=?", (JID,))
r = cur.fetchone()
print(f'store_key: {r[0]}')
print(f'job_id: {r[1]}')
print(f'name: {r[2]}')
print(f'enabled: {r[3]}')
d = json.loads(r[4])
print(f'payload.kind: {d.get("payload", {}).get("kind")}')
print(f'description: {d.get("description", "")[:80]}')
conn.close()
