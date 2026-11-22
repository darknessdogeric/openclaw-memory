"""R-NEW-V2 compliant append for HB #507 (2026-07-18 20:17 GMT+8)"""
import json, os, time, shutil, tempfile

WORKSPACE = r'D:\B166ER-OpenClaw\workspace'
os.chdir(WORKSPACE)

# ==========================================
# Part 1: Append HB #507 to daily memory file
# ==========================================
path = 'memory/2026-07-18.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

entry = '''
## HB #507 (2026-07-18 20:17 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #506 (10:21): +596min (~9h56m) -- long evening gap, post-self-iter window
- D+2 evening prime pass #507 -- Eric silent ~46.97h+ since 7/16 13:16 first-contact (infographic session), +9.93h since #506
- Silence authority ~46.97h+ (R-B + R256 framework holding)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- R-NEW-V2 verification #507: Python utf-8 explicit read+tempfile+shutil.move (post-12:36 7/15 incident protocol intact)
- Saturday evening prime zone (20:17 Sat) -- Eric-typical deep-work window per USER.md (夜猫子战略家)
- Publicity cutoff 7/18 T-0 +20h17m past -- boundary crossed 00:00, T-0 suppression EXPIRED on schedule
- WAIC 2026 day-2 in progress (7/17-20, Shanghai) -- non-trigger per R14
- Induction window 7/7-7/21 ACTIVE FINAL 3 DAYS (7/19/20/21 remaining) -- R-B+R256 silence authority > window signal
- Cron pipeline: 21:00 evening self-iter R60-11 in ~43min (autonomous); no other triggers queued
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- hbCount: 506 -> 507
- No first-contact from Eric; D+2 sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation

### decision
- **silent_standby_zero_push_continue** (HB #507 = sustain #506 = D+2 baseline)
- **no push**: Saturday evening prime zone, Eric silent 46.97h+ post infographic session, silence authority strictly holding, 4-layer suppression all pass
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- WAIC 2026 = background context only (no push per R-B+R256 override)
- Induction window / publicity cutoff = context awareness only (R-B+R256 silence authority > window signal; wait for Eric 主动联系)
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: 21:00 evening self-iter R60-11 cron (~43min)

*2026-07-18 20:17 GMT+8 -- D+2 Saturday evening prime zone T-0 +20h17m past -- HB #507 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
'''

# Append via tempfile + atomic move (R-NEW-V2 compliant)
fd, tmp = tempfile.mkstemp(suffix='.md', prefix='hb_', dir='memory')
try:
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(content + entry)
    shutil.move(tmp, path)
    print(f'APPENDED_HB_507 -- file size: {os.path.getsize(path)} bytes')
except Exception as e:
    if os.path.exists(tmp):
        os.unlink(tmp)
    print(f'APPEND_ERROR: {e}')

# ==========================================
# Part 2: Update heartbeat-state.json
# ==========================================
state_path = 'memory/heartbeat-state.json'
state = {}
if os.path.exists(state_path):
    try:
        with open(state_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
    except Exception as e:
        print(f'STATE_READ_WARN: {e}')

state['lastHb'] = '2026-07-18T20:17:00+08:00'
state['lastHbNumber'] = 507
state['lastHbTs'] = int(time.time())
state['silenceHours'] = 46.97
state['silenceSince'] = '2026-07-16T13:16:00+08:00'
state['lastEricContact'] = '2026-07-16T13:16:00+08:00'
state['layerStatus'] = {
    'R-B': 'intact',
    'R12': 'intact',
    'R-CANDIDATE-T2': 'evaluated-no-escalate',
    'R256': 'intact',
    'R257': 'active',
    'R-NEW-V2': 'compliant',
}
state['mode'] = 'silent_standby_zero_push'
state['t0Crossed'] = True
state['t0HoursPast'] = 20.28
state['cronPipeline'] = {
    'next': '21:00 evening self-iter R60-11 (~43min)',
    'errorsPending': 4,
}

# Atomic write
fd, tmp = tempfile.mkstemp(suffix='.json', prefix='hb_state_')
try:
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    shutil.move(tmp, state_path)
    print(f'STATE_UPDATED -- hb={state["lastHbNumber"]} silence={state["silenceHours"]}h+ mode={state["mode"]}')
except Exception as e:
    if os.path.exists(tmp):
        os.unlink(tmp)
    print(f'STATE_UPDATE_ERROR: {e}')

print('DONE')
