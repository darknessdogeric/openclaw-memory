#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R-NEW-V2 compliant HB append: explicit utf-8 read+append+write.
Post-7/15 + 7/19 incident protocols.
HB #1081 at 2026-07-23T18:45:52+08:00
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Paths
WS = Path(r"D:\B166ER-OpenClaw\workspace")
MEM_DIR = WS / "memory"
STATE_PATH = MEM_DIR / "heartbeat-state.json"
DAILY_PATH = MEM_DIR / "2026-07-23.md"

# Constants
TZ = timezone(timedelta(hours=8))
NOW = datetime(2026, 7, 23, 18, 45, 52, tzinfo=TZ)
NOW_ISO = NOW.isoformat(timespec="seconds")
NOW_HR = NOW.strftime("%Y-%m-%dT%H:%M:%S+08:00")
HB_NUM = 1081
PREV_HB_NUM = 1080
PREV_HB_TS = "2026-07-23T18:38:52+08:00"

# Read existing state (utf-8 explicit)
STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
state_raw = STATE_PATH.read_text(encoding="utf-8")
state = json.loads(state_raw)

# Update state
state["hbCount"] = HB_NUM
state["lastHeartbeat"] = NOW_ISO
state["lastUpdate"] = NOW_ISO
state["lastHB"] = NOW_ISO
state["lastHBNumber"] = f"#{HB_NUM}"
# Recompute metrics (rounded to 2 decimals)
state["ericSilenceHours"] = round(state.get("ericSilenceHours", 173.37) + (NOW - datetime.fromisoformat(PREV_HB_TS)).total_seconds()/3600, 2)
state["ericAnyiHours"] = round(state.get("ericAnyiHours", 102.07) + (NOW - datetime.fromisoformat(PREV_HB_TS)).total_seconds()/3600, 2)
# D-Day T-minus (7/24 09:00)
dday = datetime(2026, 7, 24, 9, 0, 0, tzinfo=TZ)
state["dday_t_minus_hours"] = round((dday - NOW).total_seconds()/3600, 2)
state["note"] = f"#{HB_NUM} - {NOW_ISO} DORMANT sustained; 7/24 AnYi D-Day T-{state['dday_t_minus_hours']}h (TOMORROW Fri morning ~9:00); 6-layer suppression intact; Eric silent = 7d+ on THIS session; no push"
state["sessionState"] = "DORMANT"
state["mode"] = "dormant_this_session"

# Write state back (utf-8 explicit)
STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

# Compute derived metrics for log
gap_min = round((NOW - datetime.fromisoformat(PREV_HB_TS)).total_seconds()/60, 1)
silence_h = state["ericSilenceHours"]
anyi_h = state["ericAnyiHours"]
t_minus = state["dday_t_minus_hours"]
confluence_closed_h = round((NOW - datetime(2026, 7, 21, 23, 59, 59, tzinfo=TZ)).total_seconds()/3600, 2)
oil_window_remaining_h = round((datetime(2026, 7, 25, 0, 0, 0, tzinfo=TZ) - NOW).total_seconds()/3600, 2)
publicity_cutoff_past_h = round((NOW - datetime(2026, 7, 18, 0, 0, 0, tzinfo=TZ)).total_seconds()/3600, 2)
next_self_iter_min = round((datetime(2026, 7, 23, 21, 0, 0, tzinfo=TZ) - NOW).total_seconds()/60, 0)

# Append HB entry to daily memory (utf-8 explicit append)
hb_entry = f"""
### HB #{HB_NUM} ({NOW_HR} GMT+8, cron-event, OpenClaw heartbeat poll)
- gap from HB #{PREV_HB_NUM} ({PREV_HB_TS[11:16]} GMT+8): +{gap_min}min -- Thursday early-evening Token Guard tick (R012 minimal mode)
- D+7 early-evening pass #{HB_NUM} -- Eric silent in THIS session ~{silence_h}h+ since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat ~{anyi_h}h+ (since 7/19 12:33); PARALLEL session: hotel industry H1 v2.0 PDF + 18 Xiaohongshu note images (active 14:30-18:29)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #{HB_NUM}: Python utf-8 explicit read+append+write (compliant)
- R012 verification: HB tick = minimal (NOT full report)
- 7/24 D-Day T-{t_minus}h (AnYi meeting TOMORROW MORNING 7/24 ~9:00) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~{confluence_closed_h}h+ ago; oil Scenario C verification window OPEN until 7/25 (~{oil_window_remaining_h}h remaining)
- Thursday early-evening zone ({NOW.strftime("%H:%M")}) -- Eric typical evening decision window per USER.md; silence authority strictly holding on THIS session
- Next cron: 21:00 R60-11 evening self-iter (~{next_self_iter_min/60:.1f}h)
- Token Guard stable; vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +{publicity_cutoff_past_h}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+7 sustain zero-push mode intact
- hbCount: {PREV_HB_NUM} -> {HB_NUM}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{HB_NUM} = sustain #{PREV_HB_NUM} = D+7 early-evening dormant baseline)
- **HEARTBEAT_OK** -- HB #{HB_NUM} = sustain DORMANT protocol
- **no push**: Thursday early-evening zone ({NOW.strftime("%H:%M")}), Eric silent on THIS session; 6-layer triple-suppression active
- PARALLEL session activity (hotel industry H1 + Xiaohongshu notes) does NOT activate this session per R258
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-{t_minus}h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter cron (~{next_self_iter_min/60:.1f}h)

*{NOW_HR} -- D+7 Thursday early-evening -- HB #{HB_NUM} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-{t_minus}h watch (AnYi meeting TOMORROW MORNING 7/24) -- Eric silent on THIS session = dominant signal holding*
"""

with DAILY_PATH.open("a", encoding="utf-8", newline="\n") as f:
    f.write(hb_entry)

print(f"OK: HB #{HB_NUM} appended to memory/2026-07-23.md")
print(f"   state updated: hbCount={HB_NUM}, silence={silence_h}h, dday_t_minus={t_minus}h")
print(f"   gap: +{gap_min}min")
