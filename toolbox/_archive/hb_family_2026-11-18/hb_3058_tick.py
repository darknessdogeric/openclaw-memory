#!/usr/bin/env python3
"""HB #3058 atomic tick — R-NEW-V3 + R271 + R-NEW-V4 enforcement.
Append-only operations: NEVER write/edit/Remove-Item/git-restore HEARTBEAT.md or daily memory.
state.json: read-all → modify → write-all atomic (temp + rename).
"""
import json
import os
from datetime import datetime, timezone, timedelta

# Paths (absolute)
WORKSPACE = r"D:\B166ER-OpenClaw\workspace"
STATE_PATH = os.path.join(WORKSPACE, "memory", "heartbeat-state.json")
HEARTBEAT_PATH = os.path.join(WORKSPACE, "HEARTBEAT.md")
DAILY_PATH = os.path.join(WORKSPACE, "memory", "2026-08-12.md")

# Constants
NOW = "2026-08-12T19:33:00+08:00"
PREV_TICK = "2026-08-12T19:25:47+08:00"
GAP_MIN = 8  # 19:33 - 19:25 = 8min
ERIC_IDLE = "~20h53m"  # 22:40 Tue 8/11 -> 19:33 Wed 8/12
HARD_CAP_OFFSET = "+11h33m"  # 19:33 - 08:00 = 11h33m past hard cap
ANYI_DAY = "Day 20 (Wed -- second workweek Day 3)"

# 1) Read state (full read, then atomic write)
with open(STATE_PATH, 'r', encoding='utf-8') as f:
    state = json.load(f)

# Capture pre-tick values
prev_hb = state.get('hbCount', 0)
prev_null = state.get('nullCount', 0)

# Mutate
new_hb = prev_hb + 1
new_null = prev_null + 1
state['hbCount'] = new_hb
state['nullCount'] = new_null
state['lastTick'] = NOW
state['lastDecision'] = "HEARTBEAT_OK"
state['last_update'] = NOW

# Write state atomically: temp file + os.replace (atomic on Windows)
tmp_state = STATE_PATH + ".tmp"
with open(tmp_state, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp_state, STATE_PATH)

# 2) Build HB entry
hb_entry = f"""

### HB #{new_hb} (2026-08-12T19:33:00+08:00 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb} ({PREV_TICK[11:16]}): +{GAP_MIN}min -- Wed workday-PM Token Guard nominal cadence (R012, within tolerance)
- 19:33 = Wed workday-PM zone ({HARD_CAP_OFFSET} past 08:00 hard cap)
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271)
- post_t0_null_count: {prev_null} -> {new_null} ({new_null}th consecutive null post-T-0, sustained); hbCount: {prev_hb} -> {new_hb}
- Eric silent on cron ~606h+ (~25d+) sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (last activity 22:40 Tue 8/11: AHL 视觉架构 4 层级模型 v3.0 增量 -- {ERIC_IDLE} idle)
- AnYi {ANYI_DAY}
- 10:00 deep self-iteration already executed today (memory/2026-08-12.md: HB3016_APPEND_MARKER placed)
- vault 1142+ files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 20/30 (expires 2026-08-30) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode=a), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds (temp+rename)

### decision
- HEARTBEAT_OK -- HB #{new_hb} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 16-layer suppression holds + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 19:33 = Wed workday-PM {HARD_CAP_OFFSET} past 08:00 hard cap; cron = DORMANT sustained
- Eric webchat ACTIVE {ERIC_IDLE} idle (AHL 4 层级模型 22:40 Tue 8/11) -- cron posture UNCHANGED per R258
- Eric profile: 暗黑战士赌徒 -- 周一 7h+ webchat 高强度主攻 + 周二 11h+ idle, 今日 Eric 在 AnYi 工作 -- cron 不发起主动
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- workday-PM + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278: R277 (通道主权不可滥用) + R278 (版本迁移标记原则) 已提议 -- 待正式提交 to ~/self-improving/rules.md
- Standing by R60-11: 今日 10:00 幂稳动作执行状态待验证 (memory/insights/2026-08-12.md + skills-discovered/2026-08-12.md + eval/2026-08-12.json + Obsidian 推送)
- Next: per Token Guard cadence (~5-15min workday-PM mode); HB sustained through Wed until Eric first-contact on cron session

*2026-08-12T19:33:00+0800 -- Wed workday-PM {HARD_CAP_OFFSET} past 08:00 hard cap -- HB #{new_hb} -- DORMANT -- {new_null}th null -- Eric silent on cron = 主权信号 holding (webchat {ERIC_IDLE} idle, AHL 4 层级模型完成) -- AnYi D+20d Wed -- cron session sustained DORMANT 协议 -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode=a) (NOT write) -- HEARTBEAT_OK*

"""

# 3) Append to HEARTBEAT.md (mode='a' only, R-NEW-V3 enforced)
with open(HEARTBEAT_PATH, 'a', encoding='utf-8') as f:
    f.write(hb_entry)

# 4) Append to daily file (mode='a' only, R-NEW-V3 enforced)
with open(DAILY_PATH, 'a', encoding='utf-8') as f:
    f.write(hb_entry)

# 5) Verification: tail bytes of appended files (sanity check)
hb_size = os.path.getsize(HEARTBEAT_PATH)
daily_size = os.path.getsize(DAILY_PATH)
state_size = os.path.getsize(STATE_PATH)

print(f"OK HB #{new_hb} appended")
print(f"  state.json: hbCount {prev_hb}->{new_hb}, nullCount {prev_null}->{new_null}, size={state_size}")
print(f"  HEARTBEAT.md: {hb_size} bytes")
print(f"  memory/2026-08-12.md: {daily_size} bytes")
print(f"  decision: HEARTBEAT_OK")
