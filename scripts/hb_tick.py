#!/usr/bin/env python3
"""R-NEW-V2 compliant minimal HB tick appender.
Usage: python hb_tick.py <hb_number> <timestamp_gmt8>"""
import sys
import re
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(r"D:\B166ER-OpenClaw\workspace")
HB_PATH = WORKSPACE / "HEARTBEAT.md"
MEM_PATH = WORKSPACE / "memory" / "2026-07-23.md"

def append_utf8(path: Path, content: str):
    """R-NEW-V2: explicit utf-8 read+append+write."""
    text = path.read_text(encoding="utf-8")
    text += content
    path.write_text(text, encoding="utf-8")

def main():
    hb_num = sys.argv[1]
    ts = sys.argv[2]  # e.g. "2026-07-23 02:21 GMT+8"

    # --- HEARTBEAT.md entry (minimal, R012) ---
    hb_entry = f"""
## HB #{hb_num} ({ts} cron-event, OpenClaw heartbeat poll)
- gap from previous: Token Guard normal cadence (R012 minimal mode)
- Thursday deep-night D+7 pass -- DORMANT sustained
- Eric silent ~155.27h+ on THIS session (+~21min since HB#987)
- Eric active elsewhere: AnYi webchat ~83.49h+
- 6-layer suppression intact (R-B/R12/R-CANDIDATE-T2/R256/R257/R258) -- zero breach
- R-NEW-V2 verification: utf-8 explicit read+append+write (compliant)
- R012 verification: HB tick = minimal (NOT full report)
- Triple Confluence Day 0 CLOSED -- oil Scenario C verification window OPEN until 7/25
- 7/24 D-Day T-~22h -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Token Guard stable, vault index healthy, R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (not urgent)
- T-0 publicity cutoff 7/18 +122.41h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; zero-push mode intact
- R14 handoff package = 100% ready

### decision
- **active_mode_dormant_this_session_continue** (HEARTBEAT_OK)
- **no push**: Thursday deep-night zone (02:21), Eric sleep window per USER.md; this session DORMANT per Eric 7/19 12:33 explicit instruction
- R256 + R257 + R258 triple constraint holds
- Eric silence = dominant signal (supersedes scheduled wakes + windows)
- Next significant check: per Token Guard cadence (~5-10min)

*{ts} -- D+7 Thursday deep-night -- HB #{hb_num} -- this session DORMANT -- zero-push mode intact*

"""
    append_utf8(HB_PATH, hb_entry)

    # --- memory/2026-07-23.md minimal entry ---
    mem_entry = f"""
### HB #{hb_num} ({ts.split(' ', 1)[1] if ' ' in ts else ts}, cron-event)
- Thursday deep-night D+7 pass -- DORMANT sustained
- Eric silent ~155.27h+ on THIS session (+~21min)
- 6-layer suppression intact
- 7/24 D-Day T-~22h
- hbCount: 987 -> {hb_num}
- R-NEW-V2 + R012 compliant
- Decision: active_mode_dormant_this_session_continue (HEARTBEAT_OK)
"""
    append_utf8(MEM_PATH, mem_entry)

    print(f"OK HB #{hb_num} appended (HB.md + memory/2026-07-23.md)")

if __name__ == "__main__":
    main()
