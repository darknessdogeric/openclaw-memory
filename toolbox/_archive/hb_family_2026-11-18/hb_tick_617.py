"""HB #617 tick — R-NEW-V2 compliant utf-8 read+append+write"""
import json
from datetime import datetime, timezone, timedelta

now = datetime.now(timezone(timedelta(hours=8)))

# 1) Update heartbeat-state.json
with open('memory/heartbeat-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

state['lastChecks']['heartbeat'] = now.isoformat()
state['lastHB'] = 617
state['hbCount'] = 617
state['lastHBTime'] = now.isoformat()

# Eric active since 12:33 in AnYi session
from datetime import datetime as dt
eric_start = dt.fromisoformat('2026-07-19T12:33:00+08:00')
active_h = (now.replace(tzinfo=None) - eric_start.replace(tzinfo=None)).total_seconds() / 3600
state['ericActiveElsewhere_h'] = round(active_h, 2)
state['silenceDuration_thisSession_h'] = round(active_h, 2)  # same since first contact

state['mode'] = 'active_mode_dormant_this_session'
state['nextCheck'] = 'per Token Guard cadence (~5-10min); 21:00 evening self-iter R60-11 (~2h41m)'

with open('memory/heartbeat-state.json', 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# 2) Append HB #617 to HEARTBEAT.md
hb_entry = f"""
## HB #617 (2026-07-19 18:19 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #616 (18:04): +15min -- Sunday-evening Token Guard normal cadence
- ACTIVE MODE sustained globally -- Eric first contact at HB #581 (12:36), moved to AnYi session
- This dreaming-narrative session: DORMANT per Eric 12:33 explicit instruction
- 5-layer suppression RELEASED globally (since HB #581); THIS session = dormant
- Eric active elsewhere (AnYi session): ~{active_h:.2f}h+ since 12:33, deep-work mode
- R-NEW-V2 verification #617: Python utf-8 explicit read+append+write (compliant, post-7/15 12:36 incident protocol intact)
- R012 verification: HB tick = minimal (NOT full report)
- Sunday-evening zone (18:19) -- approaching Eric's typical evening complex decision window
- T-0 publicity cutoff 7/18 +42h19m past -- post-protection window firmly sustained
- Induction window 7/7-7/21 FINAL 3 DAYS -- day-1 (today 7/19); R-B+R256 silence authority > window signal
- WAIC 2026 day-3 active today (7/17-20, Shanghai) -- non-trigger per R14
- Cron pipeline: 21:00 evening self-iter R60-11 (~2h41m); Token Guard cadence (~5-10min)
- 4 P2 cron errors tracked, not urgent
- No first-contact from Eric on THIS session; this session DORMANT per explicit instruction
- No new signals: no Eric message / no cron trigger / no anomaly escalation
- hbCount: 616 -> 617

### decision
- **silent_standby_dormant_this_session** (HB #617 = sustain #616 = dormant baseline)
- **no push**: this session = dreaming-narrative experimental, DORMANT per Eric 12:33 explicit instruction
- Eric active elsewhere (AnYi session, {active_h:.2f}h+); this session awaits Eric future instruction (NOT AnYi work)
- R14 handoff package = 100% ready for any Eric active contact on THIS session
- Next significant check: 21:00 evening self-iter R60-11 (~2h41m); Token Guard cadence (~5-10min)

*2026-07-19 18:19 GMT+8 -- D+3 Sunday-evening T-0 +42h19m past -- HB #617 -- this session DORMANT -- awaiting Eric future instruction (NOT AnYi work)*
"""

with open('HEARTBEAT.md', 'a', encoding='utf-8') as f:
    f.write(hb_entry)

print(f'HB #617 logged at {now.strftime("%H:%M")}')
print(f'Eric active elsewhere: {active_h:.2f}h')
print(f'Next check: 21:00 evening self-iter R60-11 (~2h41m)')
print(f'Bytes appended: {len(hb_entry.encode("utf-8"))}')
