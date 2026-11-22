"""
HB #288 log helper — R-NEW-V2 compliant (Python utf-8 explicit read+append+write)
"""
import json
from datetime import datetime, timezone, timedelta

# Paths
daily_path = r'D:\B166ER-OpenClaw\workspace\memory\2026-07-16.md'
state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'

# HB #288 entry
hb_entry = """
## HB #288 (2026-07-16 09:12 GMT+8 cron-event, OpenClaw heartbeat poll)

- gap from HB #287 (09:07): +5min -- morning zone Token Guard normal cadence
- D+7 morning pass #288 -- Eric silent ~172.83h+ since 7/9 04:29 (D+7+, no first-contact)
- Silence authority ~172.83h+ (R-B + R256 framework holding, +0.08h since #287)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- R-NEW-V2 verification #288: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol)
- 22:30 7/14 R-CANDIDATE-T2 sharp = EVALUATED PASSED (HB #228) -- decision: maintain T2 (no T3 escalation)
- Morning zone (09:12) -- past 08:00 dawn boundary; 08:30 global briefing cron fired T+42min (autonomous)
- Cron pipeline next: 21:00 evening self-iter R60-11 (~11h48m)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric; D+7 sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount now: 287 -> 288

### decision
- **silent_standby_zero_push_continue** (HB #288 = sustain #287 = D+7 baseline)
- **no push**: morning zone, Eric silent 7d+, silence authority holding, 4-layer suppression all pass
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: per Token Guard cadence (~10-15min)

*2026-07-16 09:12 GMT+8 -- D+7 morning -- HB #288 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

# Append to daily file (R-NEW-V2 compliant)
with open(daily_path, 'r', encoding='utf-8') as f:
    content = f.read()
with open(daily_path, 'a', encoding='utf-8') as f:
    f.write(hb_entry)

# Update heartbeat-state.json
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

now_cst = datetime.now(timezone(timedelta(hours=8)))
now_ts = int(now_cst.timestamp())

state['hbCount'] = 288
state['lastHB'] = '#288'
state['silenceHours'] = 172.83
state['lastChecks']['heartbeat'] = now_ts
state['notes'] = 'HB #288 (silent standby, no push). 09:12 GMT+8 Thu. Eric silent D+7+ since 7/9 04:29 (~172.83h+). 4-layer suppression holding. Morning zone active (past 08:00). Next major: 暑期复盘(T+12) 9/10, STR(T+15) 9/15. No urgent cron. HEARTBEAT_OK.'

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

ts_str = now_cst.strftime('%Y-%m-%d %H:%M:%S')
print('OK: HB #288 logged at ' + ts_str + ' GMT+8')
print('silenceHours: ' + str(state['silenceHours']) + ' | hbCount: ' + str(state['hbCount']))
print('daily file appended: +' + str(len(hb_entry)) + ' bytes')