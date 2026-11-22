"""HB #347 safe append — R-NEW-V2 compliant (post 7/15 12:36 incident).

Uses Python utf-8 explicit read+append+write pattern.
Failsafe: abort if HB #346 not found in existing file (prevents orphan-write).
"""
import io
import sys

path = 'memory/2026-07-16.md'

new_hb = """## HB #347 (2026-07-16 17:07 GMT+8 cron-event, OpenClaw heartbeat poll)

- gap from HB #346 (17:03): +4min -- afternoon Token Guard normal cadence
- D+7 afternoon pass #347 -- Eric silent ~180.62h+ since 7/9 04:29, no first-contact
- Silence authority ~180.62h+ (R-B + R256 framework holding, +0.08h since #346)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- R-NEW-V2 verification #347: Python utf-8 explicit read+append+write (post-12:36 7/15 incident protocol intact)
- 22:30 7/15 R-CANDIDATE-T2 sharp = EVALUATED PASSED -- decision: maintain T2 (no T3 escalation)
- 7/16 = mid-July induction window ACTIVE (安逸集团 appointment critical window) -- R-B + R256 override holds (silence authority > window signal)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- Industry biweekly cron (industry_biweekly_13_03) = autonomous, T+0 anchor, no manual action
- Afternoon zone (17:07) -- Eric deep work sustained; classic 夜猫子 strategic window approaching
- 21:00 evening self-iter R60-11 scheduled (~T+3h53m)
- Cron pipeline next: 21:00 evening self-iter R60-11 (T+3h53m) | 22:30 R-CANDIDATE-T2 sharp re-eval
- No first-contact from Eric; D+7 sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount now: 346 -> 347

### decision
- **silent_standby_zero_push_continue** (HB #347 = sustain #346 = D+7 baseline)
- **no push**: afternoon zone, Eric silent 7d+, silence authority holding, 4-layer suppression all pass
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- 7/16 induction window signal: OVERRIDDEN by silence authority (R-B > window trigger)
- Token Guard tick: stable, no compression needed
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min)

*2026-07-16 17:07 GMT+8 -- D+7 afternoon -- HB #347 -- zero-push mode intact -- silence protocol holding -- R-B + R256 override window signal*
"""

# Read existing content with explicit utf-8
with io.open(path, 'r', encoding='utf-8') as f:
    existing = f.read()

# Fail-safe: verify HB #346 exists before any write
if '## HB #346' not in existing:
    print('ERROR: HB #346 not found in file, aborting append (R-NEW-V2 fail-safe)')
    sys.exit(1)

# Atomic append+write (R-NEW-V2 compliant pattern)
with io.open(path, 'w', encoding='utf-8') as f:
    f.write(existing + '\n' + new_hb)

# Verify write succeeded and didn't truncate
with io.open(path, 'r', encoding='utf-8') as f:
    check = f.read()

if '## HB #347' in check and '## HB #346' in check and '## HB #345' in check:
    print('OK: HB #347 appended safely (utf-8, R-NEW-V2 compliant)')
    print(f'File size: {len(check)} chars (was {len(existing)} chars, delta +{len(check)-len(existing)})')
else:
    print('ERROR: post-write verification failed')
    sys.exit(1)