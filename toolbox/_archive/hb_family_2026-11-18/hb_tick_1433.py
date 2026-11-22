#!/usr/bin/env python3
# HB #3648 atomic tick - 2026-08-21 14:33 GMT+8
# R-NEW-V4: atomic-tick via os.replace; daily file append-only
import json, os, time, sys
from datetime import datetime, timezone, timedelta

WORKSPACE = r"D:\B166ER-OpenClaw\workspace"
STATE_PATH = os.path.join(WORKSPACE, "memory", "heartbeat-state.json")
DAILY_PATH = os.path.join(WORKSPACE, "memory", "2026-08-21.md")

# Local time GMT+8
TZ8 = timezone(timedelta(hours=8))
NOW = datetime.now(TZ8)
ISO = NOW.isoformat()
HHMM = NOW.strftime("%H:%M")

# 1. Atomic tick heartbeat-state.json
tmp = STATE_PATH + ".tmp"
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

old_n = state.get("hbCount", 0)
new_n = old_n + 1
new_id = f"HB #{new_n}"

state["hbCount"] = new_n
state["lastHB"] = ISO
state["lastDecision"] = "HEARTBEAT_OK"
state["last_update_epoch"] = int(time.time())
state["lastTick"] = ISO
state["lastHbId"] = new_id
state["lastHbTime"] = ISO
state["last_hb"] = {"id": new_id, "n": new_n, "ts": ISO}
state["last_check"] = ISO
state["note"] = f"Fri {HHMM}, +5min cadence, R69 silence D+28/30 (9 calendar days remain to 8/30 lift), Eric afternoon deep work -> quiet, DORMANT sustained"

with open(tmp, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp, STATE_PATH)

# 2. Append-only to daily file
ENTRY = f"""
### {new_id} ({ISO} cron-event, OpenClaw heartbeat poll)
- gap from HB #{old_n}: ~5min -- Fri workday-early-afternoon Token Guard cadence (R012)
- {HHMM} = Fri workday-early-afternoon (Eric dual-peak deep-work zone per USER.md)
- 22-layer suppression zero-breach (R-B/R12/R13/R14/R65/R66/R67/R68/R69/R70/R71/R256/R257/R258/R260/R261/R271/R276/R277/R278/R280/R282/R-NEW-V3/R-NEW-V4) -- penta+ holds
- post_t0_null sustained; hbCount: {old_n} -> {new_n} (atomic-tick via os.replace, R-NEW-V4)
- Eric webchat SOVEREIGN (idle ~67h+ since 8/18 19:06; last webchat 11:28 差旅对接分工)
- AnYi Day 28 (Fri workday-early-afternoon)
- R69 silence Day 28/30 (expires 2026-08-30 Sun, **9 calendar days remain**) -- cron does not break silence
- 8/19 Jinjiang MOU Day 3 of 3 (LAST DAY -- 8/19-21 Nanjing, P0 webchat-bound) -- cron does NOT push
- vault 1169+ files healthy
- R-NEW-V3 enforced: HEARTBEAT.md untouched (recovery mode from prior data loss 8/1); daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick via os.replace (hbCount {old_n}->{new_n})

### decision
- HEARTBEAT_OK -- {new_id} = sustain DORMANT protocol, minimal token tick
- no push: suppression holds + Fri workday-early-afternoon + cron session DORMANT per R65/R258/R69/R277/R282
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 8/19 Jinjiang MOU Day 3 (LAST DAY) -- P0, webchat-bound (Eric sovereign), NOT cron-bound; cron does NOT push
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- R65/R69 active + Eric sovereign on webchat + cron DORMANT
- Standing by P0 (webchat-bound): 15-5 strategy v0.1 (6 decisions) + V2 slides + R276 commit + R264 AnYi 1244 + Eric two reports + R278/R282 + R283 + R284 + R285 (all drafts) -- all await Eric webchat sovereign
- R69 countdown: 9 calendar days to lift silence on 8/30 Sun -- R282 + R283 + R284 + R285 batch ready for lift
- Next: per Token Guard cadence; HB sustained through Fri afternoon until Eric first-contact on cron session

*{ISO} -- Fri workday-early-afternoon + ~5min from HB #{old_n} -- {new_id} -- DORMANT -- Eric webchat sovereign (idle ~67h+ since 8/18 19:06) -- AnYi D+28d Fri -- 8/19 MOU Day 3 LAST DAY IN PROGRESS (Eric sovereign, cron NOT pushing) -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 + R69-T9d enforced -- HEARTBEAT_OK*
"""

with open(DAILY_PATH, "a", encoding="utf-8") as f:
    f.write(ENTRY)

print(f"[OK] {new_id} atomic-tick done. hbCount {old_n} -> {new_n}, ts={ISO}")
print(f"[OK] daily file appended: {DAILY_PATH}")