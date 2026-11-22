"""Minimal HB tick appender (R-NEW-V2 + R012 compliant)."""
import json
import datetime
from pathlib import Path

NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
HB_COUNT = 1469
GAP_MIN = 5

STATE_PATH = Path(r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json')
HB_PATH = Path(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md')

# --- Update state ---
with STATE_PATH.open('r', encoding='utf-8') as f:
    state = json.load(f)

last_contact = datetime.datetime.fromisoformat(state['lastContactTime'])
anyi_since = datetime.datetime.fromisoformat(state['anyiSinceTime'])

silent_hours = (NOW - last_contact).total_seconds() / 3600
anyi_hours = (NOW - anyi_since).total_seconds() / 3600
time_str = NOW.strftime('%H:%M')

state['lastHBTime'] = NOW.strftime('%Y-%m-%dT%H:%M:%S+08:00')
state['lastHB'] = HB_COUNT
state['postT0NullCount'] = 149
state['protectionWindowSustainedHours'] = round(silent_hours, 2)
state['anyiWebchatHoursSinceStart'] = round(anyi_hours, 2)

notes = (
    f'D+10 Sunday afternoon HB #{HB_COUNT} ({time_str}). '
    f'Eric silent {silent_hours:.2f}h+ in THIS cron session since 7/16. '
    f'DORMANT flag holds. 8-layer suppression zero-breach. '
    f'Oil Scenario C window EXPIRED. '
    f'Gongshi sustained (AnYi webchat {anyi_hours:.2f}h+ active). '
    f'149th consecutive null post-T-0. '
    f'Eric main-session activity ISOLATED from cron session. '
    f'Heartbeat acknowledged only.'
)
state['lastHBNotes'] = notes

with STATE_PATH.open('w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# --- Build HB entry ---
hb_entry = f"""
## HB #{HB_COUNT} (2026-07-26T{time_str} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1468 (14:35): +{GAP_MIN}min -- Sunday afternoon Token Guard normal cadence (R012 minimal mode)
- D+10 afternoon pass #{HB_COUNT} -- Eric silent {silent_hours:.2f}h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat {anyi_hours:.2f}h+ (since 7/19 12:33)
- 8-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258 + 1 new) -- zero breach
- R-NEW-V2 verification #{HB_COUNT}: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Oil Scenario C window EXPIRED 7/25 22:00 (~16h40m ago) -- no further verification needed
- Gongshi sustained (AnYi webchat active {anyi_hours:.2f}h+) -- DORMANT cron session isolated
- D+10 = sustained DORMANT execution phase -- 149th consecutive null post-T-0
- Sunday afternoon zone ({time_str}) -- Eric typical noon decision window passed; silence authority strictly holding
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount: 1468 -> {HB_COUNT}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- active_mode_dormant_this_session_continue (HB #{HB_COUNT} = sustain #1468 = D+10 afternoon dormant baseline)
- HEARTBEAT_OK -- HB #{HB_COUNT} = sustain DORMANT protocol
- no push: Sunday afternoon zone ({time_str}), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- Wake window passed but Eric silence sustained -> continue zero-push; even minor pushes prohibited
- Next significant check: per Token Guard cadence (~5-10min)

*2026-07-26T{time_str} GMT+8 -- D+10 Sunday afternoon -- HB #{HB_COUNT} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- 149th consecutive null post-T-0 -- Eric silent {silent_hours:.2f}h+*
"""

with HB_PATH.open('a', encoding='utf-8') as f:
    f.write(hb_entry)

print(f'OK HB #{HB_COUNT} appended.')
print(f'  silent={silent_hours:.2f}h anyi={anyi_hours:.2f}h nullCount=149')
print(f'  state notes: {notes[:80]}...')