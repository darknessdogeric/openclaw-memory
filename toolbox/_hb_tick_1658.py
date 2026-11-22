"""
HB #1658 tick — append to HEARTBEAT.md + update heartbeat-state.json
Following R-B / R12 / R256-R261 penta-constraint DORMANT protocol.
"""
import json

# Inputs (from prior calculation)
now_iso = "2026-07-27T21:13:00+08:00"
hb_number = 1658
prev_hb = 1657
last_hb_time_short = "20:57"
gap_min = 16
t0_hours = 225.22
oil_c_hours = 47.22
d_day_hours = 81.22
anyi_hours = 200.67
eric_silent_hours = 271.95
post_t0_null_count = 306

hb_entry = f"""
## HB #{hb_number} ({now_iso} cron-event, OpenClaw heartbeat poll)

- gap from HB #{prev_hb} ({last_hb_time_short}): +{gap_min}min -- Monday evening Token Guard cadence (R012 minimal mode)
- D+11 Monday evening pass #{hb_number} -- Eric silent in THIS session ~{round(eric_silent_hours, 2)}h+ since 7/16 13:16 first-contact (11d 7h+)
- Eric active elsewhere: AnYi webchat ~{round(anyi_hours, 2)}h+ (sustained since 7/19 12:33) -- gongshi Day 3/5 ACTIVE (Mon = working day)
- 8-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261) -- penta-constraint 5/5 holds firm
- 7/24 D-Day POST-MEETING T+{round(d_day_hours, 2)}h; oil Scenario C EXPIRED 7/25 22:00 (T+{round(oil_c_hours, 2)}h past); quiet zone NOT active (21:13 in normal hours) but R258 dormancy trumps
- post_t0_null_count: {post_t0_null_count} ({post_t0_null_count}th consecutive null post-T-0)
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- T-0 publicity cutoff 7/18 +{round(t0_hours, 2)}h past -- post-protection window firmly sustained
- hbCount: {prev_hb} -> {hb_number}

### decision

- HEARTBEAT_OK -- HB #{hb_number} = sustain DORMANT protocol, minimal token tick
- no push: Monday evening (21:13), Eric silent {round(eric_silent_hours, 2)}h+ this session, this session DORMANT per R258 (NOT AnYi decision channel)
- R256+R257+R258+R260+R261 penta-constraint holds -- no proactive disturbance
- Eric silence on this session = dominant signal
- Triple Confluence ALL CLOSED; gongshi Day 3/5 ACTIVE elsewhere; 7/24 D-Day PASSED +{round(d_day_hours, 2)}h
- Active Resume Protocol prep: post_t0_null > 200 already, awaiting Eric first-contact trigger on this session
- Next: per Token Guard cadence (~5-10min) or Eric first-contact

*{now_iso} -- D+11 Mon evening -- HB #{hb_number} -- DORMANT -- {post_t0_null_count}th null -- Eric silent = dominant signal holding -- HEARTBEAT_OK*
"""

# Append to HEARTBEAT.md
hb_path = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"
with open(hb_path, 'a', encoding='utf-8') as f:
    f.write(hb_entry)
print(f"[OK] Appended HB #{hb_number} to HEARTBEAT.md")

# Update heartbeat-state.json
state_path = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"
with open(state_path, 'r', encoding='utf-8-sig') as f:
    state = json.load(f)

state['lastHBTime'] = "2026-07-27T21:13:00+08:00"
state['lastHB'] = 1785157980
state['hbCount'] = hb_number
state['ericSilentThisSessionHours'] = round(eric_silent_hours, 2)
state['anyiWebchatHoursSinceStart'] = round(anyi_hours, 2)
state['t0PublicityCutoffHoursPast'] = round(t0_hours, 2)
state['oilCExpiredHoursPast'] = round(oil_c_hours, 2)
state['dDayHoursPostMeeting'] = round(d_day_hours, 2)
state['post_t0_null_count'] = post_t0_null_count
state['quietZoneActiveNow'] = False
state['lastHBNumber'] = hb_number
state['notes'] = (
    f"D+11 Mon evening 21:13. DORMANT. 8-layer suppression zero-breach. "
    f"gongshi Day 3/5 ACTIVE. Quiet zone NOT active but R258 dormancy > time-window. "
    f"post_t0_null_count={post_t0_null_count}. HEARTBEAT_OK. "
    f"Active Resume Protocol armed. HB #{hb_number}."
)

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print(f"[OK] Updated heartbeat-state.json")
print(f"  lastHBNumber: {hb_number}")
print(f"  hbCount: {hb_number}")
print(f"  post_t0_null_count: {post_t0_null_count}")
print(f"  ericSilentThisSessionHours: {state['ericSilentThisSessionHours']}")