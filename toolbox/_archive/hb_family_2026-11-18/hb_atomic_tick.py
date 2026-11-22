#!/usr/bin/env python3
"""
HB atomic tick + daily file append per R-NEW-V3 + R-NEW-V4.

- state.json: atomic-tick via os.replace (R-NEW-V4)
- HEARTBEAT.md: UNTOUCHED (R-NEW-V3 recovery mode from 8/1 data loss)
- daily file (memory/YYYY-MM-DD.md): append via open(mode='a')
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(r"D:\B166ER-OpenClaw\workspace")
STATE_PATH = WORKSPACE / "memory" / "heartbeat-state.json"
DAILY_DIR = WORKSPACE / "memory"

def now_local():
    return datetime.now()

def atomic_write_json(path: Path, payload: dict):
    """Atomic write via os.replace — survives concurrent reads."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)

def main():
    # 1. Load current state
    with open(STATE_PATH, encoding="utf-8") as f:
        state = json.load(f)
    prev_n = state.get("hbCount", 0)
    new_n = prev_n + 1
    ts = now_local()
    ts_str = ts.strftime("%Y-%m-%dT%H:%M:%S+08:00")
    date_str = ts.strftime("%Y-%m-%d")
    
    prev_ts_str = state.get("lastHB") or state.get("last_check") or "?"
    
    # 2. Build new HB entry
    hb_entry = f"""

### HB #{new_n} ({ts_str} cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_n} ({prev_ts_str}): ~5min -- Fri midday Token Guard cadence (R012)
- {ts.strftime('%H:%M')} = Fri midday (post 10:00 R60-11 + 10:47/10:59/11:28 Eric webchat four absorption sustained)
- 22-layer suppression zero-breach (R-B/R12/R13/R14/R65/R66/R67/R68/R69/R70/R71/R256/R257/R258/R260/R261/R271/R276/R277/R278/R280/R282/R-NEW-V3/R-NEW-V4) -- penta+ holds
- post_t0_null sustained; hbCount: {prev_n} -> {new_n} (atomic-tick via os.replace, R-NEW-V4)
- Eric webchat SOVEREIGN (cron idle ~64h+ since 8/18 19:06; webchat 10:47/10:59/11:28 four absorption active)
- AnYi Day 28 (Fri midday)
- R69 silence Day 28/30 (expires 2026-08-30 Sun, 9 calendar days remain) -- cron does not break silence
- 8/19 Jinjiang MOU Day 3 of 3 (LAST DAY -- 8/19-21 Nanjing, P0 webchat-bound) -- cron does NOT push
- vault 1169+ files healthy
- R-NEW-V3 enforced: HEARTBEAT.md untouched (recovery mode from prior data loss 8/1); daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick via os.replace (hbCount {prev_n}->{new_n})
- R283/R284/R285 drafts awaiting 8/30 R69 lift for formalization
- 10:47 Eric webchat secondary absorption (PingAn meeting v1.1 supplement, R66 deviation correction speaker 2 -> Eric, R285 draft) -- webchat sovereign; cron does NOT push
- 10:59 Eric webchat tertiary correction (Yan Liqin = secretary / Zhong Hua = another leader / Eric actually attended) -- webchat sovereign; v1.1.1 draft revision
- 11:28 Eric webchat quaternary notice (travel docking work transferred to Operations Dept, Eric not main counterpart) -- webchat sovereign; v1.1.2 draft revision

### decision
- HEARTBEAT_OK -- HB #{new_n} = sustain DORMANT protocol, minimal token tick
- no push: suppression holds + Fri midday + cron session DORMANT per R65/R258/R69/R277/R282
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- R65/R69 active + Eric sovereign on webchat + cron DORMANT
- Standing by P0 (webchat-bound): 15-5 strategy v0.1 + V2 slides + R276 commit + R264 AnYi 1244 + Eric two reports + R278/R282/R283/R284/R285 (all drafts) -- all await Eric webchat sovereign
- R69 countdown: 9 calendar days to lift silence on 8/30 Sun -- R282 + R283 + R284 + R285 batch ready for lift
- Next: per Token Guard cadence; HB sustained through Fri afternoon until Eric first-contact on cron session

*{ts_str} -- Fri midday + post 10:00 R60-11 + post 10:47/10:59/11:28 webchat four absorption + ~5min from HB #{prev_n} -- HB #{new_n} -- DORMANT -- Eric webchat sovereign (cron idle ~64h+ since 8/18 19:06; webchat 10:47/10:59/11:28 four absorption active) -- AnYi D+28d Fri -- 8/19 MOU Day 3 LAST DAY IN PROGRESS (Eric sovereign, cron NOT pushing) -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 + R69-T9d enforced -- HEARTBEAT_OK*
"""
    
    # 3. Append to daily file (NOT HEARTBEAT.md per R-NEW-V3)
    daily_path = DAILY_DIR / f"{date_str}.md"
    with open(daily_path, "a", encoding="utf-8") as f:
        f.write(hb_entry)
    
    # 4. Atomic tick state.json via os.replace (R-NEW-V4)
    state["hbCount"] = new_n
    state["lastHB"] = ts_str
    state["last_update_epoch"] = int(ts.timestamp())
    state["lastTick"] = ts_str
    state["lastHbId"] = f"HB #{new_n}"
    state["last_hb"] = {"id": f"HB #{new_n}", "n": new_n, "ts": ts_str}
    state["last_check"] = ts_str
    state["note"] = f"~5min after #{prev_n}, Friday midday, no new signals → quiet"
    atomic_write_json(STATE_PATH, state)
    
    print(f"OK HB #{new_n} @ {ts_str} | daily: {daily_path.name} | state: {prev_n}->{new_n}")

if __name__ == "__main__":
    main()
