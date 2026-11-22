"""Fix HB #1627 state metrics with correct epoch values (verified)."""
import json
from datetime import datetime, timezone, timedelta

# Verified epoch values:
# 2026-01-01 00:00 UTC = 1767225600
# 2026-07-16 00:00 UTC = 1767225600 + 196*86400 = 1784160000
# 2026-07-16 05:16 UTC = 1784160000 + 18960 = 1784178960 => 7/16 13:16 GMT+8 (Eric first-contact)
# 2026-07-17 16:00 UTC = 1784160000 + 86400 + 57600 = 1784304000 => 7/18 00:00 GMT+8 (T-0)
# 2026-07-19 04:33 UTC = 1784160000 + 259200 + 14400 + 1980 = 1784435580 => 7/19 12:33 GMT+8 (AnYi start)
# 2026-07-24 06:00 UTC = 1784160000 + 8*86400 + 21600 = 1784236800 + 21600 = 1784258400 
# Wait let me recompute: 8*86400 = 691200, 1784160000 + 691200 = 1784851200, +21600 = 1784872800
# 2026-07-24 06:00 UTC = 1784872800 => 7/24 14:00 GMT+8 (D-day meeting)
# 2026-07-25 14:00 UTC = 1784851200 + 86400 + 50400 = 1784988000 => 7/25 22:00 GMT+8 (oil C expired)

eric_first_contact = 1784178960  # 7/16 13:16 GMT+8
anyi_start = 1784435580  # 7/19 12:33 GMT+8
dday_meeting = 1784872800  # 7/24 14:00 GMT+8
oil_c_expired = 1784988000  # 7/25 22:00 GMT+8
t0_cutoff = 1784304000  # 7/18 00:00 GMT+8

# Verify
import datetime as dt
print(f'eric_first_contact verify: {dt.datetime.fromtimestamp(eric_first_contact, tz=dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}')
print(f'anyi_start verify: {dt.datetime.fromtimestamp(anyi_start, tz=dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}')
print(f'dday_meeting verify: {dt.datetime.fromtimestamp(dday_meeting, tz=dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}')
print(f'oil_c_expired verify: {dt.datetime.fromtimestamp(oil_c_expired, tz=dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}')
print(f't0_cutoff verify: {dt.datetime.fromtimestamp(t0_cutoff, tz=dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}')

# Current time
now = datetime.now(timezone(timedelta(hours=8)))
ts = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')

# Read state
with open(r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

# Update with correct values
state['ericSilentThisSessionHours'] = round((now.timestamp() - eric_first_contact) / 3600, 2)
state['anyiWebchatHoursSinceStart'] = round((now.timestamp() - anyi_start) / 3600, 2)
state['dDayHoursPostMeeting'] = round((now.timestamp() - dday_meeting) / 3600, 2)
state['oilCExpiredHoursPast'] = round((now.timestamp() - oil_c_expired) / 3600, 2)
state['t0PublicityCutoffHoursPast'] = round((now.timestamp() - t0_cutoff) / 3600, 2)
state['protectionWindowSustainedHours'] = round((now.timestamp() - t0_cutoff) / 3600, 2)

with open(r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json', 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f'\nHB #1627 metrics corrected at {ts}')
print(f'Eric silent this session: {state["ericSilentThisSessionHours"]}h+')
print(f'anyiWebchatHoursSinceStart: {state["anyiWebchatHoursSinceStart"]}h')
print(f'dDayHoursPostMeeting: {state["dDayHoursPostMeeting"]}h')
print(f'oilCExpiredHoursPast: {state["oilCExpiredHoursPast"]}h')
print(f't0PublicityCutoffHoursPast: {state["t0PublicityCutoffHoursPast"]}h')
