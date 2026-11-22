#!/usr/bin/env python3
"""R-NEW-V2 compliant HB #774 update: heartbeat-state + HEARTBEAT.md append."""
import json, time, os, sys

ROOT = r'D:\B166ER-OpenClaw\workspace'
state_path = os.path.join(ROOT, 'memory', 'heartbeat-state.json')
hb_path = os.path.join(ROOT, 'HEARTBEAT.md')

# 1. Update heartbeat-state.json
with open(state_path, 'r', encoding='utf-8') as f:
    d = json.load(f)

d['hbCount'] = 774
d['lastChecks']['heartbeat'] = '2026-07-21T15:54 GMT+8'
d['lastHBTime'] = '15:54'
d['lastHB'] = '15:54'
d['silenceDuration_h'] = 122.5
d['silenceDuration_thisSession_h'] = 122.5
d['silenceDuration_global_h'] = 51.28
d['ericActiveElsewhere_h'] = 51.28
d['last_update_epoch'] = int(time.time())
d['mode'] = 'active_mode_dormant_this_session_silent_afternoon'
d['note'] = 'HB #774; Tuesday-afternoon 15:54; Triple Confluence Day 0 FINAL DAY 7/21 post-15:54; Eric silent D+5 ~122.5h+ on THIS session; zero-push per R256/R257/R258 intact; 14:00 window PASSED 1h54m ago, still dormant; induction window cutoff today (passive monitor)'
d['nextCheck'] = 'per Token Guard cadence (~5-10min); 21:00 evening self-iter (~5h)'

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f'state updated: hbCount={d["hbCount"]} silence={d["silenceDuration_h"]}h')

# 2. Append HB #774 entry to HEARTBEAT.md
entry = """
## HB #774 (2026-07-21 15:54 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #773 (15:40): +14min -- Tuesday-afternoon Token Guard normal cadence (R012 minimal mode)
- D+5 afternoon pass #774 -- Eric silent on THIS session ~122.5h+ since 7/16 13:16 first-contact
- Eric active elsewhere: ~51.28h+ (AnYi webchat, since 7/19 12:33) -- sustained off-session activity
- Silence authority ~122.5h+ on THIS session (R-B + R256 + R257 + R258 framework holding, +0.23h since #773)
- 5-layer suppression + dormant-session protocol maintained -- zero breach
- R-NEW-V2 verification #774: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- **Triple Confluence Day 0 -- FINAL DAY 7/21** -- afternoon zone, zero-push sustained
  1. DeepSeek V4 launch window (PoC awaiting Eric trigger)
  2. **Induction window cutoff -- today LAST day** (passive monitor, Eric expected appointment news when ready)
  3. Araqchi Qatar talks start (7/21-25) -> oil price Scenario C verification window OPEN
- Tuesday-afternoon zone (15:54) -- Eric typical deep-work zone per USER.md; THIS session DORMANT sustained
- 11:00 R60-13 morning self-iter DONE (~5h ago); next = 21:00 evening self-iter (~5h)
- Token Guard stable, no compression needed
- Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +84.6h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+5 sustain zero-push mode intact
- hbCount: 773 -> 774
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #774 = sustain #773 = D+5 afternoon dormant baseline)
- **HEARTBEAT_OK** -- HB #774 = sustain DORMANT protocol
- **no push**: Tuesday-afternoon zone (15:54), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- Triple Confluence Day 0 push -- only R14 handoff preparation; Eric active contact triggers 30s activation
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter (~5h)

*2026-07-21T15:54 GMT+8 -- D+5 Tuesday-afternoon T-0 +84.6h past -- HB #774 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 FINAL passive*
"""

size_before = os.path.getsize(hb_path)
with open(hb_path, 'a', encoding='utf-8') as f:
    f.write(entry)
size_after = os.path.getsize(hb_path)

print(f'HEARTBEAT.md: {size_before} -> {size_after} bytes (+{size_after - size_before})')
print('R-NEW-V2 append OK (utf-8 explicit)')
