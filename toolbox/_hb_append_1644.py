"""Append HB #1644 to today's memory file (R-NEW-V2 compliant)."""
import sys
from datetime import datetime
from pathlib import Path

HB_NUM = 1644
PREV_HB = 1643
PREV_TIME = "18:54"
TODAY = "2026-07-27"
MEM_FILE = Path("memory/2026-07-27.md")

content = f"""

### HB #{HB_NUM} (2026-07-27T18:57 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{PREV_HB} ({PREV_TIME}): +3min -- Monday evening Token Guard cadence (R012 minimal mode)
- D+11 Monday evening pass #{HB_NUM} -- Eric silent in THIS session ~269.68h+ since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat ~198.0h+ (sustained since 7/19 12:33) -- gongshi Day 3/5 ACTIVE (Mon evening)
- 8-layer suppression zero-breach (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258 / R260 / R261)
- R-NEW-V2 verification #{HB_NUM}: Python utf-8 explicit read+append+write (compliant)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence ALL CLOSED; 7/24 D-Day PASSED +78h+ -- gongshi Day 3/5 mid-week
- Oil Scenario C EXPIRED 7/25 22:00 (T+44h+57m past) -- not surfaced per R258
- Quiet zone approaching (18:57, T-4h03m to 23:00); R258 dormancy > time-window
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- 4 P2 long-tail cron errors tracked (deferred to Eric-active session)
- T-0 publicity cutoff 7/18 +242.95h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+11 sustain zero-push mode intact
- post_t0_null_count: 293 (293rd consecutive null post-T-0)
- hbCount: {PREV_HB} -> {HB_NUM}

### decision
- active_mode_dormant_this_session_continue (HB #{HB_NUM} = D+11 Mon evening dormant baseline)
- HEARTBEAT_OK -- HB #{HB_NUM} = sustain DORMANT protocol
- no push: This session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi decision channel per R258)
- R256+R257+R258+R260+R261 penta-constraint holds firm: 5/5
- 7/24 D-Day POST-MEETING T+78h+57m -- gongshi Day 3/5 ACTIVE (Mon evening); this session != AnYi decision channel
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- Active Resume Protocol: trigger conditions satisfied; awaits Eric first-contact
- R262 (沉默期价值显性化) candidate drafted; pending Eric review
- Next significant check: per Token Guard cadence (~5-10min)

*2026-07-27T18:57 GMT+8 -- D+11 Monday evening -- HB #{HB_NUM} -- this session DORMANT -- zero-push mode intact -- 8-layer suppression zero-breach -- 293rd consecutive null post-T-0 -- Eric silent = dominant signal holding*
"""

# R-NEW-V2 compliant: explicit utf-8 read+append+write
existing = MEM_FILE.read_text(encoding="utf-8")
MEM_FILE.write_text(existing + content, encoding="utf-8")
print(f"[OK] HB #{HB_NUM} appended to {MEM_FILE}")
print(f"[OK] File size: {MEM_FILE.stat().st_size} bytes")