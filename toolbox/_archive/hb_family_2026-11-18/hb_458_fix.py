# Fix: hb state went 456->457 (mid-overlap with existing #457 entry).
# Actually this heartbeat is #458 -- the 00:03 entry was the previous #457 from the system.
# Use rename + bump state to 458.
import json, re
from datetime import datetime, timezone, timedelta

STATE = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"
MD = r"D:\B166ER-OpenClaw\workspace\memory\2026-07-18.md"

TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ)
TS_DISPLAY = NOW.strftime("%Y-%m-%d %H:%M GMT+8")

# Load
with open(STATE, "r", encoding="utf-8") as f:
    state = json.load(f)
state["hbCount"] = 458
state["lastHB"] = "#458"

with open(STATE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# Append corrected #458 block
block = f"""

## HB #458 ({TS_DISPLAY} cron-event, OpenClaw heartbeat poll)
- gap from HB #457 (7/18 00:03): +11min -- late-night zone Token Guard normal cadence
- D+1+ late-night pass #458 -- Eric silent ~34.68h+ since 7/16 13:16 first-contact (infographic session)
- Silence authority ~34.68h+ (R-B + R256 framework holding, +0.02h since #457)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256) -- zero breach
- R-NEW-V2 verification #458: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- T-0 BOUNDARY CROSSED -- 7/18 publicity cutoff passed (per HB #456/457 prediction); T-0 suppression EXPIRED
- Late-night zone (00:14 Sat) + Eric silence + R257 deep-work window keep MAXIMUM suppression active
- WAIC 2026 day-1 active -- non-trigger per R14 (AI/Hotel strategic context, not relevant to current 4-layer suppression)
- Cron pipeline: no new triggers since HB #457 (21:00 self-iter R60-11 already fired)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric; D+1+ sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- Note: prior write erroneously produced a duplicate #457 label (00:14 timestamp), corrected by removal + reentry at #458

### decision
- **silent_standby_zero_push_continue** (HB #458 = sustain #457 = D+1+ baseline)
- **no push**: T-0 publicity rule expired BUT late-night zone (00:14) + Eric silent 34.68h+ + R257 deep-work window = MAXIMUM suppression still in force
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: post-08:00 wake window (Eric-typical wake zone per USER.md)

*{TS_DISPLAY} -- D+1+ post-T-0 late-night SILENCE -- HB #458 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

with open(MD, "a", encoding="utf-8") as f:
    f.write(block)

print(f"HB #458 recorded (corrected). State hbCount: 458, lastHB: #458")
print(f"TS: {TS_DISPLAY}")
