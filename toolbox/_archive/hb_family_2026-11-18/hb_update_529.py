#!/usr/bin/env python3
"""HB #529 update — silent_standby_zero_push_continue."""
import json
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
p = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'

d = json.load(open(p, encoding='utf-8'))

entry = {
    'hb_id': 529,
    'ts': now.strftime('%Y-%m-%d %H:%M:%S GMT+8'),
    'gap_min': 4.8,
    'zone': 'Saturday midday',
    'last_self_iter': '2026-07-18T10:00:00+08:00',
    'silent_duration_h': 47.59,
    'silence_since': '2026-07-16 13:16',
    'tier_active': 'R256+R257+R-B+R12+R-CANDIDATE-T2',
    'r_new_v2_compliant': True,
    't0_day_active_h': 12.87,
    'silence_status': 'post-T-0 sustained (Eric silence=dominant signal)',
    'cron_pipeline': '08:30 briefing + 09:00 daily checkin + 10:00 self-iter R60-11 all fired (autonomous), 21:00 R60-11 in ~8.1h',
    'cron_errors_pending': 4,
    'cron_errors_detail': 'Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10 (P2 long-tail, tracked)',
    'eric_first_contact': False,
    'r14_handoff_ready': True,
    'decision': 'silent_standby_zero_push_continue',
    'reason': 'Sat midday zone, Eric silent ~47.59h+, post-T-0 publicity day ACTIVE (12.87h past), R14 handoff 100% ready, no proactive disturbance per R256/R257',
}

d['hb_log'].append(entry)
d['lastHB'] = now.strftime('%Y-%m-%d %H:%M:%S GMT+8')
d['last_update_epoch'] = int(now.timestamp())
d['notes'] = f'#529 (silent standby). {now.strftime("%Y-%m-%d %H:%M:%S GMT+8")} - Saturday midday, Eric silent ~47.59h+, post-T-0 publicity day ACTIVE (12.87h past), R14 handoff 100% ready, no proactive disturbance per R256/R257'

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'OK hb=529 silence=47.59h t0_active=12.87h decision=silent_standby_zero_push')