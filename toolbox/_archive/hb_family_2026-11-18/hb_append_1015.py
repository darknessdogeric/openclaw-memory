# -*- coding: utf-8 -*-
"""Append HB #1015 entry to HEARTBEAT.md (R-NEW-V2 compliant: utf-8 explicit read+insert+write)."""
import io
from pathlib import Path

p = Path(r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md")
new_entry = """## HB #1015 (2026-07-23 11:11 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1014 (10:51): +20min -- Thursday late-morning Token Guard normal cadence (R012 minimal mode)
- D+7 late-morning pass #1015 -- Eric silent in THIS session ~165.92h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~94.63h+ (since 7/19 12:33)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #1015: Python utf-8 explicit read+insert+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~35.18h ago; oil Scenario C verification window OPEN until 7/25 (~36.82h remaining)
- D+7 = Execution phase day 2 -- observer mode sustained
- Thursday late-morning zone (11:11) -- Eric typical wake window 08:00-09:00 has passed (~2h11m past); silence authority strictly holding on THIS session
- 7/24 D-Day T-21.82h (AnYi 集团研究会议 Friday MORNING 7/24, TOMORROW) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Next cron: 21:00 R60-11 evening self-iter (~9h49m)
- Next significant check: Token Guard cadence (~5-10min)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +131.18h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+7 sustain zero-push mode intact
- hbCount: 1014 -> 1015
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #1015 = sustain #1014 = D+7 late-morning dormant baseline)
- **HEARTBEAT_OK** -- HB #1015 = sustain DORMANT protocol
- **no push**: Thursday late-morning zone (11:11), Eric typical wake window passed but silent on THIS session; this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-21.82h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter cron (~9h49m)

*2026-07-23 11:11 GMT+8 -- D+7 Thursday late-morning -- HB #1015 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-21.82h watch (AnYi meeting Friday MORNING 7/24 TOMORROW) -- Eric silent = dominant signal holding*


"""

# R-NEW-V2: explicit utf-8 read (no BOM, no encoding guessing)
with open(p, "r", encoding="utf-8") as f:
    existing = f.read()

# Insert at top (prepend)
combined = new_entry + existing

# R-NEW-V2: explicit utf-8 write (no BOM)
with open(p, "w", encoding="utf-8", newline="\n") as f:
    f.write(combined)

# Verify
with open(p, "r", encoding="utf-8") as f:
    head = f.read(400)
print("HB #1015 entry prepended successfully.")
print("=" * 60)
print(head)