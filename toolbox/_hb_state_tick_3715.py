#!/usr/bin/env python3
"""Atomic tick state.json for HB #3715."""
import json
import os
from pathlib import Path

STATE = Path(r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json")

def main():
    data = json.loads(STATE.read_text(encoding="utf-8"))
    data["hbCount"] = 3715
    data["last_tick"] = "2026-08-22T12:34:00+08:00"
    data["last_heartbeat_response"] = "ok_quiet"
    data["last_tick_epoch"] = 1787373240
    # Append to lastHBs
    last_hbs = data.get("lastHBs", [])
    last_hbs.append({"hb": 3715, "ts": "2026-08-22T12:34:00+08:00"})
    # Trim to last 8
    data["lastHBs"] = last_hbs[-8:]
    data["notes"] = "Sat 12:34. HB #3715. R69 silence Day 29/30 (8d to lift 8/30 Sun). Eric weekend rest. cron DORMANT. Sustaining minimal token tick."
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, STATE)
    print(f"[OK] memory/heartbeat-state.json atomic-tick hbCount=3715")
    print(f"     last_tick={data['last_tick']}, lastHBs count={len(data['lastHBs'])}")

if __name__ == "__main__":
    main()
