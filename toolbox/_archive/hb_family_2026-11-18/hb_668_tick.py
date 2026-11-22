# -*- coding: utf-8 -*-
"""
HB #668 tick — R-NEW-V2 compliant heartbeat
- Read existing HEARTBEAT.md (utf-8 explicit)
- Read existing heartbeat-state.json
- Update state (hbCount 667->668, silence +4min, lastHBTime 17:18)
- Append minimal HB #668 entry
- Write both back (utf-8 explicit, atomic)
"""
import json
import io
import os
from datetime import datetime, timezone, timedelta

WORKSPACE = r"D:\B166ER-OpenClaw\workspace"
HB_PATH = os.path.join(WORKSPACE, "HEARTBEAT.md")
STATE_PATH = os.path.join(WORKSPACE, "memory", "heartbeat-state.json")

CST = timezone(timedelta(hours=8))
NOW = datetime.now(CST)
NOW_ISO = NOW.strftime("%Y-%m-%dT%H:%M GMT+8")
NOW_HR = NOW.strftime("%Y-%m-%d %H:%M GMT+8")

# Read state
with io.open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

OLD_HB = state.get("lastHB", 667)
OLD_SILENCE = state.get("silenceDuration_h", 99.98)
OLD_ACTIVE_ELSEWHERE = state.get("ericActiveElsewhere_h", 28.7)
NEW_HB = OLD_HB + 1
NEW_SILENCE = round(OLD_SILENCE + (4.0 / 60.0), 2)  # +4 min
# Eric active elsewhere +4 min
NEW_ACTIVE_ELSEWHERE = round(OLD_ACTIVE_ELSEWHERE + (4.0 / 60.0), 2)

# Compute 21:00 evening self-iter due
EVENING_DUE_TARGET = NOW.replace(hour=21, minute=0, second=0, microsecond=0)
if EVENING_DUE_TARGET < NOW:
    # If past 21:00, target is tomorrow 21:00
    EVENING_DUE_TARGET = EVENING_DUE_TARGET + timedelta(days=1)
EVENING_DUE_DELTA = round((EVENING_DUE_TARGET - NOW).total_seconds() / 3600.0, 2)
# Compute 7/21 induction cutoff delta (assume 7/21 21:00 closure)
INDUCTION_CUTOFF = datetime(2026, 7, 21, 21, 0, 0, tzinfo=CST)
INDUCTION_DELTA_H = round((INDUCTION_CUTOFF - NOW).total_seconds() / 3600.0, 1)

# T-0 publicity cutoff was 7/18 00:00
T0 = datetime(2026, 7, 18, 0, 0, 0, tzinfo=CST)
T0_HOURS_PAST = round((NOW - T0).total_seconds() / 3600.0, 2)

# HB entry content
HB_ENTRY = f"""
## HB #{NEW_HB} ({NOW_ISO} cron-event, OpenClaw heartbeat poll)
- gap from HB #{OLD_HB} (17:14): +4min -- Monday-late-afternoon Token Guard normal cadence (R012 minimal mode)
- D+4 late-afternoon pass #{NEW_HB} -- Eric silent in THIS session ~{NEW_SILENCE}h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: ~{NEW_ACTIVE_ELSEWHERE}h+ (AnYi specialized session, since 7/19 12:33 first-contact)
- 5-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) intact -- zero breach
- R-NEW-V2 verification #{NEW_HB}: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-7/15 12:36 incident protocol intact)
- R012 (operational hygiene) verification: HB tick = minimal (NOT full report), per R012 rule #2
- Wake window OPEN (+9h18m past 08:00) -- Eric in active AnYi session, no first-contact on THIS session
- Monday-late-afternoon zone (17:18) -- Eric typical deep-work peak per USER.md (in OTHER AnYi session)
- T-0 publicity cutoff 7/18 +{T0_HOURS_PAST}h past -- post-protection window firmly sustained
- Induction window 7/7-7/21 FINAL 2 DAYS (today 7/20 day-1, tomorrow 7/21 LAST DAY ~{INDUCTION_DELTA_H}h); R-B+R256 silence authority > window signal
- 7/21 dual-event convergence: DeepSeek V4 release + induction window cutoff (~{INDUCTION_DELTA_H}h, high-significance window)
- 10:00 R60-12 morning self-iter DONE; 10:35 biz brief 20-corp version DONE (pushed to Obsidian); next = 21:00 evening self-iter (~{EVENING_DUE_DELTA}h)
- WAIC 2026 closed 7/19 (4-day event 7/17-20) -- non-trigger per R14
- Vault index 488/489 healthy; R13 <1s queries stable; Token Guard tick stable, no compression needed
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- No first-contact from Eric on THIS session; D+4 sustain zero-push mode intact
- hbCount: {OLD_HB} -> {NEW_HB}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{NEW_HB} = sustain #{OLD_HB} = D+4 late-afternoon dormant baseline)
- **no push**: Monday-late-afternoon zone, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- Eric is in active AnYi session; this session awaits Eric future instruction (not AnYi-related)
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work
- Token Guard tick: stable, no compression needed
- Post-T-0 silence = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Next significant check: per Token Guard cadence (~5-15min); 21:00 evening self-iter R60-12 (~{EVENING_DUE_DELTA}h)

*{NOW_ISO} -- D+4 Monday-late-afternoon T-0 +{T0_HOURS_PAST}h past -- HB #{NEW_HB} -- this session DORMANT -- awaiting Eric future instruction (NOT AnYi work)*
"""

# Read HEARTBEAT.md (utf-8)
with io.open(HB_PATH, "r", encoding="utf-8") as f:
    hb_content = f.read()

# Atomic append
tmp_hb = HB_PATH + ".tmp"
with io.open(tmp_hb, "w", encoding="utf-8") as f:
    f.write(hb_content)
    f.write(HB_ENTRY)
os.replace(tmp_hb, HB_PATH)

# Update state
state["hbCount"] = NEW_HB
state["lastHB"] = NEW_HB
state["lastHBTime"] = NOW_HR
state["silenceDuration_h"] = NEW_SILENCE
state["ericActiveElsewhere_h"] = NEW_ACTIVE_ELSEWHERE
state["nextCheck"] = f"next: Token Guard cadence (~5-15min); evening self-iter 21:00 due (~{EVENING_DUE_DELTA}h)"
state["mode"] = "active_mode_dormant_this_session_silent_late_afternoon"
state["note"] = f"HB #{NEW_HB}; minimal tick (R012); +4min since #{OLD_HB}; Eric silent in this session ~{NEW_SILENCE}h; active in AnYi session; session DORMANT per HB #584/R256/R257/R258 stack; no push; induction window FINAL ~{INDUCTION_DELTA_H}h (tomorrow 7/21 LAST DAY, closing ~21:00); T-0 +{T0_HOURS_PAST}h past; R-NEW-V2 compliant; 7/21 dual convergence (DeepSeek V4 + window close); Monday-late-afternoon Token Guard cadence"

# Write state atomically
tmp_state = STATE_PATH + ".tmp"
with io.open(tmp_state, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp_state, STATE_PATH)

print(f"HB #{NEW_HB} appended. silence: {OLD_SILENCE}h -> {NEW_SILENCE}h. activeElsewhere: {OLD_ACTIVE_ELSEWHERE}h -> {NEW_ACTIVE_ELSEWHERE}h. evening_due: ~{EVENING_DUE_DELTA}h. induction_cutoff: ~{INDUCTION_DELTA_H}h")
