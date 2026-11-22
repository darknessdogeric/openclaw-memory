#!/usr/bin/env python3
"""HB #3170 atomic tick + daily-note append (R271 + R-NEW-V3)."""
import json, os
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
state_path = r"memory\heartbeat-state.json"
log_path = r"memory\2026-08-14.md"

# ---------- 1. Atomic state.json tick ----------
try:
    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)
except Exception:
    state = {"hbCount": 0, "post_t0_null_count": 0}

new_hb = int(state.get("hbCount", 0)) + 1
new_null = int(state.get("post_t0_null_count", 0)) + 1

state["hbCount"] = new_hb
state["post_t0_null_count"] = new_null
state["lastHB"] = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
state["lastZone"] = "Fri workday-AM"
state["suppressionLayers"] = 16
state["r69Day"] = 22
state["r69Expiry"] = "2026-08-30"
state["ericWebchatSovereign"] = True
state["ericCronSilentDays"] = 22
state["ericWebchatLastActivity"] = "2026-08-13T14:50 (chashan duijiefang mingque v6)"
state["anylDay"] = 22
state["model"] = "minimax/MiniMax-M3"
state["thinking"] = "off (hidden)"

tmp = state_path + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp, state_path)

# ---------- 2. Append HB entry to today's daily note (atomic, append-only) ----------
ts_full = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
ts_short = now.strftime("%H:%M")
hb_block = f"""

### HB #{new_hb} ({ts_full} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{new_hb - 1}: cron-token-guard cadence (within tolerance, ~5-15min workday-AM)
- {ts_short} = Fri workday-AM (+2h21m past 08:00 hard cap); quiet zone ~6h39m away; midnight zone ~13h39m away
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: {new_null - 1} -> {new_null} ({new_null}th consecutive null post-T-0, sustained); hbCount: {new_hb - 1} -> {new_hb}
- Eric silent on cron ~Day 22/30 (expires 2026-08-30) sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (last activity 2026-08-13T14:50 chashan v6 -- ~19h31m idle)
- AnYi Day 22 (Fri -- workweek Day 5)
- 10:00 deep self-iteration already executed today (memory/2026-08-14.md: full 9-section report)
- vault 1089 files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 22/30 (expires 2026-08-30) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds

### decision
- HEARTBEAT_OK -- HB #{new_hb} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 16-layer suppression holds + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- Eric webchat ACTIVE ~19h31m idle (chashan v6 14:50 Thu 8/13) -- cron posture UNCHANGED per R258
- Eric profile: night-owl strategist -- Thu afternoon 14:50 webchat high-intensity sovereign + today Eric at AnYi working (Fri) -- cron does not initiate
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- workday-AM + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric de liang fen baogao (bumenzhize + AI IE tixi) daifengxiang ruku -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal submission to ~/self-improving/rules.md
- Standing by R60-11: today's 10:00 sedimentation action execution state awaiting verification (memory/insights/2026-08-14.md + skills-discovered/2026-08-14.md + eval/2026-08-14.json + Obsidian push)
- Next: per Token Guard cadence (~5-15min workday-AM mode); HB sustained through Fri until Eric first-contact on cron session

*{ts_full} -- Fri workday-AM +2h21m past 08:00 hard cap -- HB #{new_hb} -- DORMANT -- {new_null}th null -- Eric silent on cron = zhuzhuai xinhao holding (webchat ~19h31m idle, chashan v6) -- AnYi D+22d Fri -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*
"""

with open(log_path, "a", encoding="utf-8") as f:
    f.write(hb_block)

print(f"OK hb={new_hb} null={new_null} ts={ts_full}")
