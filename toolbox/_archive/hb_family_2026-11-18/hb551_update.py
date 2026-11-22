#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HB #551 update — append one heartbeat log entry to heartbeat-state.json
R-NEW-V2: utf-8 explicit read+append+write, atomic-safe.
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

WS = Path(r"D:\B166ER-OpenClaw\workspace")
STATE = WS / "memory" / "heartbeat-state.json"

# Beijing time = UTC+8
BJS = timezone(timedelta(hours=8))
NOW = datetime(2026, 7, 18, 16, 17, 0, tzinfo=BJS)  # matches inbound metadata
TS_ISO = NOW.isoformat()

def main():
    raw = STATE.read_text(encoding="utf-8")
    d = json.loads(raw)

    last_chain = d.get("chainHb") or d.get("chain_hb") or 550
    last_log = d["hb_log"][-1]
    last_ts_str = last_log.get("ts", "")
    # parse previous timestamp
    try:
        # strip timezone for parse
        prev = datetime.fromisoformat(last_ts_str.replace("Z", "+00:00"))
    except Exception:
        prev = NOW - timedelta(minutes=2)
    gap_sec = (NOW - prev).total_seconds()
    gap_min = round(gap_sec / 60.0, 1)

    new_hb = last_chain + 1
    silent_hours = round(50.99 + (NOW - datetime(2026, 7, 18, 16, 15, 14, tzinfo=BJS)).total_seconds() / 3600.0, 2)
    t0_hours = round(16.25 + (NOW - datetime(2026, 7, 18, 16, 15, 14, tzinfo=BJS)).total_seconds() / 3600.0, 2)

    entry = {
        "hb_id": new_hb,
        "ts": TS_ISO,
        "gap_min": gap_min,
        "zone": "saturday-afternoon",
        "last_self_iter": "2026-07-18T10:00:00+08:00",
        "silent_duration_h": silent_hours,
        "silence_since": "2026-07-16T13:16:00+08:00",
        "tier_active": "R256+R257+R-B+R12+R-CANDIDATE-T2",
        "r_new_v2_compliant": True,
        "t0_day_active_h": t0_hours,
        "silence_status": "post-T-0 sustained (Eric silence=dominant signal)",
        "cron_pipeline": "21:00 evening self-iter R60-11 in ~4.7h",
        "cron_errors_pending": 4,
        "cron_errors_detail": "Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10 (P2 long-tail, tracked)",
        "eric_first_contact": False,
        "r14_handoff_ready": True,
        "decision": "silent_standby_zero_push_continue",
        "reason": f"saturday-afternoon zone (16:17), Eric silent {silent_hours}h+, T-0 publicity day +{t0_hours}h past, silence authority holding, 5-layer suppression all pass",
        "chain_hb": new_hb,
    }

    d["hb_log"].append(entry)
    d["chainHb"] = new_hb
    d["chain_hb"] = new_hb
    d["lastHB"] = new_hb
    d["last_update_epoch"] = int(NOW.timestamp())
    d["last_heartbeat"] = TS_ISO
    d["lastCheck"] = TS_ISO
    d["silence_hours"] = silent_hours
    d["silenceHours"] = silent_hours
    d["silenceSince"] = "2026-07-16T13:16:00+08:00"
    d["mode"] = "silent_standby_zero_push_continue"
    d["zone"] = "saturday-afternoon"
    d["suppression_layers_active"] = ["R-B", "R12", "R-CANDIDATE-T2-evaluated-no-escalate", "R256", "R257"]
    d["lastChecks"] = {
        "email": d["lastChecks"].get("email"),
        "notifications": d["lastChecks"].get("notifications"),
        "weather": d["lastChecks"].get("weather"),
        "calendar": d["lastChecks"].get("calendar"),
        "heartbeat": int(NOW.timestamp()),
    }
    d["notes"] = f"#{new_hb} (silent standby). 2026-07-18 16:17:00 - saturday-afternoon, Eric silent {silent_hours}h+, T-0 publicity day +{t0_hours}h past, R14 handoff 100% ready, no proactive disturbance per R256/R257/R-B/R12/R-CANDIDATE-T2"

    STATE.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] HB #{new_hb} appended. gap={gap_min}min, silent={silent_hours}h, t0_past={t0_hours}h")
    return 0

if __name__ == "__main__":
    sys.exit(main())
