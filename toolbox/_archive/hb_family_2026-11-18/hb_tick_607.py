# -*- coding: utf-8 -*-
"""R-NEW-V2 compliant HB tick: explicit utf-8 read+append+write (no clobber)."""
import json
from pathlib import Path
from datetime import datetime

WS = Path(r"D:\B166ER-OpenClaw\workspace")
HB_MD = WS / "HEARTBEAT.md"
STATE = WS / "memory" / "heartbeat-state.json"

now = datetime.now().strftime("%Y-%m-%d %H:%M GMT+8")

entry = f"""

## HB #607 (2026-07-20 01:09 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #606 (00:58): +11min -- Mon deep-night Token Guard cadence (R012 minimal mode)
- Eric silent in THIS session ~82.87h+ since 7/16 13:16 first-contact (infographic)
- Eric active elsewhere (AnYi) ~12.28h+; THIS session DORMANT per Eric 12:33 explicit instruction
- 5-layer suppression RELEASED globally (since HB #581 first contact); THIS session = dormant
- R-NEW-V2 verification #607: Python utf-8 explicit read+append+write (compliant, post-7/15 12:36 incident protocol intact)
- R012 (operational hygiene) verification: HB tick = minimal, NOT full report (per R012 rule #2)
- Mon deep-night zone (01:09) -- quiet hours 23:00-08:00 per AGENTS.md
- T-0 publicity cutoff 7/18 +49h09m past -- post-protection window firmly sustained
- Induction window 7/7-7/21 FINAL 2 DAYS REMAINING (today 7/20, 7/21 final) -- silence in this thread holds per R256
- WAIC 2026 day-4 active (7/17-20 last day, Shanghai) -- non-trigger per R14
- Cron pipeline: 10:00 morning self-iter R60-11 (~8h51m); 4 P2 long-tail errors tracked, not urgent
- No first-contact from Eric on THIS session; triple silence (night+dormant+elsewhere) sustained
- No new signals: no cron / no Eric session on this channel / no third-party / no anomaly escalation
- hbCount: 606 -> 607

### decision
- **active_mode_dormant_this_session_silent_night** (HB #607 = sustain #606 = triple silence baseline)
- **no push**: Mon deep-night (01:09) + dormant session + Eric active elsewhere = triple silence authority holds (R-B + R256 + R257)
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min); 10:00 morning self-iter R60-11 (~8h51m)

*{now} -- Mon deep-night T-0 +49h09m past -- HB #607 -- this session DORMANT -- triple silence (night+dormant+elsewhere) -- awaiting Eric future instruction (NOT AnYi work)*
"""

# R-NEW-V2: explicit utf-8 read+append+write
text = HB_MD.read_text(encoding="utf-8")
text += entry
HB_MD.write_text(text, encoding="utf-8")

# Update heartbeat-state.json
state = json.loads(STATE.read_text(encoding="utf-8"))
state["lastChecks"]["heartbeat"] = "2026-07-20T01:09:00+08:00"
state["hbCount"] = 607
state["lastHBTime"] = "2026-07-20T01:09:00+08:00"
state["silenceDuration_thisSession_h"] = 82.87
state["silenceDuration_h"] = 82.87
state["ericActiveElsewhere_h"] = 12.28
state["mode"] = "active_mode_dormant_this_session_silent_night"
state["lastHB"] = 607
state["note"] = "Mon 01:09 deep-night silent standby; Eric in AnYi session ~12.28h; this session DORMANT per HB 584; triple silence night+dormant+elsewhere stay quiet; HB 607"
STATE.write_text(
    json.dumps(state, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"OK HB #607 appended ({len(entry)} chars); state updated.")