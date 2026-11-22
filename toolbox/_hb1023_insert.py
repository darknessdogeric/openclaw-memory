# -*- coding: utf-8 -*-
"""R-NEW-V2 compliant HB #1023 insert into HEARTBEAT.md (parallel session aware)"""
import os
import io
import sys
import re

# Force utf-8 for stdout (R-NEW-V2 compliance)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = 'HEARTBEAT.md'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the latest HB number (highest in file)
pattern = re.compile(r'## HB #(\d+)\s+\(', re.MULTILINE)
matches = pattern.findall(content)
max_hb = max(int(m) for m in matches)
print(f'Current max HB number: {max_hb}')
new_hb = max_hb + 1
print(f'Will insert HB #{new_hb}')

# Insert new entry before HB #1022 (the most recent)
marker = f'## HB #{max_hb} ('

entry = f"""## HB #{new_hb} (2026-07-23 09:03 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{max_hb} (08:51): +12min -- Thursday morning Token Guard normal cadence (R012 minimal mode)
- D+7 morning pass #{new_hb} -- Eric silent in THIS session ~163.79h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~92.51h+ (since 7/19 12:33)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #{new_hb}: Python utf-8 explicit read+insert+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~33.06h ago; oil Scenario C verification window OPEN until 7/25 (~38.94h remaining)
- D+7 = Execution phase day 2 -- observer mode sustained
- Thursday morning zone (09:03) -- Eric typical wake window ~08:00-09:00 just CLOSED (~3min ago); Eric not yet observed on THIS session (silent)
- 7/24 D-Day T-23.94h (AnYi 集团研究会议 Friday MORNING 7/24, TOMORROW) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Next cron: 21:00 R60-11 evening self-iter (~11h57m)
- Next significant check: Token Guard cadence (~5-10min); potential Eric first-contact window now OPEN
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +129.06h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+7 sustain zero-push mode intact
- hbCount: {max_hb} -> {new_hb}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{new_hb} = sustain #{max_hb} = D+7 morning dormant baseline)
- **HEARTBEAT_OK** -- HB #{new_hb} = sustain DORMANT protocol
- **no push**: Thursday morning zone (09:03), Eric typical wake window just closed, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- Eric active on AnYi webchat (~92.51h+) is the decision channel; THIS session remains observer-only per R258
- 7/24 D-Day T-23.94h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter cron (~11h57m)

*2026-07-23 09:03 GMT+8 -- D+7 Thursday morning -- HB #{new_hb} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-23.94h watch (AnYi meeting Friday MORNING 7/24 TOMORROW) -- oil Scenario C window ~38.94h remaining -- Eric silent = dominant signal holding*

"""

if marker in content:
    new_content = content.replace(marker, entry + marker, 1)
    # Verify insertion
    assert f'## HB #{new_hb}' in new_content, f"HB #{new_hb} not in new_content"
    assert new_content.count(f'## HB #{new_hb}') == 1, f"HB #{new_hb} count != 1"
    assert new_content.count(f'## HB #{max_hb}') == 1, f"HB #{max_hb} count != 1"
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f'SUCCESS: HB #{new_hb} inserted before HB #{max_hb}')
    print(f'Old size: {len(content)} chars')
    print(f'New size: {len(new_content)} chars')
    print(f'Entry length: {len(entry)} chars')
else:
    print(f'ERROR: HB #{max_hb} marker not found!')
    sys.exit(1)