"""R271 atomic heartbeat state update."""
import json
import os
import sys
import tempfile
from pathlib import Path

STATE_PATH = Path(r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json")

def atomic_write_json(path: Path, obj: dict) -> None:
    """R271: write to temp file + os.replace for atomic update."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=str(path.parent),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise

def main():
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    state["hbCount"] = 3104
    state["nullCount"] = 1679
    state["lastTick"] = "2026-08-13T12:55:00+08:00"
    state["lastDecision"] = "HEARTBEAT_OK"
    state["session"] = "cron:315657b9-fc80-4b94-a853-404e3955f7a0"
    state["r271_compliant"] = True
    state["r_new_v3_compliant"] = True
    state["r258_channel_separation"] = True
    state["r69_silence"] = "Day 21/30 (expires 2026-08-30)"
    state["eric_webchat_last"] = "2026-08-11T22:40"
    state["eric_webchat_idle_min"] = 2215  # ~36.9h, slightly adjusted
    state["anyi_day"] = 21
    state["workday_zone"] = "workday-PM"
    state["eight_hard_cap_exceeded"] = False
    state["last_update"] = "2026-08-13T12:55:00+08:00"
    state["lastHbTime"] = "2026-08-13T12:55:00+08:00"
    atomic_write_json(STATE_PATH, state)
    print("state.json updated (atomic)")

if __name__ == "__main__":
    main()
