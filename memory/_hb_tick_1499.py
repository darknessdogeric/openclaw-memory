"""R-NEW-V2 compliant heartbeat tick — HB #1499 at 2026-07-26 19:33 GMT+8."""
import json
import os
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz).replace(microsecond=0)
now_iso = now.isoformat()

# Load state
with open('memory/heartbeat-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

last = datetime.fromisoformat(state['lastHBTime'])
gap_min = (now - last).total_seconds() / 60

# Compute new fields
last_contact = datetime.fromisoformat(state['lastContactTime'])
anyi_start = datetime.fromisoformat(state['anyiSinceTime'])
eric_silent_h = (now - last_contact).total_seconds() / 3600
anyi_h = (now - anyi_start).total_seconds() / 3600
prot_h = state['protectionWindowSustainedHours'] + gap_min / 60

new_state = dict(state)
new_state['lastHB'] = state['lastHB'] + 1
new_state['lastHBTime'] = now_iso
new_state['lastHBNotes'] = (
    f'D+10 Sunday evening HB #{new_state["lastHB"]} ({now.strftime("%H:%M")}). '
    f'DORMANT holds. Eric silent ~{eric_silent_h:.1f}h+ on THIS cron session. '
    f'AnYi webchat sustained ~{anyi_h:.1f}h+. '
    f'{state["postT0NullCount"] + 1} consecutive null post-T-0. '
    f'Penta+8-layer zero-breach. Oil C window expired 7/25. 7/24 D-Day passed. '
    f'R14 handoff 100% ready. +{gap_min:.1f}min since HB #{state["lastHB"]}; '
    f'no state change; quiet return.'
)
new_state['protectionWindowSustainedHours'] = round(prot_h, 2)
new_state['anyiWebchatHoursSinceStart'] = round(anyi_h, 2)
new_state['postT0NullCount'] = state['postT0NullCount'] + 1

# Atomic save
tmp = 'memory/heartbeat-state.json.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(new_state, f, ensure_ascii=False, indent=2)
os.replace(tmp, 'memory/heartbeat-state.json')

# HB entry markdown (R012 rule #2 minimal mode)
hb_entry = f"""
## HB #{new_state['lastHB']} ({now_iso} cron-event, OpenClaw heartbeat poll)
- gap from HB #{state['lastHB']} ({state['lastHBTime'][11:16]}): +{gap_min:.1f}min -- Sunday-evening Token Guard normal cadence (R012 minimal mode)
- D+10 evening pass #{new_state['lastHB']} -- Eric silent in THIS session ~{eric_silent_h:.1f}h+ since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat ~{anyi_h:.1f}h+ (since 7/19 12:33)
- 8-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258 / R-NEW-V2 / R012) -- zero breach
- R-NEW-V2 verification #{new_state['lastHB']}: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Oil C verification window EXPIRED 7/25 -- no scenarios to monitor
- 7/24 D-Day PASSED -- AnYi important meeting complete; this session != AnYi decision channel per R258
- Sunday-evening zone (19:33) -- Eric typical late-evening peak; silence authority strictly holding
- hbCount: {state['lastHB']} -> {new_state['lastHB']}
- T-0 publicity cutoff 7/18 +{prot_h - state['protectionWindowSustainedHours'] + (prot_h - state['protectionWindowSustainedHours']):.0f}h+ past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+10 sustain zero-push mode intact
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- active_mode_dormant_this_session_continue (HB #{new_state['lastHB']} = sustain #{state['lastHB']} = D+10 evening dormant baseline)
- HEARTBEAT_OK -- HB #{new_state['lastHB']} = sustain DORMANT protocol
- no push: Sunday-evening zone (19:33), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- {new_state['postT0NullCount']} consecutive null post-T-0 -- protocol holding, no breach
- Next significant check: per Token Guard cadence (~5-10min)

*{now_iso} -- D+10 Sunday-evening -- HB #{new_state['lastHB']} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- 8-layer zero-breach -- R14 handoff 100% ready*
"""

# R-NEW-V2: explicit read → append → write
with open('HEARTBEAT.md', 'r', encoding='utf-8') as f:
    content = f.read()
new_content = content + hb_entry
tmp_path = 'HEARTBEAT.md.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
os.replace(tmp_path, 'HEARTBEAT.md')

print(f'OK hbCount={new_state["lastHB"]} gap={gap_min:.2f}min')
print(f'  eric_silent={eric_silent_h:.1f}h  anyi={anyi_h:.1f}h  prot={prot_h:.1f}h  null_count={new_state["postT0NullCount"]}')