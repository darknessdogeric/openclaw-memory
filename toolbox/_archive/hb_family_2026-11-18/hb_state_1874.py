"""Update heartbeat-state.json for HB #1874."""
import sys
import json
from pathlib import Path

STATE_PATH = Path(r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json")

try:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8-sig"))
    state["lastHBTime"] = "2026-07-29T14:05 GMT+8"
    state["hbCount"] = 1874
    state["lastHBNumber"] = 1873
    state["ericSilentThisSessionHours"] = 312.55
    state["quietZoneActiveNow"] = False
    state["dDayHoursPostMeeting"] = 123.07
    state["oilCExpiredHoursPast"] = 88.07
    state["t0PublicityCutoffHoursPast"] = 264.27
    state["v24SoulSustainedMinutes"] = 6495
    state["post_t0_null_count"] = 493
    state["thisSessionMode"] = "DORMANT"
    state["anyiWebchatHoursSinceStart"] = 241.46
    state["notes"] = (
        "HB #1874. 2026-07-29T14:05 GMT+8. +2min from HB #1873. "
        "D+13 cron session DORMANT 312h+. Eric silent on this session per "
        "R256+R257+R258+R65+R260+R261. Afternoon zone (下午深度工作 peak). "
        "R63 入职确认 standing-by (webchat sovereign, cron no-push per R65). "
        "9-layer suppression zero breach. HB #1874 = minimal token tick, sustain DORMANT. HEARTBEAT_OK."
    )
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: heartbeat-state.json updated, hbCount={state['hbCount']}")
except Exception as e:
    print(f"FAIL: {type(e).__name__}: {e}")
    sys.exit(1)
