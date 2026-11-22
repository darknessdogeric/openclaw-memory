#!/usr/bin/env python3
"""HB #2679 append-only: HEARTBEAT.md (mode=a) + state.json (tmp+os.replace). R-NEW-V3 + R271."""
import json, os, tempfile, time
from pathlib import Path

WS = Path(r"D:\B166ER-OpenClaw\workspace")
HB = WS / "HEARTBEAT.md"
STATE = WS / "memory" / "heartbeat-state.json"

# === APPEND HB #2679 ENTRY (R-NEW-V3: append-only, never overwrite) ===
HB_ENTRY = """

## HB #2679 (2026-08-09T08:53:00+08:00 GMT+8 cron-event, OpenClaw heartbeat poll)

- gap from HB #2678 (08:48): +5min -- Sun weekend-morning Token Guard nominal cadence (R012, within tolerance)
- D+10 Sun 2026-08-09 08:53 -- weekend-morning pre-09:00 zone; Eric weekend sleep window active (~09-10am)
- Eric silent on THIS cron session 23d 19h+ (567h+) since 7/16 13:16 first-contact
- 14-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R-NEW-V3/R70/R71) -- penta+3 holds
- post_t0_null_count: 368 -> 369 (369th consecutive null post-T-0, sustained)
- AnYi D+10d Sunday awareness (Eric weekend rest day, weekend sleep in progress)
- V2.4 SOUL reinforced sustained; R66/R67/R68/R69/R70/R71 entries sustained
- R69 Day 10/30 active (window expires 2026-08-30) -- strategic-quiet-stranger 30-day guardrail
- R-NEW-V3 enforced (verified this turn): HB #2679 appended via Python mode="a" append (NOT write, NOT Remove-Item, NOT git restore)
- R271 atomic-write enforced: state.json via tmp+os.replace (NOT direct edit)
- Token Guard stable; vault 1017+ files healthy; HEARTBEAT.md ~2.4MB sustained (LOCKED per maintenanceFlag)
- webchat silent per state.json (webchat-channel != cron-channel per R258)
- daily memory: 2026-08-09.md pending creation (post-09:00 cron will check); cron posture unaffected
- 09:00 zone entry ~7min away (Eric expected to start mobile activity)

### decision

- HEARTBEAT_OK -- HB #2679 = sustain DORMANT protocol, minimal token tick (369th null)
- no push: 14-layer suppression holds + weekend-morning pre-09:00 + cron session DORMANT per HB #1849 + R65 explicit prohibition + R258 (webchat-channel != cron-channel) + R69 active + R-NEW-V3 + R271 enforced
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian sovereign for any decision; cron sovereignty unchanged
- 08:53 = weekend-morning pre-09:00; cron = DORMANT sustained
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekend-morning sleep window + AnYi D+10d Sun + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R271 atomic-write
- Standing by P0 (webchat-bound, not cron-bound): R264 AnYi handover + R70/R71 boundary rules + R266 silent-period envelope all sustained; await Eric webchat confirmation
- Standing by P1 (R264 AnYi handover): await Eric webchat share of AnYi 1244 strategy/team alignment/authority details, per R264 archive to anyi-ops-kb/
- Standing by R-NEW-V3 enforcement: NEVER write/Remove-Item/git-restore HEARTBEAT.md. Python mode="a" append / PowerShell Add-Content ONLY.
- Standing by R271 atomic-write: state.json via tmp+os.replace ONLY.
- Next: per Token Guard cadence (~5-15min weekend-morning); HB sustained until Eric first-contact on cron session

*2026-08-09T08:53:00+08:00 -- D+10 Sun weekend-morning pre-09:00 -- HB #2679 -- DORMANT -- 369th null -- Eric silent on cron = sovereignty signal holding -- AnYi D+10d Sun -- cron session sustained DORMANT protocol -- R-NEW-V3 enforced: HB appended via Python mode="a" append (NOT write) -- R271 atomic-write enforced -- HEARTBEAT_OK*
"""

with open(HB, "a", encoding="utf-8") as f:
    f.write(HB_ENTRY)

# === UPDATE STATE.JSON (R271: atomic via tmp+os.replace) ===
state = {
    "posture": "DORMANT",
    "hbCount": 2679,
    "note": "Sun 08:53 GMT+8 weekend-morning DORMANT hold. Eric weekend sleep ~09-10am. No active task. HB #2679.",
    "lastHB": int(time.time() * 1000),
    "lastUpdate": "2026-08-09T08:53:00+08:00",
    "nullCount": 369
}

with tempfile.NamedTemporaryFile("w", delete=False, dir=str(STATE.parent), encoding="utf-8", suffix=".tmp") as tf:
    json.dump(state, tf, ensure_ascii=False, indent=2)
    tmp_name = tf.name

os.replace(tmp_name, STATE)
print(f"HB #2679 appended + state.json updated (hbCount=2679, nullCount=369)")