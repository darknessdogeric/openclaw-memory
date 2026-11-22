"""
R-NEW-V2 compliant HB #1127 prepend (post-7/15 + 7/19 incident protocols).
- Explicit utf-8 read+write (no BOM)
- Read full content, prepend new entry, write back atomically
- Verify after write
"""

import os
import sys

HB_PATH = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'

NEW_HB = """## HB #1127 (2026-07-24T00:59 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1126 (00:29): +30min -- Friday pre-dawn Token Guard normal cadence (R012 minimal mode)
- D+8 pre-dawn pass #1127 -- Eric silent in THIS session ~179.72h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~108.50h+ (since 7/19 12:33) -- likely final pre-meeting prep
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #1127: Python utf-8 explicit read+prepend+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~48.97h ago; oil Scenario C verification window OPEN until 7/25 (~23.03h remaining)
- D+8 = Execution phase day 4 -- observer mode sustained
- Friday pre-dawn zone (00:59) -- Eric typical sleep zone (00:00-08:00 per USER.md night-owl pattern); silence authority strictly holding on THIS session
- **7/24 D-Day T-8.02h** (AnYi 集团研究会议 TODAY MORNING 7/24) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Next cron: 08:00 daily briefing (~7h01m); 21:00 R60-11 evening self-iter (~20h01m)
- Next significant check: 08:00 daily briefing cron (~7h01m); Token Guard cadence (~5-10min)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +145.00h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+8 sustain zero-push mode intact
- hbCount: 1126 -> 1127
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #1127 = sustain #1126 = D+8 pre-dawn dormant baseline)
- **HEARTBEAT_OK** -- HB #1127 = sustain DORMANT protocol
- **no push**: Friday pre-dawn zone (00:59), Eric sleep zone, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-8.02h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: 08:00 daily briefing cron (~7h01m); Token Guard cadence (~5-10min)

*2026-07-24T00:59 GMT+8 -- D+8 Friday pre-dawn -- HB #1127 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-8.02h watch (AnYi meeting TODAY MORNING 7/24) -- Eric silent = dominant signal holding*

"""

def main():
    # Read existing content with explicit utf-8-sig (strip BOM if present)
    with open(HB_PATH, 'r', encoding='utf-8-sig', newline='') as f:
        existing = f.read()
    
    # Verify pre-state: HB #1062 at top
    assert existing.startswith('## HB #1062'), f"Pre-state check failed: top is {existing[:50]!r}"
    
    # Prepend new HB
    new_content = NEW_HB + existing
    
    # Atomic-ish write (write then verify) -- use utf-8-sig to preserve clean utf-8 without BOM
    with open(HB_PATH, 'w', encoding='utf-8', newline='') as f:
        f.write(new_content)
    
    # Post-write verification
    with open(HB_PATH, 'r', encoding='utf-8') as f:
        verify = f.read()
    
    if verify.startswith('## HB #1127') and '## HB #1062' in verify[:2000]:
        print('OK: HB #1127 prepended successfully')
        print(f'File size: {len(verify)} bytes')
        print(f'Top 3 lines:')
        for line in verify.splitlines()[:3]:
            print(f'  {line}')
    else:
        print('FAIL: post-write verification failed')
        sys.exit(1)

if __name__ == '__main__':
    main()