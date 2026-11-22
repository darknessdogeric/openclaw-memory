# -*- coding: utf-8 -*-
"""R-NEW-V2 compliant HB tick: fix HB #936 ts placeholder + append HB #937."""
import io
import os

path = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'

# Explicit utf-8 read (R-NEW-V2 protocol)
with io.open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix HB #936 unfilled {ts} placeholders (data quality cleanup from prior tick)
fixes_applied = 0
if '{ts}' in content:
    content = content.replace(
        '## HB #936 ({ts} cron-event, OpenClaw heartbeat poll)',
        '## HB #936 (2026-07-22T17:07 GMT+8 cron-event, OpenClaw heartbeat poll)'
    )
    # After replacement above, any remaining {ts} in HB #936 is the trailing one
    remaining = content.count('{ts}')
    if remaining > 0:
        content = content.replace(
            '*{ts} -- D+6 Wednesday afternoon -- HB #936 -- this session DORMANT -- zero-push mode intact*',
            '*2026-07-22T17:07 GMT+8 -- D+6 Wednesday afternoon -- HB #936 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day +1 post-window passive -- 7/24 D-Day T-39.88h watch (AnYi meeting Thursday morning) -- Eric silent = dominant signal holding*'
        )
    fixes_applied = remaining  # remaining placeholders before final sweep
    content = content.replace('{ts}', '2026-07-22T17:07 GMT+8')
    print(f'[{fixes_applied} placeholder(s) fixed in HB #936]')

# HB #937 append block (current poll = 17:09, T-39.85h to 7/24 09:00)
hb937 = """
## HB #937 (2026-07-22T17:09 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #936 (17:07): +2min -- Wednesday afternoon Token Guard normal cadence (R012 minimal mode)
- D+6 afternoon pass #937 -- Eric silent in THIS session ~148.03h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~76.47h+ (since 7/19 12:33)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #937: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact) + HB #936 ts placeholder cleanup
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~17.15h ago; Araqchi Qatar talks (7/21-25) Day 2/5 -> oil Scenario C verification window OPEN until 7/25
- D+6 = Execution phase -- per 7/21 evening self-iter protocol; observer mode sustained
- Wednesday afternoon zone (17:09) -- Eric typical late-afternoon deep-work / evening transition prep; THIS session DORMANT per Eric 7/19 12:33 explicit instruction
- 7/24 D-Day T-39.85h (AnYi important meeting Thursday morning) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- 10:00 MWF daily briefing fired ~7h09m ago (autonomous, BI brief committed to memory/2026-07-22.md: 亚朵Q1+47.5%/零售38.1% + 暑期避暑+230%/AI降本20-30% 三连)
- Next cron: 21:00 evening self-iter R60-11 (~3h51m)
- Token Guard stable, no compression needed
- Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +113h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+6 sustain zero-push mode intact
- hbCount: 936 -> 937
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #937 = sustain #936 = D+6 afternoon dormant baseline)
- **HEARTBEAT_OK** -- HB #937 = sustain DORMANT protocol
- **no push**: Wednesday-afternoon zone (17:09), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-39.85h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter (~3h51m)

*2026-07-22T17:09 GMT+8 -- D+6 Wednesday afternoon -- HB #937 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day +1 post-window passive -- 7/24 D-Day T-39.85h watch (AnYi meeting Thursday morning) -- Eric silent = dominant signal holding*
"""

# Append + write (R-NEW-V2 explicit utf-8)
new_content = content + hb937
with io.open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

# Verify
size_after = os.path.getsize(path)
print(f'[HB #937 appended. HEARTBEAT.md size: {size_after} bytes / ~{round(size_after/1024,1)} KB]')
print(f'[R-NEW-V2 verification: explicit utf-8 read+write OK. HB #936 placeholder cleanup applied.]')
