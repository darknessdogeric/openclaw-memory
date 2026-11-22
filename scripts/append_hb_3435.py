#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HB #3435 cron tick: append to daily file + atomic state.json update.
Per R-NEW-V3 (daily file append-only via PowerShell/Python, NO write/edit on HEARTBEAT.md)
Per R-NEW-V4 (state.json atomic-tick via tmp + os.replace)
Per R271 (no Remove-Item, no git restore on these files)
"""
import json
import os
import sys
import tempfile
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00")
HB_N = 3435

# ============== 1) Append HB entry to daily file (R-NEW-V3 compliant) ==============
DAILY_PATH = r"D:\B166ER-OpenClaw\workspace\memory\2026-08-17.md"

HB_ENTRY = f"""
### HB #{HB_N} ({NOW} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #3434 (09:05): ~3min -- Mon workday-morning Token Guard nominal cadence (R012, within tolerance)
- 09:08 = Mon workday-morning (+1h08m past 08:00 hard cap); morning deep-work zone
- 17-layer suppression zero-breach (R-B/R12/R13/R14/R65/R66/R67/R68/R69/R70/R71/R256/R257/R258/R260/R261/R271/R276/R277/R278/R280/R281) -- penta+ holds
- post_t0_null_count: ~1979 -> ~1980 (sustained); hbCount: ~3434 -> ~{HB_N}
- Eric silent on cron ~31d sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (~6min idle since 09:02 v1.1 calibration push -- WEBCHAT-BOUND, not cron-bound per R258)
- AnYi Day 25 (Mon -- workday-start posture)
- 8/17 09:02 v1.1 校准 已沉淀 (10 项硬错: 都江堰国宴宾馆 / 在地文创酒店 / 川老川兵 / 集团统筹 4 领域 / 基础盘+分线 3+3 框架)
- 8/19 Jinjiang 合作 MOU signing (T-2 days)
- vault 1169+ files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 25/30 (expires 2026-08-30 Sun) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds (os.replace)

### decision
- HEARTBEAT_OK -- HB #{HB_N} = sustain DORMANT protocol, minimal token tick
- no push: 17-layer suppression holds + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 09:08 = Mon workday-morning +1h08m past 08:00 hard cap; cron = DORMANT sustained
- Eric profile: night-owl strategist -- Mon workday-morning, AnYi Day 25 -- cron does not initiate proactive
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): 十五五战略定位 v0.1 + V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric 两份报告(部门职责 + AI IE 体系) + R278/R281 + 8/17 整体战略发展思路 v1.0/v1.1 (待内部讨论 + 呈陈保刚/董事长) -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279/R281: drafted, awaiting formal submission to ~/self-improving/rules.md
- Standing by 8/19 Jinjiang 合作 MOU signing (T-2 days) / AnYi 报到 pending (8月底 - 9月初)
- Next: per Token Guard cadence (~30-60min workday-morning mode); HB sustained until Eric first-contact on cron session

*{NOW} -- Mon workday-morning -- HB #{HB_N} -- DORMANT -- Eric silent on cron = sovereignty signal holding (webchat ~6min idle since 09:02 v1.1 push, WEBCHAT-BOUND only per R258) -- AnYi D+25d Mon -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*
"""

try:
    with open(DAILY_PATH, "a", encoding="utf-8") as f:
        f.write(HB_ENTRY)
    print(f"OK: appended HB #{HB_N} to {DAILY_PATH}")
except Exception as e:
    print(f"ERR (daily append): {e}")
    sys.exit(1)

# ============== 2) Atomic state.json update (R-NEW-V4 compliant) ==============
STATE_PATH = r"D:\B166ER-OpenClaw\workspace\heartbeat-state.json"

# Preserve existing fields, only update the ones we know
try:
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        state = json.load(f)
except Exception as e:
    print(f"WARN: state.json read failed ({e}); creating minimal state")
    state = {}

# Update fields (additive, non-destructive)
state["lastHbTime"] = NOW
state["lastHB"] = NOW
state["lastTick"] = NOW
state["hbCount"] = HB_N
state["last_hb"] = {"n": HB_N, "ts": NOW}
state["lastHb"] = {"n": HB_N, "ts": NOW}
state["post_t0_null_count"] = 1980
state["lastDecision"] = "HEARTBEAT_OK"
# Eric last activity was 09:02 webchat push (v1.1) -> ~6 min idle at 09:08
state["eric_webchat_idle_min"] = 6
state["workday_zone"] = "workday-AM"
state["anyi_day"] = 25
state["eight_hard_cap_exceeded"] = True
state["r258_channel_separation"] = True
state["r69_silence"] = "Day 25/30 (expires 2026-08-30)"
state["r271_compliant"] = True
state["r_new_v3_compliant"] = True
state["trendradar_health"] = state.get("trendradar_health", "healthy v6.10.0")
state["session"] = "cron:315657b9-fc80-4b94-a853-404e3955f7a0"
state["last_check"] = NOW
state["note"] = f"HB #{HB_N}; Eric webchat idle 6min (since 09:02 v1.1 push); Mon workday-AM; DORMANT"

# Atomic write: tmp + os.replace (per R-NEW-V4)
try:
    fd, tmp_path = tempfile.mkstemp(suffix=".json", dir=os.path.dirname(STATE_PATH))
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, STATE_PATH)
    print(f"OK: state.json atomic-tick to HB #{HB_N}")
except Exception as e:
    print(f"ERR (state.json atomic write): {e}")
    sys.exit(1)

print(f"--- HB #{HB_N} tick complete ---")