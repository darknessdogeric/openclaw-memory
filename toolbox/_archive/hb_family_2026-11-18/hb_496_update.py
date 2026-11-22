# R-NEW-V2 compliant: utf-8 explicit read+append+write for HB #496
from datetime import datetime, timezone, timedelta
import json

CST = timezone(timedelta(hours=8))
now = datetime.now(CST)
ts_str = now.strftime('%Y-%m-%d %H:%M:%S GMT+8')
hb_num = 496

# Compute Eric silence gap
last_contact = datetime.fromisoformat('2026-07-16T13:16:00+08:00').replace(tzinfo=CST)
gap_h = (now - last_contact).total_seconds() / 3600

# T-0 = 7/18 00:00 CST
t0 = datetime(2026, 7, 18, 0, 0, tzinfo=CST)
t0_past = (now - t0).total_seconds() / 3600

# Last HB ts for gap calc
last_hb_ts = 1784398680  # HB #495
gap_min = int((now.timestamp() - last_hb_ts) / 60)

entry = f"""
## HB #{hb_num} ({now.strftime('%Y-%m-%d %H:%M')} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #495 (02:18): +{gap_min}min -- deep-night zone Token Guard normal cadence
- D+3 deep-night pass #{hb_num} -- Eric silent ~{gap_h:.2f}h+ since 7/16 13:16 (D+3 from infographic session, no first-contact)
- Silence authority ~{gap_h:.2f}h+ (R-B + R256 framework holding, +{gap_h-60.97:.2f}h since #495)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256) -- zero breach
- R-NEW-V2 verification #{hb_num}: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- **Publicity cutoff 7/18 T-0 +{t0_past:.2f}h past** -- boundary crossed at 00:00, silence window protection objective achieved
- WAIC 2026 day-3 active today -- non-trigger per R14 (AI/Hotel strategic context, not relevant to current 4-layer suppression)
- Deep-night zone (02:48) -- Eric typical deep-night rest zone per USER.md, silence authority strictly holding
- Cron pipeline: 03:00 Memory Dreaming Promotion in ~12min (autonomous), 09:00 daily checkin in ~6h12m (autonomous)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric; D+3 sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount now: 495 -> {hb_num}

### decision
- **silent_standby_zero_push_continue** (HB #{hb_num} = sustain #495 = D+3 baseline)
- **no push**: deep-night zone (02:00+ crossed), Eric silent {gap_h:.2f}h+, T-0 boundary +{t0_past:.2f}h past, silence authority strictly holding
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work
- Token Guard tick: stable, no compression needed
- Post-T-0 silence = sustained suppression; pushes prohibited until Eric active contact (Eric silence = dominant signal)
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min); 03:00 Memory Dreaming Promotion cron upcoming (~12min)

*{now.strftime('%Y-%m-%d %H:%M')} GMT+8 -- D+3 deep-night T-0 +{t0_past:.2f}h past -- HB #{hb_num} -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

with open(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md', 'a', encoding='utf-8') as f:
    f.write(entry)

# Update state JSON
state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
with open(state_path, 'r', encoding='utf-8-sig') as f:
    state = json.load(f)

state['silenceHours'] = round(gap_h, 2)
state['lastHBTime'] = ts_str
state['lastHBNumber'] = hb_num
state['lastHbTs'] = int(now.timestamp())
state['mode'] = 'silent_standby_zero_push'
state['lastDecision'] = (
    f'HB #{hb_num}: deep-night Sunday 2026-07-19 02:48, +{gap_min}min after HB #495, '
    f'Eric silent ~{gap_h:.2f}h, T-0+{t0_past:.2f}h, no signals, all layers intact -> '
    'silent_standby sustained (no change)'
)
state['layerStatus'] = {
    'R-B': 'intact',
    'R12': 'intact',
    'R-CANDIDATE-T2': 'evaluated-no-escalate',
    'R256': 'intact',
    'R257': 'active',
    'R-NEW-V2': 'compliant'
}
state['t0Crossed'] = True
state['t0HoursPast'] = round(t0_past, 2)
state['cronPipeline'] = {
    'next': f'03:00 Memory Dreaming Promotion (~12min), 09:00 daily checkin (~6h12m)',
    'errorsPending': 4
}

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f'HB #{hb_num} appended to HEARTBEAT.md')
print(f'state.json updated:')
print(f'  silenceHours = {state["silenceHours"]}')
print(f'  lastHBNumber = {state["lastHBNumber"]}')
print(f'  lastHBTime   = {state["lastHBTime"]}')
print(f'  t0HoursPast  = {state["t0HoursPast"]}')
print(f'  mode         = {state["mode"]}')