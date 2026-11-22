#!/usr/bin/env python3
"""HB #555 tick - update heartbeat state + memory log (R-NEW-V2 compliant)."""
import json
from datetime import datetime, timezone, timedelta

NOW = datetime(2026, 7, 18, 17, 12, 0, tzinfo=timezone(timedelta(hours=8)))
SILENCE_SINCE = datetime(2026, 7, 16, 13, 16, 0, tzinfo=timezone(timedelta(hours=8)))
T0_ANCHOR = datetime(2026, 7, 18, 0, 0, 0, tzinfo=timezone(timedelta(hours=8)))

silent_h = round((NOW - SILENCE_SINCE).total_seconds() / 3600, 2)
t0_h = round((NOW - T0_ANCHOR).total_seconds() / 3600, 2)

hb_entry = {
    "hb_id": 555,
    "ts": NOW.isoformat(timespec="seconds"),
    "gap_min": 5,
    "zone": "saturday-afternoon-late",
    "last_self_iter": "2026-07-18T10:00:00+08:00",
    "silent_duration_h": silent_h,
    "silence_since": "2026-07-16T13:16:00+08:00",
    "tier_active": "R256+R257+R-B+R12+R-CANDIDATE-T2",
    "r_new_v2_compliant": True,
    "t0_day_active_h": t0_h,
    "silence_status": "post-T-0 sustained (Eric silence=dominant signal)",
    "cron_pipeline": "21:00 evening self-iter R60-11 in ~3h48m",
    "cron_errors_pending": 4,
    "cron_errors_detail": "Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10 (P2 long-tail, tracked)",
    "eric_first_contact": False,
    "r14_handoff_ready": True,
    "decision": "silent_standby_zero_push_continue",
    "reason": (
        "saturday-afternoon-late zone (17:12), Eric silent " + str(silent_h)
        + "h+, T-0 publicity day +" + str(t0_h)
        + "h past, silence authority holding, 5-layer suppression all pass"
    ),
}

state_path = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

# Load (utf-8-sig strips any existing BOM for robust read)
with open(state_path, "r", encoding="utf-8-sig") as f:
    state = json.load(f)

# Update top-level
state["last_heartbeat"] = NOW.isoformat(timespec="seconds")
state["lastCheck"] = NOW.isoformat(timespec="seconds")
state["silence_hours"] = silent_h
state["silenceHours"] = silent_h
state["silenceSince"] = "2026-07-16T13:16:00+08:00"
state["lastHB"] = 555
state["chainHb"] = 555
state["chain_hb"] = 555
state["zone"] = "saturday-afternoon-late"
state["mode"] = "silent_standby_zero_push_continue"
state["notes"] = (
    "#555 (silent standby). 2026-07-18 17:12 GMT+8 - saturday-afternoon-late, "
    "Eric silent " + str(silent_h) + "h+, T-0 publicity day +" + str(t0_h)
    + "h past, R14 handoff 100% ready, no proactive disturbance per R256/R257/R-B/R12/R-CANDIDATE-T2"
)

# Append
state["hb_log"].append(hb_entry)

# Write back R-NEW-V2 style (explicit utf-8, no BOM)
with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print("BOM_STRIPPED -> utf-8 no-BOM canonical")

print("STATE_OK HB=555 silent_h=" + str(silent_h) + " t0_h=" + str(t0_h))
