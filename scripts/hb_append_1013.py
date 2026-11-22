"""R-NEW-V2 compliant: explicit utf-8 read+append+write for HEARTBEAT.md
Post 7/15 + 7/19 incident protocol: no implicit encoding, no platform default."""

import io
import sys

path = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
entry = r'''
## HB #1013 (2026-07-23 09:53 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1012 (09:32): +21min -- Thursday late-morning Token Guard normal cadence (R012 minimal mode); within tolerance
- D+7 late-morning pass #1013 -- Eric silent in THIS session ~163.85h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~92.48h+ (since 7/19 12:33)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #1013: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~33.88h ago; oil Scenario C verification window OPEN until 7/25 (~38h12m remaining)
- D+7 = Execution phase day 2 -- observer mode sustained
- Thursday late-morning zone (09:53) -- Eric typical wake window 08:00-09:00 has passed (~53min past); silence authority strictly holding on THIS session
- 7/24 D-Day T-23.12h (AnYi 集团研究会议 Friday MORNING 7/24, TOMORROW) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Next cron: 21:00 R60-11 evening self-iter (~11.10h)
- Next significant check: Token Guard cadence (~5-10min)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +128.88h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+7 sustain zero-push mode intact
- hbCount: 1012 -> 1013
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #1013 = sustain #1012 = D+7 late-morning dormant baseline)
- **HEARTBEAT_OK** -- HB #1013 = sustain DORMANT protocol
- **no push**: Thursday late-morning zone (09:53), Eric typical wake window passed but silent on THIS session; this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-23.12h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter cron (~11.10h)

*2026-07-23 09:53 GMT+8 -- D+7 Thursday late-morning -- HB #1013 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-23.12h watch (AnYi meeting Friday MORNING 7/24 TOMORROW) -- Eric silent = dominant signal holding*
'''

with io.open(path, 'r', encoding='utf-8') as f:
    existing = f.read()

if 'HB #1013' in existing:
    print('SKIP: HB #1013 already present')
else:
    with io.open(path, 'a', encoding='utf-8') as f:
        f.write(entry)
    print('OK: HB #1013 appended (utf-8 explicit IO)')
