#!/usr/bin/env python3
"""HB #2296 state update — written to file to avoid shell escaping issues."""
import json
import datetime

PATH = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
EPOCH = int(NOW.timestamp())

with open(PATH, 'r', encoding='utf-8') as f:
    state = json.load(f)

prev_hb = state.get('lastHB')
prev_epoch = state.get('last_update_epoch')
prev_count = state.get('hbCount', 2295)
prev_null = state.get('nullCount', 912)

print(f'PREV: lastHB={prev_hb}, epoch={prev_epoch}, hbCount={prev_count}, nullCount={prev_null}')

hb_num = prev_count + 1
state['hbCount'] = hb_num
state['nullCount'] = prev_null + 1
state['last_update_epoch'] = EPOCH
state['lastHB'] = NOW.isoformat()
state['lastHBContext'] = (
    f'Wed 22:41 weekday-NIGHT-deep-quiet. DORMANT held. HB #{hb_num}. '
    f'Eric silent on BOTH cron + webchat (~17d 8h+ cron / webchat 5 sovereign bursts today '
    f'12:24/13:22/18:18/21:21/22:18 all absorbed silently via R264). '
    f'AnYi D+26d Wed. 18-layer suppression holds.'
)
state['posture'] = 'DORMANT'
state['zone'] = 'weekday-NIGHT-deep-quiet'

note_key = f'hb_{hb_num}_special'
state['notes'][note_key] = (
    'Wed weekday-NIGHT-deep-quiet +41m past 22:00 cap, AnYi D+26d Wed, '
    'AHL v3.0 + PPT13 (715 nodes + 82 TMC/RFP + market-segmentation) sustained, '
    '18-layer suppression holds, cadence 4min, '
    'Eric webchat 5 sovereign bursts today all absorbed silently, '
    'HEARTBEAT.md ~1.22MB sustained (file-state maintenance_flag awaiting Eric instruction), '
    'Eric night-owl complex-decision mode per USER.md, R69 Day 6/30 active'
)

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f'UPDATED: HB #{hb_num}, nullCount {state["nullCount"]}, epoch {EPOCH}')
print(f'lastHB: {state["lastHB"]}')
