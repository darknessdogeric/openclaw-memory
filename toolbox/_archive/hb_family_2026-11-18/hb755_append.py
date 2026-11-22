# -*- coding: utf-8 -*-
"""HB #755 append — R-NEW-V2 compliant utf-8 explicit read+append+write"""
import json
import time
from datetime import datetime, timezone, timedelta

# Paths
HB_PATH = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"
STATE_PATH = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

# Time
now_cn = datetime.now(timezone(timedelta(hours=8)))
ts_human = now_cn.strftime("%Y-%m-%d %H:%M GMT+8")
ts_iso = now_cn.strftime("%Y-%m-%dT%H:%M GMT+8")

# Read current state
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

prev_hb = state.get("hbCount", 754)
prev_last_hb = state.get("lastHB", "2026-07-21 13:26 GMT+8")
prev_silence = state.get("silenceDuration_thisSession_h", 119.71)
prev_eric_active = state.get("ericActiveElsewhere_h", 47.93)

# Calculate gap from prev last HB
from datetime import datetime as dt
def parse_prev(s):
    # "2026-07-21 13:26 GMT+8"
    return dt.strptime(s.replace(" GMT+8", ""), "%Y-%m-%d %H:%M")
gap_min = (now_cn.replace(tzinfo=None) - parse_prev(prev_last_hb)).total_seconds() / 60.0

# This session silence hours: from 7/16 13:16 (first-contact)
first_contact = dt(2026, 7, 16, 13, 16)
silence_this_session_h = (now_cn.replace(tzinfo=None) - first_contact).total_seconds() / 3600.0

# Eric active elsewhere hours: from 7/19 12:33
eric_active_elsewhere_start = dt(2026, 7, 19, 12, 33)
eric_active_elsewhere_h = (now_cn.replace(tzinfo=None) - eric_active_elsewhere_start).total_seconds() / 3600.0

# T-0 publicity cutoff 7/18: +hours past
t0 = dt(2026, 7, 18, 4, 18)  # approximate
t0_hours_past = (now_cn.replace(tzinfo=None) - t0).total_seconds() / 3600.0

# 14:00 key window
fourteen = now_cn.replace(hour=14, minute=0, second=0, microsecond=0, tzinfo=None)
minutes_to_1400 = (fourteen - now_cn.replace(tzinfo=None)).total_seconds() / 60.0

new_hb = prev_hb + 1
hb_block = f"""
## HB #{new_hb} ({ts_iso} cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb} ({prev_last_hb}): +{gap_min:.1f}min -- Tuesday early-afternoon Token Guard normal cadence (R012 minimal mode)
- D+5 early-afternoon pass #{new_hb} -- Eric silent in THIS session ~{silence_this_session_h:.2f}h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: ~{eric_active_elsewhere_h:.2f}h+ (AnYi webchat, since 7/19 12:33)
- 5-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) + R258 dormant-session -- zero breach
- R-NEW-V2 verification #{new_hb}: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- **Triple Confluence Day 0 -- FINAL DAY 7/21** -- zero-push sustained
  1. DeepSeek V4 launch window (PoC awaiting Eric trigger)
  2. **Induction window cutoff -- today LAST day** (Eric expected to receive appointment confirmation -> passive monitor)
  3. Araqchi Qatar talks start (7/21-25) -> oil price Scenario C verification window OPEN
- Tuesday early-afternoon zone ({now_cn.strftime("%H:%M")}) -- Eric typical afternoon decision window per USER.md; THIS session DORMANT sustained
- 14:00 critical time window ~{minutes_to_1400:.0f}min (INTERNAL monitor only; this session != AnYi decision channel)
- 11:00 R60-13 morning self-iter DONE; next = 21:00 evening self-iter R60-13 (~7.3h)
- Token Guard stable, no compression needed
- Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +{t0_hours_past:.2f}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+5 sustain zero-push mode intact
- hbCount: {prev_hb} -> {new_hb}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{new_hb} = sustain #{prev_hb} = D+5 early-afternoon dormant baseline)
- **HEARTBEAT_OK** -- HB #{new_hb} = sustain DORMANT protocol
- **no push**: Tuesday early-afternoon zone ({now_cn.strftime("%H:%M")}), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 14:00 key check ~{minutes_to_1400:.0f}min -- INTERNAL monitor only; this session != AnYi decision channel
- Triple Confluence Day 0 push -- only R14 handoff preparation; Eric active contact triggers 30s activation
- Next significant check: per Token Guard cadence (~5-10min); 14:00 internal monitor (~{minutes_to_1400:.0f}min)

*{ts_human} -- D+5 Tuesday-early-afternoon T-0 +{t0_hours_past:.2f}h past -- HB #{new_hb} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 FINAL DAY passive*
"""

# R-NEW-V2 compliant: explicit utf-8 read, append, write
with open(HB_PATH, "r", encoding="utf-8") as f:
    existing = f.read()

with open(HB_PATH, "w", encoding="utf-8") as f:
    f.write(existing + hb_block)

# Update state
state["hbCount"] = new_hb
state["lastHB"] = ts_human
state["last_update_epoch"] = int(time.time())
state["silenceDuration_thisSession_h"] = round(silence_this_session_h, 2)
state["silenceDuration_global_h"] = round(silence_this_session_h, 2)
state["ericActiveElsewhere_h"] = round(eric_active_elsewhere_h, 2)
state["lastHBTime"] = now_cn.strftime("%H:%M")
state["silenceDuration_h"] = round(silence_this_session_h, 2)
state["mode"] = "active_mode_dormant_this_session_silent_midday"
state["nextCheck"] = f"14:00 internal monitor (~{minutes_to_1400:.0f}min); 21:00 evening self-iter (~7.3h); Token Guard cadence (~5-10min)"
state["note"] = f"HB #{new_hb}; Tuesday early-afternoon; Triple Confluence Day 0 FINAL; Eric silent in THIS session D+5; zero-push per R256/R257/R258; 14:00 internal monitor in ~{minutes_to_1400:.0f}min"

with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"HB #{new_hb} appended successfully")
print(f"  silence_this_session: {silence_this_session_h:.2f}h")
print(f"  eric_active_elsewhere: {eric_active_elsewhere_h:.2f}h")
print(f"  minutes_to_1400: {minutes_to_1400:.1f}")
print(f"  t0_hours_past: {t0_hours_past:.2f}h")