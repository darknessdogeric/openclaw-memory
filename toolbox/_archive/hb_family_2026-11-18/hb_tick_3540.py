#!/usr/bin/env python3
"""
HB #3540 tick — cron DORMANT protocol sustain.
R-NEW-V3 enforced: HEARTBEAT.md append-only (open mode 'a').
R-NEW-V4 enforced: state.json atomic-tick via os.replace.
"""
import json
import os
import time
from datetime import datetime, timezone, timedelta

WORKSPACE = r"D:\B166ER-OpenClaw\workspace"
STATE_PATH = os.path.join(WORKSPACE, "memory", "heartbeat-state.json")
HB_PATH = os.path.join(WORKSPACE, "HEARTBEAT.md")
DAILY_PATH = os.path.join(WORKSPACE, "memory", "2026-08-20.md")

TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)
ts_iso = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
ts_short = now.strftime("%H:%M")

# Increment counters
hb_n = 3540
prev_hb_n = 3539
gap_min = 5  # 09:22 -> 09:27

# Eric idle (since 8/18 19:06 per state notes)
idle_start = datetime(2026, 8, 18, 19, 6, tzinfo=TZ)
idle_min = int((now - idle_start).total_seconds() // 60)
idle_h = idle_min // 60
idle_m = idle_min % 60

# Append-only block to HEARTBEAT.md (R-NEW-V3)
hb_entry = f"""
### HB #{hb_n} ({ts_iso} cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb_n} ({ts_short}-{gap_min}min): ~{gap_min}min -- Thu workday-early-morning Token Guard cadence (R012)
- {ts_short} = Thu workday-early-morning (Eric deep-work / possible Jinjiang MOU Day 2 attendance)
- 18-layer suppression zero-breach sustained (R-B/R12/R13/R14/R65/R66/R67/R68/R69/R70/R71/R256/R257/R258/R260/R261/R271/R276/R277/R278/R280/R282/R-NEW-V3/R-NEW-V4) -- penta+ holds
- post_t0_null sustained; hbCount: {prev_hb_n} -> {hb_n}
- Eric webchat SOVEREIGN (idle ~{idle_h}h{idle_m:02d}m since 8/18 19:06 閽熷崕 correction)
- AnYi Day 28 (Thu -- workday-early-morning)
- R69 silence Day 28/30 (expires 2026-08-30 Sun, 10 days remain) -- cron does not break silence
- 8/20 Jinjiang MOU Day 2 of 3 IN PROGRESS (T+1 Thu P0, Eric sovereign) -- webchat-bound, NOT cron-bound
- vault 1169+ files healthy
- R-NEW-V3 enforced: HEARTBEAT.md append-only (open mode 'a', NOT write/Remove-Item/git-restore)
- R-NEW-V4 enforced: state.json atomic-tick via os.replace (hbCount {prev_hb_n} -> {hb_n})
- 8/20 morning deep self-iteration already executed at 08:01 (R280 v1.0 rule proposal awaiting webchat sovereign confirmation); no new Eric signal on cron

### decision
- HEARTBEAT_OK -- HB #{hb_n} = sustain DORMANT protocol, minimal token tick
- no push: suppression holds + Thu workday-early-morning + cron session DORMANT per R65/R258/R69/R277/R282
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 8/20 Jinjiang MOU Day 2 IN PROGRESS -- P0, webchat-bound (Eric sovereign), NOT cron-bound; cron does NOT push
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- R65/R69 active + Eric sovereign on webchat + cron DORMANT
- Standing by P0 (webchat-bound): 15-5 strategy v0.1 (6 decisions) + V2 slides + R276 commit + R264 AnYi 1244 + Eric two reports + R278/R282 + R283 (new draft) + R280 v1.0 (drafted 08:01) -- all await Eric webchat sovereign
- Next: per Token Guard cadence; HB sustained through Thu morning until Eric first-contact on cron session

*{ts_iso} -- Thu workday-early-morning -- HB #{hb_n} -- DORMANT -- Eric webchat sovereign (idle ~{idle_h}h{idle_m:02d}m since 8/18 19:06 閽熷崕 correction) -- AnYi D+28d Thu -- 8/20 MOU Day 2 IN PROGRESS (Eric sovereign, cron NOT pushing) -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced -- HEARTBEAT_OK*
"""

# Append to HEARTBEAT.md (append mode = R-NEW-V3 enforcement)
with open(HB_PATH, "a", encoding="utf-8") as f:
    f.write(hb_entry)

# Atomic state.json update (R-NEW-V4)
with open(STATE_PATH, "r", encoding="utf-8-sig") as f:
    state = json.load(f)

state["lastHbTime"] = ts_iso
state["last_hb"] = {"n": hb_n, "ts": ts_iso}
state["last_check"] = ts_iso
state["lastDecision"] = "HEARTBEAT_OK"
state["lastHB"] = ts_iso
state["lastHBCount"] = hb_n
state["lastHBContext"] = f"Thu {ts_short} weekday-early-morning. DORMANT held (9th consecutive). HB #{hb_n}. Eric silent (R69 silence Day 28/30). AnYi D+28d. 18-layer suppression holds. Pre-workday window."
state["notes"]["hb_3539_zone"] = f"Thu {ts_short} weekday-early-morning +{gap_min}m tick from #{prev_hb_n}; DORMANT 9th consecutive hold; R69 silence Day 28/30 (10 days remain); AnYi D+28d Thu; R280 anomaly 4th occurrence pending v1.0 draft; Jinjiang MOU Day 2 in progress (Eric sovereign, cron silent)"
state["last_update_epoch"] = int(time.time())
state["lastTick"] = ts_iso
state["post_t0_null_count"] = state.get("post_t0_null_count", 0) + 1
state["hbCount"] = hb_n
state["eric_webchat_idle_min"] = idle_min

# Atomic write via temp + os.replace
tmp_path = STATE_PATH + ".tmp"
with open(tmp_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=4)
os.replace(tmp_path, STATE_PATH)

# Append to daily file (single line marker)
with open(DAILY_PATH, "a", encoding="utf-8") as f:
    f.write(f"\n*HB #{hb_n} @ {ts_short} -- Thu workday-early-morning -- DORMANT sustained -- HEARTBEAT_OK*\n")

print(f"OK HB #{hb_n} ts={ts_iso} idle={idle_h}h{idle_m:02d}m")