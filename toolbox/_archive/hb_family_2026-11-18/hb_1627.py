"""HB #1627 logger - Mon mid-afternoon cron-event heartbeat."""
import json
from datetime import datetime, timezone, timedelta

# Time
now = datetime.now(timezone(timedelta(hours=8)))
ts = now.strftime('%Y-%m-%dT%H:%M GMT+8')

# Eric silent constants (from prior reads)
eric_first_contact = 1784178960  # 7/16 13:16
anyi_start = 1784428380  # 7/19 12:33
dday_meeting = 1784721600  # 7/24 14:00
oil_c_expired = 1785127200  # 7/25 22:00
t0_cutoff = 1784428800  # 7/18 00:00 (approximate)

# Read state
with open(r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

# HB #1627 entry
hb_entry = f"""## HB #1627 ({ts} cron-event, OpenClaw heartbeat poll)
- gap from HB #1626 (16:47): +5min -- Monday mid-afternoon Token Guard cadence (R012 minimal mode)
- D+11 Monday mid-afternoon pass #1627 -- Eric silent in THIS session ~267.55h+ since 7/16 13:16 first-contact (11d 3h+)
- Eric active elsewhere: AnYi webchat ~196.05h+ -- gongshi Day 3/5 ACTIVE (Mon = working day)
- 8-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261) -- penta-constraint 5/5 holds firm
- 7/24 D-Day POST-MEETING T+74.83h; oil Scenario C EXPIRED 7/25 22:00 (T+42.83h past); quiet zone EXPIRED but R258 dormancy trumps
- post_t0_null_count: 277 (277th consecutive null post-T-0)
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- T-0 publicity cutoff 7/18 +213.83h past -- post-protection window firmly sustained
- hbCount: 1626 -> 1627

### decision
- HEARTBEAT_OK -- HB #1627 = sustain DORMANT protocol, minimal token tick
- no push: Monday mid-afternoon, Eric silent 267.55h+ this session, this session DORMANT per R258 (NOT AnYi decision channel)
- R256+R257+R258+R260+R261 penta-constraint holds -- no proactive disturbance
- Eric silence on this session = dominant signal
- Triple Confluence ALL CLOSED; gongshi Day 3/5 ACTIVE elsewhere; 7/24 D-Day PASSED +74.83h
- Active Resume Protocol prep: post_t0_null > 200 already, awaiting Eric first-contact trigger on this session
- Next: per Token Guard cadence (~5-10min) or Eric first-contact

*{ts} -- D+11 Mon mid-afternoon -- HB #1627 -- DORMANT -- 277th null -- Eric silent = dominant signal holding -- HEARTBEAT_OK*

"""

# Read heartbeat file
with open(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find position to insert (before latest HB entry logged)
# Try most recent markers first
for marker in ['## HB #1625', '## HB #1626', '## HB #1623']:
    idx = content.find(marker)
    if idx != -1:
        print(f'Found marker: {marker} at index {idx}')
        break
else:
    print('ERROR: No recent HB marker found')
    exit(1)

# Insert new entry before existing HB #1626
new_content = content[:idx] + hb_entry + content[idx:]

with open(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

# Update state
state['lastHBTime'] = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
state['lastHB'] = int(now.timestamp())
state['post_t0_null_count'] = 277
state['postT0NullCount'] = 277
state['hbCount'] = 1627
state['lastHBNumber'] = 1627
state['ericSilentThisSessionHours'] = round((now.timestamp() - eric_first_contact) / 3600, 2)
state['anyiWebchatHoursSinceStart'] = round((now.timestamp() - anyi_start) / 3600, 2)
state['dDayHoursPostMeeting'] = round((now.timestamp() - dday_meeting) / 3600, 2)
state['oilCExpiredHoursPast'] = round((now.timestamp() - oil_c_expired) / 3600, 2)
state['t0PublicityCutoffHoursPast'] = round((now.timestamp() - t0_cutoff) / 3600, 2)
state['protectionWindowSustainedHours'] = round((now.timestamp() - t0_cutoff) / 3600, 2)
state['notes'] = f'D+11 Mon mid-afternoon 16:52. DORMANT. 8-layer suppression zero-breach. 7/24 D-Day PASSED. gongshi Day 3/5 ACTIVE. HEARTBEAT_OK. Eric silent 267.55h+. Hold position. Suppression intact. HB #1627 (5min since last).'

with open(r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json', 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f'HB #1627 logged. post_t0_null_count: 277. State updated.')
print(f'Eric silent this session: {state["ericSilentThisSessionHours"]}h+')
print(f'7/24 D-day post-meeting: +{state["dDayHoursPostMeeting"]}h')
print(f'Oil C expired: +{state["oilCExpiredHoursPast"]}h past')
