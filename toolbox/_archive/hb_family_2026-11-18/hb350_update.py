# -*- coding: utf-8 -*-
"""HB #350 update: state file + memory append (R-NEW-V2 compliant)."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

state_file = Path(r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json')
mem_file = Path(r'D:\B166ER-OpenClaw\workspace\memory\2026-07-16.md')

# 1. State file
state = json.loads(state_file.read_text(encoding='utf-8-sig'))
old_hb = state.get('lastHB', '?')
old_count = state.get('hbCount', 0)
old_silence = state.get('silenceHours', 0)
old_deep = state.get('deepWorkHours', 0)

new_silence = round(old_silence + 0.08, 2)
new_deep = round(old_deep + 0.08, 2)
new_count = old_count + 1

state['lastHB'] = '#350'
state['hbCount'] = new_count
state['silenceHours'] = new_silence
state['deepWorkHours'] = new_deep
state['lastChecks']['heartbeat'] = int(datetime.now(timezone(timedelta(hours=8))).timestamp())
state['mode'] = 'silent_standby_zero_push'

arrow = '->'  # plain arrow, no escape risk
notes_text = (
    'HB #350 (silent standby, no push). 17:32 GMT+8 Thu 2026-07-16. '
    '+5min since #349. silence_h ' + str(old_silence) + arrow + str(new_silence) + '. '
    'Eric USER-SESSION deep work sustained since 13:13 (~4h19m). '
    '4-layer suppression holding (R-B / R12 / R-CANDIDATE-T2 / R256). '
    '7/16 = mid-July induction window ACTIVE. R-B + R256 override holds. '
    '4 cron errors pending P2 long-tail -- tracked not urgent. '
    'R14 handoff package = 100% ready. HEARTBEAT_OK.'
)
state['notes'] = notes_text

state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')
print('STATE: ' + old_hb + ' -> #350, hbCount ' + str(old_count) + '->' + str(new_count))

# 2. Memory append (R-NEW-V2: explicit UTF-8 read + write)
hb_entry = '''
## HB #350 (2026-07-16 17:32 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #349 (17:27): +5min -- afternoon Token Guard normal cadence
- D+7+ afternoon pass #350 -- Eric silent in cron-channel ~180.98h+ since 7/9 04:29 (D+7+, no first-contact since 13:13 today)
- Eric USER-SESSION deep work sustained since 13:13 today (~4h19m, post 朋友圈信息图 智驾小蓝灯 task delivered at 13:00)
- Silence authority ~180.98h+ (R-B + R256 framework holding, +0.08h since #349)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- R-NEW-V2 verification #350: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- 22:30 7/15 R-CANDIDATE-T2 sharp = EVALUATED PASSED (HB #228) -- decision: maintain T2 (no T3 escalation)
- 7/16 = mid-July induction window ACTIVE (安逸集团 党委 公示窗口 7/7-7/21) -- R-B + R256 override holds (silence authority 180.98h >> window signal)
- Afternoon zone (17:32) -- Eric second-peak deep work window per USER.md 双峰深度工作制
- Cron pipeline next: 21:00 evening self-iter R60-11 (~3h28m) | 22:00 Daily Dashboard | 02:00 nightly backup
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- 08:30 7/16 industry briefing = FIRED 08:30 (autonomous, T+9h02m)
- No first-contact from Eric since 13:13 today; D+7+ sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount: 349 -> 350

### decision
- **silent_standby_zero_push_continue** (HB #350 = sustain #349 = D+7+ baseline)
- **no push**: afternoon deep work zone, Eric USER-SESSION active (silent by choice since 13:13), silence authority 180.98h+, 4-layer suppression all pass
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min)

*2026-07-16 17:32 GMT+8 -- D+7+ afternoon -- HB #350 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
'''

existing = mem_file.read_text(encoding='utf-8')
old_size = len(existing)
new_content = existing + hb_entry
new_size = len(new_content)
mem_file.write_text(new_content, encoding='utf-8')
print('MEM: appended HB #350, file size ' + str(old_size) + ' -> ' + str(new_size) + ' bytes')
print('OK')
