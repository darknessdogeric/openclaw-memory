"""Minimal HB tick updater — R-NEW-V2 compliant (Python utf-8 explicit read+write)."""
import json
from datetime import datetime, timezone, timedelta

# Time setup
tz_china = timezone(timedelta(hours=8))
now = datetime.now(tz_china)
ts_str = now.strftime('%Y-%m-%dT%H:%M GMT+8')

# Load heartbeat-state
with open('memory/heartbeat-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

# Update state (HB #860 -> #861)
new_count = state['hbCount'] + 1
state['hbCount'] = new_count
state['lastHB'] = now.strftime('%H:%M')
state['lastHBTime'] = ts_str
state['last_update_epoch'] = int(now.timestamp())
# Eric last active elsewhere 7/19 12:33 -> ~64h+ by 04:58 7/22
state['silenceDuration_h'] = round((now.timestamp() - 1752895980) / 3600, 2)
state['silenceDuration_thisSession_h'] = round((now.timestamp() - 1752647760) / 3600, 2)
state['silenceDuration_global_h'] = state['silenceDuration_thisSession_h']
state['ericActiveElsewhere_h'] = state['silenceDuration_h']
state['mode'] = 'active_mode_dormant_this_session_silent_deep_night_post_cutoff'
state['note'] = 'HB #{n}; Wednesday deep-night 04:58; D+6 silent this session; execution-phase observer mode; zero-push per R256/R257/R258 intact; Triple Confluence Day 0 closed (7/21 24:00 cutoff passed)'.format(n=new_count)

# Save state
with open('memory/heartbeat-state.json', 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print('STATE UPDATED: HB #{} at {}'.format(new_count, ts_str))
print('Mode:', state['mode'])
print('Silence (this session):', state['silenceDuration_thisSession_h'], 'h')
print('Silence (Eric elsewhere):', state['silenceDuration_h'], 'h')
print('Next: 08:00 daily briefing (~3h2m); 21:00 evening self-iter')