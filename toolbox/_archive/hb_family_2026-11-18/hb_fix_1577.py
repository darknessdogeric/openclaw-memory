#!/usr/bin/env python3
"""Fix HB count to 1577 (state.json was lagging vs HEARTBEAT.md)"""
import json

with open('memory/heartbeat-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

# HB #1577 = current tick at 08:29; HB #1576 was at 08:24 (in HEARTBEAT.md)
# state.json was at 1575 before this update; this update should bring it to 1577
state['hbCount'] = 1577
state['postT0NullCount'] = 228

notes = 'D+11 Mon morning 08:29. DORMANT. 8-layer. Triple Confluence ALL CLOSED. 7/24 D-Day PASSED +68h. HEARTBEAT_OK. HB #1577.'
state['notes'] = notes

with open('memory/heartbeat-state.json', 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print('Fixed to HB #1577')
print('  hbCount:', state['hbCount'])
print('  post_t0_null_count:', state['postT0NullCount'])
print('  notes:', state['notes'])
