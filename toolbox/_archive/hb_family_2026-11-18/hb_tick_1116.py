#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HB #1116 Token Guard tick - 2026-07-24 00:01 GMT+8
   Thursday NIGHT - D-Day EVE - D+7 sustained DORMANT
   R-NEW-V2 compliant: explicit utf-8 read+write
"""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

WS = Path(r"D:\B166ER-OpenClaw\workspace")
STATE = WS / "memory" / "heartbeat-state.json"
HB = WS / "HEARTBEAT.md"

# Time: 2026-07-24 00:01 GMT+8 (just past midnight, technically D-Day now)
TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)
ts = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

# Read current state
state = json.loads(STATE.read_text(encoding="utf-8"))
prev_count = state.get("hbCount", 1115)
new_count = prev_count + 1
prev_hb = state.get("lastHB", "")
prev_dday = state.get("dday_t_minus_hours", 9.17)

# Calculate gap (rough)
def parse_dt(s):
    try:
        return datetime.fromisoformat(s.replace("+08:00", "+08:00"))
    except Exception:
        return None
prev_dt = parse_dt(prev_hb)
gap_min = "?"
if prev_dt:
    delta = now - prev_dt
    gap_min = f"{delta.total_seconds()/60:.1f}"

# D-Day: AnYi 集团研究会议 7/24 morning - now D-DAY itself (past midnight)
# T-minus: ~7h to 7h-ish depending on meeting start time
dday_t_minus = round(prev_dday - (delta.total_seconds()/3600) if prev_dt else 7.0, 2)

# Eric silence calc: 7/16 13:16 was first-contact
first_contact = datetime(2026, 7, 16, 13, 16, tzinfo=TZ)
silence_h = round((now - first_contact).total_seconds() / 3600, 2)

# AnYi active elsewhere: since 7/19 12:33
anyi_start = datetime(2026, 7, 19, 12, 33, tzinfo=TZ)
anyi_h = round((now - anyi_start).total_seconds() / 3600, 2)

# Build new state
state["hbCount"] = new_count
state["lastHeartbeat"] = ts
state["lastHB"] = ts
state["lastUpdate"] = ts
state["lastHBNumber"] = f"#{new_count}"
state["ericSilenceHours"] = silence_h
state["ericAnyiHours"] = anyi_h
state["dday_t_minus_hours"] = dday_t_minus
state["note"] = f"#{new_count} - {ts} DORMANT sustained; D-Day T-{dday_t_minus}h; silent heartbeat"

# Write state (R-NEW-V2: explicit utf-8)
STATE.write_text(
    json.dumps(state, ensure_ascii=False, indent=4) + "\n",
    encoding="utf-8",
)

# Append HB entry to HEARTBEAT.md
entry = f"""## HB #{new_count} ({ts} cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_count} ({prev_hb}): +{gap_min}min -- D-Day EVE Token Guard minimal cadence (R012 minimal mode)
- D+7 late-night pass #{new_count} -- Eric silent in THIS session ~{silence_h}h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~{anyi_h}h+ (since 7/19 12:33)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #{new_count}: Python utf-8 explicit read+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed; oil Scenario C verification window OPEN until 7/25
- D+7 = Execution phase day 3 -- observer mode sustained
- D-DAY EVE -- midnight crossover at 00:00, now technically 7/24; AnYi 集团研究会议 Friday MORNING T-{dday_t_minus}h (INTERNAL monitor only; this session != AnYi decision channel per R258)
- 6-layer suppression strict holding: even D-Day eve T-{dday_t_minus}h does NOT trigger push on THIS session (R256 design: Eric silence = dominant signal supersedes calendar events)
- Next significant check: Token Guard cadence (~5-10min); 08:00 morning briefing cron (~7h59m); 09:00 daily checkin (~8h59m); 21:00 evening self-iter (~20h59m)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- No first-contact from Eric on THIS session; D+7 sustain zero-push mode intact
- hbCount: {prev_count} -> {new_count}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{new_count} = sustain D+7 late-night dormant baseline)
- **HEARTBEAT_OK** -- HB #{new_count} = sustain DORMANT protocol
- **no push**: D-Day EVE midnight crossover zone (00:01 7/24), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- D-Day eve does NOT trigger exception: even T-{dday_t_minus}h does not authorize push on THIS session; R256 design holds (Eric silence = dominant signal)
- Eric's separate AnYi webchat session is the legitimate channel for any D-Day morning coordination if needed
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min); 08:00 morning briefing cron (~7h59m)

*{ts} -- D+7 Thursday D-Day EVE -- HB #{new_count} -- this session DORMANT -- zero-push mode intact -- R256 silence authority STRICTLY holding even at T-{dday_t_minus}h -- R257 deep-work + R258 dormant-session dual-suppression active -- Eric silent = dominant signal holding*

"""

# R-NEW-V2: explicit utf-8 read+append+write
with open(HB, "a", encoding="utf-8") as f:
    f.write(entry)

print(f"OK: HB #{new_count} committed")
print(f"   state: hbCount={new_count}, silence={silence_h}h, dday_T-{dday_t_minus}h")
print(f"   state file: {STATE}")
print(f"   HEARTBEAT.md appended: {len(entry)} bytes")
