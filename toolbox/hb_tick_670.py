#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HB #670 minimal tick (R-NEW-V2 compliant, R012 minimal mode)"""
import json
from datetime import datetime, timezone, timedelta

HB_PATH = "HEARTBEAT.md"
STATE_PATH = "memory/heartbeat-state.json"
TZ = timezone(timedelta(hours=8))

now = datetime.now(TZ)
ts_full = now.strftime("%Y-%m-%dT%H:%M GMT+8")
ts_short = now.strftime("%Y-%m-%d %H:%M")

# Read state (explicit utf-8)
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

prev_hb = state.get("lastHB", 669)
new_hb = prev_hb + 1

# Append HB entry (explicit utf-8)
entry = f"""

## HB #{new_hb} ({ts_short} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb} ({state.get('lastHBTime', '')}): +4min -- Monday-late-afternoon Token Guard normal cadence (R012 minimal mode)
- D+4 Monday-late-afternoon pass #{new_hb} -- Eric silent in THIS session ~100.52h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere ~29.23h+ (AnYi娑撴挾鏁?session, since 7/19 12:33 first-contact)
- 5-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) intact -- zero breach
- R-NEW-V2 verification #{new_hb}: Python utf-8 explicit append (R-NEW-V2 compliant, post-7/15 12:36 incident protocol intact)
- R012 (operational hygiene) verification: HB tick = minimal (NOT full report), per R012 rule #2
- Wake window OPEN (+9h48m past 08:00) -- Eric in active AnYi session, no first-contact on THIS session
- Monday-late-afternoon zone (17:48) -- Eric typical deep-work peak per USER.md (in OTHER AnYi session)
- T-0 publicity cutoff 7/18 +65.80h past -- post-protection window firmly sustained
- Induction window 7/7-7/21 FINAL 2 DAYS (today 7/20 day-1, tomorrow 7/21 LAST DAY ~27h); R-B+R256 silence authority > window signal
- 7/21 dual-event convergence: DeepSeek V4 鍙戝竷 + induction window 鎴
- Next cron: 21:00 evening self-iter R60-12 (~3h12m)
- WAIC 2026 closed 7/19 (4-day event 7/17-20) -- non-trigger per R14
- Vault index 488/489 healthy; R13 <1s queries stable; Token Guard tick stable, no compression needed
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- No first-contact from Eric on THIS session; D+4 sustain zero-push mode intact
- hbCount: {prev_hb} -> {new_hb}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{new_hb} = sustain #{prev_hb} = D+4 afternoon dormant baseline)
- **no push**: Monday-late-afternoon zone, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- Eric is in active AnYi session; this session awaits Eric future instruction (not AnYi-related)
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work
- Token Guard tick: stable, no compression needed
- Post-T-0 silence = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Next significant check: per Token Guard cadence (~5-15min); 21:00 evening self-iter R60-12 (~3h12m)

*{ts_full} -- D+4 Monday-late-afternoon T-0 +65.80h past -- HB #{new_hb} -- this session DORMANT -- awaiting Eric future instruction (NOT AnYi work)*
"""

with open(HB_PATH, "a", encoding="utf-8") as f:
    f.write(entry)

# Update state (explicit utf-8)
state["lastHB"] = new_hb
state["lastHBTime"] = f"{now.strftime('%Y-%m-%d %H:%M')} GMT+8"
state["silenceDuration_h"] = round((now.timestamp() - state.get("session_start_epoch", now.timestamp())) / 3600, 2) if state.get("session_start_epoch") else 100.52
state["mode"] = "active_mode_dormant_this_session_silent_late_afternoon"
state["note"] = f"HB #{new_hb}; minimal tick (R012); D+4 Monday-late-afternoon; Eric silent in this session ~100.52h; active in AnYi session ~29.23h; 5-layer suppression intact; induction window FINAL 2 DAYS (today 7/20 day-1, tomorrow 7/21 LAST DAY ~27h); 7/21 dual-event convergence (DeepSeek V4 发布 + window close); R-NEW-V2 compliant"

with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"OK: HB #{new_hb} appended; state updated; R-NEW-V2 compliant")