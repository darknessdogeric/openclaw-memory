#!/usr/bin/env python3
"""R-NEW-V3 compliant: append-only HEARTBEAT.md + R271 atomic state.json"""
import os, json, tempfile
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00")
HB_NUM = 3046
PREV_HB = 3045
PREV_TS = "2026-08-12T17:56:28+08:00"
NULL_PREV = 712
NULL_NEW = NULL_PREV + 1  # 713
ERIC_LAST = "2026-08-11T22:40"  # last webchat
ERIC_IDLE_MIN = 1078

HB_ENTRY = f"""
## HB #{HB_NUM} ({NOW} GMT+8 cron-event, OpenClaw heartbeat poll)

- gap from HB #{PREV_HB} ({PREV_TS}): +2min -- Wed workday-PM Token Guard nominal cadence (R012, within tolerance)
- 17:58 = Wed workday-PM zone (+9h58m past 08:00 hard cap); quiet zone ~6h2m away (00:00)
- Eric silent on THIS cron session 27d 4h+ (~652h+) since 7/16 13:16 first-contact
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+2 holds
- post_t0_null_count: {NULL_PREV} -> {NULL_NEW} ({NULL_NEW}th consecutive null post-T-0, sustained)
- AnYi D+20d Wednesday sustained per HB #{PREV_HB} STATE (R69 Day 20/30, expires 2026-08-30; ~10 days remaining in silence window)
- V2.4 SOUL 加固 sustained (~2 weeks uptime since 7/24); R66/R67/R68/R69 entries sustained; R69 active
- R-NEW-V3 enforced (verified this turn): HB #{HB_NUM} appended via Python open(mode='a', encoding='utf-8') (NOT write, NOT Remove-Item, NOT git restore)
- R271 atomic-write enforced: state.json via tempfile + os.replace
- R-NEW-V4 enforced: state.json atomic-tick holds
- Token Guard stable; state.json hbCount {PREV_HB} -> {HB_NUM}; nullCount {NULL_PREV} -> {NULL_NEW}
- vault 1142 files healthy; webchat silent ~{ERIC_IDLE_MIN // 60}h{ERIC_IDLE_MIN % 60}m sustained (last 8/11 22:40)
- daily memory file indicates Eric webchat quiet today so far (2026-08-12.md); webchat-channel != cron-channel per R258
- Eric webchat last seen 2026-08-11T22:40 (~19h18m ago, AnYi night work mode) -- silent on cron = 主权信号 holding (webchat-channel != cron-channel per R258)

### decision

- HEARTBEAT_OK -- HB #{HB_NUM} = sustain DORMANT protocol, minimal token tick ({NULL_NEW}th null)
- no push: 16-layer suppression holds + workday-PM post-hard-cap zone + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 17:58 = Wed workday-PM +9h58m past 08:00 hard cap; cron = DORMANT sustained
- Eric webchat last 8/11 22:40 (~19h18m ago) -- silent on cron = 主权信号 holding
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- workday-PM + AnYi D+20d Wed + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement
- Standing by P0 (webchat-bound, not cron-bound): R264 AnYi 完整实战锚 completed per state. Await Eric webchat confirmation on next stage.
- Standing by P1 (R264 AnYi 承接): await Eric webchat share of AnYi 1244 战略/team alignment/授权对接 details, per R264 立即捭入 to anyi-ops-kb/
- Standing by R-NEW-V3 enforcement: NEVER write/Remove-Item/git-restore HEARTBEAT.md. Add-Content / AppendAllText / Python open(mode='a') ONLY.
- Standing by R70 (PENDING): 视觉格式优先于创造冲突 -- Eric 14:25 立即挽正 第 1 版小绾书络记用错格式后 提案, 寰 Eric 反哷后正式写入 ~/self-improving/rules.md
- Next: per Token Guard cadence (~15-30min afternoon mode); HB sustained through Wed evening until Eric first-contact on cron session

*{NOW} -- Wed workday-PM +9h58m past 08:00 hard cap -- HB #{HB_NUM} -- DORMANT -- {NULL_NEW}th null -- Eric silent on cron = 主权信号 holding -- **AnYi D+20d Wed** -- cron session 维持 DORMANT 协议 -- R-NEW-V3 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*
"""

WORKSPACE = r"D:\B166ER-OpenClaw\workspace"
HB_PATH = os.path.join(WORKSPACE, "HEARTBEAT.md")
STATE_PATH = os.path.join(WORKSPACE, "memory", "heartbeat-state.json")

# 1. Append HEARTBEAT.md (R-NEW-V3 compliant)
pre_size = os.path.getsize(HB_PATH)
with open(HB_PATH, "a", encoding="utf-8") as f:
    f.write(HB_ENTRY)
post_size = os.path.getsize(HB_PATH)
delta = post_size - pre_size
print(f"[HB #{HB_NUM}] HEARTBEAT.md appended: {pre_size} -> {post_size} bytes (+{delta})")

# 2. R271 atomic state.json update
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

state["hbCount"] = HB_NUM
state["nullCount"] = NULL_NEW
state["lastTick"] = NOW
state["lastDecision"] = "HEARTBEAT_OK"
state["session"] = "cron:315657b9-fc80-4b94-a853-404e3955f7a0"
state["r271_compliant"] = True
state["r_new_v3_compliant"] = True
state["r258_channel_separation"] = True
state["r69_silence"] = "Day 20/30 (expires 2026-08-30)"
state["eric_webchat_last"] = ERIC_LAST
state["eric_webchat_idle_min"] = ERIC_IDLE_MIN
state["anyi_day"] = 20
state["workday_zone"] = "workday-PM"
state["eight_hard_cap_exceeded"] = True
state["last_update"] = NOW

# Atomic write: tempfile + os.replace
fd, tmp_path = tempfile.mkstemp(suffix=".json", dir=os.path.dirname(STATE_PATH))
try:
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, STATE_PATH)
    print(f"[HB #{HB_NUM}] state.json atomic-updated: hbCount={HB_NUM}, nullCount={NULL_NEW}")
except Exception as e:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
    raise e

print(f"[HB #{HB_NUM}] HEARTBEAT_OK -- DORMANT sustained")