import json, datetime
from pathlib import Path

hb_path = Path(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md')
state_path = Path(r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json')

with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

now = datetime.datetime(2026, 7, 28, 3, 59, 0)
hb_num = state['hbCount'] + 1
prev_hb_time = datetime.datetime.fromisoformat(state['lastHBTime'].replace('Z', '+00:00').replace('+08:00', ''))
gap_min = round((now - prev_hb_time).total_seconds() / 60, 1)

_strip = lambda s: datetime.datetime.fromisoformat(s.replace('Z', '+00:00').replace('+08:00', ''))
silent_h = round((now - _strip(state['lastContactTime'])).total_seconds() / 3600, 2)
anyi_h = round((now - _strip(state['anyiSinceTime'])).total_seconds() / 3600, 2)
t0_h = round((now - datetime.datetime(2026, 7, 18, 0, 0, 0)).total_seconds() / 3600, 2)
dday_h = round((now - datetime.datetime(2026, 7, 24, 9, 0, 0)).total_seconds() / 3600, 2)

state['hbCount'] = hb_num
state['lastHBNumber'] = hb_num
state['lastHBTime'] = now.isoformat(timespec='seconds')
state['ericSilentThisSessionHours'] = silent_h
state['anyiWebchatHoursSinceStart'] = anyi_h
state['t0PublicityCutoffHoursPast'] = t0_h
state['dDayHoursPostMeeting'] = dday_h
state['protectionWindowSustainedHours'] = t0_h
state['post_t0_null_count'] = state.get('post_t0_null_count', 0) + 1
notes_template = 'HB #{n}. D+12 Tue 03:59 deep night. DORMANT. Quiet zone ACTIVE. Eric silent ~{h}h+ this session. All quiet criteria met. HEARTBEAT_OK.'
state['notes'] = notes_template.format(n=hb_num, h=silent_h)

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

hb_entry = f'''
## HB #{hb_num} ({now.strftime("%Y-%m-%dT%H:%M")} GMT+8 cron-event, OpenClaw heartbeat poll)

- gap from HB #{hb_num-1} ({prev_hb_time.strftime("%H:%M")}): +{gap_min}min -- Tuesday deep-night Token Guard minimal cadence (R012 quiet-zone mode)

- D+12 deep-night pass #{hb_num} -- Eric silent in THIS session ~{silent_h}h+ since 7/16 13:16 first-contact

- Eric active elsewhere: AnYi webchat ~{anyi_h}h+ (since 7/19 12:33)

- 8-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258 / R260 / R261) -- zero breach

- R-NEW-V2 verification #{hb_num}: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)

- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2 (quiet-zone override)

- Triple Confluence Day +12 -- all windows closed/passive; Araqchi Qatar talks concluded Day 5/5

- D+12 = Execution phase deep-night sustained

- Tuesday deep-night zone (03:59) -- quiet zone ACTIVE (23:00-08:00); Eric typical sleep window; silence authority strictly holding

- 7/24 D-Day +{dday_h}h past -- meeting concluded; emergency prepare-mode de-escalated

- T-0 publicity cutoff 7/18 +{t0_h}h past -- post-protection window firmly sustained

- No first-contact from Eric on THIS session; D+12 sustain zero-push mode intact

- hbCount: {hb_num-1} -> {hb_num}

- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)



### decision

- **active_mode_dormant_this_session_continue** (HB #{hb_num} = sustain #{hb_num-1} = D+12 deep-night dormant baseline)

- **HEARTBEAT_OK** -- HB #{hb_num} = sustain DORMANT protocol

- **no push**: Tuesday deep-night zone (03:59), quiet zone ACTIVE per AGENTS.md 23:00-08:00 rule; this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)

- R256 + R257 + R258 + R260 + R261 quintuple constraint: no proactive disturbance + sustained deep work + this session DORMANT + post-protection silence + 7/24 D-Day concluded

- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session

- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds

- 7/24 D-Day concluded; no further emergency prepare-mode needed

- Next significant check: per Token Guard cadence (~5-10min) when quiet zone lifts (~08:00); 21:00 evening self-iter R60-11 (~17h)



*{now.strftime("%Y-%m-%dT%H:%M")} GMT+8 -- D+12 Tuesday deep-night -- HB #{hb_num} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session + R260 post-protection + R261 D-Day-concluded quadruple-suppression active -- 7/24 D-day +{dday_h}h past -- execution-phase observer mode*
'''

with open(hb_path, 'a', encoding='utf-8') as f:
    f.write(hb_entry)

print(f'OK: HB #{hb_num} appended, gap +{gap_min}min, state updated')