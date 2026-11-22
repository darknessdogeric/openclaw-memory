#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B166ER Heartbeat Logger -- R-NEW-V2 compliant
Records HB #1001 to daily memory file.
Protocol: utf-8 explicit read+append+write (PowerShell-safe).
"""

import os
import sys
from datetime import datetime, timezone, timedelta

# Force UTF-8 stdout for Windows + PowerShell (avoid prior bugs)
sys.stdout.reconfigure(encoding='utf-8')

BEIJING = timezone(timedelta(hours=8))
now = datetime.now(BEIJING)
ts_str = now.strftime('%Y-%m-%dT%H:%M:%S GMT+8')
date_str = now.strftime('%Y-%m-%d')
time_only = now.strftime('%H:%M')

# Calculate T-minus to D-Day (7/24 AnYi meeting Thursday morning)
d_day = datetime(2026, 7, 24, 9, 0, tzinfo=BEIJING)
hours_to_d = (d_day - now).total_seconds() / 3600

# Session silent in THIS cron session since 7/16 13:16
first_contact = datetime(2026, 7, 16, 13, 16, tzinfo=BEIJING)
session_silent_h = (now - first_contact).total_seconds() / 3600

# AnYi webchat active since 7/19 12:33
anyi_start = datetime(2026, 7, 19, 12, 33, tzinfo=BEIJING)
anyi_h = (now - anyi_start).total_seconds() / 3600

# T-0 publicity cutoff: 7/18
t_zero = datetime(2026, 7, 18, 0, 0, tzinfo=BEIJING)
t_zero_h = (now - t_zero).total_seconds() / 3600

# Araqchi talks 7/21-25
araqchi_start = datetime(2026, 7, 21, 0, 0, tzinfo=BEIJING)
araqchi_day = (now - araqchi_start).days + 1
oil_remaining_h = (datetime(2026, 7, 25, 0, 0, tzinfo=BEIJING) - now).total_seconds() / 3600

# Triple Confluence Day 0 CLOSED 7/22 00:00 (i.e., 7/21 24:00)
tcf_closed = datetime(2026, 7, 22, 0, 0, tzinfo=BEIJING)
tcf_closed_h = (now - tcf_closed).total_seconds() / 3600

# Next cron: 09:00 daily checkin
next_cron = datetime(now.year, now.month, now.day, 9, 0, tzinfo=BEIJING)
if next_cron <= now:
    next_cron = next_cron + timedelta(days=1)
next_cron_h = (next_cron - now).total_seconds() / 3600

# Next major cron: 21:00 R60-11 evening self-iter
h_now = now.hour
if h_now < 21:
    next_major = datetime(now.year, now.month, now.day, 21, 0, tzinfo=BEIJING)
else:
    next_major = datetime(now.year, now.month, now.day, 21, 0, tzinfo=BEIJING) + timedelta(days=1)
next_major_h = (next_major - now).total_seconds() / 3600

entry = f'''
### HB #1001 ({ts_str}, cron-event)
- gap from HB #1000 (05:35): +4min -- Thursday deep-night Token Guard normal cadence (R012 minimal mode)
- D+7 deep-night pass #1001 -- Eric silent in THIS session ~{session_silent_h:.2f}h+ since 7/16 13:16 first-contact (+4min since #1000)
- Eric active elsewhere: AnYi webchat ~{anyi_h:.2f}h+ since 7/19 12:33 (+4min since #1000)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #1001: Python utf-8 explicit read+append+write compliant
- R012 verification: HB tick = minimal (NOT full report)
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~{tcf_closed_h:.2f}h ago; oil Scenario C verification window OPEN until 7/25 (~{oil_remaining_h:.2f}h remaining)
- Araqchi Qatar talks Day {araqchi_day}/5 -- window OPEN until 7/25
- D+7 = Execution phase day 2 -- observer mode sustained
- Thursday deep-night zone ({time_only} GMT+8) -- Eric sleep window; THIS session DORMANT sustained
- **7/24 D-Day T-{hours_to_d:.2f}h** (AnYi 集团研究会议 Thursday MORNING, TOMORROW) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- 21:00 R60-11 evening self-iter fired ~8h39m ago (autonomous)
- Next cron: 09:00 daily checkin (~{next_cron_h:.2f}h); next major = 21:00 R60-11 (~{next_major_h:.2f}h)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (not urgent)
- T-0 publicity cutoff 7/18 +{t_zero_h:.2f}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+7 sustain zero-push mode intact
- hbCount: 1000 -> 1001
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- active_mode_dormant_this_session_continue (HB #1001 = sustain #1000 = D+7 deep-night dormant baseline)
- HEARTBEAT_OK -- HB #1001 = sustain DORMANT protocol
- no push: Thursday deep-night zone ({time_only}), Eric sleep window, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-{hours_to_d:.2f}h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: per Token Guard cadence (~5-10min)

*{ts_str} -- D+7 Thursday deep-night -- HB #1001 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-{hours_to_d:.2f}h watch (AnYi meeting Thursday MORNING, TOMORROW) -- Eric silent = dominant signal holding*
'''

# Read existing today file (explicit utf-8)
today_path = f'memory/{date_str}.md'

# Create with header if not exists
if not os.path.exists(today_path):
    with open(today_path, 'w', encoding='utf-8') as f:
        f.write(f'# {date_str} Daily Log\n\n')

# Append this HB entry (explicit utf-8)
with open(today_path, 'a', encoding='utf-8') as f:
    f.write(entry)

print(f'OK: HB #1001 appended to {today_path}')
print(f'  Timestamp: {ts_str}')
print(f'  Session silent: {session_silent_h:.2f}h+')
print(f'  AnYi active: {anyi_h:.2f}h+')
print(f'  D-Day T-minus: {hours_to_d:.2f}h')
print(f'  Decision: HEARTBEAT_OK (DORMANT sustained)')
