#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R-NEW-V2 revert: restore heartbeat-state.json to pre-my-modification state
(before hbCount=630 was written; original was hbCount=629)
"""
import json
from pathlib import Path

STATE_PATH = Path(r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json")

# Read current (post-my-modification) state
with open(STATE_PATH, 'r', encoding='utf-8') as f:
    cur = json.load(f)

# Build reverted state matching the pre-modification baseline
reverted = {
    "ericActiveElsewhere_h": 106.88,
    "silenceDuration_thisSession_h": 93.7,
    "hbCount": 629,
    "lastHB": 629,
    "nextCheck": "next: Token Guard cadence (~5-15min); evening self-iter 21:00 due (~9h52m)",
    "mode": "active_mode_dormant_this_session_silent_morning",
    "lastHBTime": "2026-07-20T11:09:45+08:00",
    "silenceDuration_h": 93.7,
    "lastChecks": cur.get("lastChecks", {
        "evening_self_iter_fired": "2026-07-19 21:00",
        "global_briefing": "2026-07-19 08:30",
        "heartbeat": "2026-07-20T11:03:00+08:00",
        "morning_self_iter": "2026-07-20 10:00",
        "daily_checkin": "2026-07-20 09:00",
        "daily_briefing": "2026-07-20 10:35",
        "evening_self_iter_due": "2026-07-20 21:00"
    }),
    "note": "HB #629; minimal tick (R012); Eric silent in this session ~93.7h; active in AnYi session ~106.88h; session DORMANT per HB #584/R256/R257/R258 stack; no push; induction window FINAL 2 DAYS (7/20, 7/21)"
}

# Guard: only revert if currently equals 630 (my modification)
if cur.get("hbCount") == 630:
    with open(STATE_PATH, 'w', encoding='utf-8') as f:
        json.dump(reverted, f, ensure_ascii=False, indent=2)
    print(f"OK: reverted heartbeat-state.json from hbCount=630 to hbCount=629")
else:
    print(f"SKIP: current hbCount={cur.get('hbCount')}, expected 630 to revert")
