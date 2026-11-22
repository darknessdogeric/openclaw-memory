#!/usr/bin/env python3
"""R-NEW-V5: state.json atomic-restore helper (avoid PowerShell ConvertTo-Json bug)."""
import json
import os
import sys

state = {
    'lastHb': '2026-08-14T15:14:00+08:00',
    'hbCount': 3208,
    'nullCount': 1770,
    'postT0NullSustained': True,
    'lastDecision': 'HEARTBEAT_OK -- HB #3208 = DORMANT -- cron sustained',
    'lastChannel': 'cron-event',
    'posture': 'DORMANT',
    'r69Day': 22,
    'r69Expiry': '2026-08-30',
    'anyiDay': 22,
    'anyiDayLabel': 'Fri -- second workweek Day 5',
    'webchatLastActivity': '2026-08-14T11:31:00+08:00',
    'webchatLastTopic': '十五五战略线定位研究 v0.1 push',
    'webchatIdleMin': 223,
    'hardCapZone': 'workday-PM',
    'minutesPastHardCap': 434,
    'quietZoneArrivalMin': 346,
    'suppressionsActive': [
        'R-B', 'R12', 'R-CANDIDATE-T2',
        'R256', 'R257', 'R258', 'R260', 'R261',
        'R65', 'R68', 'R69', 'R70', 'R71',
        'R-NEW-V3', 'R276', 'R271'
    ],
    'suppressionLayers': 16,
    'appendMethod': 'Python open(mode="a") UTF-8',
    'heartbeatMdTouched': True,
    'dailyFileAppended': True,
    'stateUpdate': 'atomic-via-tmp-move',
    'vaultFilesHealthy': 1169
}

tmp_path = r'D:\B166ER-OpenClaw\workspace\memory\state.json.tmp'
target_path = r'D:\B166ER-OpenClaw\workspace\memory\state.json'

with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=4)

size = os.path.getsize(tmp_path)
if size == 0:
    print('ABORT: tmp file empty', file=sys.stderr)
    sys.exit(1)

os.replace(tmp_path, target_path)
print(f'state.json restored: {os.path.getsize(target_path)} bytes')