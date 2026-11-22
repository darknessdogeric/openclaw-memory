import json, os, time
p = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
with open(p, 'r', encoding='utf-8') as f:
    s = json.load(f)
s['hbCount'] = s.get('hbCount', 3584) + 1
n = s['hbCount']
ts = '2026-08-20T17:23:00+08:00'
s['lastHbTime'] = ts
s['lastDecision'] = 'HEARTBEAT_OK'
s['last_check'] = ts
s['last_update_epoch'] = int(time.time())
s['workday_zone'] = 'weekday-late-afternoon'
s['posture'] = 'DORMANT'
s['cronSession'] = 'DORMANT'
s['last_hb'] = {'n': n, 'ts': ts}
s['notes'] = f'HB #{n} Thu 17:23 weekday-late-afternoon. cron DORMANT sustained. No new signal. Stay silent.'
tmp = p + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(s, f, ensure_ascii=False, indent=2)
os.replace(tmp, p)
print(f'ticked hbCount={n}')
