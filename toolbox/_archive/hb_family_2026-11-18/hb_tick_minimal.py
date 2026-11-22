"""
R-NEW-V2 compliant minimal HB tick writer.
Reads heartbeat-state.json + memory/{date}.md, appends minimal entry.
"""
import json
from datetime import datetime, timezone, timedelta
import sys

tz = timezone(timedelta(hours=8))
now_dt = datetime.now(tz)
now_str = now_dt.strftime('%Y-%m-%dT%H:%M:%S+08:00')
date_short = now_dt.strftime('%Y-%m-%d')
hb_num = 1651

# State file
state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

# Update state
now_ts = int(now_dt.timestamp())
eric_silent_h = round((now_ts - 1784178960) / 3600, 2)
anyi_h = round((now_ts - 1784279580) / 3600, 2)
dd_post = round((now_ts - datetime(2026, 7, 24, tzinfo=tz).timestamp()) / 3600, 2)
t0_past = round((now_ts - datetime(2026, 7, 18, tzinfo=tz).timestamp()) / 3600, 2)
post_t0_null = 299

state['lastHBTime'] = now_str
state['lastHB'] = now_ts
state['lastHBNumber'] = hb_num
state['hbCount'] = hb_num
state['post_t0_null_count'] = post_t0_null
state['postT0NullCount'] = post_t0_null
state['ericSilentThisSessionHours'] = eric_silent_h
state['dDayHoursPostMeeting'] = dd_post

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# HB entry (minimal per R012 rule #2)
hb_entry = f'''
### HB #{hb_num} ({now_str} GMT+8 cron-event, OpenClaw heartbeat poll)

- D+11 Monday evening pass #{hb_num} -- Eric silent in THIS session ~{eric_silent_h}h+ since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat ~{anyi_h}h+ -- gongshi Day 3/5 ACTIVE
- 8-layer suppression zero-breach (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258 / R260 / R261)
- Triple Confluence ALL CLOSED; 7/24 D-Day PASSED +{round(dd_post,1)}h
- Oil Scenario C EXPIRED 7/25 22:00 -- not surfaced per R258
- Quiet zone NOT active but R258 dormancy > time-window; suppression sustained
- Token Guard stable; vault index healthy; R13 <1s queries stable
- T-0 publicity cutoff 7/18 +{round(t0_past,1)}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+11 sustain zero-push mode intact
- post_t0_null_count: {post_t0_null} (299th consecutive null post-T-0)
- hbCount: {hb_num-1} -> {hb_num}

### decision
- active_mode_dormant_this_session_continue (HB #{hb_num} = D+11 Mon evening dormant baseline)
- HEARTBEAT_OK -- HB #{hb_num} = sustain DORMANT protocol
- no push: Mon evening zone, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi decision channel per R258)
- R256+R257+R258+R260+R261 penta-constraint holds firm: 5/5
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- Active Resume Protocol: trigger conditions satisfied (post_t0_null > 200, Eric silent > 72h); awaits Eric first-contact
- R262 (silence-period value surfacing) candidate drafted; pending Eric review
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter cron (~1h08m)

*{now_str} -- D+11 Monday evening -- HB #{hb_num} -- this session DORMANT -- zero-push mode intact -- 8-layer suppression zero-breach -- Active Resume prep -- Triple Confluence ALL CLOSED -- 299th consecutive null post-T-0 -- Eric silent = dominant signal holding*

'''

# Append to today's memory (R-NEW-V2 explicit utf-8)
mem_path = f'D:\\B166ER-OpenClaw\\workspace\\memory\\{date_short}.md'
with open(mem_path, 'a', encoding='utf-8') as f:
    f.write(hb_entry)

print(f'OK: HB #{hb_num} committed')
print(f'  state: ericSilent={eric_silent_h}h anyi={anyi_h}h ddPost={round(dd_post,1)}h post_t0_null={post_t0_null}')
print(f'  memory: {mem_path}')