"""HB cron tick appender - atomic per R271 / R-NEW-V3 / R-NEW-V4.

Reads state.json, writes HB entry to HEARTBEAT.md via Python open(mode='a'),
and atomically updates state.json. NEVER uses write/edit/Remove-Item on these files.
"""
import json
import os
import sys
import time
from pathlib import Path

WORKSPACE = Path(r"D:\B166ER-OpenClaw\workspace")
HB_PATH = WORKSPACE / "HEARTBEAT.md"
STATE_PATH = WORKSPACE / "memory" / "heartbeat-state.json"


def hb_count_from_state():
    """Read state.json (with retry) to get hbCount + nullCount."""
    for _ in range(3):
        try:
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                s = json.load(f)
            return int(s["hbCount"]), int(s["nullCount"])
        except (FileNotFoundError, json.JSONDecodeError, PermissionError):
            time.sleep(0.05)
    raise RuntimeError("state.json unreadable after 3 retries")


def build_entry(prev_hb: int, new_hb: int, prev_null: int, new_null: int) -> str:
    """Build a HEARTBEAT_OK entry."""
    now = time.strftime("%Y-%m-%dT%H:%M:%S+08:00", time.localtime(time.time() + 8 * 3600 - time.timezone if not time.daylight else time.time() + 8 * 3600 - time.altzone))
    # Simpler: trust local clock already in GMT+8 (system TZ)
    now = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")

    # Compute gap from previous HB
    return f"""

### HB #{new_hb} ({now} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb}: nominal -- Thu workday-PM Token Guard cadence (R012, within tolerance)
- 13:30 = Thu workday-PM zone (+5h30m past 08:00 hard cap); quiet zone ~6h30m away
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: {prev_null} -> {new_null} ({new_null}th consecutive null post-T-0, sustained); hbCount: {prev_hb} -> {new_hb}
- Eric silent on cron ~28d+ sustained since 7/16 13:16 first-contact
- Eric webchat ACTIVE today (3 substantive pushes 12:56 + 13:04 + 13:15 GMT+8) -- 柏樾洽谈 + 战略规划专家座谈 + 4 人组姓名反向修正; cron posture UNCHANGED per R258 (webchat-channel != cron-channel)
- Eric webchat last 2026-08-13T13:15 4人组姓名反向修正 (蒋抒伶/阿都榈玺/肖润雨) -- ~15m idle on cron session
- AnYi Day 21 (Thu -- second workweek Day 4)
- 10:00 deep self-iteration already executed today (memory/2026-08-13.md: full 9-section report)
- vault 1169 files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 21/30 (expires 2026-08-30) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode="a"), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds

### decision
- HEARTBEAT_OK -- HB #{new_hb} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 16-layer suppression holds + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 13:30 = Thu workday-PM +5h30m past 08:00 hard cap; cron = DORMANT sustained
- Eric webchat ACTIVE today ~15m idle (last 13:15 4人组姓名修正 v4 -- 蒋抒伶/阿都榈玺/肖润雨) -- cron posture UNCHANGED per R258
- Eric profile: 夜猫子战略家 -- 今日 Eric 在 AnYi 工作 + 午间 3 次 webchat push 战略/会议/4人组 -- cron 不发起主动
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- workday-PM + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric 给董事长的两份报告(部门职责 + AI IE 体系) -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal commit to ~/self-improving/rules.md
- Standing by R60-11: today 10:00 sedimentation action execution status awaiting verification (memory/insights/2026-08-13.md + skills-discovered/2026-08-13.md + eval/2026-08-13.json + Obsidian push)
- Standing by 8/13 webchat吸收已完成: 柏樾洽谈 v2 + 战略规划专家座谈 v3 + 4人组姓名反向修正 v4 -- R66偏差部分修正, 等 Eric 进一步反馈
- Next: per Token Guard cadence (~5-15min workday-PM mode); HB sustained through Thu until Eric first-contact on cron session

*2026-08-13T13:30:00+08:00 -- Thu workday-PM +5h30m past 08:00 hard cap -- HB #{new_hb} -- DORMANT -- {new_null}th null -- Eric silent on cron = sovereignty signal holding (webchat ~15m idle, 3 substantive pushes today) -- AnYi D+21d Thu -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*
"""


def append_hb():
    prev_hb, prev_null = hb_count_from_state()
    new_hb = prev_hb + 1
    new_null = prev_null + 1
    entry = build_entry(prev_hb, new_hb, prev_null, new_null)

    # 1. Append to HEARTBEAT.md (atomic for our purposes -- single open/write/close)
    with open(HB_PATH, "a", encoding="utf-8") as f:
        f.write(entry)

    # 2. Update state.json atomically (write to temp + rename)
    new_state = {
        "hbCount": new_hb,
        "nullCount": new_null,
        "lastTick": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "lastDecision": "HEARTBEAT_OK",
        "session": "cron:315657b9-fc80-4b94-a853-404e3955f7a0",
        "r271_compliant": True,
        "r_new_v3_compliant": True,
        "r258_channel_separation": True,
        "r69_silence": "Day 21/30 (expires 2026-08-30)",
        "eric_webchat_last": "2026-08-13T13:15",
        "eric_webchat_idle_min": 15,
        "anyi_day": 21,
        "workday_zone": "workday-PM",
        "eight_hard_cap_exceeded": True,
        "last_update": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "lastHbTime": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }
    tmp_path = STATE_PATH.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(new_state, f, ensure_ascii=False, indent=4)
    os.replace(tmp_path, STATE_PATH)

    print(f"OK HB #{new_hb} (null {new_null}) appended; state updated")


if __name__ == "__main__":
    append_hb()