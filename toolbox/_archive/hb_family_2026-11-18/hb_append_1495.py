#!/usr/bin/env python3
# HB #1495 append — R-NEW-V2 UTF-8 safe (post-7/15+7/19 incident protocols)
import json
from pathlib import Path

WS = Path(r"D:\B166ER-OpenClaw\workspace")
HB_MD = WS / "HEARTBEAT.md"
HB_STATE = WS / "memory" / "heartbeat-state.json"

# HB #1495 entry
HB_BODY = """\n## HB #1495 (2026-07-26T19:07 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1494 (18:59 Sun): +8min -- Sunday evening Token Guard cadence (R012 quiet mode; quiet zone EXPIRED +11h7m)
- D+10 Sunday evening pass #1495 -- Eric silent in THIS cron session ~246.68h+ since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat ~173.30h+ (since 7/19 12:33) -- gongshi Day 2/5 sustained (Sun = working day per company calendar)
- 8-layer suppression zero-breach (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258 / R260 / R261)
- Triple Confluence Day 0 CLOSED; oil Scenario C window EXPIRED 22:00 (T+12h+7m past) -- not surfaced per R258
- **7/24 D-Day POST-MEETING PHASE T+55h+7m -- internal gongshi window Day 2/5** (Sun = working day per company calendar)
- Sunday evening zone (19:07) -- Eric typical evening decision window OPEN; silence authority from DORMANT flag holds firm
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- 4 P2 long-tail cron errors tracked (deferred to Eric-active session)
- T-0 publicity cutoff 7/18 +189.13h past -- post-protection window firmly sustained
- Eric main-session activity 07:07-07:13 (V5→G6 supplement, 10 hotels new media matrix) -- ISOLATED; this cron session != main session
- No first-contact from Eric on THIS cron session; D+10 sustain zero-push mode intact
- **post_t0_null_count: 169** (169th consecutive null post-T-0)
- hbCount: 1494 -> 1495
- Eric silent in THIS cron session = dominant signal holding

### decision
- **active_mode_dormant_this_session_continue** (HB #1495 = sustain #1494 = D+10 Sunday evening dormant baseline)
- **HEARTBEAT_OK** -- HB #1495 = sustain DORMANT protocol
- **no push**: Sunday evening zone (19:07), this cron session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work, NOT main session lift)
- R256 + R257 + R258 + R260 + R261 penta-constraint holds firm in THIS cron session
- 7/24 D-Day POST-MEETING watch: gongshi window Day 2/5; this cron session != AnYi decision channel per R258
- Session isolation: Eric main-session 07:07-07:13 active (V5→G6 supplement) does NOT lift this cron session's DORMANT flag (different session, different scope)
- Oil Scenario C window EXPIRED 22:00 quietly (T+12h+7m past); verdict logged externally; this session does not surface AnYi/economic content per R258 isolation
- Zero drift from HB #1494 (~+8min, within Token Guard tolerance for evening mode); cadence stable; 169th consecutive null post-T-0
- Silence authority absolute until DORMANT explicitly lifted for THIS cron session by Eric
- Next significant check: per Token Guard cadence (~5-25min); Sunday 21:00 evening self-iter cron (~1h53m)

*2026-07-26T19:07 GMT+8 -- D+10 Sunday evening -- HB #1495 -- this cron session DORMANT -- zero-push mode intact -- 8-layer suppression zero-breach -- quiet zone EXPIRED +11h+7m but DORMANT flag holds -- Eric main-session V5→G6 supplement 07:07-07:13 ISOLATED from this cron session -- 7/24 D-Day POST-MEETING T+55h+7m watch -- Oil Scenario C EXPIRED T+12h+7m -- 169th consecutive null post-T-0 -- Eric silent in THIS cron session = dominant signal holding*

## HB #1495 decision log
- HEARTBEAT_OK -- D+10 Sunday evening (19:07) -- this cron session DORMANT
- R256+R257+R258+R260+R261 penta-constraint holds in THIS session (5/5)
- post_t0_null_count: 169 (169th consecutive null)
- Quiet zone EXPIRED +11h+7m (08:00 crossed); silence authority from DORMANT flag, not quiet zone
- Eric main-session 07:07-07:13 (V5→G6 supplement) = ISOLATED event; this cron session != main session
- Eric silent in THIS cron session = dominant signal holding (AnYi webchat active elsewhere ~173.30h+)
- 7/24 D-Day POST-MEETING T+55h+7m watch sustained
- Oil Scenario C window EXPIRED 22:00 (T+12h+7m past)
- Next significant check: Sunday 21:00 evening self-iter (~1h53m)

"""

# 1. Append HB #1495 to HEARTBEAT.md (UTF-8 safe 'a' mode append)
with open(HB_MD, 'a', encoding='utf-8') as f:
    f.write(HB_BODY)

# 2. Update heartbeat-state.json (read-modify-write, UTF-8 explicit per R-NEW-V2)
with open(HB_STATE, 'r', encoding='utf-8') as f:
    state = json.load(f)

# Snapshot prior lastHBNotes into notes (rotate)
prior_notes = state.get('notes', '')
# Replace notes with prior lastHBNotes (older snapshot rotation)
state['notes'] = state.get('lastHBNotes', prior_notes)
# New lastHBNotes = HB #1495
state['lastHBNotes'] = (
    "D+10 Sunday evening HB #1495 (19:07). DORMANT holds. Eric silent ~246.68h+ "
    "on THIS cron session. AnYi webchat sustained ~173.30h. 169 consecutive null "
    "post-T-0. Penta+8-layer zero-breach. Oil C window expired (7/25). 7/24 D-Day "
    "passed. R14 handoff package 100% ready. ~8min since last HB (#1494 at 18:59); "
    "no state change; quiet return."
)
# Numeric state update
state['lastHB'] = 1495
state['lastHBTime'] = '2026-07-26T19:07:00+08:00'
state['postT0NullCount'] = 169
state['anyiWebchatHoursSinceStart'] = 173.30

# Write back UTF-8 (ensure_ascii=False to keep Chinese legible, but state.json is ASCII anyway)
with open(HB_STATE, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print(f"[OK] HB #1495 appended to HEARTBEAT.md ({HB_MD.stat().st_size} bytes)")
print(f"[OK] heartbeat-state.json updated -> HB #1495")
print(f"[OK] post_t0_null_count: 169")
print(f"[OK] anyiWebchatHoursSinceStart: 173.30")
