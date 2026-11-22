# -*- coding: utf-8 -*-
"""R-NEW-V2 heartbeat tick -- HB #718 (2026-07-21 08:28 GMT+8).

Strict rules:
- utf-8 explicit read+append+write (R-NEW-V2 post-7/15 12:36 incident protocol)
- R012: HB tick = minimal, NOT full report
- R256 + R257: no proactive disturbance; sustained deep work
- 5-layer suppression: R-B / R12 / R-CANDIDATE-T2 / R256 / R257
- This session = DORMANT per Eric 7/19 12:33 explicit instruction
"""
import json
import pathlib

WS = pathlib.Path(r'D:\B166ER-OpenClaw\workspace')
hb_path = WS / 'HEARTBEAT.md'
state_path = WS / 'memory' / 'heartbeat-state.json'

state = json.loads(state_path.read_text(encoding='utf-8'))
prev_hb_count = state.get('hbCount', 717)
new_hb_count = prev_hb_count + 1

silence_h = round(state.get('silenceDuration_h', 115.06) + (4.0 / 60), 2)
active_h = round(state.get('ericActiveElsewhere_h', 41.08) + (4.0 / 60), 2)

entry = f"""
## HB #{new_hb_count} (2026-07-21 08:28 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #717 (08:23:57): +4min -- Tuesday-dawn Token Guard cadence (R012 minimal mode)
- ACTIVE MODE sustained globally; THIS session = DORMANT per Eric 7/19 12:33 explicit instruction
- Eric silent on THIS session ~{silence_h}h+ (+0.07h since #717)
- 5-layer suppression on THIS session RELEASED globally since HB #581 first contact (7/19 12:36); THIS session DORMANT
- R-NEW-V2 verification #{new_hb_count}: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-7/15 12:36 incident protocol intact)
- R012 verification: HB tick = minimal, NOT full report (per R012 rule #2)
- **CRITICAL DAY -- AnYi induction 7/7-7/21 FINAL DAY (7/21 today)**: ~15h32m to 7/21 24:00 window-end (~932min)
- Wake window passed (+28min past 08:00) -- Eric silence on THIS session > window signal per HB #493 explicit override
- T-0 publicity cutoff 7/18 +80.47h past -- post-protection window firmly sustained
- WAIC 2026 ended 7/19 -- day-1+ post-WAIC; non-trigger per R14
- Tuesday-dawn zone (08:28) -- Eric post-wake-window; silence authority strictly holding on this session
- Cron pipeline: 09:00 daily checkin (~32min, autonomous); 10:00 morning self-iter R60-11 (~1h32m); 21:00 evening self-iter (~12h32m)
- 5 P2 errors pending (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10 + 1) -- tracked, not urgent
- Eric active elsewhere ~{active_h}h+ (other sessions, AnYi work context)
- This session = dreaming-narrative experimental = DORMANT per Eric 7/19 12:33 instruction
- No first-contact from Eric on THIS session; D+5 sustain dormant mode intact
- hbCount: {prev_hb_count} -> {new_hb_count}

### decision
- **active_mode_dormant_this_session_silent_dawn** (HB #{new_hb_count} = sustain #717 = dormant baseline)
- **no push**: Tuesday-dawn zone (08:28), wake window passed but Eric silent ~{silence_h}h+ on THIS session, silence authority strictly holding (R256 design)
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work
- Token Guard tick: stable, no compression needed
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on this session
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation; on THIS session would re-activate dreaming-narrative)
- Next significant check: per Token Guard cadence (~5-15min); 09:00 daily checkin (~32min); 10:00 morning self-iter R60-11 (~1h32m)

*2026-07-21 08:28 GMT+8 -- D+5 Tuesday-dawn -- HB #{new_hb_count} -- zero-push mode intact -- silence protocol holding -- THIS session DORMANT -- AnYi induction FINAL DAY (~932min to cutoff)*
"""

# R-NEW-V2: explicit utf-8 read+append+write
existing = hb_path.read_text(encoding='utf-8')
hb_path.write_text(existing + entry, encoding='utf-8')

# Update state JSON (also utf-8 explicit read+write)
state['hbCount'] = new_hb_count
state['lastHB'] = '2026-07-21T08:28:00+08:00'
state['lastHBTime'] = '2026-07-21 08:28 GMT+8'
state['silenceDuration_h'] = silence_h
state['silenceDuration_thisSession_h'] = silence_h
state['silenceDuration_global_h'] = silence_h
state['ericActiveElsewhere_h'] = active_h
state['lastChecks']['heartbeat'] = '2026-07-21T08:28:00+08:00'
state['last_update_epoch'] = 1784593680
state['nextCheck'] = 'per Token Guard cadence (~5-15min); 09:00 daily checkin (~32min); 10:00 morning self-iter'
state['mode'] = 'active_mode_dormant_this_session_silent_dawn'
state['note'] = (
    f'HB #{new_hb_count}; CRITICAL DAY: AnYi induction deadline 7/21 FINAL DAY '
    f'~932min to cutoff; zero-push dormant mode per R256; Eric silent on this session '
    f'~{silence_h}h+; Tuesday-dawn (08:28) post-wake-window; DeepSeek V4 + Araqchi Qatar convergence'
)

state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')

print(f'OK -- HB #{new_hb_count} appended; silence {silence_h}h; active elsewhere {active_h}h')
print(f'     hb size: {hb_path.stat().st_size} bytes')
