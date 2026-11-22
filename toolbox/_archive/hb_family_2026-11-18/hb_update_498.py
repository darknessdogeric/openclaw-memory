"""HB #498 update — 2026-07-19 03:28 GMT+8"""
import json
from datetime import datetime
from pathlib import Path

state_path = Path(r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json')
state = json.loads(state_path.read_text(encoding='utf-8'))

now_ts = int(datetime(2026, 7, 19, 3, 28).timestamp())
state['lastHBTime'] = '2026-07-19 03:28:00 GMT+8'
state['lastHBNumber'] = 498
state['lastHbTs'] = now_ts
state['silenceHours'] = 62.20
state['t0HoursPast'] = 27.47
state['lastDecision'] = (
    'HB #498: deep-night Sunday 2026-07-19 03:28, +30min after HB #497, '
    'Eric silent ~62.2h, T-0+27.47h, no signals, all layers intact -> '
    'silent_standby sustained (no change)'
)
state['cronPipeline']['errorsPending'] = 4
state['cronPipeline']['next'] = (
    '03:00 Memory Dreaming Promotion (~-32min, due imminent), '
    '09:00 daily checkin (~5h32m)'
)

state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')
print('heartbeat-state.json updated to HB #498')
print('gap: +30min from #497; Eric silent 62.2h')