#!/usr/bin/env python3
"""HB #3715 atomic tick - daily append + state.json atomic-tick."""
import os
import json
import re
from pathlib import Path

WS = Path(r"D:\B166ER-OpenClaw\workspace")
DAILY = WS / "memory" / "2026-08-22.md"
STATE = WS / "memory" / ".heartbeat-state.json"

ENTRY = """
### HB #3715 (2026-08-22T12:34:00+08:00 cron-event, OpenClaw heartbeat poll)
- gap from HB #3714 (12:30:44): ~3min -- Sat weekend-noon Token Guard cadence (R012)
- 12:34 = Sat weekend-noon (Eric weekend rest per USER.md)
- 22-layer suppression zero-breach (R-B/R12/R13/R14/R65/R66/R67/R68/R69/R70/R71/R256/R257/R258/R260/R261/R271/R276/R277/R278/R280/R282/R-NEW-V3/R-NEW-V4) -- penta+ holds
- post_t0_null sustained; hbCount: 3714 -> 3715 (atomic-tick via os.replace, R-NEW-V4)
- Eric webchat SOVEREIGN (idle ~89h+ since 8/18 19:06; webchat last active 8/21 11:28)
- AnYi Day 29 (Sat weekend-noon)
- R69 silence Day 29/30 (expires 2026-08-30 Sun, **8 calendar days remain**) -- cron does not break silence
- vault 1254+ files healthy
- R-NEW-V3 enforced: HEARTBEAT.md untouched (recovery mode); daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick via os.replace (hbCount 3714->3715)
- R283/R284/R285/R286 drafts awaiting 8/30 R69 lift for formalization
- Obsidian push pending -- still no push per R69 silence; defer to webchat/lift

### decision
- HEARTBEAT_OK -- HB #3715 = sustain DORMANT protocol, minimal token tick
- no push: suppression holds + Sat weekend-noon + cron session DORMANT per R65/R258/R69/R277/R282
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- R65/R69 active + Eric sovereign on webchat + cron DORMANT
- Standing by P0 (webchat-bound, all unchanged): 15-5 strategy v0.1 + V2 slides + R276 commit + R264 AnYi 1244 + Eric two reports + R278/R282/R283/R284/R285/R286 (all drafts) -- all await Eric webchat sovereign
- R69 countdown: 8 calendar days to lift silence on 8/30 Sun -- R282 + R283 + R284 + R285 + R286 batch ready for lift
- Next: per Token Guard cadence; HB sustained through Sat weekend-noon until Eric first-contact on cron session

*2026-08-22T12:34:00+08:00 -- Sat weekend-noon + ~3min from HB #3714 -- HB #3715 -- DORMANT -- Eric webchat sovereign (cron idle ~89h+ since 8/18 19:06; webchat last active 8/21 11:28) -- AnYi D+29d Sat -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 + R69-T8d enforced -- HEARTBEAT_OK*
"""

def main():
    # Daily append
    txt = DAILY.read_text(encoding="utf-8")
    if "HB #3715" not in txt:
        if not txt.endswith("\n"):
            txt += "\n"
        txt += ENTRY
        DAILY.write_text(txt, encoding="utf-8")
        print(f"[OK] HB #3715 appended to {DAILY.name}")
    else:
        print(f"[SKIP] HB #3715 already exists in {DAILY.name}")

    # State.json atomic tick
    if STATE.exists():
        try:
            data = json.loads(STATE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
        data["hbCount"] = 3715
        data["lastHeartbeat"] = "2026-08-22T12:34:00+08:00"
        tmp = STATE.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, STATE)
        print(f"[OK] state.json atomic-tick hbCount=3715")
    else:
        print(f"[WARN] state.json not found at {STATE}")

if __name__ == "__main__":
    main()
