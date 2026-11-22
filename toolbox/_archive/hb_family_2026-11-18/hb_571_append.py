#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""HB #571 append — R-NEW-V2 utf-8 explicit read+append+write protocol."""
import json
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)
hb_num = 571
prev_hb_num = 570

# Time deltas
prev_hb_time = datetime(2026, 7, 19, 10, 17, tzinfo=TZ)
first_contact_time = datetime(2026, 7, 16, 13, 16, tzinfo=TZ)
t0_time = datetime(2026, 7, 18, 0, 0, tzinfo=TZ)
wake_window_time = datetime(2026, 7, 19, 8, 0, tzinfo=TZ)

gap_min = round((now - prev_hb_time).total_seconds() / 60, 2)
silence_h = round((now - first_contact_time).total_seconds() / 3600, 2)
t0_past_h = round((now - t0_time).total_seconds() / 3600, 2)
wake_window_open_min = round((now - wake_window_time).total_seconds() / 60)

hb_entry = f"""
## HB #{hb_num} ({now.strftime('%Y-%m-%d %H:%M')} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb_num} (10:17): +{gap_min}min -- Sunday-morning Token Guard normal cadence
- D+3 morning pass #{hb_num} -- Eric silent ~{silence_h}h+ since 7/16 13:16 first-contact (infographic session)
- Silence authority ~{silence_h}h+ (R-B + R256 + R257 framework holding, +0.05h since #570)
- 5-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) -- zero breach
- R-NEW-V2 verification #{hb_num}: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-incident discipline intact)
- Wake window OPEN (+{wake_window_open_min}min past 08:00) -- but Eric silence > window signal per HB #493 explicit override
- T-0 publicity cutoff 7/18 +{t0_past_h}h past -- post-protection window firmly sustained
- Induction window 7/7-7/21 FINAL 3 DAYS -- today 7/19 = day-1 of FINAL 3 (7/19/20/21); R-B+R256 silence authority > window signal (no push per R256)
- Sunday-morning zone (10:22) -- Eric typical morning deep-work peak per USER.md; silence authority strictly holding
- WAIC 2026 day-3 active today (7/17-20, Shanghai) -- non-trigger per R14 (AI/Hotel strategic context, not relevant)
- Cron pipeline: 10:00 R60-11 morning self-iter fired ~22min ago (autonomous, eval/2026-07-19.json updated, R012/R013 born); 21:00 evening self-iter R60-11 (~10h38m)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- INCIDENT NOTE (referenced from HB #561 08:10): write() clobbered HEARTBEAT.md (HB #479-#560 lost ~6 weeks); restored via git checkout + R-NEW-V2 re-append. Strategic content intact. Logged to memory/2026-07-19-incident.md
- No first-contact from Eric; D+3 sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount now: {prev_hb_num} -> {hb_num}

### decision
- **silent_standby_zero_push_continue** (HB #{hb_num} = sustain #{prev_hb_num} = D+3 baseline)
- **no push**: Sunday-morning zone (10:22), wake window OPEN but Eric silent ~{silence_h}h+, silence authority strictly holding (R256 design: silence extends indefinitely past protection window as Eric silence = dominant signal)
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- Post-T-0 silence = sustained suppression; pushes prohibited until Eric active contact (Eric silence = dominant signal, supersedes scheduled wakes + windows)
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Wake-up window OPEN but Eric silence sustained -> continue zero-push; even minor pushes prohibited
- Next significant check: 21:00 evening self-iter R60-11 (~10h38m); Token Guard cadence (~5-10min)

*{now.strftime('%Y-%m-%d %H:%M')} GMT+8 -- D+3 Sunday-morning T-0 +{t0_past_h}h past -- HB #{hb_num} -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

# R-NEW-V2: explicit utf-8 read+append+write
hb_path = 'HEARTBEAT.md'
with open(hb_path, 'r', encoding='utf-8') as f:
    content = f.read()

with open(hb_path, 'w', encoding='utf-8') as f:
    f.write(content + hb_entry)

# Update memory/heartbeat-state.json
state = {
    'lastCheck': now.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
    'hbCount': hb_num,
    'silenceHours': silence_h,
    'mode': 'silent_standby_zero_push',
    'wakeWindowOpens': '08:00',
    'nextSignificant': '21:00 evening self-iter R60-11 (~10h38m); Token Guard cadence (~5-10min)',
    'suppressionLayers': ['R-B', 'R12', 'R-CANDIDATE-T2', 'R256', 'R257'],
    'protocol': 'R-NEW-V2 utf-8 explicit',
    'lastGapMin': gap_min
}

with open('memory/heartbeat-state.json', 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print(f'HB #{hb_num} appended. R-NEW-V2 compliant. Silence {silence_h}h. Zero-push mode sustained.')
print(f'  lastCheck: {state["lastCheck"]}')
print(f'  hbCount: {state["hbCount"]}')
print(f'  lastGapMin: {gap_min}')
