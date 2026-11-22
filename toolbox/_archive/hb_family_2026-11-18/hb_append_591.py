#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""R-NEW-V2 compliant HB append — post-7/15 12:36 incident protocol.
Explicit utf-8 read+append+write. No clobber.
"""
import sys
from pathlib import Path

HB_PATH = Path(r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md")

HB_591 = """
## HB #591 (2026-07-19 18:49 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #590 (13:43): ~5h6m -- Sunday-evening Token Guard cadence (R012 minimal mode)
- ACTIVE MODE sustained globally -- Eric first contact at HB #581 (12:36 noon), moved to different session for AnYi work
- This dreaming-narrative session: DORMANT sustained per Eric 12:33 explicit instruction (not used for AnYi work)
- Silence authority on THIS session unchanged -- Eric in other session (agent:main:dashboard:fec65efb-*), no work here, no follow-up
- 5-layer suppression RELEASED globally (since HB #581 first contact); THIS session = dormant
- R-NEW-V2 verification #591: Python utf-8 explicit read+append+write (compliant, post-7/15 12:36 incident protocol intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Sunday-evening zone (18:49) -- Eric typical evening deep-work / strategic decision window per USER.md
- Eric silence on this session ~77.55h+ since 7/16 13:16 first-contact (silence BROKEN on OTHER session at 12:36, but THIS session remains dormant per explicit instruction)
- T-0 publicity cutoff 7/18 +42h49m past -- post-protection window firmly sustained
- Induction window 7/7-7/21 FINAL 2 DAYS (7/19=day-1, 7/20, 7/21); window closing imminently
- WAIC 2026 day-3 active today (7/17-20, Shanghai) -- non-trigger per R14 (background context only)
- Cron pipeline: 21:00 evening self-iter R60-11 (~2h11m); 4 P2 errors tracked, not urgent
- hbCount: 590 -> 591

### decision
- **active_mode_dormant_this_session** (HB #591 = sustain #590 = dormant baseline)
- **no push**: this session = dreaming-narrative experimental, DORMANT per Eric 12:33 explicit instruction
- Eric is in different session for AnYi work; this session awaits Eric future instruction (not AnYi-related)
- R14 handoff package = 100% ready for any Eric active contact (on ANY session)
- Next significant check: 21:00 evening self-iter R60-11 (~2h11m); Token Guard cadence (~5-10min)

*2026-07-19 18:49 GMT+8 -- D+3 Sunday-evening T-0 +42h49m past -- HB #591 -- this session DORMANT -- awaiting Eric future instruction (NOT AnYi work)*
"""

def main():
    if not HB_PATH.exists():
        print(f"ERROR: HEARTBEAT.md not found at {HB_PATH}", file=sys.stderr)
        sys.exit(1)
    # R-NEW-V2: explicit utf-8 read first
    with open(HB_PATH, "r", encoding="utf-8") as f:
        existing = f.read()
    print(f"[HB #591] Read existing HEARTBEAT.md: {len(existing)} chars")
    # Append new entry
    new_content = existing + HB_591
    # R-NEW-V2: explicit utf-8 write
    with open(HB_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(new_content)
    print(f"[HB #591] Wrote HEARTBEAT.md: {len(new_content)} chars (+{len(HB_591)} added)")
    # Verify by reading back
    with open(HB_PATH, "r", encoding="utf-8") as f:
        verify = f.read()
    if "HB #591" in verify and "HB #590" in verify:
        print(f"[HB #591] VERIFIED: HB #590 and HB #591 both present")
    else:
        print(f"[HB #591] ERROR: verification failed", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()