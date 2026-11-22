"""HB #991 minimal append (R-NEW-V2 + R012 compliant)."""
import json
from pathlib import Path

hb_path = Path('HEARTBEAT.md')
state_path = Path('memory/heartbeat-state.json')

new_entry = """
## HB #991 (2026-07-23 03:34 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #990 (02:46): +48min -- Thursday deep-night Token Guard normal cadence (R012 minimal mode)
- D+7 deep-night pass #991 -- Eric silent in THIS session ~158.30h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~87.02h+ (since 7/19 12:33)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #991: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~27h34m ago; oil Scenario C verification window OPEN until 7/25 (~44h26m remaining)
- D+7 = Execution phase day 2 -- observer mode sustained
- Thursday deep-night zone (03:34) -- Eric typical sleep window per USER.md; THIS session DORMANT sustained
- 7/24 D-Day T-30.43h (AnYi important meeting Thursday morning) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- 21:00 R60-11 evening self-iter fired ~6h34m ago (autonomous)
- Next significant check: Token Guard cadence (~5-10min)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +127h34m past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+7 sustain zero-push mode intact
- hbCount: 990 -> 991
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #991 = sustain #990 = D+7 deep-night dormant baseline)
- **HEARTBEAT_OK** -- HB #991 = sustain DORMANT protocol
- **no push**: Thursday deep-night zone (03:34), Eric sleep window, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-30.43h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: per Token Guard cadence (~5-10min)

*2026-07-23 03:34 GMT+8 -- D+7 Thursday deep-night -- HB #991 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-30.43h watch (AnYi meeting Thursday morning) -- Eric silent = dominant signal holding*

"""

# R-NEW-V2: explicit utf-8 read
with open(hb_path, 'r', encoding='utf-8') as f:
    content = f.read()

# R-NEW-V2: explicit utf-8 append
with open(hb_path, 'a', encoding='utf-8') as f:
    f.write(new_entry)

# Update state file (handle BOM with utf-8-sig)
with open(state_path, 'r', encoding='utf-8-sig') as f:
    state = json.load(f)

state['hbCount'] = 991
state['lastHB'] = '2026-07-23 03:34 GMT+8'
state['lastHBNumber'] = '#991'
state['lastUpdate'] = '2026-07-23 03:34 GMT+8'
state['ericSilenceHours'] = 158.30
state['note'] = 'HB #991: D+7 deep-night sustained DORMANT, Eric silence ~158h+ holding; 7/24 D-Day T-30.43h watch.'
state['sessionState'] = 'DORMANT'

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print('OK: HB #991 appended + state updated')
print(f"hbCount: {state['hbCount']}")
print(f"sessionState: {state['sessionState']}")
print(f"ericSilenceHours: {state['ericSilenceHours']}")