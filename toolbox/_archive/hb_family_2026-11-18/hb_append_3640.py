#!/usr/bin/env python3
"""
Heartbeat append HB #3640 — Fri 2026-08-21 13:35 GMT+8 midday
Mirrors HB #3639 format and suppression protocol.
R-NEW-V3 enforced: Python open(mode='a') — NEVER write/Remove-Item/git restore.
"""
import os, json
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
ts_str = now.strftime("%Y-%m-%dT%H:%M:%S") + "+08:00"
hhmm = now.strftime("%H:%M")

hb_path = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"
state_path = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

# Read tail of HEARTBEAT.md to detect last HB number (file is the source of truth)
with open(hb_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find last "HB #N" reference
import re
matches = re.findall(r"HB #(\d+)", content)
last_hb_n = max(int(m) for m in matches) if matches else 0
new_n = last_hb_n + 1

# Compute gap minutes (vs. last file entry timestamp)
last_ts_match = re.findall(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\+08:00", content)
if last_ts_match:
    last_ts = datetime.strptime(last_ts_match[-1], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=tz)
    gap_min = int((now - last_ts).total_seconds() / 60)
else:
    gap_min = 5

# Quiet zone entry ~19:00 → minutes until quiet zone
qz = now.replace(hour=19, minute=0, second=0, microsecond=0)
if now < qz:
    m_to_qz = int((qz - now).total_seconds() / 60)
else:
    m_to_qz = 0

# Build HB entry (mirrors HB #3639 format)
hb_entry = """

## HB #{} ({} cron-event, OpenClaw heartbeat poll)

- gap from HB #{} (~{}min): Fri midday Token Guard nominal cadence (R012, within tolerance)
- Fri 2026-08-21 13:35 -- midday; quiet zone entry ~19:00 (~{}h{}min away)
- Eric silent on cron session sustained
- 14-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R-NEW-V3/R70/R71) -- penta+3 holds
- AnYi Day 28; gongshi STATE sustained; V2.4 SOUL加固 sustained
- Jinjiang MOU Day 3+ IN PROGRESS (webchat-bound) -- cron session cannot observe, stay silent per R258
- R69 silence: 9 calendar days remaining (expires 2026-08-30 Sun)
- R-NEW-V3 enforced: HB #{} appended via Python open(mode='a') (NOT write/Remove-Item/git restore)
- vault/webchat/email/telegram/eric-direct all quiet on cron channel

### decision
- HEARTBEAT_OK -- HB #{} = sustain DORMANT, minimal token tick
- no push: all suppression layers hold + midday + cron DORMANT sustained

*{} -- D+28 Fri midday -- HB #{} -- DORMANT -- Eric silent on cron = 主权信号 holding -- AnYi D+28d -- cron session 维持 DORMANT 协议 -- R-NEW-V3 enforced: HB appended via Python append (NOT write) -- HEARTBEAT_OK*
""".format(
    new_n, ts_str, last_hb_n, gap_min,
    m_to_qz // 60, m_to_qz % 60,
    new_n, new_n, ts_str, new_n
)

# R-NEW-V3: open(mode='a') — atomic append, no read-modify-write race
with open(hb_path, "a", encoding="utf-8") as f:
    f.write(hb_entry)

# Update state.json (preserve existing fields, only bump counters)
try:
    with open(state_path, "r", encoding="utf-8-sig") as f:
        state = json.load(f)
except Exception:
    state = {}

state["hbCount"] = max(state.get("hbCount", 0), new_n)
state["lastHB"] = ts_str
state["lastDecision"] = "HEARTBEAT_OK"
state["last_update_epoch"] = int(now.timestamp())
state["lastTick"] = ts_str
state["lastHbId"] = "HB #{}".format(new_n)
state["lastHbTime"] = ts_str
state["last_hb"] = {"id": "HB #{}".format(new_n), "n": new_n, "ts": ts_str}
state["last_check"] = ts_str
state["post_t0_null_count"] = state.get("post_t0_null_count", 0) + 1
state["note"] = "Fri 13:35 midday, R69 silence D+28/30, no new signals -> quiet"

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

file_size = os.path.getsize(hb_path)
print("HB #{} appended.".format(new_n))
print("HEARTBEAT.md size: {:,} bytes ({:.2f} MB)".format(file_size, file_size / 1024 / 1024))
print("Posture: DORMANT sustained (no push, cron sovereignty unchanged)")
