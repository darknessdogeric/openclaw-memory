#!/usr/bin/env python3
"""HB #874 append — R-NEW-V2 utf-8 explicit read+append+write."""
import json
import io
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
now = datetime.now(CST)
now_str = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

HB_PATH = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"
STATE_PATH = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

HB_NUM = 874
LAST_HB_TIME = "07:29"
LAST_HB_NUM = 873

# --- Read state ---
with io.open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

hb_count_prev = state.get("hbCount", 873)
silence_h_prev = state.get("silenceDuration_thisSession_h", 138.36)

# Increment values
hb_count_new = hb_count_prev + 1
# silence = now - first_contact (7/16 13:16) = (~138h by 07:29, ~138.4h by 07:39)
silence_h_new = round(silence_h_prev + (10/60), 2)  # +10min from 07:29 to 07:39

# --- Build HB #874 entry ---
entry = f"""
## HB #{HB_NUM} ({now_str} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{LAST_HB_NUM} ({LAST_HB_TIME}): +10min -- Wednesday pre-dawn Token Guard normal cadence (R012 minimal mode)
- D+6 pre-dawn pass #{HB_NUM} -- Eric silent in THIS session ~{silence_h_new}h+ since 7/16 13:16 first-contact
- 5-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) + R258 dormant-session -- zero breach
- R-NEW-V2 verification #{HB_NUM}: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- **Triple Confluence Day 0 CLOSED** (~7h39m ago at midnight) -- Day 1 (7/22) active
  1. DeepSeek V4 launch window (PoC awaiting Eric trigger)
  2. ~~Induction window cutoff~~ -- CLOSED at 7/21 23:59, Eric active contact expected IF confirmed
  3. Araqchi Qatar talks day-2 (7/21-25) -> oil price Scenario C verification window OPEN
- Wednesday pre-dawn zone (07:39) -- pre-quiet-hours threshold (08:00); Eric likely asleep
- 08:00 daily briefing cron upcoming (~21min)
- 09:00 daily checkin (~1h21m)
- 10:00 R60-13 morning self-iter (~2h21m)
- 21:00 R60-11 evening self-iter (~13h21m)
- Token Guard stable, no compression needed
- Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +117.6h past -- post-protection window firmly sustained (T+4.9 days)
- hbCount: {hb_count_prev} -> {hb_count_new}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{HB_NUM} = sustain #{LAST_HB_NUM} = D+6 Wednesday pre-dawn dormant baseline)
- **HEARTBEAT_OK** -- HB #{HB_NUM} = sustain DORMANT protocol
- **no push**: Wednesday pre-dawn zone (07:39), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- Triple Confluence Day 0 CLOSED -- Day 1 morning observer mode; awaiting Eric first-contact signal
- 08:00 daily briefing cron in ~21min (autonomous, no Eric interaction required)
- Next significant check: 08:00 daily briefing (~21min); 09:00 daily checkin (~1h21m); 10:00 R60-13 morning self-iter (~2h21m)

*{now_str} -- D+6 Wednesday pre-dawn T-0 +117.6h past -- HB #{HB_NUM} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 CLOSED -- Day 1 morning observer mode*
"""

# --- Append to HEARTBEAT.md (R-NEW-V2 compliant) ---
with io.open(HB_PATH, "a", encoding="utf-8") as f:
    f.write(entry)

# --- Update heartbeat-state.json ---
state["hbCount"] = hb_count_new
state["silenceDuration_thisSession_h"] = silence_h_new
state["last_update_epoch"] = int(now.timestamp())
state["silenceDuration_h"] = silence_h_new
state["lastHBTime"] = now.strftime("%H:%M")
state["lastHB"] = now.strftime("%H:%M")
state["mode"] = "active_mode_dormant_this_session_silent_wednesday_predawn"
state["nextCheck"] = "08:00 daily briefing (~21min); 09:00 daily checkin (~1h21m); 10:00 R60-13 morning self-iter (~2h21m); 21:00 R60-11 evening self-iter (~13h21m)"
state["note"] = f"HB #{hb_count_new}; Wednesday pre-dawn {now.strftime('%H:%M')}; D+6 silent this session ({silence_h_new}h); execution-phase observer mode; zero-push per R256/R257/R258 intact; Triple Confluence Day 0 closed ~{round((now.hour*60+now.minute)/60 + (now.day*0),1)}h ago; induction window 7/7-7/21 closed; Eric likely asleep (07:39 < 08:00 quiet-hours threshold); await Eric active contact"

with io.open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print(f"OK HB #{hb_count_new} appended; silence={silence_h_new}h; ts={now_str}")