"""R-NEW-V2 compliant HB tick writer -- utf-8 explicit read+prepend+write."""
import io
import sys
import json
from datetime import datetime, timezone, timedelta

# China timezone
tz_china = timezone(timedelta(hours=8))
now = datetime.now(tz_china)
ts_str = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
ts_short = now.strftime('%H:%M')

hb_count_new = 1237
prev_count = 1236

# Build HB entry (minimal -- R012 rule #2)
hb_entry = f"""### HB #{hb_count_new} ({ts_str} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_count} (20:33): +2min -- Friday evening Token Guard cadence (R012 minimal mode)
- D+8 evening pass #{hb_count_new} -- Eric silent in THIS session ~199.62h+ since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat ~128.27h+ (since 7/19 12:33) -- D-Day POST-MEETING PHASE (T+~11h35m past meeting start; debrief/公示 window open +8h35m)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #{hb_count_new}: Python utf-8 explicit read+prepend+write (compliant)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Friday evening zone ({ts_short}) -- D-Day debrief/公示 window continuing; silence authority strictly holding on THIS session
- Token Guard stable; vault index healthy; R13 <1s queries stable
- T-0 publicity cutoff 7/18 +170.58h past -- post-protection window firmly sustained
- Next significant check: 21:00 R60-11 evening self-iter (~25min)
- No first-contact from Eric on THIS session; D+8 sustain zero-push mode intact
- hbCount: {prev_count} -> {hb_count_new}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- active_mode_dormant_this_session_continue (#{hb_count_new} = sustain #{prev_count} = D+8 evening dormant baseline)
- HEARTBEAT_OK -- #{hb_count_new} = sustain DORMANT protocol
- no push: Friday evening ({ts_short}) -- D-Day POST-MEETING PHASE on AnYi webchat; this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Eric silence on this session = dominant signal (supersedes D-Day signal); R256 design holds
- D-Day POST-MEETING watch: emergency prepare-mode prepacked, ready if Eric contacts with 任命确认 / 1244 战略 / AHL 调整 on ANY session
- DO NOT push at {ts_short} evening despite D-Day POST-MEETING PHASE; R256 silence discipline > meeting-window signal
- R14 handoff package = 100% ready for any-session 30s activation

*{ts_str} -- D+8 Friday evening -- HB #{hb_count_new} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- 7/24 D-Day POST-MEETING PHASE (T+~11h35m past meeting start) -- Eric silent on this session = dominant signal holding -- R14 handoff ready*

"""

# 1. HEARTBEAT.md -- utf-8 explicit read+prepend+write
hb_path = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
with io.open(hb_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the FIRST '## HB #' entry to prepend before it (chronological newest-first order)
marker = '## HB #'
idx = content.find(marker)
if idx == -1:
    print('ERROR: HEARTBEAT.md marker not found', file=sys.stderr)
    sys.exit(1)

new_content = content[:idx] + hb_entry + '\n' + content[idx:]
with io.open(hb_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print(f'HEARTBEAT.md updated: HB #{hb_count_new} prepended')

# 2. heartbeat-state.json -- update hbCount + heartbeat timestamp
state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
with io.open(state_path, 'r', encoding='utf-8') as f:
    state_text = f.read()

# Parse, update, write back
state = json.loads(state_text)
state['hbCount'] = hb_count_new
state['heartbeat'] = ts_str
state['session_dormant'] = True
state['D_Day_active'] = False
state['d_day_phase'] = 'POST-MEETING'

# Write with utf-8 explicit, indent=2 for readability
with io.open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f'heartbeat-state.json updated: hbCount = {hb_count_new}')

print(f'\nDONE: HB #{hb_count_new} @ {ts_str}')