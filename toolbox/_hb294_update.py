"""One-shot heartbeat state updater for HB #294 (10:03 GMT+8, 2026-07-16)"""
import json
from datetime import datetime, timezone

path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'

# Load existing
with open(path, 'r', encoding='utf-8') as f:
    s = json.load(f)

# Current hbCount from JSON = 293 (last logged). This run = HB #294
prev = int(s.get('hbCount', 293))
new_count = 294  # explicit: this is HB #294

# Silence start: 2026-07-09 04:29 GMT+8 = 2026-07-08 20:29 UTC
silence_start_utc = datetime(2026, 7, 8, 20, 29, tzinfo=timezone.utc)
now_utc = datetime.now(timezone.utc)
silence_hours = round((now_utc - silence_start_utc).total_seconds() / 3600, 1)

s['hbCount'] = new_count
s['lastHB'] = '#' + str(new_count)
s['silenceHours'] = silence_hours
s['deepWorkHours'] = silence_hours
s['lastChecks']['heartbeat'] = int(now_utc.timestamp())
s['mode'] = 'silent_standby_zero_push'
s['notes'] = (
    f"HB #{new_count} (silent standby, no push). 10:03 GMT+8 Thu. "
    f"Eric silent D+7+ since 7/9 04:29 (~{silence_hours}h). "
    f"4-layer suppression holding. Morning zone active (post 08:30 cron boundary). "
    f"08:30 global industry briefing cron = fired (T+1h33m, autonomous). "
    f"Next major: 暑期复盘(T+12) 9/10. No urgent cron. HEARTBEAT_OK."
)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(s, f, ensure_ascii=False, indent=2)

print(f"OK hbCount={s['hbCount']} lastHB={s['lastHB']} silenceHours={s['silenceHours']}")
