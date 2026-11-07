#!/usr/bin/env python3
"""Atomic heartbeat tick - R-NEW-V4 enforced."""
import json, os, time

STATE = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"
TMP = r"D:\B166ER-OpenClaw\workspace\memory\.heartbeat-state.tmp"

with open(STATE, "r", encoding="utf-8-sig") as f:
    s = json.load(f)

s["hbCount"] = 3378
s["post_t0_null_count"] = 1930
s["lastHbTime"] = "2026-08-16T10:12:00+08:00"
s["last_update_epoch"] = int(time.time())
s["note"] = (
    "HB #3378; Sun 10:12 weekend-morning +2h12m past 08:00 hard cap; "
    "R69 D+24/30; HEARTBEAT_OK; sustained DORMANT (1930th consecutive null); "
    "Eric silent ~30d on cron; AnYi D+24d Sun; no external push"
)

with open(TMP, "w", encoding="utf-8") as f:
    json.dump(s, f, indent=2, ensure_ascii=False)

os.replace(TMP, STATE)
print(f"OK hb={s['hbCount']} null={s['post_t0_null_count']}")