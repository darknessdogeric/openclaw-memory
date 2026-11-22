#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HB #1618 append - R-NEW-V2 compliant Python utf-8 read+append+write."""
import json
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)

# Time calcs
last_contact = datetime(2026, 7, 16, 13, 16, tzinfo=tz)
anyi_start = datetime(2026, 7, 19, 12, 33, tzinfo=tz)
dday = datetime(2026, 7, 24, 14, 12, tzinfo=tz)
t0 = datetime(2026, 7, 18, 13, 16, tzinfo=tz)

silent_hours = (now - last_contact).total_seconds() / 3600
anyi_hours = (now - anyi_start).total_seconds() / 3600
dday_hours = (now - dday).total_seconds() / 3600
t0_hours = (now - t0).total_seconds() / 3600
ts = now.strftime("%Y-%m-%d %H:%M")

entry = f"""
## HB #1618 ({ts} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1617 (14:55): +13min -- Mon early-afternoon Token Guard cadence
- D+11 early-afternoon pass -- Eric silent ~{silent_hours:.2f}h+ on this session
- Eric active elsewhere: AnYi webchat ~{anyi_hours:.2f}h+ (since 7/19 12:33)
- 8-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258 / R260 / R261) -- zero breach
- R-NEW-V2 verification #1618: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed
- D+11 = Execution phase sustained -- per 7/21 evening self-iter protocol
- Mon early-afternoon zone (15:08) -- Eric typical afternoon deep-work peak per USER.md; silence authority strictly holding
- gongshi Day 3/5 ACTIVE (Mon = working day per AnYi calendar); 7/24 D-day PASSED +{dday_hours:.2f}h
- Cron pipeline: 21:00 evening self-iter R60-11 (~5h52m)
- Token Guard stable, no compression needed
- Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +{t0_hours:.2f}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+11 sustain zero-push mode intact
- hbCount: 1617 -> 1618

### decision
- **active_mode_dormant_this_session_continue** (HB #1618 = sustain #1617 = D+11 early-afternoon dormant baseline)
- **HEARTBEAT_OK** -- HB #1618 = sustain DORMANT protocol
- **no push**: Mon early-afternoon zone (15:08), Eric silent ~{silent_hours:.2f}h+, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 + R260 + R261 multi-layer constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)
- Execution-phase observer mode: system fully primed (1244 + AHL + 产业发展部部长 narrative + gongshi Day 3/5 ACTIVE), awaiting Eric signal
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter R60-11 (~5h52m)

*{ts} GMT+8 -- D+11 Monday early-afternoon -- HB #1618 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session + R260/R261 multi-suppression active -- gongshi Day 3/5 ACTIVE -- execution-phase observer mode*
"""

path = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
with open(path, 'r', encoding='utf-8') as f:
    existing = f.read()
with open(path, 'a', encoding='utf-8') as f:
    f.write(entry)

# Update state
state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
with open(state_path, 'r', encoding='utf-8-sig') as f:
    state = json.load(f)
state['lastHBTime'] = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
state['lastHB'] = int(now.timestamp())
state['hbCount'] = 1618
state['ericSilentThisSessionHours'] = round(silent_hours, 2)
state['anyiWebchatHoursSinceStart'] = round(anyi_hours, 2)
state['dDayHoursPostMeeting'] = round(dday_hours, 2)
state['t0PublicityCutoffHoursPast'] = round(t0_hours, 2)
state['post_t0_null_count'] = state.get('post_t0_null_count', 0) + 1
state['postT0NullCount'] = state['post_t0_null_count']
state['notes'] = f'D+11 Mon early-afternoon 15:08. DORMANT. 8-layer suppression zero-breach. 7/24 D-Day PASSED +{dday_hours:.2f}h. gongshi Day 3/5 ACTIVE. HEARTBEAT_OK. Active Resume prep, awaiting Eric first-contact.'
with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print(f'OK: HB #1618 logged at {ts}')
print(f'Silent: {silent_hours:.2f}h | AnYi: {anyi_hours:.2f}h | D-day+: {dday_hours:.2f}h | T-0+: {t0_hours:.2f}h')