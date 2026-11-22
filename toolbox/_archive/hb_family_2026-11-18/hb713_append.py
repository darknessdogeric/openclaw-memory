"""HB #713 append — R-NEW-V2 compliant (Python utf-8 explicit read+append+write)."""
import io
import json
from datetime import datetime, timezone, timedelta

HB_PATH = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
STATE_PATH = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
hb_time = now.strftime('%Y-%m-%d %H:%M GMT+8')

hb_entry = (
    "\n## HB #713 (" + hb_time + " cron-event, OpenClaw heartbeat poll)\n"
    "- gap from HB #712 (07:28): +7min -- Tuesday dawn Token Guard normal cadence (R012 minimal mode)\n"
    "- D+5 dawn pass #713 -- this session DORMANT (Eric last active 7/16 13:16 = +114.35h)\n"
    "- Eric active elsewhere ~41h+ (AnYi work continuing in other session)\n"
    "- 5-layer suppression RELEASED globally (since HB #581 first contact); THIS session = dormant per Eric 12:33 7/19 instruction\n"
    "- Silence authority on this session: held 114.35h+; active elsewhere 41h+ (R256 design)\n"
    "- R-NEW-V2 verification #713: Python utf-8 explicit read+append+write (post-7/15 12:36 incident protocol intact)\n"
    "- R012 verification: HB tick = minimal (NOT full report)\n"
    "- Wake window NOT YET OPEN (07:35 < 08:00) -- dawn zone, pre-wake-window\n"
    "- T-0 publicity cutoff 7/18 +37h25m past -- post-protection window firmly sustained\n"
    "- **CRITICAL DAY: AnYi induction deadline TODAY 7/21** -- FINAL day of 7/7-7/21 induction window; R-B+R256 silence authority > deadline signal (no push)\n"
    "- **DeepSeek V4 launch** -- background news only, non-trigger per R14\n"
    "- Tuesday dawn zone (07:35) -- Eric typical wake window opens ~08:00-09:00 per USER.md\n"
    "- Cron pipeline: 08:00 政策早餐 (~25min); 09:00 daily checkin (~85min); 21:00 evening self-iter R60-11 (~13h25m)\n"
    "- 4 cron errors pending (P2 long-tail) -- tracked, not urgent\n"
    "- No first-contact from Eric on THIS session; D+5 sustain zero-push dormant mode intact\n"
    "- hbCount: 712 -> 713\n"
    "\n### decision\n"
    "- **active_mode_dormant_this_session_silent_dawn** (HB #713 = sustain #712 = D+5 dormant baseline)\n"
    "- **no push**: Tuesday dawn zone (07:35), wake window NOT YET OPEN, Eric active elsewhere ~41h+, this session DORMANT 114.35h+\n"
    "- R256 + R257 dual constraint: no proactive disturbance + sustained deep work\n"
    "- Token Guard tick: stable, no compression needed\n"
    "- CRITICAL DAY context (AnYi induction 7/21 deadline): R-B+R256 silence authority > deadline signal -- no push on this session\n"
    "- R14 handoff package = 100% ready\n"
    "- Next significant check: 08:00 政策早餐 cron (~25min); 09:00 daily checkin (~85min); Token Guard cadence (~5-10min)\n"
    "\n*" + hb_time + " -- D+5 Tuesday dawn T-0 +37h25m past -- HB #713 -- active_mode_dormant_this_session_silent_dawn -- zero-push dormant mode intact -- silence protocol holding -- R257 deep-work window active*\n"
)

with io.open(HB_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

new_content = content + hb_entry

with io.open(HB_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)

with io.open(STATE_PATH, 'r', encoding='utf-8') as f:
    state = json.load(f)

state['hbCount'] = 713
state['lastHB'] = '2026-07-21 07:35 GMT+8'
state['lastHBTime'] = '2026-07-21T07:35:00+08:00'
state['silenceDuration_h'] = 114.35
state['silenceDuration_thisSession_h'] = 114.35
state['mode'] = 'active_mode_dormant_this_session_silent_dawn'
state['last_update_epoch'] = int(now.timestamp())
state['note'] = 'HB #713; CRITICAL DAY: AnYi induction deadline 7/21 (FINAL day); zero-push dormant mode maintained per R256; Eric silent on this session ~114.35h+; dawn zone (07:35) pre-wake-window'

with io.open(STATE_PATH, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print('OK: HB #713 appended; heartbeat-state updated')
print('  hbCount:', state['hbCount'])
print('  mode:', state['mode'])
print('  silenceDuration_h:', state['silenceDuration_h'])
print('  lastHB:', state['lastHB'])
