import json, os, sys
from datetime import datetime, timezone, timedelta

state_path = sys.argv[1] if len(sys.argv) > 1 else "heartbeat-state.json"
tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
ts = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
epoch = int(now.timestamp())

with open(state_path, "r", encoding="utf-8-sig") as f:
    state = json.load(f)

old_count = state["hbCount"]
new_count = old_count + 1

state["hbCount"] = new_count
state["last_update_epoch"] = epoch
state["lastHbTime"] = ts
state["lastTick"] = ts
state["lastHbId"] = f"HB #{new_count}"
state["last_check"] = ts
state["lastDecision"] = "HEARTBEAT_OK"
state["last_hb"] = {"ts": ts, "id": f"HB #{new_count}", "n": new_count}
state["lastHB"] = ts
state["note"] = f"~1min after #{new_count-1}, Fri 13:26 afternoon, R69 silence D+28/30, no new signals -> quiet"

tmp = state_path + ".tmp"
with open(tmp, "w", encoding="utf-8-sig") as f:
    json.dump(state, f, indent=2, ensure_ascii=False)
os.replace(tmp, state_path)

print(f"hbCount: {old_count} -> {new_count}")
print(f"ts: {ts}")
print(f"epoch: {epoch}")
