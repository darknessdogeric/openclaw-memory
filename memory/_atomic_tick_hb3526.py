import json, os
p = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
s = json.load(open(p, encoding='utf-8'))
s['hbCount'] = 3526
s['lastHBCount'] = 3526
s['last_hb'] = {'n': 3526, 'ts': '2026-08-19T20:43:00+08:00'}
s['lastTick'] = '2026-08-19T20:43:00+08:00'
s['lastHbTime'] = '2026-08-19T20:43:00+08:00'
s['lastHBTime'] = '2026-08-19T20:43:00+08:00'
s['lastHeartbeat'] = '2026-08-19T20:43:00+08:00'
s['lastHB'] = '2026-08-19T20:43:00+08:00'
s['lastDecision'] = 'HEARTBEAT_OK'
s['note'] = 'HB #3526 Wed 20:43 + qixi -- DORMANT sustained; Eric webchat sovereign (idle ~25h37m); Jinjiang MOU Day 1 P0 Eric sovereign; R69 Day 27/30; quiet per R65/R258/R69/R277/R282'
tmp = p + '.tmp'
json.dump(s, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
os.replace(tmp, p)
print('atomic-tick OK hb=3526')
