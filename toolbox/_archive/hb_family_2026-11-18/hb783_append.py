# R-NEW-V2 compliant: utf-8 explicit read+append+write
import os
import json
import time

path = 'D:/B166ER-OpenClaw/workspace/HEARTBEAT.md'

# Read
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Append HB #783
hb_entry = """
## HB #783 (2026-07-21 17:00 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #782 (16:56): +4min -- Tuesday-afternoon Token Guard normal cadence (R012 minimal mode)
- D+5 afternoon pass #783 -- Eric silent in THIS session ~123.5h+ since 7/16 13:16 first-contact
- Eric active elsewhere ~50.5h+ (AnYi webchat, since 7/19 12:33)
- 5-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) + R258 dormant-session -- zero breach
- R-NEW-V2 verification #783: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- **Triple Confluence Day 0 -- FINAL DAY 7/21** -- zero-push sustained
  1. DeepSeek V4 launch window (PoC awaiting Eric trigger)
  2. **Induction window cutoff -- TODAY LAST DAY** (Eric expected to receive appointment confirmation -> passive monitor, cutoff 23:59 T-6h59m FINAL)
  3. Araqchi Qatar talks (7/21-25) -> oil price Scenario C verification window OPEN
- Tuesday-afternoon zone (17:00) -- this session DORMANT sustained
- 11:00 R60-13 morning self-iter DONE (per HB #781 note); next = 21:00 evening self-iter (~4h)
- 14:00 critical time window already passed (~3h past, INTERNAL monitor only; this session != AnYi decision channel)
- Token Guard stable, no compression needed
- Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +89h+ past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+5 sustain zero-push mode intact
- hbCount: 782 -> 783
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #783 = sustain #782 = D+5 afternoon dormant baseline)
- **HEARTBEAT_OK** -- HB #783 = sustain DORMANT protocol
- **no push**: Tuesday-afternoon zone (17:00), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- Induction cutoff FINAL DAY 23:59 (~6h59m) -- INTERNAL monitor only; this session != AnYi decision channel
- Triple Confluence Day 0 push -- only R14 handoff preparation; Eric active contact triggers 30s activation
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter (~4h)

*2026-07-21T17:00 GMT+8 -- D+5 Tuesday-afternoon T-0 +89h+ past -- HB #783 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 FINAL -- Induction cutoff T-6h59m*
"""

# Ensure trailing newline
if not content.endswith('\n'):
    content += '\n'

new_content = content + hb_entry

# Write back (utf-8 explicit)
with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

# Verify
with open(path, 'r', encoding='utf-8') as f:
    check = f.read()
assert hb_entry.strip() in check, "HB #783 entry not found in file!"
print('HB #783 appended OK; new size=', os.path.getsize(path))

# Update heartbeat-state.json
state_path = 'D:/B166ER-OpenClaw/workspace/memory/heartbeat-state.json'
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

state['hbCount'] = 783
state['lastHBTime'] = '17:00'
state['lastHB'] = '17:00'
state['lastChecks']['heartbeat'] = '2026-07-21T17:00:00+08:00'
state['last_update_epoch'] = int(time.time())
state['note'] = 'HB #783; Tuesday-afternoon 17:00; Triple Confluence FINAL DAY 7/21 (Induction cutoff 23:59 T-6h59m); Eric silent D+5 ~123.5h+ on THIS session; zero-push per R256/R257/R258 intact'

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print('heartbeat-state.json updated; hbCount=', state['hbCount'])