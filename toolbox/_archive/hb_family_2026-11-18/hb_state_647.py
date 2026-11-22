# -*- coding: utf-8 -*-
"""R-NEW-V2 compliant heartbeat-state.json update for HB #647."""
import json
from pathlib import Path

state = {
    "ericActiveElsewhere_h": 24.76,
    "silenceDuration_thisSession_h": 96.21,
    "hbCount": 647,
    "lastHB": 647,
    "nextCheck": "next: Token Guard cadence (~5-15min); evening self-iter 21:00 due (~7h32m)",
    "mode": "active_mode_dormant_this_session_silent_early_afternoon",
    "lastHBTime": "2026-07-20 13:28:00 GMT+8",
    "silenceDuration_h": 96.21,
    "lastChecks": {
        "global_briefing": "2026-07-19 08:30",
        "heartbeat": "2026-07-20 13:28:00 GMT+8",
        "evening_self_iter_fired": "2026-07-19 21:00",
        "evening_self_iter_due": "2026-07-20 21:00",
        "daily_checkin": "2026-07-20 09:00",
        "morning_self_iter": "2026-07-20 10:00",
        "daily_briefing": "2026-07-20 10:35",
    },
    "note": "HB #647; minimal tick (R012); Eric silent in this session ~96.21h; active in AnYi session (~24.76h); session DORMANT per HB #584/R256/R257/R258 stack; no push; induction window FINAL 2 DAYS (today 7/20 day-1, tomorrow 7/21 LAST DAY ~33h); T-0 +45h28m past; R-NEW-V2 compliant; tomorrow 7/21 = dual convergence (DeepSeek V4 + induction window close)",
}

path = Path(r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json")
path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("STATE_UPDATED HB=647")