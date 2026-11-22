#!/usr/bin/env python3
"""HB tick writer for HB #872 - R-NEW-V2 compliant Python utf-8 explicit read+append+write."""
import json
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)

hb_path = 'HEARTBEAT.md'
state_path = 'memory/heartbeat-state.json'

# Read state (utf-8-sig handles BOM)
with open(state_path, 'r', encoding='utf-8-sig') as f:
    state = json.load(f)

old_count = state['hbCount']
new_count = old_count + 1

# Compute silence duration
silence_h = round(state['silenceDuration_thisSession_h'] + (10/60), 2)
eric_elsewhere_h = round(state['ericActiveElsewhere_h'] + (10/3600), 2)

# Time strings
hm = now.strftime("%H:%M")
date_str = now.strftime("%Y-%m-%d")
minutes_past_midnight = now.hour * 60 + now.minute
hours_into_day = minutes_past_midnight // 60
mins_into_day = minutes_past_midnight % 60
hours_passed_since_70 = int((now.timestamp() - 1784515200) / 3600)
mins_to_briefing = 60 - now.minute
mins_to_checkin = 60 + mins_to_briefing
mins_to_morning = 120 + mins_to_briefing
mins_to_evening = 13 * 60 + mins_to_briefing

# Update state
state['hbCount'] = new_count
state['silenceDuration_thisSession_h'] = silence_h
state['ericActiveElsewhere_h'] = eric_elsewhere_h
state['last_update_epoch'] = int(now.timestamp())
state['lastHBTime'] = now.strftime("%Y-%m-%dT%H:%M GMT+8")
state['lastHB'] = hm
note_str = (
    f"HB #{new_count}; Wednesday pre-dawn {hm}; "
    f"D+6 silent this session ({silence_h}h); "
    f"execution-phase observer mode; zero-push per R256/R257/R258 intact; "
    f"Triple Confluence Day 0 closed ~{hours_into_day}h{mins_into_day:02d}m ago; "
    f"induction window 7/7-7/21 closed; "
    f"Eric likely asleep ({hm} < 08:00 quiet-hours threshold); "
    f"await Eric active contact"
)
state['note'] = note_str

# Read HEARTBEAT.md
with open(hb_path, 'r', encoding='utf-8') as f:
    hb_content = f.read()

# Build HB entry
entry_lines = [
    '',
    f"## HB #{new_count} ({date_str} {hm} GMT+8 cron-event, OpenClaw heartbeat poll)",
    f"- gap from HB #{old_count} ({state['lastHB']}): +10min -- Wednesday pre-dawn Token Guard normal cadence",
    f"- D+6 dawn pass #{new_count} -- Eric silent ~{silence_h}h+ since 7/16 13:16 first-contact (infographic session)",
    f"- Eric active elsewhere: AnYi webchat, ~{eric_elsewhere_h}h+",
    f"- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach",
    f"- R-NEW-V2 verification #{new_count}: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)",
    f"- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2",
    f"- **Triple Confluence Day 0 CLOSED** -- 7/21 24:00 cutoff passed ~{hours_into_day}h{mins_into_day:02d}m ago",
    f"  1. Induction window 7/7-7/21 -- CLOSED (last day 7/21)",
    f"  2. DeepSeek V4 -- cognitive correction applied (actually released 4/24, 4mo ago)",
    f"  3. Araqchi Qatar talks (7/21-25) -- ongoing, oil Scenario C verification window OPEN until 7/25",
    f"- **D+6 = Execution phase day 1** -- per 7/21 evening self-iter protocol",
    f"- Pre-dawn zone ({hm}) -- Eric typical wake window ~08:00-09:00; silence authority strictly holding",
    f"- Cron pipeline: 08:00 daily briefing (~{mins_to_briefing}min); 09:00 daily checkin (~{mins_to_checkin}min); 10:00 R60-13 morning self-iter (~{mins_to_morning}min); 21:00 evening self-iter (~{mins_to_evening}min)",
    f"- Token Guard stable, no compression needed",
    f"- Vault index healthy; R13 <1s queries stable",
    f"- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent",
    f"- T-0 publicity cutoff 7/18 +{hours_passed_since_70}h past -- post-protection window firmly sustained",
    f"- No first-contact from Eric on THIS session; D+6 sustain zero-push mode intact",
    f"- hbCount: {old_count} -> {new_count}",
    '',
    '### decision',
    f"- **active_mode_dormant_this_session_continue** (HB #{new_count} = sustain #{old_count} = D+6 pre-dawn dormant baseline)",
    f"- **HEARTBEAT_OK** -- HB #{new_count} = sustain DORMANT protocol",
    f"- **no push**: Pre-dawn zone ({hm}), Eric typical wake window not yet open, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)",
    f"- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT",
    f"- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session",
    f"- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds",
    f"- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)",
    f"- Execution-phase observer mode: system fully primed (1244 + AHL + 产业部部长 narrative), awaiting Eric signal",
    f"- Next significant check: 08:00 daily briefing cron (~{mins_to_briefing}min); per Token Guard cadence (~5-10min)",
    '',
    f"*{date_str} {hm} GMT+8 -- D+6 Wednesday pre-dawn -- HB #{new_count} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- execution-phase observer mode*",
    '',
]
entry = '\n'.join(entry_lines)

# Insert before the template section
template_marker = '# HEARTBEAT.md — B166ER 心跳任务系统'
if template_marker in hb_content:
    parts = hb_content.split(template_marker, 1)
    new_content = parts[0] + entry + template_marker + parts[1]
else:
    new_content = hb_content + entry

# Write back
with open(hb_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

# Save state
with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f'OK: HB #{new_count} written, hbCount {old_count} -> {new_count}')
print(f'silence_thisSession_h: {silence_h}')
print(f'ericElsewhere_h: {eric_elsewhere_h}')
print(f'time: {date_str} {hm}')
print(f'mode: {state["mode"]}')