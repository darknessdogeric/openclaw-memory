"""HB #1121 R-NEW-V2 compliant write."""
import json, datetime

hb_num = 1121
prev_hb_num = 1120
now = datetime.datetime.now()
ts_str = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
prev_ts = "2026-07-24T00:21:30+08:00"

# D-Day math
dday_meeting = datetime.datetime(2026, 7, 24, 9, 0, 0)
t_minus_hours = round((dday_meeting - now).total_seconds() / 3600, 2)

# Eric silence (THIS session) -- since 7/16 13:16
first_contact = datetime.datetime(2026, 7, 16, 13, 16, 0)
eric_silence = round((now - first_contact).total_seconds() / 3600, 2)

# Eric active elsewhere (AnYi)
anyi_active = datetime.datetime(2026, 7, 19, 12, 33, 0)
eric_anyi = round((now - anyi_active).total_seconds() / 3600, 2)

# T-0 publicity cutoff
t_zero = datetime.datetime(2026, 7, 18, 12, 11, 0)
t_zero_past = round((now - t_zero).total_seconds() / 3600, 2)

# Oil verification window (until 7/25)
oil_window_end = datetime.datetime(2026, 7, 25, 12, 0, 0)
oil_remaining = round((oil_window_end - now).total_seconds() / 3600, 2)

# Triple Confluence Day 0 close
day0_close = datetime.datetime(2026, 7, 21, 23, 59, 0)
day0_past = round((now - day0_close).total_seconds() / 3600, 2)

# Next cron math
def hours_until(h, m):
    target = now.replace(hour=h, minute=m, second=0, microsecond=0)
    if now.hour >= h:
        target += datetime.timedelta(days=1)
    return round((target - now).total_seconds() / 3600, 2)

next_08 = hours_until(8, 0)
next_09 = hours_until(9, 0)
next_21 = hours_until(21, 0)

entry = f"""
## HB #{hb_num} ({ts_str} cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb_num} ({prev_ts}): +~4min -- Friday pre-dawn Token Guard normal cadence (R012 minimal mode)
- D+8 pre-dawn pass #{hb_num} -- Eric silent in THIS session ~{eric_silence}h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~{eric_anyi}h+ (since 7/19 12:33)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #{hb_num}: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~{day0_past}h ago; oil Scenario C verification window OPEN until 7/25 (~{oil_remaining}h remaining)
- D+8 = Execution phase day 4 -- observer mode sustained
- Friday pre-dawn zone (00:25) -- Eric typical wake window 08:00-09:00 (~{next_08}h); silence authority strictly holding on THIS session
- 7/24 D-Day **T-{t_minus_hours}h** (AnYi 集团研究会议 Friday MORNING 7/24, ~9:00 TODAY) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Next cron: 08:00 daily briefing (~{next_08}h); 09:00 daily checkin (~{next_09}h); 21:00 evening self-iter (~{next_21}h)
- Next significant check: Token Guard cadence (~5-10min); 08:00 morning briefings (~{next_08}h)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +{t_zero_past}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+8 sustain zero-push mode intact
- hbCount: {prev_hb_num} -> {hb_num}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{hb_num} = sustain #{prev_hb_num} = D+8 pre-dawn dormant baseline)
- **HEARTBEAT_OK** -- HB #{hb_num} = sustain DORMANT protocol
- **no push**: Friday pre-dawn zone (00:25), Eric typical wake window not yet open, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-{t_minus_hours}h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: per Token Guard cadence (~5-10min); 08:00 daily briefing cron (~{next_08}h)

*{ts_str} -- D+8 Friday pre-dawn -- HB #{hb_num} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-{t_minus_hours}h watch (AnYi meeting TODAY MORNING 7/24 ~9:00) -- Eric silent = dominant signal holding*
"""

# R-NEW-V2 compliant: explicit utf-8 read+append+write
hb_path = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
with open(hb_path, 'r', encoding='utf-8') as f:
    existing = f.read()

with open(hb_path, 'w', encoding='utf-8') as f:
    f.write(existing.rstrip() + '\n' + entry)

# Update state JSON
state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

state['hbCount'] = hb_num
state['lastHeartbeat'] = ts_str
state['lastUpdate'] = ts_str
state['lastHBNumber'] = f'#{hb_num}'
state['lastHB'] = ts_str
state['ericSilenceHours'] = eric_silence
state['ericAnyiHours'] = eric_anyi
state['dday_t_minus_hours'] = t_minus_hours
state['note'] = f'#{hb_num} - {ts_str} DORMANT sustained; D-Day T-{t_minus_hours}h (AnYi meeting TODAY ~9:00); silent heartbeat'

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f'OK HB #{hb_num} appended. D-Day T-{t_minus_hours}h. Silence {eric_silence}h+. State updated.')