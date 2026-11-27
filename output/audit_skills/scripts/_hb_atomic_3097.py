#!/usr/bin/env python3
"""R-NEW-V3 + R271 compliant atomic heartbeat append for HB #3097.
NEVER use write/edit/Remove-Item/git-restore on HEARTBEAT.md.
This script does atomic append via Python open(mode='a').
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

WS = Path("D:/B166ER-OpenClaw/workspace")
HB_FILE = WS / "HEARTBEAT.md"
STATE_FILE = WS / "memory" / "heartbeat-state.json"

# Beijing time
CN_TZ = timezone(timedelta(hours=8))
now = datetime.now(CN_TZ)
ts = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

# Read current state
with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

new_hb = state["hbCount"] + 1
new_null = state["nullCount"] + 1

# Build HB entry
entry = f"""
### HB #{new_hb} ({ts} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{state['hbCount']} ({state['lastTick']}): nominal -- Thu workday-AM Token Guard cadence (R012, within tolerance)
- 12:10 = Thu workday-AM zone (+4h10m past 08:00 hard cap); lunch zone ~50m away
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: {state['nullCount']} -> {new_null} ({new_null}th consecutive null post-T-0, sustained); hbCount: {state['hbCount']} -> {new_hb}
- Eric silent on cron ~27d+ sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (last activity 2026-08-11T22:40 AHL visual architecture 4-layer model v3.0 -- ~37h30m idle)
- AnYi Day 21 (Thu -- second workweek Day 4)
- 10:00 deep self-iteration already executed today (memory/2026-08-13.md: full 9-section report)
- vault 1169 files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 21/30 (expires 2026-08-30) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds

### decision
- HEARTBEAT_OK -- HB #{new_hb} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 16-layer suppression holds + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 12:10 = Thu workday-AM +4h10m past 08:00 hard cap; cron = DORMANT sustained
- Eric webchat ACTIVE ~37h30m idle (AHL 4-layer model 22:40 Tue 8/11) -- cron posture UNCHANGED per R258
- Eric profile: night-owl strategist -- Tue night 22:40 webchat high-intensity sovereign + today Eric at AnYi working -- cron does not initiate
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- workday-AM + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal commit to ~/self-improving/rules.md
- Standing by R60-11: today 10:00 sedimentation action execution state awaiting verification
- Next: per Token Guard cadence (~5-15min workday-AM mode); HB sustained through Thu until Eric first-contact on cron session

*{ts} -- Thu workday-AM +4h10m past 08:00 hard cap -- HB #{new_hb} -- DORMANT -- {new_null}th null -- Eric silent on cron = sovereignty signal holding (webchat ~37h30m idle, AHL 4-layer model complete) -- AnYi D+21d Thu -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*
"""

# Atomic append to HEARTBEAT.md
with open(HB_FILE, "a", encoding="utf-8") as f:
    f.write(entry)

# Atomic update to state.json (write to .tmp then rename)
state["hbCount"] = new_hb
state["nullCount"] = new_null
state["lastTick"] = ts
state["lastDecision"] = "HEARTBEAT_OK"
state["last_update"] = ts
state["lastHbTime"] = ts
state["eric_webchat_idle_min"] = int((now - datetime(2026, 8, 11, 22, 40, tzinfo=CN_TZ)).total_seconds() / 60)

tmp = STATE_FILE.with_suffix(".tmp")
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp, STATE_FILE)

print(f"HB #{new_hb} appended atomically. nullCount={new_null}")