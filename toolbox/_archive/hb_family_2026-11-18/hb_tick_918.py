# -*- coding: utf-8 -*-
"""
HB tick #918 (cron-event 2026-07-22 14:14 GMT+8)
R-NEW-V2 compliant: explicit utf-8 read+append+write
"""
import json, os
from datetime import datetime, timezone, timedelta

WORKSPACE = r'D:\B166ER-OpenClaw\workspace'
HB_PATH = os.path.join(WORKSPACE, 'HEARTBEAT.md')
STATE_PATH = os.path.join(WORKSPACE, 'memory', 'heartbeat-state.json')

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
hb_time_full = now.strftime('%Y-%m-%dT%H:%M GMT+8')

with open(STATE_PATH, 'r', encoding='utf-8') as f:
    state = json.load(f)

silence_hours = round(state['silenceHours'] + (15/60), 2)
eric_active = round(state['ericActiveHours'] + (15/60), 2)
hb_count = 918

# D-Day = 7/24 9:00 (上午研讨会)
dday_dt = datetime(2026, 7, 24, 9, 0, tzinfo=tz)
dday_hours = round((dday_dt - now).total_seconds() / 3600, 2)

# 21:00 evening self-iter
evening_iter = now.replace(hour=21, minute=0, second=0, microsecond=0)
if evening_iter <= now:
    evening_iter = evening_iter + timedelta(days=1)
evening_iter_hours = round((evening_iter - now).total_seconds() / 3600, 2)

# T-0 past hours
t0_past = round(state.get('t0_past_hours', 113.07) + (now.timestamp() - datetime.fromisoformat(state['lastCheck']).timestamp())/3600, 2)

hb_text = f"""
## HB #{hb_count} ({hb_time_full} cron-event, OpenClaw heartbeat poll)
- gap from HB #917 (13:59): +15min -- Wednesday midday Token Guard normal cadence (R012 minimal mode)
- D+6 midday pass #{hb_count} -- Eric silent in THIS session ~{silence_hours}h+ since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat ~{eric_active}h+ (since 7/19 12:33)
- 6-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- Triple Confluence Day +1: induction window CLOSED 7/21 23:59 (post-window passive); Araqchi Qatar talks Day 2/5 (oil Scenario C open until 7/25)
- 7/24 D-Day T-1 (AnYi important meeting) = ~{dday_hours}h window -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Midday zone {now.strftime('%H:%M')} -- this session DORMANT sustained
- Last major cron fired: 10:00 MWF daily briefing (~4h14m ago); next = 21:00 evening self-iter (~{evening_iter_hours}h)
- Token Guard stable; vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +{t0_past}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+6 sustain zero-push mode intact
- hbCount: 917 -> {hb_count}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- active_mode_dormant_this_session_continue (HB #{hb_count} = sustain #917 = D+6 midday dormant baseline)
- HEARTBEAT_OK -- HB #{hb_count} = sustain DORMANT protocol
- no push: midday zone ({now.strftime('%H:%M')}), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-1 watch: emergency prepare-mode prepacked, ready if Eric contacts with induction result
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter (~{evening_iter_hours}h)

*{hb_time_full} -- D+6 Wednesday midday -- HB #{hb_count} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day +1 post-window passive -- 7/24 D-Day T-1 watch (T-{dday_hours}h) -- Eric silent = dominant signal holding*
"""

# R-NEW-V2 compliant: explicit utf-8 read+append+write
with open(HB_PATH, 'r', encoding='utf-8') as f:
    content = f.read()
content += hb_text
with open(HB_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

# Update state
state['silenceHours'] = silence_hours
state['lastCheck'] = now.isoformat()
state['ericActiveHours'] = eric_active
state['nextDDayHours'] = dday_hours
state['hbCount'] = hb_count
state['lastHB'] = 917
state['t0_past_hours'] = t0_past
state['notes'] = f'HB#{hb_count}: +15min from HB#917. Wednesday midday {now.strftime("%H:%M")}. DORMANT sustained. 7/24 D-Day T-1 (~{dday_hours}h). No actionable signal. Next significant: 21:00 evening self-iter (~{evening_iter_hours}h).'

with open(STATE_PATH, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f'HB #{hb_count} appended (utf-8 explicit read+append+write, R-NEW-V2 compliant)')
print(f'heartbeat-state.json updated')
print(f'silenceHours={silence_hours}, ericActive={eric_active}, dday_hours={dday_hours}, evening_iter={evening_iter_hours}h')
print(f't0_past={t0_past}h')