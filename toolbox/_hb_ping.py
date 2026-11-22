#!/usr/bin/env python3
"""Heartbeat ping updater — minimal state bump."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

HB_PATH = Path(r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json")
TZ = timezone(timedelta(hours=8))

def main():
    state = json.loads(HB_PATH.read_text(encoding="utf-8"))
    now = datetime.now(TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00")
    state["lastHBTime"] = now
    state["hbCount"] = int(state.get("hbCount", 0)) + 1
    state["post_t0_null_count"] = int(state.get("post_t0_null_count", 0)) + 1
    state["note"] = (
        "2026-07-31 11:10 GMT+8 Fri +10m post 11:00 ping; "
        "AnYi 报到 D-DAY HISTORIC IN PROGRESS 5h+; "
        "Eric silent-on-cron 341h+; cron DORMANT R65 sustained; "
        "DO NOT DISTURB; reply HEARTBEAT_OK only"
    )
    HB_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK hbCount={state['hbCount']} post_t0={state['post_t0_null_count']} lastHB={now}")

if __name__ == "__main__":
    main()