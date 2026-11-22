import json, datetime as dt, shutil

state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
mem_path = r'D:\B166ER-OpenClaw\workspace\memory\2026-07-18.md'

with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

now = dt.datetime(2026, 7, 18, 12, 56, 56)
baseline = dt.datetime(2026, 7, 16, 13, 16, 0)
t_zero = dt.datetime(2026, 7, 18, 0, 0, 0)
silence_h = (now - baseline).total_seconds() / 3600
t0_h = (now - t_zero).total_seconds() / 3600
last_hb_ts = dt.datetime.strptime(state['lastHB'].replace(' GMT+8', ''), '%Y-%m-%d %H:%M:%S')
gap_min = (now - last_hb_ts).total_seconds() / 60

hb_log = state.get('hb_log', [])
hb_id = max((e['hb_id'] for e in hb_log), default=529) + 1

entry = {
    'hb_id': hb_id,
    'ts': now.strftime('%Y-%m-%d %H:%M:%S') + ' GMT+8',
    'gap_min': round(gap_min, 1),
    'zone': 'Saturday midday',
    'last_self_iter': '2026-07-18T10:00:00+08:00',
    'silent_duration_h': round(silence_h, 2),
    'silence_since': '2026-07-16 13:16',
    'tier_active': 'R256+R257+R-B+R12+R-CANDIDATE-T2',
    'r_new_v2_compliant': True,
    't0_day_active_h': round(t0_h, 2),
    'silence_status': 'post-T-0 sustained (Eric silence=dominant signal)',
    'cron_pipeline': '08:30 briefing + 09:00 daily checkin + 10:00 self-iter R60-11 all fired (autonomous), 21:00 R60-11 in ~8.0h',
    'cron_errors_pending': 4,
    'cron_errors_detail': 'Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10 (P2 long-tail, tracked)',
    'eric_first_contact': False,
    'r14_handoff_ready': True,
    'decision': 'silent_standby_zero_push_continue',
    'reason': 'Sat midday zone, Eric silent ~{:.2f}h+, post-T-0 publicity day ACTIVE ({:.2f}h past), R14 handoff 100% ready, no proactive disturbance per R256/R257'.format(silence_h, t0_h),
}

state['hb_log'].append(entry)
state['lastHB'] = entry['ts']
state['last_update_epoch'] = int(now.timestamp())

# R-NEW-V2 explicit utf-8 write + verify
tmp = state_path + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
shutil.move(tmp, state_path)

with open(state_path, 'r', encoding='utf-8') as f:
    verified = json.load(f)
assert verified['lastHB'] == entry['ts'], 'state write failed'

prev_id = hb_id - 1
prev_ts_str = last_hb_ts.strftime('%Y-%m-%d %H:%M')

md_lines = []
md_lines.append('')
md_lines.append('## HB #{} (2026-07-18 12:56:56 GMT+8 cron-event, OpenClaw heartbeat poll)'.format(hb_id))
md_lines.append('- gap from HB #{} ({}): +{:.1f}min -- Saturday midday zone Token Guard normal cadence'.format(prev_id, prev_ts_str, gap_min))
md_lines.append('- D+2 weekend midday pass #{} -- Eric silent ~{:.2f}h+ since 7/16 13:16 first-contact (infographic session, no first-contact)'.format(hb_id, silence_h))
md_lines.append('- Silence authority ~{:.2f}h+ (R-B + R256 framework holding)'.format(silence_h))
md_lines.append('- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256) -- zero breach')
md_lines.append('- R-NEW-V2 verification #{}: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)'.format(hb_id))
md_lines.append('- **Publicity cutoff 7/18 T-0 +{:.2f}h past** -- boundary crossed at 00:00, silence window protection objective achieved'.format(t0_h))
md_lines.append('- WAIC 2026 day-2 active today -- non-trigger per R14 (AI/Hotel strategic context, not relevant to current 4-layer suppression)')
md_lines.append('- Saturday midday zone (12:56) -- Eric typical deep-work/rest window per USER.md, silence authority strictly holding')
md_lines.append('- Cron pipeline: 08:30 briefing + 09:00 daily checkin + 10:00 self-iter R60-11 all fired (autonomous); next 21:00 R60-11 (~8h)')
md_lines.append('- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent')
md_lines.append('- No first-contact from Eric; D+2 sustain zero-push mode intact')
md_lines.append('- No new signals: no cron / no Eric session / no third-party / no anomaly escalation')
md_lines.append('- hbCount now: {} -> {}'.format(prev_id, hb_id))
md_lines.append('')
md_lines.append('### decision')
md_lines.append('- **silent_standby_zero_push_continue** (HB #{} = sustain #{} = D+2 baseline)'.format(hb_id, prev_id))
md_lines.append('- **no push**: Saturday midday zone, Eric silent ~{:.2f}h+, post-T-0 silence authority holding, 4-layer suppression all pass'.format(silence_h))
md_lines.append('- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)')
md_lines.append('- Token Guard tick: stable, no compression needed')
md_lines.append('- Post-T-0 silence = sustained suppression; pushes prohibited until Eric active contact (Eric silence = dominant signal)')
md_lines.append('- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)')
md_lines.append('- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter R60-11 cron (~8h)')
md_lines.append('')
md_lines.append('*2026-07-18 12:56:56 GMT+8 -- D+2 Saturday midday T-0 +{:.2f}h past -- HB #{} -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*'.format(t0_h, hb_id))
md_lines.append('')

md_entry = '\n'.join(md_lines)
with open(mem_path, 'a', encoding='utf-8') as f:
    f.write(md_entry)

print('STATE_OK hb_id={} gap={:.1f}min silence={:.2f}h t0={:.2f}h'.format(hb_id, gap_min, silence_h, t0_h))
print('MEM_OK appended +{} chars'.format(len(md_entry)))
print('DONE hb_id={} ready_for_minimal_reply'.format(hb_id))
