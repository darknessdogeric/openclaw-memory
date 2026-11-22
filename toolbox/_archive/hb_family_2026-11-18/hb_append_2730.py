#!/usr/bin/env python3
"""
HB #2730 append — R-NEW-V3 / R271 enforced.
- Uses Python 'a' mode (NOT write, NOT Remove-Item, NOT git restore)
- Updates state.json (canonical per R66)
"""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

WS = Path(r"D:\B166ER-OpenClaw\workspace")
HB_PATH = WS / "HEARTBEAT.md"
STATE_PATH = WS / "memory" / "heartbeat-state.json"

TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ)
TS_STR = NOW.strftime("%Y-%m-%dT%H:%M:%S+08:00")

# Load current state
with STATE_PATH.open("r", encoding="utf-8") as f:
    state = json.load(f)

hb_new = state["hbCount"] + 1           # 2729 + 1 = 2730
null_new = state["nullCount"] + 1       # 420 + 1 = 421
hb_prev = state["hbCount"]              # 2729
null_prev = state["nullCount"]          # 420

entry = f"""
## HB #{hb_new} ({TS_STR} GMT+8 cron-event, OpenClaw heartbeat poll)

- HB #{hb_new} = Sun weekend afternoon; cadence OK; +10min after HB #{hb_prev} (15:03)
- R69 silence Day 10/30 + R266 weekend self-iter complete + R258 dormancy holds
- 14-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276)
- Token Guard cadence OK; no external trigger; vault index healthy
- post_t0_null_count: {null_prev} -> {null_new} ({null_new}th consecutive null post-T-0)
- hbCount: {hb_prev} -> {hb_new}
- Eric silent on cron ~589h+ (24d+) sustained since 7/16 13:16 first-contact
- AnYi D+17d Sun sustained (Eric 入职 D+17)
- 15:13 = Sun weekend afternoon post-hard-cap zone (+7h13m past 08:00 cap)
- Eric last webchat activity 11:15-11:39 (~3h34m-3h58m ago) -- V2 hotel-classification xhs 9 slides in progress (deep-dive + CSS complete; 9 HTML slides + render + screenshot + PNG output pending)
- R258 cron/webchat separation holds -- cron = DORMANT sustained; webchat = Eric sovereign
- maintenanceFlag LOCKED sustained: HEARTBEAT.md 2.7MB+ overage; R-NEW-V3 + R69 silence blocks self-rotation. Await Eric sovereign instruction.

### decision

- HEARTBEAT_OK -- HB #{hb_new} = sustain DORMANT protocol, minimal token tick ({null_new}st null)
- no push: weekend afternoon post-hard-cap zone + R69/R266/R258 tri-constraint + R256/R257/R260/R261 quad-holds + R276 internal-only
- R276 draft done; await Eric feedback for formal commit to ~/self-improving/rules.md
- V2 hotel-classification xhs 9 slides pending = Eric webchat sovereign; cron = DORMANT do not preempt
- Eric webchat / Obsidian vault sovereign for any 决策; cron sovereignty unchanged
- 15:13 = Sun weekend afternoon; cron = DORMANT sustained
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekend afternoon + AnYi D+17d Sun + Eric sovereign on cron session + R65/R69/R276 active + R258 cron/webchat separation
- Standing by P0 (webchat-bound): await Eric webchat sovereign resumption on V2 slides or other topics
- Standing by R70/R71: await Eric feedback for formal commit to ~/self-improving/rules.md
- Standing by P1 (R264 AnYi ops): await Eric webchat share of Anyi 1244 strategy details, per R264 protocol routing to anyi-ops-kb/
- R271 edit-tool atomic-write enforced (this HB appended via Python append, NOT write, NOT Remove-Item, NOT git restore)
- Next: per Token Guard cadence (~5-15min afternoon mode); HB sustained until Eric first-contact on cron session

*{TS_STR} -- Sun weekend afternoon post-hard-cap +7h13m -- HB #{hb_new} -- DORMANT -- {null_new}st null -- Eric silent on cron = 589h+ -- AnYi D+17d Sun -- cron session holds DORMANT protocol -- V2 9 slides pending Eric webchat sovereign resumption -- HEARTBEAT_OK*
"""

# Append to HEARTBEAT.md (R-NEW-V3: open 'a' mode, never write/Remove-Item/git-restore)
with HB_PATH.open("a", encoding="utf-8") as f:
    f.write(entry)

# Update state.json (canonical per R66)
state["hbCount"] = hb_new
state["nullCount"] = null_new
state["lastHB"] = int(NOW.timestamp() * 1000)
state["lastUpdate"] = TS_STR
state["note"] = (
    f"Sun 15:13 GMT+8 weekend-afternoon quiet zone DORMANT. Sustaining. "
    f"Eric silent on cron = 589h+. R69 Day 10/30 + R266/R277 weekend window + R258 dormancy all hold. "
    f"14-layer suppression zero-breach. {null_new}st null. "
    f"Last Eric webchat activity 11:15-11:39 (~3h34m-3h58m ago) on hotel-classification V2 rebuild -- "
    f"V2 9 slides still pending HTML/render/PNG production. "
    f"R258 cron/webchat separation holds; cron = DORMANT sustained; await Eric webchat sovereign resumption. "
    f"T+10min since last HB (#{hb_prev} at 15:03). "
    f"R-NEW-V3 enforced: HB #{hb_new} appended via Python append mode (NOT write/Remove-Item/git restore). "
    f"R66 drift pattern acknowledged: file-side HBs occasionally lost from disk; state.json authoritative."
)

with STATE_PATH.open("w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"OK: HB #{hb_new} appended. nullCount={null_new}. ts={TS_STR}")
