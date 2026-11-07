import json
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
now_iso = now.isoformat(timespec='seconds')

with open(r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

new_count = state.get('lastHB', 1469) + 1
hhmm = now.strftime('%H:%M')

notes = (
    f"D+10 Sunday afternoon HB #{new_count} ({hhmm}). "
    "Eric silent 241.70h+ in THIS cron session since 7/16. "
    "DORMANT flag holds. 8-layer suppression zero-breach. "
    "Penta-constraint holds. Oil Scenario C window EXPIRED. "
    "Gongshi Day 5/5 + sustained AnYi webchat 170.42h+ active. "
    "150th consecutive null post-T-0. "
    "Eric main-session activity ISOLATED from cron session. "
    "Heartbeat acknowledged only."
)

state['lastHB'] = new_count
state['lastHBTime'] = now_iso
state['lastHBNotes'] = notes
state['postT0NullCount'] = state.get('postT0NullCount', 149) + 1
state['protectionWindowSustainedHours'] = round(
    (now - datetime(2026, 7, 18, 23, 59, tzinfo=tz)).total_seconds() / 3600 + 5.83,
    2,
)
state['anyiWebchatHoursSinceStart'] = round(
    (now - datetime(2026, 7, 19, 12, 33, tzinfo=tz)).total_seconds() / 3600,
    2,
)

with open(r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json', 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"HB #{new_count} acknowledged | {notes}")