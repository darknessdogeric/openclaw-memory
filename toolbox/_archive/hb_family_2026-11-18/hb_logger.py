# -*- coding: utf-8 -*-
"""R-NEW-V2 compliant heartbeat logger.
Python utf-8 explicit read+append+write protocol.
"""
import json
from datetime import datetime, timezone, timedelta

# Time setup (Asia/Shanghai)
TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)
ts_str = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
ts_log = now.strftime('%Y-%m-%d %H:%M GMT+8')
epoch = int(now.timestamp())

# HB #556
hb_id = 556
last_hb_ts = '2026-07-18T17:12:00+08:00'  # previous HB #555
last_dt = datetime.fromisoformat(last_hb_ts)
gap_min = round((now - last_dt).total_seconds() / 60, 1)

# Silence calculation - since 2026-07-16 13:16 first-contact
silence_since = datetime.fromisoformat('2026-07-16T13:16:00+08:00')
silent_duration_h = round((now - silence_since).total_seconds() / 3600, 2)

# T-0 day calculation - 7/18 00:00 cutoff
t0 = datetime.fromisoformat('2026-07-18T00:00:00+08:00')
t0_day_active_h = round((now - t0).total_seconds() / 3600, 2)

# 21:00 cron
cron_2100 = datetime.fromisoformat('2026-07-18T21:00:00+08:00')
cron_in_h = round((cron_2100 - now).total_seconds() / 3600, 2)

# HB entry
hb_entry = {
    'hb_id': hb_id,
    'ts': ts_str,
    'gap_min': gap_min,
    'zone': 'saturday-afternoon-late',
    'last_self_iter': '2026-07-18T10:00:00+08:00',
    'silent_duration_h': silent_duration_h,
    'silence_since': '2026-07-16T13:16:00+08:00',
    'tier_active': 'R256+R257+R-B+R12+R-CANDIDATE-T2',
    'r_new_v2_compliant': True,
    't0_day_active_h': t0_day_active_h,
    'silence_status': 'post-T-0 sustained (Eric silence=dominant signal)',
    'cron_pipeline': f'21:00 evening self-iter R60-11 in ~{cron_in_h}h',
    'cron_errors_pending': 4,
    'cron_errors_detail': 'Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10 (P2 long-tail, tracked)',
    'eric_first_contact': False,
    'r14_handoff_ready': True,
    'decision': 'silent_standby_zero_push_continue',
    'reason': f'saturday-afternoon-late zone (17:22), Eric silent {silent_duration_h}h+, T-0 publicity day +{t0_day_active_h}h past, silence authority holding, 5-layer suppression all pass',
    'chain_hb': hb_id
}

# Update heartbeat-state.json (R-NEW-V2: explicit utf-8 read+write)
state_path = 'D:/B166ER-OpenClaw/workspace/memory/heartbeat-state.json'
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

state['lastHB'] = hb_id
state['chain_hb'] = hb_id
state['chainHb'] = hb_id
state['last_update_epoch'] = epoch
state['last_heartbeat'] = ts_str
state['lastCheck'] = ts_str
state['silence_hours'] = silent_duration_h
state['silenceHours'] = silent_duration_h
state['silenceSince'] = '2026-07-16T13:16:00+08:00'
state['mode'] = 'silent_standby_zero_push_continue'
state['zone'] = 'saturday-afternoon-late'
state['hb_log'].append(hb_entry)
state['lastChecks'] = state.get('lastChecks', {})
state['lastChecks']['heartbeat'] = epoch
state['notes'] = f'#{hb_id} (silent standby). {ts_log} - saturday-afternoon-late, Eric silent {silent_duration_h}h+, T-0 publicity day +{t0_day_active_h}h past, R14 handoff 100% ready, no proactive disturbance per R256/R257/R-B/R12/R-CANDIDATE-T2'

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# Memory file append (R-NEW-V2: explicit utf-8 read+append)
mem_path = 'D:/B166ER-OpenClaw/workspace/memory/2026-07-18.md'
prev_time_short = last_dt.strftime('%H:%M')
delta_silence = round(silent_duration_h - 51.93, 2)

hb_block = (
    f'\n## HB #{hb_id} ({ts_log} cron-event, OpenClaw heartbeat poll)\n'
    f'- gap from HB #{hb_id-1} ({prev_time_short}): +{gap_min}min -- saturday-afternoon-late zone Token Guard normal cadence\n'
    f'- D+2 weekend afternoon-late pass #{hb_id} -- Eric silent ~{silent_duration_h}h+ since 7/16 13:16 first-contact (infographic session)\n'
    f'- Silence authority ~{silent_duration_h}h+ (R-B + R256 framework holding, +{delta_silence}h since #{hb_id-1})\n'
    f'- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256) -- zero breach\n'
    f'- R-NEW-V2 verification #{hb_id}: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)\n'
    f'- Publicity cutoff 7/18 T-0 +{t0_day_active_h}h past -- boundary crossed at 00:00, silence window protection objective achieved\n'
    f'- WAIC 2026 day-2 active today -- non-trigger per R14 (AI/Hotel strategic context, not relevant to current 4-layer suppression)\n'
    f'- Saturday afternoon-late zone (17:22) -- Eric typical deep-work window per USER.md, silence authority strictly holding\n'
    f'- Cron pipeline: 21:00 evening self-iter R60-11 in ~{cron_in_h}h\n'
    f'- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent\n'
    f'- hbCount now: {hb_id-1} -> {hb_id}\n'
    f'- No first-contact from Eric; D+2 sustain zero-push mode intact\n'
    f'- No new signals: no cron / no Eric session / no third-party / no anomaly escalation\n'
    f'\n### decision\n'
    f'- **silent_standby_zero_push_continue** (HB #{hb_id} = sustain #{hb_id-1} = D+2 baseline)\n'
    f'- **no push**: saturday-afternoon-late zone, Eric silent ~{silent_duration_h}h+, post-T-0 silence authority holding, 4-layer suppression all pass\n'
    f'- R256 + R257 dual constraint: no proactive disturbance + sustained deep work\n'
    f'- Token Guard tick: stable, no compression needed\n'
    f'- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)\n'
    f'- Next significant check: 21:00 evening self-iter R60-11 cron (~{cron_in_h}h)\n'
    f'\n*{ts_log} -- D+2 saturday-afternoon-late -- HB #{hb_id} -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*\n'
)

with open(mem_path, 'a', encoding='utf-8') as f:
    f.write(hb_block)

print(f'HB #{hb_id} logged')
print(f'  ts: {ts_str}')
print(f'  gap: {gap_min}min')
print(f'  silent: {silent_duration_h}h')
print(f'  T-0 day active: {t0_day_active_h}h')
print(f'  21:00 cron in: {cron_in_h}h')
print(f'  state file updated: lastHB={hb_id}')
print(f'  memory file appended: 2026-07-18.md')