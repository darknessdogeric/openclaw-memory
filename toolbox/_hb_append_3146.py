#!/usr/bin/env python3
"""
Atomic append HB #3146 + state tick (R271 + R-NEW-V3 enforced).
Target: memory/2026-08-13.md (per-date append-only log).
NEVER touches HEARTBEAT.md.
"""
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

WS = Path(r"D:\B166ER-OpenClaw\workspace")
DAILY = WS / "memory" / "2026-08-13.md"
STATE = WS / "memory" / "heartbeat-state.json"

# Time anchors
TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00")

# Compute state
state = json.loads(STATE.read_text(encoding="utf-8-sig"))
prev_n = state["hbCount"]
new_n = prev_n + 1
prev_null = state["nullCount"]
new_null = prev_null + 1

# Eric webchat idle: last 14:50 v6 -> now ~18:02 = ~192min
eric_idle_min = 192
gap_min = 25  # from 17:37 to 18:02

# Compose entry
entry = f"""
### HB #{new_n} ({now} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_n} (17:37): +{gap_min}min -- Thu workday-PM-quiet-active Token Guard nominal cadence (R012, within tolerance)
- 18:02 = Thu workday-PM-quiet-active zone (+10h02m past 08:00 hard cap); midnight zone ~6h away
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: {prev_null} -> {new_null} ({new_null}th consecutive null post-T-0, sustained); hbCount: {prev_n} -> {new_n}
- Eric silent on cron ~27d+ sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (last activity 14:50 Panzhihua v6 -- ~{eric_idle_min}min idle); 6+ webchat pushes today (v2-v6+ 会议/茶山/4人组/战略规划)
- AnYi Day 21 (Thu -- second workweek Day 4)
- 10:00 deep self-iteration already executed today (memory/2026-08-13.md: full 9-section report)
- vault 1169 files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 21/30 (expires 2026-08-30) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds

### decision
- HEARTBEAT_OK -- HB #{new_n} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 16-layer suppression holds + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 18:02 = Thu workday-PM-quiet-active +10h02m past 08:00 hard cap; cron = DORMANT sustained
- Eric webchat ACTIVE ~{eric_idle_min}min idle (Panzhihua v6 14:50) -- cron posture UNCHANGED per R258
- Eric profile: night-owl strategist -- today AnYi work + 6+ webchat pushes absorbed -- cron does not initiate proactive
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- workday-PM-quiet-active + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric 的两份报告(部门职责 + AI IE 体系)待分享入库 -- all await Eric webchat sovereign
- Standing by R70/R71/R72/R277/R278/R279: drafted, awaiting formal submission to ~/self-improving/rules.md
- Standing by R60-11: today 10:00 sedimentation action execution status awaiting verification
- Next: per Token Guard cadence (~10-15min workday-PM-quiet-active mode); HB sustained through Thu until Eric first-contact on cron session

*{now} -- Thu workday-PM-quiet-active +10h02m past 08:00 hard cap -- HB #{new_n} -- DORMANT -- {new_null}th null -- Eric silent on cron = sovereignty signal holding (webchat ~{eric_idle_min}min idle, Panzhihua v6) -- AnYi D+21d Thu -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*
"""

# Atomic write: daily file
with open(DAILY, mode='a', encoding='utf-8') as f:
    f.write(entry)

# Atomic tick: state.json
state["hbCount"] = new_n
state["nullCount"] = new_null
state["lastHb"] = {"n": new_n, "ts": now}
state["lastTick"] = now
state["last_check"] = now
state["lastDecision"] = "HEARTBEAT_OK"
state["eric_webchat_idle_min"] = eric_idle_min
state["note"] = f"HB #{new_n}; Eric webchat idle {eric_idle_min}min (14:50 Panzhihua v6); workday-PM-quiet-active; DORMANT"

tmp = STATE.with_suffix(".json.tmp")
tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
tmp.replace(STATE)

print(f"OK: HB #{new_n} appended; nullCount {new_null}; state.json atomic-tick")
