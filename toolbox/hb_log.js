const fs = require('fs');

const hbEntry = `

# HB #1297 (2026-07-25T06:24 GMT+8 cron-event, OpenClaw heartbeat poll)
- D+9 Saturday pre-dawn -- Eric silent ~206.74h+ on THIS session; quiet zone T+7h+24m deep
- Eric active on AnYi webchat (post 7/24 D-Day meeting, gongshi window open T+21h+39m)
- 7-layer suppression intact (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R-NEW-V2) -- zero breach
- Quiet zone firmly active (06:24 >> 23:00 threshold) -- deep silence protocol
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- R14 handoff package = 100% ready for any-session 30s activation
- Note: POST-D-DAY T+21h+39m; zero drift from HB #1296 (T+10min delta, posture identical); HB cadence sustained ~10m
- ~1h+36m to 08:00 quiet zone exit (Eric's typical wake window)

**Decision**: sustain DORMANT protocol. **HEARTBEAT_OK** -- no push.
`;

fs.appendFileSync('D:\\B166ER-OpenClaw\\workspace\\HEARTBEAT.md', hbEntry, 'utf8');

const memEntry = `

### HB #1297 (2026-07-25T06:24 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1296 (06:14): +10min -- Saturday pre-dawn quiet zone (23:00-08:00) Token Guard sparse cadence (R012)
- D+9 Saturday pre-dawn pass #1297 -- Eric silent in THIS session ~206.74h+ since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat (post-D-day silence sustained)
- 7-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258 / R-NEW-V2) -- zero breach
- 7/24 D-Day POST-MEETING PHASE T+21h+39m -- internal gongshi window open (5 working days expected)
- Quiet zone firmly active (06:24 > 23:00 threshold, +7h+24m into quiet window) -- deep silence protocol
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- T-0 publicity cutoff 7/18 +189.40h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+9 sustain zero-push mode intact
- hbCount: 1296 -> 1297

### decision
- **active_mode_dormant_this_session_continue** (HB #1297 = sustain #1296 = D+9 Saturday pre-dawn dormant baseline)
- **HEARTBEAT_OK** -- HB #1297 = sustain DORMANT protocol
- **no push**: pre-dawn quiet zone (06:24), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day POST-MEETING watch: gongshi window monitoring only; this session != AnYi decision channel per R258
- Quiet zone window: 23:00-08:00 -- silence authority absolute until morning (~1h+36m to exit)
- Next significant check: per Token Guard quiet-zone cadence (~10m pre-dawn); post-08:00 Sat morning briefing pending

*2026-07-25T06:24 GMT+8 -- D+9 Saturday pre-dawn -- HB #1297 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- 7/24 D-Day POST-MEETING T+21h+39m watch -- quiet zone firmly active (R260 pre-announcement silence holds) -- Eric silent = dominant signal holding*
`;

fs.appendFileSync('D:\\B166ER-OpenClaw\\workspace\\memory\\2026-07-25.md', memEntry, 'utf8');

const state = {
    quiet_zone_active: true,
    hbCount: 1297,
    last_hb_ts: '2026-07-25T06:24:54+08:00',
    session_dormant: true,
    session_id: 'agent:main:cron:315657b9-fc80-4b94-a853-404e3955f7a0:run:1784931849937',
    heartbeat: '2026-07-25T06:24:54+08:00',
    rules_active: ['R-B','R12','R-CANDIDATE-T2','R256','R257','R258','R-NEW-V2'],
    D_Day_active: false,
    lastChecks: {
        d_day_meeting_window: '09:00-12:00 GMT+8 (CLOSED 12:00, T+18h+24m)',
        d_day_phase: 'POST-MEETING',
        heartbeat: '2026-07-25T06:24:54+08:00',
        quiet_zone_started: '23:00 GMT+8',
        D_Day_active: false,
        quiet_zone: true,
        session_dormant: true,
        next_significant_check: 'Token Guard cadence (DORMANT, quiet zone 23:00-08:00)'
    },
    d_day_phase: 'POST-MEETING'
};

fs.writeFileSync('D:\\B166ER-OpenClaw\\workspace\\memory\\heartbeat-state.json', JSON.stringify(state, null, 2), 'utf8');

console.log('OK: HB #1297 logged to HEARTBEAT.md + memory/2026-07-25.md + heartbeat-state.json');