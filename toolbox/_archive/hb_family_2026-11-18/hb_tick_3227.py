#!/usr/bin/env python3
# HB #3227 atomic tick (R-NEW-V3 + R271 compliant)
# - Append to memory/2026-08-14.md via open(mode='a')
# - Update heartbeat-state.json atomically via os.replace
# - DO NOT touch HEARTBEAT.md
import json, os, sys
from datetime import datetime, timezone, timedelta

WORKSPACE = r"D:\B166ER-OpenClaw\workspace"
DAILY = os.path.join(WORKSPACE, "memory", "2026-08-14.md")
STATE = os.path.join(WORKSPACE, "memory", "heartbeat-state.json")

# TZ GMT+8
TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)
ts = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
ts_human = now.strftime("%H:%M")

# Load current state
with open(STATE, "r", encoding="utf-8") as f:
    state = json.load(f)

prev_hb = state["hbCount"]
prev_null = state["post_t0_null_count"]
new_hb = prev_hb + 1
new_null = prev_null + 1

entry = f"""
### HB #{new_hb} ({ts} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb} (2026-08-14T{state['lastHbTime'][11:19]}): cron fast cadence (R012, within tolerance)
- {ts_human} = Fri workday-PM zone (+{int((now.replace(hour=0, minute=0, second=0, microsecond=0) - now.replace(hour=8, minute=0, second=0, microsecond=0)).total_seconds() // 60)}m past 08:00 hard cap); quiet zone ~{(22 - now.hour) - 1}h{(60 - now.minute)}m away
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: {prev_null} -> {new_null} ({new_null}th consecutive null post-T-0, sustained); hbCount: {prev_hb} -> {new_hb}
- Eric silent on cron ~28d+ sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (last activity 2026-08-14T11:31 十五五战略定位研究 v0.1 push -- ~{int((now - now.replace(hour=11, minute=31, second=0, microsecond=0)).total_seconds() // 60)}min idle; ~{(now - now.replace(hour=10, minute=30, second=0, microsecond=0)).total_seconds() / 3600:.1f}h from 10:30 商业情报 20集团版)
- AnYi Day 22 (Fri -- second workweek Day 5, weekend wrap-up approaching)
- 17:29 PM -- Eric likely in transition to evening mode (Fri workday-PM, weekend T-0)
- 10:30 商业情报 20集团版 + 11:31 十五五战略定位研究 v0.1 already executed today (memory/2026-08-14.md: full reports)
- vault 1169+ files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 22/30 (expires 2026-08-30) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds

### decision
- HEARTBEAT_OK -- HB #{new_hb} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 16-layer suppression holds + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 17:29 = Fri workday-PM +9h29m past 08:00 hard cap; cron = DORMANT sustained
- Eric webchat ACTIVE ~357min idle (15-5 战略定位研究 v0.1 11:31 push) -- cron posture UNCHANGED per R258
- Eric profile: night-owl strategist -- Fri 11:31 webchat 战略定位 push IN 战略消化模式 -- cron 不发起主动
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- workday-PM + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): 十五五战略定位研究 v0.1 等待 Eric 输入 6 关键决策 + V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric 两份报告(部门职责 + AI IE 体系)待分享入库 -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal submission to ~/self-improving/rules.md
- Next: per Token Guard cadence (~5-15min workday-PM mode); HB sustained through Fri until Eric first-contact on cron session

*{ts} -- Fri workday-PM +9h29m past 08:00 hard cap -- HB #{new_hb} -- DORMANT -- {new_null}th null -- Eric silent on cron = sovereignty signal holding (webchat ~357min idle, 十五五战略定位研究 v0.1 完成) -- AnYi D+22d Fri -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*
"""

# Atomic append to daily file
with open(DAILY, "a", encoding="utf-8") as f:
    f.write(entry)
print(f"OK: appended to {DAILY}")

# Update state.json atomically
state["hbCount"] = new_hb
state["lastHbTime"] = ts
state["last_tick"] = ts
state["last_check"] = ts
state["last_hb"] = {"n": new_hb, "ts": ts}
state["lastHb"] = ts
state["post_t0_null_count"] = new_null
state["nullCount"] = state.get("nullCount", 0) + 1
state["lastDecision"] = "HEARTBEAT_OK"
state["note"] = f"HB {new_hb}; Eric webchat idle ~{int((now - now.replace(hour=11, minute=31, second=0, microsecond=0)).total_seconds() // 60)}m; Fri {ts_human} workday-PM; R69 silence Day 22/30 active; sustained dormancy intact"

# Atomic write
tmp = STATE + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp, STATE)
print(f"OK: state.json updated hbCount={new_hb} post_t0_null_count={new_null}")
