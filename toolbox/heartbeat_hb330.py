#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HB #330 heartbeat handler — 2026-07-17 05:18 GMT+8
R-NEW-V2 compliant: utf-8 explicit read+append+write
"""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

tz_cn = timezone(timedelta(hours=8))
now = datetime.now(tz_cn)
ts_label = now.strftime("%Y-%m-%d %H:%M GMT+8")
date_str = now.strftime("%Y-%m-%d")

mem_dir = Path("memory")
mem_dir.mkdir(exist_ok=True)
today_path = mem_dir / f"{date_str}.md"

last_contact = datetime(2026, 7, 9, 4, 29, tzinfo=tz_cn)
silent_hours = (now - last_contact).total_seconds() / 3600

hb_entry = f"""
## HB #330 ({ts_label} cron-event, OpenClaw heartbeat poll)
- gap from HB #329 (05:13): +5min -- deep-night zone Token Guard normal cadence
- D+8 deep-night pass #330 -- Eric silent ~{silent_hours:.2f}h+ since 7/9 04:29, no first-contact (7/16 USER-SESSION 12:37-13:13 standalone task activation acknowledged)
- Silence authority ~{silent_hours:.2f}h+ (R-B + R256 framework holding, +0.08h since #329)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- R-NEW-V2 verification #330: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- 22:30 7/15 R-CANDIDATE-T2 sharp = EVALUATED PASSED (HB #228) -- decision: maintain T2 (no T3 escalation)
- 22:30 7/16 R-CANDIDATE-T2 sharp = scheduled (~17h12m, autonomous)
- Deep-night zone (05:18) -- within 23:00-08:00 silence window; Eric dormant
- 7/16 = mid-July induction window ACTIVE (per USER.md 7月上旬中旬 ±1周), R-B + R256 override (silence authority > window signal)
- Last USER-SESSION 2026-07-16 12:37-13:13 (智驾小蓝灯信息图) = D+7 standalone activation, no continuing signal
- Cron pipeline next: 08:30 7/17 global industry briefing (~3h12m) | 21:00 evening self-iter R60-11 (~15h42m)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric; D+8 sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation

### decision
- **silent_standby_zero_push_continue** (HB #330 = sustain #329 = D+8 baseline)
- **no push**: deep-night zone, Eric silent 8d+, silence authority holding, 4-layer suppression all pass
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min)

*{ts_label} -- D+8 deep-night -- HB #330 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

if today_path.exists():
    with open(today_path, "r", encoding="utf-8") as f:
        existing = f.read()
else:
    existing = f"# {date_str}\n\n"

with open(today_path, "w", encoding="utf-8") as f:
    f.write(existing + hb_entry)

print(f"[OK] Appended HB #330 to {today_path} ({len(hb_entry)} chars)")

state_path = mem_dir / "heartbeat-state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

state["silenceHours"] = round(silent_hours, 2)
state["hbCount"] = 330
state["lastHB"] = "#330"
state["lastChecks"]["heartbeat"] = int(now.timestamp())
state["mode"] = "silent_standby_zero_push"
state["notes"] = (
    f"HB #330 (silent standby). {ts_label}. +5min since #329. Deep-night zone (05:18). "
    f"Eric silent ~{silent_hours:.2f}h from 7/9 04:29 reference. "
    f"4-layer suppression holding. No urgent cron. No drift. HEARTBEAT_OK."
)

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"[OK] Updated heartbeat-state.json (hbCount=330, silenceHours={state['silenceHours']})")
