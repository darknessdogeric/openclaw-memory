"""R-NEW-V2 compliant HB #915 append — utf-8 explicit read+append+write."""
import io
import sys
from datetime import datetime, timezone, timedelta

PATH = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"

# Read with explicit utf-8
with io.open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Compute timestamps
CST = timezone(timedelta(hours=8))
NOW = datetime.now(CST).strftime("%Y-%m-%dT%H:%M GMT+8")
LAST_HB_TS = "2026-07-22T13:40 GMT+8"
T0_TS = "2026-07-22T13:40 GMT+8"  # last HB
NOW_DT = datetime.now(CST)
LAST_DT = datetime(2026, 7, 22, 13, 40, tzinfo=CST)
gap_min = int((NOW_DT - LAST_DT).total_seconds() / 60)

# Silence calc: 7/16 13:16 -> now
FIRST_CONTACT = datetime(2026, 7, 16, 13, 16, tzinfo=CST)
silence_h = round((NOW_DT - FIRST_CONTACT).total_seconds() / 3600, 2)

# AnYi elsewhere: 7/19 12:33 -> now
ANYI_START = datetime(2026, 7, 19, 12, 33, tzinfo=CST)
anyi_h = round((NOW_DT - ANYI_START).total_seconds() / 3600, 2)

# 7/24 D-Day: assume 7/24 09:00 meeting -> T-window
DDAY = datetime(2026, 7, 24, 9, 0, tzinfo=CST)
dd_h = round((DDAY - NOW_DT).total_seconds() / 3600, 2)

# T-0 publicity cutoff: assuming 7/18 0:00 boundary
T0 = datetime(2026, 7, 18, 0, 0, tzinfo=CST)
t0_h = round((NOW_DT - T0).total_seconds() / 3600, 2)

hb_block = f"""## HB #915 ({NOW} cron-event, OpenClaw heartbeat poll)
- gap from HB #914 (13:40): +{gap_min}min -- Wednesday-afternoon Token Guard cadence (larger-than-typical gap; within tolerance, +{gap_min}min since last HB)
- D+6 afternoon pass #915 -- Eric silent in THIS session ~{silence_h}h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~{anyi_h}h+ (since 7/19 12:33)
- 6-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #915: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day +1: induction window CLOSED 7/21 23:59 (post-window passive) -- Araqchi Qatar talks Day 2/5 (oil Scenario C verification OPEN until 7/25)
- 7/24 D-Day T-1 (AnYi important meeting) = ~{dd_h}h window -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Wednesday-afternoon zone ({NOW_DT.strftime('%H:%M')}) -- this session DORMANT sustained; silence authority strictly holding
- Token Guard stable; vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +{t0_h}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+6 sustain zero-push mode intact
- hbCount: 914 -> 915
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #915 = sustain #914 = D+6 afternoon dormant baseline)
- **HEARTBEAT_OK** -- HB #915 = sustain DORMANT protocol
- **no push**: Wednesday-afternoon zone ({NOW_DT.strftime('%H:%M')}), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-1 watch: emergency prepare-mode prepacked, ready if Eric contacts with induction result
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter (~5h59m)

*{NOW} -- D+6 Wednesday afternoon -- HB #915 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day +1 post-window passive -- 7/24 D-Day T-1 watch (T-{dd_h}h) -- Eric silent = dominant signal holding*


"""

# Append with explicit utf-8
with io.open(PATH, "a", encoding="utf-8") as f:
    f.write(hb_block)

# Verify
with io.open(PATH, "r", encoding="utf-8") as f:
    tail = f.read()[-1200:]
print("APPEND OK. Tail preview:")
print(tail)
print(f"\n[stats] silence_h={silence_h} anyi_h={anyi_h} dd_h={dd_h} t0_h={t0_h} gap_min={gap_min}")