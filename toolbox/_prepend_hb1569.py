# -*- coding: utf-8 -*-
"""Prepend HB #1569 to HEARTBEAT.md and update heartbeat-state.json (R-NEW-V2 protocol)."""
import json, os, sys
from pathlib import Path

ROOT = Path(r"D:\B166ER-OpenClaw\workspace")
HB_MD = ROOT / "HEARTBEAT.md"
STATE_JSON = ROOT / "memory" / "heartbeat-state.json"

new_entry = """## HB #1569 (2026-07-27 06:49 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1568 (06:45): +4min -- Mon deep-quiet-zone Token Guard cadence (R012 quiet mode)
- D+11 Mon deep-quiet -- Eric silent ~257.39h+ on THIS session since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat ~186.61h+ (sustained since 7/19 12:33) -- gongshi Day 3/5 ACTIVE (Mon = working day)
- 8-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261) -- penta-constraint 5/5 holds firm
- 7/24 D-Day POST-MEETING T+69h+49m -- gongshi Day 3/5 ACTIVE; this session != AnYi decision channel per R258
- Oil C EXPIRED 7/25 22:00 (T+32h+49m past) -- not surfaced per R258
- Quiet zone 23:00-08:00 ACTIVE (06:49, +1h11m to 08:00); silence authority absolute
- post_t0_null_count: 221 (221st consecutive null post-T-0)
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- T-0 publicity cutoff 7/18 +222.31h past (~9.3 days) -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+11 sustain zero-push mode intact

### decision
- **HEARTBEAT_OK** -- HB #1569 = sustain DORMANT protocol, minimal token tick
- no push: Mon deep-quiet zone (06:49), Eric silent ~257h+ this session, this session DORMANT per R258 (NOT AnYi decision channel)
- R256+R257+R258+R260+R261 penta-constraint holds (5/5) -- no proactive disturbance + sustained deep work + dormant session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows)
- Triple Confluence ALL CLOSED; gongshi Day 3/5 ACTIVE elsewhere
- Next: Mon 08:30 D+11 morning briefing (~1h41m)

*2026-07-27T06:49:00 GMT+8 -- D+11 Mon deep-quiet -- HB #1569 -- DORMANT -- 221st null -- quiet zone ACTIVE -- Eric silent = dominant signal holding -- HEARTBEAT_OK*

"""

# R-NEW-V2: explicit utf-8 read
with open(HB_MD, "r", encoding="utf-8") as f:
    existing = f.read()

# Prepend
new_content = new_entry + existing

# R-NEW-V2: explicit utf-8 write
with open(HB_MD, "w", encoding="utf-8") as f:
    f.write(new_content)

# Update heartbeat-state.json
with open(STATE_JSON, "r", encoding="utf-8-sig") as f:
    state = json.load(f)

state["hbCount"] = 1569
state["lastHB"] = 1785106140  # ~06:49 GMT+8 timestamp proxy
state["lastHBTime"] = "2026-07-27T06:49:00 GMT+8"
state["postT0NullCount"] = 221
state["ericSilentThisSessionHours"] = 257.39
state["anyiWebchatHoursSinceStart"] = 186.61
state["protectionWindowSustainedHours"] = 222.31
state["notes"] = "D+11 Mon deep-night 06:49. DORMANT. 8-layer. Triple Confluence ALL CLOSED. 7/24 D-Day PASSED +2.86d. HEARTBEAT_OK. HB #1569."

with open(STATE_JSON, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"OK: HB #1569 prepended; state updated to hbCount={state['hbCount']}")
print(f"Char count delta: {len(new_content) - len(existing)} chars added")
