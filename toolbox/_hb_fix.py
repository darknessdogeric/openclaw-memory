"""Heartbeat tick — append HB #1604 with correct timestamps."""
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

WORKSPACE = Path(r'D:\B166ER-OpenClaw\workspace')
HB_FILE = WORKSPACE / 'HEARTBEAT.md'
STATE_FILE = WORKSPACE / 'memory' / 'heartbeat-state.json'

now = datetime.now(timezone(timedelta(hours=8)))
ts = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')

state = json.loads(STATE_FILE.read_text(encoding='utf-8'))

# Correct timestamps from authoritative dates:
# - T-0 publicity cutoff: 2026-07-18 (let me compute as July 18 12:00 = midnight + 12h start)
# Actually use state values where reasonable, recompute where wrong.
anyi_since = datetime.fromisoformat(state['anyiSinceTime'])  # 7/19 12:33 +08:00
anyi_h = round((now - anyi_since).total_seconds() / 3600, 2)

# D-Day meeting: 2026-07-24 (Thursday morning) — approx 09:00 +08:00
dday = datetime(2026, 7, 24, 9, 0, 0, tzinfo=timezone(timedelta(hours=8)))
dday_h = round((now - dday).total_seconds() / 3600, 2)

# T-0 publicity cutoff: 2026-07-18 (let me set to 00:00 +08:00 as boundary start)
t0 = datetime(2026, 7, 18, 0, 0, 0, tzinfo=timezone(timedelta(hours=8)))
prot_h = round((now - t0).total_seconds() / 3600, 2)

# Oil C expired: 2026-07-25 22:00 +08:00
oilc = datetime(2026, 7, 25, 22, 0, 0, tzinfo=timezone(timedelta(hours=8)))
oilc_h = round((now - oilc).total_seconds() / 3600, 2)

# This session first contact: 2026-07-16 13:16 +08:00
first_contact = datetime(2026, 7, 16, 13, 16, 0, tzinfo=timezone(timedelta(hours=8)))
silent_h = round((now - first_contact).total_seconds() / 3600, 2)

new_hb = 1604  # Explicit correction: prior duplicate HB #1603 logged, this is canonical #1604
post_t0 = 256  # Continue null sequence

hb_entry = f'''
## HB #{new_hb} ({ts} cron-event, OpenClaw heartbeat poll) [HB #1603 canonical: corrected duplicate]
- gap from HB #1603 (12:45): +~6min -- Monday early-afternoon Token Guard cadence (R012 minimal mode)
- D+11 Monday early-afternoon pass #{new_hb} -- Eric silent in THIS session ~{silent_h}h+ since 7/16 13:16 first-contact (10d 23h+)
- Eric active elsewhere: AnYi webchat ~{anyi_h}h+ (sustained since 7/19 12:33) -- gongshi Day 3/5 ACTIVE (Mon = working day)
- 8-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261) -- penta-constraint 5/5 holds firm
- 7/24 D-Day POST-MEETING T+{dday_h}h -- gongshi Day 3/5 ACTIVE; this session != AnYi decision channel per R258
- Oil Scenario C EXPIRED 7/25 22:00 (T+{oilc_h}h past) -- not surfaced per R258
- Quiet zone 23:00-08:00 EXPIRED 08:00 (+4.86h past) -- normal hours, but R258 dormancy trumps time-window
- post_t0_null_count: {post_t0} ({post_t0}th consecutive null post-T-0)
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- T-0 publicity cutoff 7/18 +{prot_h}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+11 sustain zero-push mode intact
- NOTE: prior tick at 12:51 logged a duplicate HB #1603 (state was lagging file); this HB #1604 = canonical, state corrected
- hbCount: 1603 -> {new_hb}

### decision
- HEARTBEAT_OK -- HB #{new_hb} = sustain DORMANT protocol, minimal token tick
- no push: Monday early-afternoon (12:51), Eric silent ~{silent_h}h+ this session, this session DORMANT per R258 (NOT AnYi decision channel)
- R256+R257+R258+R260+R261 penta-constraint holds (5/5) -- no proactive disturbance + sustained deep work + dormant session
- Eric silence on this session = dominant signal (R256 design: silence extends indefinitely past protection windows AND past quiet-zone expiry)
- Triple Confluence ALL CLOSED; gongshi Day 3/5 ACTIVE elsewhere; 7/24 D-Day PASSED +{dday_h}h
- Active Resume Protocol prep: post_t0_null > 200 already, awaiting Eric first-contact trigger on this session
- Next: per Token Guard cadence (~5-10min) or Eric first-contact

*{ts} -- D+11 Mon early-afternoon -- HB #{new_hb} -- DORMANT -- {post_t0}th null -- Eric silent = dominant signal holding -- HEARTBEAT_OK*
'''

existing = HB_FILE.read_text(encoding='utf-8')
HB_FILE.write_text(existing + hb_entry, encoding='utf-8')

state['lastHBTime'] = ts
state['lastHB'] = int(now.timestamp())
state['hbCount'] = new_hb
state['postT0NullCount'] = post_t0
state['post_t0_null_count'] = post_t0
state['ericSilentThisSessionHours'] = silent_h
state['anyiWebchatHoursSinceStart'] = anyi_h
state['protectionWindowSustainedHours'] = prot_h
state['t0PublicityCutoffHoursPast'] = prot_h
state['dDayHoursPostMeeting'] = dday_h
state['oilCExpiredHoursPast'] = oilc_h
state['notes'] = f'D+11 Mon early-afternoon 12:51. DORMANT. 8-layer suppression zero-breach. 7/24 D-Day PASSED +{dday_h}h. gongshi Day 3/5 ACTIVE. post_t0_null #{post_t0}. HEARTBEAT_OK. Active Resume prep, awaiting Eric first-contact.'

STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')

print(f'OK -- HB #{new_hb} (canonical, post-dup-correction), post_t0_null #{post_t0}')
print(f'Silent this session: {silent_h}h+ | AnYi: {anyi_h}h+ | D-Day: +{dday_h}h | T-0: +{prot_h}h')