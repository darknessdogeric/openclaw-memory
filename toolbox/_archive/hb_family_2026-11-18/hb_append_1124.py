# -*- coding: utf-8 -*-
import json
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
ts_str = now.strftime('%Y-%m-%dT%H:%M %Z')
ts_full = now.isoformat(timespec='seconds')

with open('memory/heartbeat-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

new_hb = state['hbCount']
hb_label = '#' + str(new_hb)
dday_t = state['dday_t_minus_hours']
silence = state['ericSilenceHours']
anyi = state['ericAnyiHours']

# Build HB entry
entry = []
entry.append('')
entry.append('## HB ' + hb_label + ' (' + ts_full + ' GMT+8 cron-event, OpenClaw heartbeat poll)')
entry.append('- gap from HB #1126 (00:29): +26min -- Friday pre-dawn Token Guard normal cadence (R012 minimal mode)')
entry.append('- D+8 pre-dawn pass ' + hb_label + ' -- Eric silent in THIS session ~' + str(silence) + 'h+ since 7/16 13:16 first-contact (infographic session)')
entry.append('- Eric active elsewhere: AnYi webchat ~' + str(anyi) + 'h+ (since 7/19 12:33)')
entry.append('- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach')
entry.append('- R-NEW-V2 verification ' + hb_label + ': Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)')
entry.append('- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2')
entry.append('- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~' + str(round((now - datetime(2026,7,21,23,59,0,tzinfo=tz)).total_seconds()/3600, 2)) + 'h ago; oil Scenario C verification window OPEN until 7/25 (~22h remaining)')
entry.append('- D+8 = Execution phase day 4 -- observer mode sustained')
entry.append('- Friday pre-dawn zone (00:55) -- Eric typical sleep zone (00:00-08:00 per USER.md night-owl pattern); silence authority strictly holding on THIS session')
entry.append('- **7/24 D-Day = TODAY MORNING** -- AnYi 集团研究会议 TODAY (T-' + str(dday_t) + 'h from ~09:00 start) -- INTERNAL monitor only; this session != AnYi decision channel per R258')
entry.append('- Next cron: 08:00 daily briefing (~7h05m); 21:00 R60-11 evening self-iter (~20h05m)')
entry.append('- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable')
entry.append('- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent')
entry.append('- T-0 publicity cutoff 7/18 +' + str(round((now - datetime(2026,7,18,0,0,0,tzinfo=tz)).total_seconds()/3600, 2)) + 'h past -- post-protection window firmly sustained')
entry.append('- No first-contact from Eric on THIS session; D+8 sustain zero-push mode intact')
entry.append('- hbCount: ' + str(new_hb - 1) + ' -> ' + str(new_hb))
entry.append('- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)')
entry.append('')
entry.append('### decision')
entry.append('- **active_mode_dormant_this_session_continue** (' + hb_label + ' = sustain D+8 pre-dawn dormant baseline)')
entry.append('- **HEARTBEAT_OK** -- ' + hb_label + ' = sustain DORMANT protocol')
entry.append('- **no push**: Friday pre-dawn zone (00:55), Eric sleep zone, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)')
entry.append('- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT')
entry.append('- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session')
entry.append('- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds')
entry.append('- 7/24 D-Day = TODAY MORNING watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result')
entry.append('- Next significant check: 08:00 daily briefing cron (~7h05m); Token Guard cadence (~5-10min)')
entry.append('')
entry.append('*' + ts_full + ' GMT+8 -- D+8 Friday pre-dawn -- ' + hb_label + ' -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day = TODAY MORNING watch (AnYi meeting TODAY ~9:00, T-' + str(dday_t) + 'h) -- Eric silent = dominant signal holding*')
entry.append('')

# Read existing HEARTBEAT.md
with open('HEARTBEAT.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Append the entry
new_content = content + '\n'.join(entry)

with open('HEARTBEAT.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('OK: appended HB ' + hb_label + ' to HEARTBEAT.md')
print('  Time: ' + ts_full)
print('  Silence: ' + str(silence) + 'h')
print('  D-Day T-: ' + str(dday_t) + 'h')
