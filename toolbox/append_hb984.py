#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R-NEW-V2 compliant HEARTBEAT.md append for HB #984
Thursday pre-dawn 2026-07-23 06:04 GMT+8
"""
import sys
from datetime import datetime, timezone, timedelta

HB_FILE = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"
TZ_SH = timezone(timedelta(hours=8))

# 1. Explicit UTF-8 read
with open(HB_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 2. Build HB #984 entry
hb984 = """## HB #984 (2026-07-23 06:04 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #983 (04:39): +85min -- Thursday pre-dawn Token Guard normal cadence (R012 minimal mode)
- D+7 pre-dawn pass #984 -- Eric silent in THIS session ~160.80h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~89.52h+ (since 7/19 12:33)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #984: Python utf-8 explicit read+insert+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~30h4m ago; oil Scenario C verification window OPEN until 7/25 (~41h56m remaining)
- D+7 = Execution phase day 2 -- observer mode sustained
- Thursday pre-dawn zone (06:04) -- Eric typical wake window ~08:00-09:00 (~1h56m); silence authority strictly holding
- 7/24 D-Day T-28.93h (AnYi important meeting Thursday morning) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- 21:00 R60-11 evening self-iter upcoming ~14h56m
- Next cron: 08:00 daily briefing (~1h56m); 09:00 daily checkin (~2h56m); 10:00 R60-13 morning self-iter (~3h56m)
- Next significant check: Token Guard cadence (~5-10min)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +126.07h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+7 sustain zero-push mode intact
- hbCount: 983 -> 984
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #984 = sustain #983 = D+7 pre-dawn dormant baseline)
- **HEARTBEAT_OK** -- HB #984 = sustain DORMANT protocol
- **no push**: Thursday pre-dawn zone (06:04), Eric typical wake window not yet open, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-28.93h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: 08:00 daily briefing cron (~1h56m); per Token Guard cadence (~5-10min)

*2026-07-23 06:04 GMT+8 -- D+7 Thursday pre-dawn -- HB #984 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-28.93h watch (AnYi meeting Thursday morning) -- Eric silent = dominant signal holding*

"""

# 3. Insert before "## HB #983" (so it sits on top in chronological order matching the pattern)
target = "## HB #983 (2026-07-23 04:39"
idx = content.find(target)
if idx == -1:
    print("ERROR: HB #983 anchor not found. Aborting append.")
    sys.exit(1)

new_content = content[:idx] + hb984 + content[idx:]

# 4. Verify len grew correctly
old_len = len(content)
new_len = len(new_content)
expected_delta = len(hb984)
actual_delta = new_len - old_len
if actual_delta != expected_delta:
    print(f"ERROR: length delta mismatch. expected={expected_delta}, actual={actual_delta}")
    sys.exit(1)

# 5. Write back
with open(HB_FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

# 6. Verify write by reading back the inserted block
with open(HB_FILE, 'r', encoding='utf-8') as f:
    verify = f.read()

if "## HB #984 (2026-07-23 06:04" not in verify:
    print("ERROR: HB #984 not found in file after write")
    sys.exit(1)

if "## HB #983 (2026-07-23 04:39" not in verify:
    print("ERROR: HB #983 lost after write")
    sys.exit(1)

print(f"OK: HB #984 appended before HB #983; +{actual_delta} chars; dual-anchor verified.")