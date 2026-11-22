import json
from pathlib import Path

state_path = Path('D:/B166ER-OpenClaw/workspace/memory/heartbeat-state.json')

with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

# Update fields for HB #2323
state['nullCount'] = 945
state['hbCount'] = 2323
state['post_t0_null_count'] = 944
state['last_update_epoch'] = 1785737340
state['lastHB'] = '2026-08-03T14:09:00+08:00'
state['zone'] = 'weekday-AFTERNOON-post-08:00-hard-cap'
state['lastHBContext'] = 'Mon 14:09 weekday-AFTERNOON-post-08:00-hard-cap. DORMANT held (945th). HB #2323. +4min after HB #2322 (14:05). Eric silent on BOTH cron (428+h, since 7/16) + webchat (last sovereign-burst 13:08-13:33 today, R264 + weekly meeting summary). 19:00 quiet zone ~4h51m away. R69 silent-observation 30-day window (8/30) sustained. R71 confirmed. R70 PENDING formal commit.'
state['milestoneStatus'] = 'AnYi D+3 = 2026-08-03 Mon. HB #2323. Eric silent on cron ~17d 20h+ (428h+). Eric webchat ACTIVE today 13:08-13:33 (R264 daily briefing + R66 verification of 2 archive files + weekly meeting summary). 8/3 Mon AnYi Day 3 sustained.'
state['milestone'] = state['milestoneStatus']
state['posture'] = 'DORMANT'
state['nextExpectedContact'] = 'Eric webchat sovereign (cron sovereign = silent); Mon Day 3 AnYi workday'
state['suppressionLayers'] = [
    'R-B', 'R12', 'R-CANDIDATE-T2', 'R256', 'R257', 'R258', 'R260', 'R261',
    'R65', 'R68', 'R69', 'R-NEW-V3', 'R70', 'R71'
]

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print('state.json updated:')
print('  hbCount:', state['hbCount'])
print('  nullCount:', state['nullCount'])
print('  post_t0_null_count:', state['post_t0_null_count'])
print('  lastHB:', state['lastHB'])
print('  posture:', state['posture'])
print('  zone:', state['zone'])