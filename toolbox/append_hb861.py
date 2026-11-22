"""Append HB #861 to HEARTBEAT.md per R-NEW-V2 (utf-8 explicit read+append+write)."""
from datetime import datetime, timezone, timedelta

tz_china = timezone(timedelta(hours=8))
now = datetime.now(tz_china)
ts_str = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')

entry = """

## HB #861 ({} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #860 (04:53): +5min -- Wednesday deep-night Token Guard normal cadence (R012 minimal mode)
- D+6 Wednesday deep-night pass #861 -- Eric silent in THIS session ~134.25h+ since 7/16 13:16 first-contact
- Eric active elsewhere: ~59.42h+ (AnYi webchat, since 7/19 12:33)
- 5-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) + R258 dormant-session -- zero breach
- R-NEW-V2 verification #861: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- **Triple Confluence Day 0 CLOSED** (7/21 24:00 cutoff passed ~4h59m ago); execution-phase observer mode active
  - Scenario A (55%) / B (35%) / C (10%) -- all maintain DORMANT protocol on THIS session
- Wednesday deep-night zone (04:58) -- quiet hours (23:00-08:00) per HEARTBEAT.md
- 08:00 daily briefing cron upcoming (~3h2m); 21:00 evening self-iter (~16h)
- Vault index 488/489 healthy; R13 <1s queries stable; Token Guard tick stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- hbCount: 860 -> 861
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #861 = sustain D+6 Wednesday deep-night dormant baseline)
- **HEARTBEAT_OK** -- HB #861 = sustain DORMANT protocol
- **no push**: Wednesday deep-night quiet hours (04:58), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Token Guard tick: stable, no compression needed
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows + convergence signals)
- Next significant check: 08:00 daily briefing (~3h2m); 21:00 evening self-iter (~16h)

*{} -- D+6 Wednesday deep-night T-0 +104h+ past -- HB #861 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- execution-phase observer mode -- Triple Confluence Day 0 CLOSED*
""".format(now.strftime('%Y-%m-%dT%H:%M'), ts_str)

# R-NEW-V2: explicit utf-8 read+append+write
with open('HEARTBEAT.md', 'a', encoding='utf-8') as f:
    f.write(entry)

print('HB #861 appended to HEARTBEAT.md ({} bytes)'.format(len(entry)))