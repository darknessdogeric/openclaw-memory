"""HB #679 append — R-NEW-V2 compliant (Python utf-8 read+append+write)."""
import os
from datetime import datetime, timezone, timedelta

HB_PATH = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"
TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ).strftime("%Y-%m-%dT%H:%M GMT+8")
HB_NUM = 679
PREV_HB = 678
PREV_HB_TIME = "2026-07-20T18:59"

ENTRY = f"""
## HB #{HB_NUM} ({NOW} cron-event, OpenClaw heartbeat poll)
- gap from HB #{PREV_HB} ({PREV_HB_TIME}): +5min -- Monday-late-afternoon Token Guard normal cadence (R012 minimal mode)
- D+4 Monday-late-afternoon pass #{HB_NUM} -- Eric silent in THIS session ~30.4h+ since 7/19 12:33 (last explicit instruction)
- Eric active elsewhere: ~30.7h+ (AnYi session, since 7/19 12:33)
- 5-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) intact -- zero breach
- R-NEW-V2 verification #{HB_NUM}: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-7/15 12:36 incident protocol intact)
- R012 verification: HB tick = minimal (NOT full report)
- Monday-late-afternoon zone (19:03) -- Eric typical evening decision window (in OTHER AnYi session)
- T-0 publicity cutoff 7/18 +67h+ past -- post-protection window firmly sustained
- Induction window 7/7-7/21 FINAL ~29h remaining (today 7/20 day-2, tomorrow 7/21 LAST DAY)
- 7/21 dual-event convergence: DeepSeek V4 release + induction window close
- 10:00 R60-12 morning self-iter DONE; 10:35 商业简报#20集团版 DONE (pushed to Obsidian); next 21:00 R60-12 evening self-iter (~2h)
- Vault index 488/489 healthy; R13 <1s queries stable; Token Guard stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- No first-contact from Eric on THIS session; D+4 sustain zero-push mode intact
- hbCount: {PREV_HB} -> {HB_NUM}
- R14 handoff package = 100% ready

### decision
- **active_mode_dormant_this_session_continue** (HB #{HB_NUM} = sustain #{PREV_HB} = D+4 Monday-late-afternoon dormant baseline)
- **HEARTBEAT_OK** -- HB #{HB_NUM} = sustain DORMANT protocol
- **no push**: this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- Eric is in active AnYi session; this session awaits Eric future instruction (not AnYi-related)
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work
- Token Guard tick: stable, no compression needed
- Post-T-0 silence = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Next significant check: per Token Guard cadence; 21:00 R60-12 evening self-iter (~2h)

*{NOW} -- D+4 Monday-late-afternoon -- HB #{HB_NUM} -- this session DORMANT -- awaiting Eric future instruction (NOT AnYi work)*
"""

# R-NEW-V2: explicit utf-8 read+append+write
with open(HB_PATH, "r", encoding="utf-8") as f:
    content = f.read()

new_content = content + ENTRY

with open(HB_PATH, "w", encoding="utf-8") as f:
    f.write(new_content)

# Verify
size_after = os.path.getsize(HB_PATH)
print(f"OK: HB #{HB_NUM} appended; file size {size_after} bytes (+{size_after - len(content.encode('utf-8'))} bytes)")
print(f"Append timestamp: {NOW}")
