"""Minimal HB tick updater — fix: preserve existing duration fields, just bump count + timestamps."""
import json
from datetime import datetime, timezone, timedelta

# Time setup
tz_china = timezone(timedelta(hours=8))
now = datetime.now(tz_china)
ts_str = now.strftime('%Y-%m-%dT%H:%M GMT+8')

# Load heartbeat-state (preserving existing duration fields which were already correct)
with open('memory/heartbeat-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

# Update only count + timestamps + mode
new_count = state['hbCount'] + 1
state['hbCount'] = new_count
state['lastHB'] = now.strftime('%H:%M')
state['lastHBTime'] = ts_str
state['last_update_epoch'] = int(now.timestamp())
state['mode'] = 'active_mode_dormant_this_session_silent_deep_night_post_cutoff'
state['note'] = 'HB #{n}; Wednesday deep-night 04:58; D+6 silent this session; execution-phase observer mode; zero-push per R256/R257/R258 intact; Triple Confluence Day 0 closed (7/21 24:00 cutoff passed); await Eric active contact'.format(n=new_count)
state['nextCheck'] = 'per Token Guard cadence (~5-10min); 08:00 daily briefing (~3h2m); 21:00 evening self-iter (~16h)'

# Save state
with open('memory/heartbeat-state.json', 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print('STATE UPDATED: HB #{} at {}'.format(new_count, ts_str))
print('Mode:', state['mode'])
print('Existing silence (this session):', state.get('silenceDuration_thisSession_h'), 'h')
print('Existing silence (Eric elsewhere):', state.get('ericActiveElsewhere_h'), 'h')
print('Next check: 08:00 daily briefing (~3h2m)')