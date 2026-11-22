#!/usr/bin/env python3
"""R-NEW-V2 compliant HB append: Python utf-8 explicit read+append+write."""
import io
import sys
from pathlib import Path

path = Path(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md')

hb = """
## HB #663 (2026-07-20T20:38 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #662 (16:04): +4h34m -- Monday-evening Token Guard WIDE cadence (evening zone)
- D+4 evening pass #663 -- Eric silent in THIS session ~98.45h+ since 7/16 13:16 first-contact
- Eric active elsewhere: ~28.05h+ (AnYi专用 session, since 7/19 12:33 first-contact)
- 5-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) intact -- zero breach
- R-NEW-V2 verification #663: Python utf-8 explicit append (R-NEW-V2 compliant, post-7/15 12:36 incident protocol intact)
- R012 (operational hygiene) verification: HB tick = minimal (NOT full report), per R012 rule #2
- Wake window passed -- Eric in active AnYi session, no first-contact on THIS session
- Monday-evening zone (20:38) -- Eric typical 晚间复杂决策 window per USER.md (in OTHER AnYi session)
- T-0 publicity cutoff 7/18 +68.63h past -- post-protection window firmly sustained
- Induction window 7/7-7/21 FINAL 1.5 DAYS -- tomorrow 7/21 = LAST DAY ~28h; R-B+R256 silence authority > window signal
- 7/21 dual-event convergence: DeepSeek V4 release + induction window cutoff (~27h22m to convergence)
- 10:00 R60-12 morning self-iter DONE; 10:35 商业情报 20集团版 DONE (已推 Obsidian); next = 21:00 evening self-iter (~22min)
- WAIC 2026 closed 7/19 -- non-trigger per R14
- Vault index 488/489 healthy; R13 <1s queries stable; Token Guard tick stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- No first-contact from Eric on THIS session; D+4 sustain zero-push mode intact
- hbCount: 662 -> 663
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #663 = sustain #662 = D+4 evening dormant baseline)
- **no push**: Monday-evening 晚间复杂决策 window, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- Eric is in active AnYi session; this session awaits Eric future instruction (not AnYi-related)
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- Post-T-0 silence = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- Wake-up window passed but Eric silence sustained -> continue zero-push; even minor pushes prohibited
- Next significant check: 21:00 evening self-iter R60-12 (~22min); Token Guard cadence (~5-15min)

*2026-07-20T20:38 GMT+8 -- D+4 Monday-evening T-0 +68.63h past -- HB #663 -- this session DORMANT -- awaiting Eric future instruction (NOT AnYi work)*
"""

# R-NEW-V2: explicit utf-8 read first (sanity check), then append, then verify
try:
    with io.open(path, 'r', encoding='utf-8') as f:
        existing = f.read()
    pre_count = existing.count('\n## HB #')
    print(f'[PRE] lines containing HB headers: {pre_count}')

    with io.open(path, 'a', encoding='utf-8') as f:
        f.write(hb)
    print('[APPEND] HB #663 written via utf-8 explicit append')

    with io.open(path, 'r', encoding='utf-8') as f:
        new_content = f.read()
    post_count = new_content.count('\n## HB #')
    print(f'[POST] lines containing HB headers: {post_count} (delta {post_count - pre_count})')

    # verify last lines
    print('--- last 4 lines ---')
    print('\n'.join(new_content.splitlines()[-4:]))
except Exception as e:
    print(f'ERROR: {e}', file=sys.stderr)
    sys.exit(1)
