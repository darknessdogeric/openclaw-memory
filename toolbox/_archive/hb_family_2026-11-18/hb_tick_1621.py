import json
from datetime import datetime

ts = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')
hm = datetime.now().strftime('%H:%M')
state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'

with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

# correct base timestamps (fixed from prior heartbeat bug)
T_LAST_CONTACT = 1784178960    # 2026-07-16 13:16 +08:00 (Eric first-contact)
T_ANYI_START = 1784449920      # 2026-07-19 12:33 +08:00 (AnYi webchat start)
T_D_DAY = 1784866080           # 2026-07-24 12:08 +08:00 (D-Day meeting start, approx)
T_OIL_C_EXPIRY = 1784952000    # 2026-07-25 22:00 +08:00 (oil Scenario C expiry)
T_T0_PUBLICITY = 1784366400    # 2026-07-18 12:00 +08:00 (T-0 publicity cutoff)
T_PROTECTION_WINDOW = 1782441600  # protection window reference (kept from prior)

now = datetime.now().timestamp()

state['lastHB'] = int(now)
state['lastHBTime'] = ts
state['hbCount'] = 1621
state['post_t0_null_count'] = 271
state['postT0NullCount'] = 271
state['lastContactTime'] = '2026-07-16T13:16:00+08:00'
state['anyiSinceTime'] = '2026-07-19T12:33:00+08:00'
state['oilScenarioCExpiredSince'] = '2026-07-25T22:00:00+08:00'
state['oilCExpiredHoursPast'] = round((now - T_OIL_C_EXPIRY) / 3600, 2)
state['anyiWebchatHoursSinceStart'] = round((now - T_ANYI_START) / 3600, 2)
state['ericSilentThisSessionHours'] = round((now - T_LAST_CONTACT) / 3600, 2)
state['dDayHoursPostMeeting'] = round((now - T_D_DAY) / 3600, 2)
state['t0PublicityCutoffHoursPast'] = round((now - T_T0_PUBLICITY) / 3600, 2)
state['protectionWindowSustainedHours'] = round((now - T_PROTECTION_WINDOW) / 3600, 2)
state['quietZoneActiveNow'] = False
state['thisSessionMode'] = 'DORMANT'
state['thisSessionDormant'] = True
state['anyiWebchatActive'] = True
state['oilScenarioCWindowExpired'] = True
state['gongshiDay'] = 'Day 3/5 ACTIVE (Mon = working day per AnYi calendar)'
state['suppressionLayers'] = ['R-B', 'R12', 'R-CANDIDATE-T2', 'R256', 'R257', 'R258', 'R260', 'R261']
state['lastContactTimestamp'] = T_LAST_CONTACT
state['notes'] = 'D+11 Mon mid-afternoon ' + hm + '. DORMANT. 8-layer suppression zero-breach. 7/24 D-Day PASSED. gongshi Day 3/5 ACTIVE. HEARTBEAT_OK. Eric silent ' + str(state['ericSilentThisSessionHours']) + 'h+. Hold position. Suppression intact.'

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print('HB #1621 ' + ts)
print('post_t0_null: 271 | ericSilent: ' + str(state['ericSilentThisSessionHours']) + 'h | dDayPost: ' + str(state['dDayHoursPostMeeting']) + 'h | anyiHours: ' + str(state['anyiWebchatHoursSinceStart']) + 'h')