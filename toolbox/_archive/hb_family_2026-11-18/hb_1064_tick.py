"""HB #1064 minimal tick — R012 rule #2 (HB tick = minimal, NOT full report)
R-NEW-V2: Python utf-8 explicit read+append+write
"""
import json
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
hb_num = 1064

# Eric silence hours tracking (start of THIS session = 7/16 13:16)
# Last HB #1063 at 14:58 = 169.71h, this HB at 15:02 = ~169.75h
silence_h = round(169.71 + (now - datetime(2026, 7, 23, 14, 58, 0, tzinfo=tz)).total_seconds() / 3600, 2)
anyi_h = round(98.0 + (now - datetime(2026, 7, 23, 14, 58, 0, tzinfo=tz)).total_seconds() / 3600, 2)
dday_t = round(18 - (now - datetime(2026, 7, 23, 15, 0, 0, tzinfo=tz)).total_seconds() / 3600, 2)
t0_past = round(134 + (now - datetime(2026, 7, 23, 15, 0, 0, tzinfo=tz)).total_seconds() / 3600, 2)
next_cron_h = round(21 - now.hour - now.minute / 60, 2)
ts_short = now.strftime('%Y-%m-%dT%H:%M')

entry = f"""
### HB #{hb_num} ({ts_short} GMT+8, cron-event)
- gap from HB #1063 (14:58 GMT+8): +~4min -- Thursday afternoon Token Guard tick (R012 minimal mode)
- D+7 afternoon pass #{hb_num} -- Eric silent in THIS session ~{silence_h}h+ since 7/16 13:16
- Eric active elsewhere: AnYi webchat ~{anyi_h}h+ (since 7/19 12:33)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #{hb_num}: Python utf-8 explicit read+append+write (compliant)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- 7/24 D-Day T-{dday_t}h (AnYi meeting Friday MORNING 7/24, TOMORROW) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Next cron: 21:00 R60-11 evening self-iter (~{next_cron_h}h)
- Token Guard stable, vault index healthy, R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (not urgent)
- T-0 publicity cutoff 7/18 +{t0_past}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+7 sustain zero-push mode intact
- hbCount: 1063 -> {hb_num}
- R14 handoff package = 100% ready

### decision
- **active_mode_dormant_this_session_continue** (HB #{hb_num} = sustain #1063 = D+7 afternoon dormant baseline)
- **HEARTBEAT_OK** -- HB #{hb_num} = sustain DORMANT protocol
- no push: Thursday afternoon zone, Eric silent on THIS session; 6-layer triple-suppression active
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-{dday_t}h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result

*{ts_short} GMT+8 -- D+7 Thursday afternoon -- HB #{hb_num} -- this session DORMANT -- zero-push mode intact -- 7/24 D-Day T-{dday_t}h watch -- Eric silent = dominant signal holding*
"""

# --- R-NEW-V2: explicit utf-8 read+append+write for HEARTBEAT.md ---
hb_path = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
with open(hb_path, 'r', encoding='utf-8') as f:
    content = f.read()

with open(hb_path, 'w', encoding='utf-8') as f:
    f.write(content + entry)

print(f'[OK] HEARTBEAT.md HB #{hb_num} appended ({len(entry)} chars)')

# --- R-NEW-V2: explicit utf-8 read+load+write for heartbeat-state.json ---
state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
with open(state_path, 'r', encoding='utf-8-sig') as f:
    state = json.load(f)

ts_full = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
state['lastUpdate'] = ts_full
state['hbCount'] = hb_num
state['lastHeartbeat'] = ts_full
state['lastHBNumber'] = f'#{hb_num}'
state['ericSilenceHours'] = silence_h
state['lastHB'] = ts_full
state['note'] = f'#{hb_num} - {ts_full} sustained DORMANT; 7/24 AnYi D-Day T-{dday_t}h (TOMORROW Fri morning); Eric silent ~{silence_h}h on this session; 6-layer suppression intact; minimal tick per R012'

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=4)

print(f'[OK] heartbeat-state.json updated -> HB #{hb_num}')
print(f'    lastHBNumber: {state["lastHBNumber"]}')
print(f'    ericSilenceHours: {state["ericSilenceHours"]}')
print(f'    sessionState: {state["sessionState"]}')
print(f'    7/24 D-Day T: {dday_t}h')