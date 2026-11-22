#!/usr/bin/env python3
"""
R-NEW-V4 compliant atomic tick for state.json.
Uses os.replace() for atomic write on Windows.
"""
import json
import os
import sys
import tempfile
from pathlib import Path

STATE_PATH = Path(r"D:\B166ER-OpenClaw\workspace\memory\state.json")
TS = "2026-08-16T12:17:00+08:00"
HB = 3395
NULL = 1947
ANYI = 24

def main():
    if not STATE_PATH.exists():
        print(f"ERROR: {STATE_PATH} not found", file=sys.stderr)
        sys.exit(1)
    
    # Read current
    with open(STATE_PATH, 'r', encoding='utf-8') as f:
        state = json.load(f)
    
    # Backup current
    backup = STATE_PATH.with_suffix('.json.bak')
    with open(backup, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    # Update canonical fields (reconciling 39-HB drift)
    updates = {
        "note": f"HB #{HB}; Sun 12:17 weekend-MIDDAY-quiet-zone; Eric webchat idle ~18h25m+; R69 silence Day {ANYI}/30 active; 17-layer suppression holds; cron DORMANT sustained; state.json drift reconciled (+39 HBs since 8/15T22:19); HEARTBEAT_OK",
        "lastHbTime": TS,
        "lastHb": TS,
        "last_hb": TS,
        "last_hb_time": TS,
        "last_tick": TS,
        "lastUpdate": TS,
        "last_update": TS,
        "last_check": TS,
        "post_t0_null_count": NULL,
        "post_t0_null": NULL,
        "nullCount": NULL,
        "null_count": NULL,
        "hbCount": HB,
        "hb_count": HB,
        "last_hb_n": HB,
        "anyi_day": ANYI,
        "workday_zone": "weekend-MIDDAY-quiet-zone (+4h17m past 08:00)",
        "r69_silence": f"Day {ANYI}/30 (expires 2026-08-30)",
        "eric_webchat_idle_min": 1105,  # ~18h25m
        "lastDecision": "HEARTBEAT_OK",
        "last_hb_decision": f"HEARTBEAT_OK -- DORMANT -- WEEKEND-MIDDAY -- HB #{HB}",
        "status": "DORMANT",
        "r_new_v3_compliant": True,
        "r271_compliant": True,
        "r258_channel_separation": True,
        "null_milestone_1800": True,
        "eight_hard_cap_exceeded": True,
    }
    
    # Apply updates (preserve any extra fields)
    for k, v in updates.items():
        state[k] = v
    
    # Atomic write: write to temp file then os.replace()
    tmp_fd, tmp_path = tempfile.mkstemp(
        prefix="state_", suffix=".json.tmp",
        dir=str(STATE_PATH.parent)
    )
    try:
        with os.fdopen(tmp_fd, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        # Atomic replace
        os.replace(tmp_path, STATE_PATH)
        print(f"OK: state.json atomic-ticked to HB #{HB}")
        print(f"  hbCount: {HB}")
        print(f"  post_t0_null_count: {NULL}")
        print(f"  anyi_day: {ANYI}")
        print(f"  timestamp: {TS}")
        print(f"  backup: {backup}")
    except Exception as e:
        # Clean up temp on failure
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
