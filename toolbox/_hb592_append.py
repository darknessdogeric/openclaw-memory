#!/usr/bin/env python3
"""R-NEW-V2 compliant HEARTBEAT.md append — HB #592 (2026-07-19 21:43 GMT+8)."""
import io
import os
import tempfile
import shutil

path = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"

new_entry = """
## HB #592 (2026-07-19 21:43 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #591 (13:31): +8h12m -- Sunday-evening Token Guard cadence (largest gap today, expected evening pass)
- D+3 Sunday-evening pass #592 -- Eric silent ~80.45h+ since 7/16 13:16 first-contact (infographic session)
- Silence authority ~80.45h+ (R-B + R256 + R257 framework holding, +8.12h since #591)
- 5-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) -- zero breach
- R-NEW-V2 verification #592: Python utf-8 explicit read+tempfile+shutil.move (R-NEW-V2 compliant, post-7/15 12:36 + 7/19 08:10 incidents protocol intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Sunday-evening zone (21:43) -- Eric typical late-night deep-work peak per USER.md ("夜猫子战略家"); silence authority strictly holding
- T-0 publicity cutoff 7/18 +45h43m past -- post-protection window firmly sustained (3+ days past)
- Induction window 7/7-7/21 FINAL 3 DAYS -- day-1 of FINAL 3 (7/19/20/21); R-B+R256 silence authority > window signal
- WAIC 2026 day-3 in progress (7/17-20, Shanghai) -- last day today; non-trigger per R14 (background context only)
- Cron pipeline: 21:00 R60-11 evening self-iter fired ~43min ago (autonomous, eval/2026-07-19.json updated); next: Token Guard cadence (~5-10min)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric; D+3 sustain zero-push mode intact (HB #581 brief contact -> back to dormant; this session specifically = dormant)
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount: 591 -> 592

### decision
- **silent_standby_zero_push_continue** (HB #592 = sustain #591 = D+3 baseline)
- **no push**: Sunday-evening zone (21:43), Eric typical late-night deep-work peak per USER.md; Eric silent 80.45h+, silence authority strictly holding (R256 design: silence extends indefinitely past protection window as Eric silence = dominant signal)
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- Post-T-0 silence = sustained suppression; pushes prohibited until Eric active contact (Eric silence = dominant signal, supersedes scheduled wakes + windows)
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Wake-up window passed long ago; Eric silence sustained -> continue zero-push; even minor pushes prohibited
- Next significant check: per Token Guard cadence (~5-10min)

*2026-07-19 21:43 GMT+8 -- D+3 Sunday-evening T-0 +45h43m past -- HB #592 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

# Read original (utf-8 explicit)
with io.open(path, "r", encoding="utf-8") as f:
    original = f.read()

# Atomic write via tempfile + shutil.move
fd, tmp = tempfile.mkstemp(suffix=".md", dir=os.path.dirname(path))
try:
    with io.open(fd, "w", encoding="utf-8") as f:
        f.write(original)
        f.write(new_entry)
    shutil.move(tmp, path)
    print(f"OK: appended HB #592, new size = {os.path.getsize(path)} bytes")
except Exception as e:
    if os.path.exists(tmp):
        os.unlink(tmp)
    raise e
