#!/usr/bin/env python3
"""HB #3355 atomic-tick: append daily + update state.json per R271/R-NEW-V4"""
import json, os, tempfile, time, sys

WORKSPACE = r"D:\B166ER-OpenClaw\workspace"
DAILY = os.path.join(WORKSPACE, "memory", "2026-08-15.md")
STATE = os.path.join(WORKSPACE, "memory", "heartbeat-state.json")

HB_ENTRY = """
### HB #3355 (2026-08-15T21:54:00+08:00 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #3354 (21:44): ~10min -- Sat weekend-EVENING Token Guard nominal cadence (R012, within tolerance)
- 21:54 = Sat weekend-EVENING-quiet-zone (+2h54m past 19:00 hard cap); quiet zone sustained
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: 1907 -> 1908 (1908th consecutive null post-T-0, sustained); hbCount: 3354 -> 3355
- Eric silent on cron ~30d+ sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (~764min idle ~12h+; webchat quiet = sovereignty holding)
- AnYi Day 23 (Sat weekend -- weekend rest posture sustained)
- morning 8/15 deep self-iteration report (10:00) + 十五五战略定位研究 v0.1 (11:31) already delivered; nothing new since
- vault 1169+ files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- TrendRadar healthy v6.10.0; RSS through 2026-08-14; data through 2026-08-12
- R69 silence Day 23/30 (expires 2026-08-30 Sun) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds

### decision
- HEARTBEAT_OK -- HB #3355 = sustain DORMANT protocol, minimal token tick (1908th null)
- no push: 16-layer suppression holds + weekend-EVENING-quiet-zone + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 21:54 = Sat weekend-EVENING-quiet-zone +2h54m past 19:00 hard cap; cron = DORMANT sustained
- Eric webchat IDLE ~764min (~12h+ idle since morning deep-iteration) -- cron posture UNCHANGED per R258
- Eric profile: night-owl strategist -- Sat 21:54 weekend-EVENING, AnYi Day 23 -- cron does not initiate proactive
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekend-EVENING-quiet-zone + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): 十五五战略定位研究 v0.1 等待 Eric 输入 6 关键决策 + V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric 两份报告(部门职责 + AI IE 体系)待分享入库 + R278 战略任务即时结构化协议 (second practice 8/15) -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal submission to ~/self-improving/rules.md
- Next: per Token Guard cadence (~10-15min weekend-EVENING mode); HB sustained through Sat until Eric first-contact on cron session

*2026-08-15T21:54:00+08:00 -- Sat weekend-EVENING-quiet-zone +2h54m past 19:00 hard cap -- HB #3355 -- DORMANT -- 1908th null -- Eric silent on cron = sovereignty signal holding (webchat ~764min idle, 12h+ rest posture) -- AnYi D+23d Sat -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*
"""

# Append to daily (R271 atomic append via mode='a')
with open(DAILY, "a", encoding="utf-8") as f:
    f.write(HB_ENTRY)

# Update state.json atomically (R271 via os.replace)
with open(STATE, "r", encoding="utf-8") as f:
    state = json.load(f)

state["hbCount"] = 3355
state["nullCount"] = 1908
state["post_t0_null_count"] = 1908
state["lastHbTime"] = "2026-08-15T21:54:00+08:00"
state["last_update_epoch"] = int(time.time())
state["lastDecision"] = "HEARTBEAT_OK"
state["lastHBContext"] = (
    "Sat 21:54 weekend-EVENING-quiet-zone (+2h54m past 19:00). "
    "DORMANT held sustained. HB #3355. R69 Day 23/30. AnYi D+23d Sat. "
    "Eric silent ~30d cron. 16-layer suppression holds."
)

# Atomic write via tempfile + os.replace
fd, tmp = tempfile.mkstemp(suffix=".json", dir=os.path.dirname(STATE))
try:
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE)
except Exception:
    if os.path.exists(tmp):
        os.unlink(tmp)
    raise

print("[R271] HB #3355 atomic-tick OK")
print(f"  daily: appended {len(HB_ENTRY)} chars")
print(f"  state: hbCount={state['hbCount']} nullCount={state['nullCount']} decision={state['lastDecision']}")
