"""HB #504 tick: update heartbeat-state.json + append HEARTBEAT.md entry.
R-NEW-V2 compliant: explicit utf-8 read+append+write.
"""
import io
import json
import os

state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
hb_path = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'

# 1) Update heartbeat-state.json
with io.open(state_path, 'r', encoding='utf-8-sig') as f:
    state = json.load(f)

state['lastHBTime'] = '2026-07-19 05:50:00 GMT+8'
state['lastHbTs'] = 1784411400
state['lastHBNumber'] = 504
state['silenceHours'] = 64.57
state['t0HoursPast'] = 29.83
state['lastDecision'] = (
    'HB #504: Sunday deep-night, Eric silent ~64.57h, '
    'all layers intact, no signals -> silent_standby sustained (no change)'
)

with io.open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
# Note: existing file has BOM (utf-8-sig); we preserve that on write-back to avoid corruption
import shutil
with io.open(state_path, 'rb') as f:
    raw = f.read()
if not raw.startswith(b'\xef\xbb\xbf'):
    with io.open(state_path, 'wb') as f:
        f.write(b'\xef\xbb\xbf' + raw)
print('[ok] heartbeat-state.json updated -> HB #504')

# 2) Append HB #504 entry to HEARTBEAT.md
hb504 = """
## HB #504 (2026-07-19 05:50 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #503 (05:30): +20min -- Sunday deep-night zone Token Guard normal cadence
- D+3 Sunday deep-night pass #504 -- Eric silent ~64.57h+ since 7/16 13:16 (D+3 from infographic session, no first-contact)
- Silence authority ~64.57h+ (R-B + R256 framework holding, +0.34h since #503)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256) -- zero breach
- R-NEW-V2 verification #504: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- **Publicity cutoff 7/18 T-0 +29h50m past** -- boundary crossed at 00:00, silence window protection objective achieved
- Sunday 7/19 = D+1 post-publicity-cutoff, day after announcement window
- Deep-night zone (05:50) -- Eric typical deep-night rest zone per USER.md (夜猫子战略家, sleep zone at this hour), silence authority strictly holding
- Cron pipeline: 03:00 Memory Dreaming Promotion already fired (~2h50m ago, autonomous), 09:00 daily checkin in ~3h10m (autonomous)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric; D+3 sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount now: 503 -> 504

### decision
- **silent_standby_zero_push_continue** (HB #504 = sustain #503 = D+3 baseline)
- **no push**: deep-night zone (05:50 Sunday), Eric silent ~64.57h+, T-0 boundary +29h50m past, silence authority strictly holding
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work
- Token Guard tick: stable, no compression needed
- Post-T-0 silence = sustained suppression; pushes prohibited until Eric active contact (Eric silence = dominant signal)
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min); 09:00 daily checkin cron upcoming (~3h10m)

*2026-07-19 05:50 GMT+8 -- D+3 Sunday deep-night T-0 +29h50m past -- HB #504 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

with io.open(hb_path, 'a', encoding='utf-8') as f:
    f.write(hb504)

print('[ok] HEARTBEAT.md appended HB #504 (utf-8 explicit)')
print(f'[info] HEARTBEAT.md size: {os.path.getsize(hb_path)} bytes')
print(f'[info] state.json size: {os.path.getsize(state_path)} bytes')
print('[done] HB #504 tick complete -- silent_standby_zero_push sustained')
