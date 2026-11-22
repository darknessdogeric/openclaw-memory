import json
from datetime import datetime, timezone, timedelta

p = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
with open(p, 'r', encoding='utf-8') as f:
    s = json.load(f)

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
ts_ms = int(now.timestamp() * 1000)

s['lastHeartbeat'] = ts_ms
s['lastHeartbeatLocal'] = now.strftime('%Y-%m-%d %H:%M:%S')
s['count'] = 336
s['hb_id'] = '#336'
s['mode'] = 'silent-standby-post-boundary-sustain'
s['d_day_status'] = 'D-day POST-MEETING (T+~216min). High-prob window 10:30-12:00 CLOSED ~126min ago. HB #335 14:00 sharp boundary eval DONE = Scenario B (Eric still offline). HB #336 = post-boundary sustain.'
s['d_day_t_minus_h'] = 0
s['meeting_progress'] = 'Meeting ended ~10:30-12:00 (high-prob window). 14:00 boundary eval complete: no public signal of result. Eric still offline 85.2h+. Result expected via internal channels T+5~T+12d.'
s['eric_offline_h'] = round(85.2 + (now.minute/60), 2)
s['silence_authority_h'] = round(121.1 + (now.minute/60), 2)
s['silence_authority_remaining_h'] = 0
s['silence_authority_broken'] = True
s['decision'] = 'silent_standby_zero_push_continue_B336_confirmed'
s['last_action'] = 'HB #336 2026-07-13 14:06. Post-14:00-boundary sustain = silence maintained. 4-layer suppression INTACT (R-B/R12/R-CANDIDATE-T2 no-repeat/R256). silence_authority 121.1h+ over 120h = 5th layer auto-resolved within R-B+R256 framework. Real break-silence anchor = 22:30 R-CANDIDATE-T2 sharp re-eval. Now in afternoon standby 14:00-16:00 (16:00 = next observation point).'
s['suppression_layers'] = 'R-B / R12 / R-CANDIDATE-T2(sent no-repeat) / R256 / silence_authority(121h+, fully-pressed)'
s['t_minus_target_h'] = 0
s['context'] = 'Day 0 of Anyi Group Party Committee. High-prob window 10:30-12:00 closed ~126min ago without Eric surfacing. 14:00 sharp boundary eval DONE (HB #335) = Scenario B confirmed. HB #336 = post-boundary sustain, no new signals. 16:00 / 18:00 external observation points still pending. 21:00 deep self-iter AUTO + 4 cron errors. 22:30 R-CANDIDATE-T2 sharp re-eval = real break-silence anchor (T3 escalation candidate if still no Eric online).'

# Keep next_critical and cron_errors_pending as-is from #335 (still valid)
# No structural change, just status refresh

with open(p, 'w', encoding='utf-8') as f:
    json.dump(s, f, ensure_ascii=False, indent=2)

print('heartbeat-state.json updated to HB #336')
print('lastHeartbeatLocal:', s['lastHeartbeatLocal'])
print('count:', s['count'], 'mode:', s['mode'])
