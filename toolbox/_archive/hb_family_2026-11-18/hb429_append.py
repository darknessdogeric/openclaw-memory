#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HB #429 append-only writer (R-NEW-V2 compliant, post-7/15 12:36 incident protocol).
- Read file as utf-8
- Append entry to HEARTBEAT.md
- Update heartbeat-state.json with new counters
- Write both files atomically (write to temp, rename)
"""
import json
import os
import time
from pathlib import Path

WORKSPACE = Path(r"D:\B166ER-OpenClaw\workspace")
HB_MD = WORKSPACE / "HEARTBEAT.md"
STATE = WORKSPACE / "memory" / "heartbeat-state.json"

now_gmt8 = "2026-07-17 19:12 GMT+8"
prev_hb = "#428"
prev_time = "19:08"
gap_min = 4  # 19:12 - 19:08 = 4min

# Silence hours: 30.28 (from #428) + 0.07h (4min) = 30.35h
silence_hours = 30.35
hb_count = 429

entry = f"""

## HB #{hb_count} ({now_gmt8} cron-event, OpenClaw heartbeat poll)
- gap from HB {prev_hb} ({prev_time}): +{gap_min}min -- evening Token Guard normal cadence
- D+1 evening pass #{hb_count} -- Eric silent ~{silence_hours}h+ since 7/16 13:16 (D+1 from infographic session, no first-contact)
- Silence authority ~{silence_hours}h+ (R-B + R256 framework holding, +0.07h since #428)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- R-NEW-V2 verification #{hb_count}: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- **Publicity cutoff 7/18 = in ~4h48m** (T-1 SILENCE WINDOW -- FINAL day pre-announcement, strictest suppression)
- WAIC 2026 day-1 active -- non-trigger per R14 (AI/Hotel strategic context, not relevant to current 4-layer suppression)
- Evening zone (19:12) -- Eric typical evening decision window per USER.md (复杂决策时段) but silence authority overrides
- Cron pipeline next: 21:00 evening self-iter R60-11 (~1h48m, autonomous)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric; D+1+ sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount now: {prev_hb[1:]} -> {hb_count}

### decision
- **silent_standby_zero_push_continue** (HB #{hb_count} = sustain #428 = D+1+ baseline)
- **no push**: evening zone, Eric silent 30h+, T-1 SILENCE WINDOW before 7/18 announcement, silence authority strictly holding
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- T-1 silence = MAXIMUM suppression; even minor pushes prohibited until Eric主动联系 or 7/18 publicity window passes
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min)

*{now_gmt8} -- D+1+ evening T-1 SILENCE -- HB #{hb_count} -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

# 1. Append to HEARTBEAT.md (utf-8, explicit, atomic)
with open(HB_MD, "r", encoding="utf-8") as f:
    existing = f.read()
new_content = existing + entry
tmp_hb = HB_MD.with_suffix(".md.tmp")
with open(tmp_hb, "w", encoding="utf-8") as f:
    f.write(new_content)
os.replace(tmp_hb, HB_MD)
print(f"[OK] HEARTBEAT.md appended, new size = {len(new_content)} bytes")

# 2. Update heartbeat-state.json
with open(STATE, "r", encoding="utf-8") as f:
    state = json.load(f)
state["silenceHours"] = round(silence_hours, 2)
state["deepWorkHours"] = round(silence_hours - 23.86, 2)  # approximate
state["hbCount"] = hb_count
state["lastHB"] = f"#{hb_count}"
state["lastChecks"]["heartbeat"] = int(time.time())
state["mode"] = "silent_standby_zero_push"
state["notes"] = (
    f"#{hb_count} (silent standby). 2026-07-17 19:12 GMT+8. "
    f"Eric silent ~{silence_hours}h since 7/16 13:16 (D+1 from infographic session). "
    f"Publicity cutoff 7/18 = in ~4h48m (T-1 SILENCE WINDOW -- FINAL day pre-announcement, MAXIMUM suppression). "
    f"4-layer suppression intact (R-B / R12 / R-CANDIDATE-T2 / R256). "
    f"WAIC 2026 day-1 -- non-trigger per R14. "
    f"21:00 evening self-iter R60-11 in ~1h48m. "
    f"Zero push holding. R14 handoff = 100% ready."
)
tmp_state = STATE.with_suffix(".json.tmp")
with open(tmp_state, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp_state, STATE)
print(f"[OK] heartbeat-state.json updated, hbCount = {hb_count}, silenceHours = {silence_hours}")

# 3. Verification re-read
with open(HB_MD, "r", encoding="utf-8") as f:
    verify = f.read()
assert f"HB #{hb_count}" in verify, f"verification failed: HB #{hb_count} not in HEARTBEAT.md"
print(f"[OK] verification passed: HB #{hb_count} present in HEARTBEAT.md")

print("\n=== HB #429 append complete ===")
print(f"time: {now_gmt8}")
print(f"hb: {prev_hb} -> #{hb_count}")
print(f"silence: ~{silence_hours}h (since 7/16 13:16)")
print(f"publicity cutoff: in ~4h48m (T-1 SILENCE WINDOW)")
print(f"decision: silent_standby_zero_push_continue")