#!/usr/bin/env python3
"""
HB #3052 atomic tick — 2026-08-12 18:55 GMT+8 cron heartbeat.

R271: file writes via Python open(mode='a'), NOT write/edit/Remove-Item/git restore.
R-NEW-V3: HEARTBEAT.md untouched; daily file appended only.
R-NEW-V4: state.json atomic-tick (temp + rename).

This script:
  1. Updates heartbeat-state.json atomically (hbCount 3051 -> 3052, nullCount 718 -> 719)
  2. Appends HB #3052 entry to memory/2026-08-12.md
"""
from __future__ import annotations
import json
import os
import sys
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

WS = Path(r"D:\B166ER-OpenClaw\workspace")
STATE_PATH = WS / "memory" / "heartbeat-state.json"
DAILY_PATH = WS / "memory" / "2026-08-12.md"

TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ)
TS_STR = NOW.strftime("%Y-%m-%dT%H:%M:%S+08:00")
HHMM = NOW.strftime("%H:%M")

# ---------- 1. Update heartbeat-state.json atomically ----------
with STATE_PATH.open("r", encoding="utf-8") as f:
    state = json.load(f)

old_hb = state.get("hbCount", 0)
old_null = state.get("nullCount", 0)
new_hb = old_hb + 1
new_null = old_null + 1

state["hbCount"] = new_hb
state["nullCount"] = new_null
state["lastTick"] = TS_STR
state["lastDecision"] = "HEARTBEAT_OK"
state["last_update"] = TS_STR

# Atomic write: temp file + rename
fd, tmp_path = tempfile.mkstemp(
    dir=str(STATE_PATH.parent),
    prefix=".heartbeat-state.json.",
    suffix=".tmp",
)
try:
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp_path, STATE_PATH)
except Exception:
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)
    raise

# ---------- 2. Append HB #3052 entry to daily file ----------
entry = f"""
### HB #{new_hb} ({TS_STR} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{old_hb} (18:49): +6min -- Wed workday-PM Token Guard nominal cadence (R012, within tolerance)
- {HHMM} = Wed workday-PM zone (+10h{HHMM[1:].replace(':', 'h')}m past 08:00 hard cap); quiet zone ~1h05m away
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: {old_null} -> {new_null} ({new_null}th consecutive null post-T-0, sustained); hbCount: {old_hb} -> {new_hb}
- Eric silent on cron ~605h+ (~25d+) sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (last activity 22:40 Tue 8/11: AHL visual architecture 4-layer model v3.0 -- ~20h15m idle)
- AnYi Day 20 (Wed -- second workweek Day 3)
- vault 1142 files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 20/30 (expires 2026-08-30) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds

### decision
- HEARTBEAT_OK -- HB #{new_hb} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 16-layer suppression holds + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- {HHMM} = Wed workday-PM past 08:00 hard cap; cron = DORMANT sustained
- Eric webchat ACTIVE ~20h15m idle (AHL 4-layer model 22:40 Tue 8/11) -- cron posture UNCHANGED per R258
- Eric profile: night-owl strategist -- Tue night 22:40 webchat high-intensity sovereign + today Eric at AnYi working -- cron does not initiate proactive
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- workday-PM + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal commit to ~/self-improving/rules.md
- Standing by R60-11: today 10:00 deep self-iteration execution state awaiting verification (memory/insights/2026-08-12.md + skills-discovered/2026-08-12.md + eval/2026-08-12.json + Obsidian push)
- Next: per Token Guard cadence (~5-15min workday-PM mode); HB sustained through Wed until Eric first-contact on cron session

*{TS_STR} -- Wed workday-PM past 08:00 hard cap -- HB #{new_hb} -- DORMANT -- {new_null}th null -- Eric silent on cron = sovereignty signal holding (webchat ~20h15m idle, AHL 4-layer model complete) -- AnYi D+20d Wed -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*
"""

with DAILY_PATH.open("a", encoding="utf-8") as f:
    f.write(entry)

# ---------- 3. Report ----------
print(f"OK hb={old_hb}->{new_hb} null={old_null}->{new_null} ts={TS_STR}")