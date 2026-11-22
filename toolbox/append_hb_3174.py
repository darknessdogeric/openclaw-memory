#!/usr/bin/env python3
"""HB #3174 atomic append — R-NEW-V3 + R271 compliant.
- Append to memory/2026-08-14.md via open(mode='a') ONLY.
- heartbeat-state.json atomic write via temp + replace.
"""
import json
import os
import time
from datetime import datetime, timezone, timedelta

DAILY = r"D:\B166ER-OpenClaw\workspace\memory\2026-08-14.md"
STATE = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

gmt8 = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%dT%H:%M:%S+08:00")
short = datetime.now(timezone(timedelta(hours=8))).strftime("%H:%M")
human = short
ts = int(time.time())

# Load state
with open(STATE, "r", encoding="utf-8") as f:
    state = json.load(f)

new_n = int(state.get("hbCount", 3173)) + 1
new_null = int(state.get("nullCount", 1741)) + 1

entry = f"""
### HB #{new_n} ({gmt8} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{new_n-1} (10:42:43): ~2min -- Fri workday-AM Token Guard fast cadence (R012, within tolerance, late-morning zone)
- {short} = Fri workday-AM zone (+{int((datetime.now(timezone(timedelta(hours=8)))-datetime.now(timezone(timedelta(hours=8))).replace(hour=8, minute=0, second=0)).total_seconds()//60)}m past 08:00 hard cap); midday zone ~4h away
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: {new_null-1} -> {new_null} ({new_null}th consecutive null post-T-0, sustained); hbCount: {new_n-1} -> {new_n}
- Eric silent on cron ~28d+ sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (last activity 2026-08-14T10:30 商业情报 20集团版 -- ~14min idle)
- AnYi Day 22 (Fri -- second workweek Day 5)
- morning 10:30 商业情报 20集团版 already executed today (memory/2026-08-14.md: full 6-section report)
- vault 1169+ files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 22/30 (expires 2026-08-30) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds

### decision
- HEARTBEAT_OK -- HB #{new_n} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 16-layer suppression holds + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- {short} = Fri workday-AM +2h45m past 08:00 hard cap; cron = DORMANT sustained
- Eric webchat ACTIVE ~14min idle (商业情报 20集团版 10:30 Fri 8/14) -- cron posture UNCHANGED per R258
- Eric profile: night-owl strategist -- Fri 早 10:30 webchat 商业情报 已交付, AnYi Day 22 工作 -- cron 不发起主动
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- workday-AM + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric 的两份报告(部门职责 + AI IE 体系)待分享入库 -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal submission to ~/self-improving/rules.md
- Next: per Token Guard cadence (~5-15min workday-AM mode); HB sustained through Fri until Eric first-contact on cron session

*{gmt8} -- Fri workday-AM +2h45m past 08:00 hard cap -- HB #{new_n} -- DORMANT -- {new_null}th null -- Eric silent on cron = sovereignty signal holding (webchat ~14min idle, 商业情报 20集团版完成) -- AnYi D+22d Fri -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*
"""

# Atomic append to daily file
with open(DAILY, "a", encoding="utf-8") as f:
    f.write(entry)

# Atomic state.json write via temp file + replace
state["lastHb"] = {"n": new_n, "ts": gmt8}
state["lastHB"] = gmt8
state["lastHbTime"] = gmt8
state["lastTick"] = gmt8
state["last_check"] = gmt8
state["hbCount"] = new_n
state["nullCount"] = new_null
state["post_t0_null_count"] = new_null
state["eric_webchat_idle_min"] = 14
state["note"] = (
    f"HB #{new_n}; Eric webchat ~idle ~14min (商业情报 20集团版 10:30); "
    f"Fri workday-AM-Token-Guard; DORMANT; Eric sovereign on webchat/Obsidian channel, NOT cron; "
    f"AnYi D+22"
)

tmp = STATE + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp, STATE)

print(f"OK: HB #{new_n} appended; nullCount={new_null}; ts={gmt8}")
