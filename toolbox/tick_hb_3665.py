import json, os
state_path = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"
with open(state_path, "r", encoding="utf-8-sig") as f:
    state = json.load(f)
state["hbCount"] += 1
state["last_tick"] = "2026-08-21T16:45:00+08:00"
state["lastHBs"] = [{"ts": "2026-08-21T16:45:00+08:00", "hb": state["hbCount"]}]
tmp = state_path + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp, state_path)
print("state.json ticked:", state["hbCount"])
