"""Update heartbeat-state.json for HB #642."""
import json
from datetime import datetime, timezone, timedelta

state_path = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)

state = {
    "ericActiveElsewhere_h": round((now - datetime(2026, 7, 19, 12, 36, tzinfo=tz)).total_seconds() / 3600, 2),
    "silenceDuration_thisSession_h": round((now - datetime(2026, 7, 16, 13, 16, tzinfo=tz)).total_seconds() / 3600, 2),
    "hbCount": 642,
    "lastHB": 642,
    "nextCheck": "next: Token Guard cadence (~5-15min); evening self-iter 21:00 due (~7h51m)",
    "mode": "active_mode_dormant_this_session_silent_noon",
    "lastHBTime": now.strftime("%Y-%m-%d %H:%M:%S GMT+8"),
    "silenceDuration_h": round((now - datetime(2026, 7, 16, 13, 16, tzinfo=tz)).total_seconds() / 3600, 2),
    "lastChecks": {
        "global_briefing": "2026-07-19 08:30",
        "heartbeat": now.strftime("%Y-%m-%d %H:%M:%S GMT+8"),
        "evening_self_iter_fired": "2026-07-19 21:00",
        "evening_self_iter_due": "2026-07-20 21:00",
        "daily_checkin": "2026-07-20 09:00",
        "morning_self_iter": "2026-07-20 10:00",
        "daily_briefing": "2026-07-20 10:35"
    },
    "note": "HB #642; minimal tick (R012); Eric silent in this session ~95.89h; active in AnYi session; session DORMANT per HB #584/R256/R257/R258 stack; no push; induction window FINAL 2 DAYS (today 7/20 day-1, tomorrow 7/21 LAST DAY ~34.83h); T-0 +61.16h past; R-NEW-V2 compliant"
}

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"OK: heartbeat-state.json updated for HB #642")
print(f"hbCount={state['hbCount']}, mode={state['mode']}")
print(f"silence_h={state['silenceDuration_h']}, ericActiveElsewhere_h={state['ericActiveElsewhere_h']}")