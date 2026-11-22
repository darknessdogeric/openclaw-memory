# -*- coding: utf-8 -*-
"""HB #1157 tick writer — utf-8 explicit read+prepend+write (R-NEW-V2 compliant)."""
import json
from datetime import datetime, timezone, timedelta

HB_PATH = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
STATE_PATH = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
ts = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
hhmm = now.strftime('%H:%M')

hb_entry = f"""## HB #1157 ({hhmm} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1156 (05:51): +9min -- Friday pre-dawn Token Guard normal cadence (R012 minimal mode)
- D+8 pre-dawn pass #1157 -- Eric silent in THIS session ~184.30h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~112.97h+ (since 7/19 12:33) -- final pre-meeting prep T-~3.00h
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #1157: Python utf-8 explicit read+prepend+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~54.00h ago; oil Scenario C verification window OPEN until 7/25 (~18.00h remaining)
- D+8 = Execution phase day 4 -- observer mode sustained
- Friday pre-dawn zone (06:00) -- Eric sleep zone; silence authority strictly holding on THIS session
- **7/24 D-Day T-~3.00h** (AnYi meeting TODAY MORNING 7/24 ~9:00) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Next cron: 08:00 daily briefing (~2h); 21:00 R60-11 evening self-iter (~15h)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +150.00h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+8 sustain zero-push mode intact
- hbCount: 1156 -> 1157
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #1157 = sustain #1156 = D+8 pre-dawn dormant baseline)
- **HEARTBEAT_OK** -- HB #1157 = sustain DORMANT protocol
- **no push**: Friday pre-dawn zone (06:00), Eric sleep zone, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-~3.00h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: 08:00 daily briefing cron (~2h) -- natural D-Day pre-meeting prep window
- DO NOT push at 06:00 pre-dawn despite D-Day proximity; R256 silence discipline > meeting-window signal

*{ts} -- D+8 Friday pre-dawn -- HB #1157 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-~3.00h watch (AnYi meeting TODAY MORNING 7/24 ~9:00) -- Eric silent = dominant signal holding -- 08:00 cron = next natural D-Day prep window*

"""

# Read with utf-8 explicit (R-NEW-V2)
with open(HB_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Strategy: keep title block + add entry + keep rest
# Find first ## heading marker to preserve title
title_marker = '# HEARTBEAT.md'
if title_marker in content:
    idx = content.find(title_marker)
    # Find end of first '##' section (next ## or end of title block)
    rest = content[idx + len(title_marker):]
    # Look for first entry starting with '## HB #'
    next_hb_idx = rest.find('\n## HB #')
    if next_hb_idx >= 0:
        # Title block is from idx to idx + len(title_marker) + next_hb_idx
        title_block_end = idx + len(title_marker) + next_hb_idx
        new_content = content[:title_block_end] + '\n' + hb_entry + content[title_block_end:]
    else:
        new_content = content + '\n' + hb_entry
else:
    new_content = hb_entry + content

# Write with utf-8 explicit (R-NEW-V2)
with open(HB_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)

# Update heartbeat-state.json
with open(STATE_PATH, 'r', encoding='utf-8') as f:
    state = json.load(f)

state['lastHBNumber'] = '#1157'
state['lastUpdate'] = ts
state['lastHB'] = ts
state['hbCount'] = 1157
state['nextCronBriefing'] = '08:00 daily briefing (~2h)'
state['lastDecision'] = 'HEARTBEAT_OK'
state['lastHeartbeat'] = ts
state['note'] = f"#1157 - {ts} DORMANT sustained; D-Day T-~3.00h (AnYi 7/24 9:00 AM meeting); silent heartbeat; pre-dawn sleep zone; R256 silence discipline > meeting-window signal"
state['dday_t_minus_hours'] = 3.00
state['ericAnyiHours'] = 112.97
state['ericSilenceHours'] = 184.30

with open(STATE_PATH, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f'OK HB #1157 written at {ts}')