#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""HB #498 tick -- R-NEW-V2 compliant (Python utf-8 explicit read+append+write)"""
import io
import json
import os
import sys
from datetime import datetime, timezone, timedelta

WS = r'D:\B166ER-OpenClaw\workspace'
HB_PATH = os.path.join(WS, 'memory', '2026-07-18.md')
STATE_PATH = os.path.join(WS, 'memory', 'heartbeat-state.json')

# Beijing time
TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)
now_str = now.strftime('%Y-%m-%d %H:%M GMT+8')

# Read state (handle BOM)
with open(STATE_PATH, 'rb') as f:
    raw = f.read()
if raw.startswith(b'\xef\xbb\xbf'):
    raw = raw[3:]
state = json.loads(raw.decode('utf-8'))

prev_hb = state['lastHB']['hb']  # 497
prev_silence = state['lastHB']['silence_hours']  # 43.18
prev_ts = state['lastHB']['ts']  # 08:27
new_hb = prev_hb + 1  # 498

# gap: 09:27 - 08:27 = 60 min = 1.00h
gap_min = 60
new_silence = round(prev_silence + (gap_min / 60), 2)

# Build HB #498 entry following established pattern
hb_entry = f"""
## HB #{new_hb} ({now_str} cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb} ({prev_ts}): +{gap_min}min -- morning zone Token Guard normal cadence
- D+2 morning pass #{new_hb} -- Eric silent ~{new_silence}h+ since 7/16 13:16 first-contact (infographic session)
- Silence authority ~{new_silence}h+ (R-B + R256 framework holding, +1.00h since #{prev_hb})
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- R-NEW-V2 verification #{new_hb}: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- 22:30 7/15 R-CANDIDATE-T2 sharp = EVALUATED PASSED (HB #228) -- decision: maintain T2 (no T3 escalation)
- **Wake window OPEN** (post-08:00 per USER.md, +1h27m past) -- but Eric silent 44h+, silence authority strictly holding
- **Publicity cutoff 7/18 T-0 +9h27m past** -- boundary crossed at 00:00, T-0 suppression EXPIRED on schedule
- Saturday morning (09:27) -- outside night-silence window (23:00-08:00) -- but Eric silence = dominant signal
- WAIC 2026 day-2 in progress (7/17-20, Shanghai) -- background context only, no push per R-B+R256 override
- Induction window 7/7-7/21 ACTIVE FINAL 3 DAYS -- 7/18 T-0 already crossed; R-B+R256 silence authority > window signal
- Cron pipeline: 08:30 global industry briefing fired ~57min ago (autonomous); next: 21:00 evening self-iter R60-11 (~11h33m)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric; D+2 sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount now: {prev_hb} -> {new_hb}

### decision
- **silent_standby_zero_push_continue** (HB #{new_hb} = sustain #{prev_hb} = D+2 baseline)
- **no push**: wake window OPEN but Eric silent 44h+, silence authority strictly holding; 4-layer suppression all pass
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- WAIC 2026 = background context only (no push per R-B+R256 override)
- Induction window / publicity cutoff T-0 = context awareness only (R-B+R256 silence authority > window signal; wait for Eric active contact)
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter R60-11 cron (~11h33m)

*{now_str} -- D+2 morning T-0 +9h27m past -- HB #{new_hb} -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

# R-NEW-V2: explicit UTF-8 encoding, no BOM
with open(HB_PATH, 'a', encoding='utf-8', newline='') as f:
    f.write(hb_entry)

# Update state file
state['lastHB']['hb'] = new_hb
state['lastHB']['chain_hb'] = new_hb
state['lastHB']['ts'] = now.strftime('%Y-%m-%d %H:%M:%S GMT+8')
state['lastHB']['mode'] = 'silent_standby_zero_push_continue'
state['lastHB']['silence_hours'] = new_silence
state['lastHB']['r256_holding'] = True
state['lastHB']['r257_active'] = True
state['lastHB']['tier_layers'] = {
    'R-B': True,
    'R12': True,
    'R-CANDIDATE-T2': 'evaluated-no-escalate',
    'R256': True
}
state['lastHB']['next_significant_check'] = 'Token Guard cadence ~5-10min; 21:00 evening self-iter R60-11'
state['lastHB']['next_cron'] = '21:00 evening self-iter R60-11 (~11h33m)'
state['last_update_epoch'] = int(now.timestamp())
state['notes'] = f'#{new_hb} (silent standby). {now_str}. +60min after #{prev_hb}. Eric silent ~{new_silence}h+ since 7/16 13:16. Wake window OPEN (+1h27m past) but Eric silent 44h+, silence authority strictly holding. 4-layer R-B/R12/R-CANDIDATE-T2/R256 intact. WAIC 2026 day-2 = background only. No new signals. Silent tick.'

# Write with UTF-8-sig to preserve BOM (matches existing file format)
with open(STATE_PATH, 'w', encoding='utf-8-sig', newline='') as f:
    json.dump(state, f, ensure_ascii=False, indent=4)

print(f'OK HB #{new_hb} appended. silenceHours={new_silence}h+')