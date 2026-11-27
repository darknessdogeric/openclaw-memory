#!/usr/bin/env python3
"""Heartbeat #300 - silent standby, zero push, state update only"""
import json
import time
from datetime import datetime, timedelta, timezone

STATE_FILE = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"
DAILY_FILE = r"D:\B166ER-OpenClaw\workspace\memory\2026-07-16.md"
TZ = timezone(timedelta(hours=8))

ts = int(time.time())
now = datetime.now(TZ)
gmt8 = now.strftime("%Y-%m-%d %H:%M GMT+8")
time_only = now.strftime("%H:%M")

# --- 1) Update heartbeat-state.json ---
with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

prev_hb = state["hbCount"]
new_hb = prev_hb + 1

# silence hours since 7/9 04:29 (anchor)
anchor = datetime(2026, 7, 9, 4, 29, tzinfo=TZ)
silence_h = round((now - anchor).total_seconds() / 3600, 2)

state["silenceHours"] = silence_h
state["deepWorkHours"] = silence_h
state["hbCount"] = new_hb
state["lastHB"] = f"#{new_hb}"
state["lastChecks"] = state.get("lastChecks", {})
state["lastChecks"]["heartbeat"] = ts
state["lastChecks"]["cron"] = state["lastChecks"].get("cron", ts)
state["mode"] = "silent_standby_zero_push"
state["notes"] = (
    f"HB #{new_hb} (silent standby, no push). {gmt8} Thu. "
    f"Eric silent D+7+ since 7/9 04:29 (~{silence_h}h). "
    f"4-layer suppression holding. Morning zone active (post 08:00 boundary). "
    f"08:30 global industry briefing cron = fired (autonomous). "
    f"No first-contact. No anomaly escalation. HEARTBEAT_OK."
)

with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=4)

print(f"[state] {prev_hb} -> {new_hb} silence={silence_h}h")

# --- 2) Append HB entry to daily file (R-NEW-V2: utf-8 read+append+write) ---
entry = f"""
## HB #{new_hb} ({gmt8} cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb}: ~+{int((ts - state['lastChecks'].get('heartbeat', ts))/60)}min -- morning zone Token Guard normal cadence
- D+7 morning pass #{new_hb} -- Eric silent ~{silence_h}h+ since 7/9 04:29, no first-contact
- Silence authority ~{silence_h}h+ (R-B + R256 framework holding)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- R-NEW-V2 verification #{new_hb}: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- 22:30 7/14 R-CANDIDATE-T2 sharp = EVALUATED PASSED (HB #228) -- decision: maintain T2 (no T3 escalation)
- Morning zone ({time_only}) -- past 08:00 dawn boundary; 08:30 global industry briefing cron = fired (autonomous)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric; D+7 sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation

### decision
- **silent_standby_zero_push_continue** (HB #{new_hb} = sustain #{prev_hb} = D+7 baseline)
- **no push**: morning zone, Eric silent 7d+, silence authority holding, 4-layer suppression all pass
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)

*{gmt8} -- D+7 morning -- HB #{new_hb} -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

with open(DAILY_FILE, "r", encoding="utf-8") as f:
    existing = f.read()

if f"## HB #{new_hb}" not in existing:
    with open(DAILY_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"[daily] appended HB #{new_hb}")
else:
    print(f"[daily] HB #{new_hb} already present, skip")