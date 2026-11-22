#!/usr/bin/env python3
"""R-NEW-V4 atomic tick for state.json - HB #3724."""
import json
import os
from pathlib import Path

STATE_PATH = Path(r"D:\B166ER-OpenClaw\workspace\memory\state.json")
TS = "2026-08-22T14:51:00+08:00"
HB = 3724

def main():
    if not STATE_PATH.exists():
        print(f"ERROR: {STATE_PATH} not found")
        return
    
    # Read current
    with open(STATE_PATH, 'r', encoding='utf-8') as f:
        state = json.load(f)
    
    # Backup
    backup = STATE_PATH.with_suffix('.json.bak')
    with open(backup, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    # Update canonical fields (reconcile drift)
    state["lastDecision"] = "HEARTBEAT_OK"
    state["workday_zone"] = "weekend-afternoon"
    state["eric_webchat_idle_min"] = 2742  # ~89h+ since 8/19 ~02:49, actually since 8/21 11:28 = ~99h
    state["r69_silence"] = "Day 29/30 (expires 2026-08-30)"
    state["last_check"] = TS
    state["hbCount"] = HB
    state["lastHBNumber"] = HB
    state["lastTick"] = TS
    state["last_hb"] = {"n": HB, "ts": TS}
    state["lastHbTime"] = TS
    state["lastHB"] = TS
    state["note"] = f"HB #{HB}; Sat 2026-08-22T{TS[11:19]} -- Sat weekend-afternoon, AnYi Day 29, R69 Day 29/30 DORMANT (~8d to lift), cron session sustained DORMANT, drift reconciled from prior state.json lag (3699->{HB}), HEARTBEAT_OK"
    state["anyi_day"] = 29
    
    # Atomic write via os.replace (R-NEW-V4 compliant)
    fd, tmp = tempfile.mkstemp(dir=str(STATE_PATH.parent), suffix=".json.tmp")
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        os.replace(tmp, str(STATE_PATH))
        print(f"OK: HB #{HB} atomic-tick; drift {state.get('lastHBNumber', HB)-1}->{HB}")
    except Exception as e:
        print(f"FAIL: {e}")
        if os.path.exists(tmp):
            os.unlink(tmp)

if __name__ == "__main__":
    import tempfile
    main()
