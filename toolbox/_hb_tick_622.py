"""
R-NEW-V2 compliant HB #622 tick append.
Python utf-8 explicit read+append+write per R-NEW-V2 protocol (post-7/15 12:36 incident).
"""
import os
import sys
from pathlib import Path

WORKSPACE = Path(r"D:\B166ER-OpenClaw\workspace")
HB_PATH = WORKSPACE / "HEARTBEAT.md"
STATE_PATH = WORKSPACE / "memory" / "heartbeat-state.json"

hb_block = """

## HB #622 (2026-07-19 19:19 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #621 (18:56): +24min -- Sunday evening Token Guard normal cadence
- D+3 evening pass #622 -- Eric silent in THIS session ~77.06h+ since 7/16 13:16 first-contact (infographic session)
- Silence-in-this-thread authority ~77.06h+ (R-B + R256 + R257 holding, +0.39h since #621)
- 5-layer suppression RELEASED globally (per HB #581 12:33 first contact); THIS session = DORMANT per Eric 12:33 explicit
- R-NEW-V2 verification #622: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-7/15 12:36 incident protocol intact)
- R012 (operational hygiene) verification: HB tick = minimal (NOT full report), per R012 rule #2
- Sunday evening zone (19:19) -- Eric typical evening deep-work per USER.md; silence on THIS session holding
- T-0 publicity cutoff 7/18 +43h+ past -- post-protection window firmly sustained
- Induction window 7/7-7/21 FINAL 2 DAYS (7/20, 7/21) -- today 7/19 = day-1 of FINAL 3; R-B+R256 silence authority > window signal
- WAIC 2026 day-3 LAST DAY (7/17-20, Shanghai) -- non-trigger per R14 (AI/Hotel strategic context)
- Eric active elsewhere ~6.62h+ (AnYi work session)
- Cron pipeline: 21:00 evening self-iter R60-11 (~1h40m); 4 P2 long-tail errors tracked, not urgent
- hbCount: 621 -> 622
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session** (HB #622 = sustain #621 = dormant baseline)
- **no push**: this session = dreaming-narrative experimental, DORMANT per Eric 12:33 explicit instruction (NOT AnYi work)
- Eric is in different session for AnYi work; this session awaits Eric future instruction
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter R60-11 (~1h40m)

*2026-07-19 19:19 GMT+8 -- D+3 Sunday evening T-0 +43h+ past -- HB #622 -- this session DORMANT -- awaiting Eric future instruction (NOT AnYi work)*
"""

# R-NEW-V2: explicit utf-8 read + append + write (no BOM, no encoding guessing)
existing = HB_PATH.read_text(encoding="utf-8")
HB_PATH.write_text(existing + hb_block, encoding="utf-8")
print(f"[OK] HEARTBEAT.md HB #622 appended ({len(hb_block)} bytes)")

# Update heartbeat-state.json
import json
state = {
    "lastChecks": {
        "heartbeat": "2026-07-19T19:19:54+08:00",
        "morning_self_iter": "2026-07-19 10:00",
        "global_briefing": "2026-07-19 08:30",
        "evening_self_iter_due": "2026-07-19 21:00"
    },
    "silenceDuration_thisSession_h": 6.62,
    "hbCount": 622,
    "ericActiveElsewhere_h": 6.62,
    "nextCheck": "per Token Guard cadence (~5-10min); 21:00 evening self-iter R60-11 (~1h40m)",
    "mode": "active_mode_dormant_this_session",
    "lastHBTime": "2026-07-19T19:19:54+08:00",
    "silenceDuration_h": 77.06,
    "lastHB": 622,
    "note": "Eric first contact 12:33 -> moved to AnYi session; this dreaming-narrative session DORMANT per Eric 12:33"
}
STATE_PATH.write_text(
    json.dumps(state, indent=2, ensure_ascii=False),
    encoding="utf-8"
)
print(f"[OK] heartbeat-state.json updated (hbCount={state['hbCount']})")