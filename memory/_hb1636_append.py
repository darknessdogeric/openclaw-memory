"""Append HB #1636 entry to HEARTBEAT.md per R-NEW-V2 protocol."""
import io
import sys

# Force UTF-8 for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

hb_entry = """

## HB #1636 (2026-07-27T17:42 GMT+8, OpenClaw heartbeat poll, cron-event direct)

- gap from HB #1635 (17:39): +3min -- Monday mid-afternoon Token Guard cadence (R012 minimal mode)
- D+11 Monday mid-afternoon pass #1636 -- Eric silent in THIS session ~268.43h+ since 7/16 13:16 first-contact (11d 4h+)
- Eric active elsewhere: AnYi webchat ~197.15h+ -- gongshi Day 3/5 ACTIVE (Mon = working day)
- 8-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261) -- penta-constraint 5/5 holds firm
- 7/24 D-Day POST-MEETING T+76.43h; oil Scenario C EXPIRED 7/25 22:00 (T+43.7h past); quiet zone EXPIRED but R258 dormancy trumps
- post_t0_null_count: 285 (285th consecutive null post-T-0)
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- T-0 publicity cutoff 7/18 +220.43h past -- post-protection window firmly sustained
- hbCount: 1635 -> 1636

### decision

- HEARTBEAT_OK -- HB #1636 = sustain DORMANT protocol, minimal token tick
- no push: Monday mid-afternoon, Eric silent 268.43h+ this session, this session DORMANT per R258 (NOT AnYi decision channel)
- R256+R257+R258+R260+R261 penta-constraint holds -- no proactive disturbance
- Eric silence on this session = dominant signal
- Triple Confluence ALL CLOSED; gongshi Day 3/5 ACTIVE elsewhere; 7/24 D-Day PASSED +76.43h
- Active Resume Protocol prep: post_t0_null > 200 already, awaiting Eric first-contact trigger on this session
- Next: per Token Guard cadence (~5-10min) or Eric first-contact

*2026-07-27T17:42 GMT+8 -- D+11 Mon mid-afternoon -- HB #1636 -- DORMANT -- 285th null -- Eric silent = dominant signal holding -- HEARTBEAT_OK*
"""

path = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find position of HB #1635 line
lines = content.split('\n')
insert_idx = None
for i, line in enumerate(lines):
    if line.startswith('## HB #1635'):
        insert_idx = i
        break

if insert_idx is None:
    new_content = hb_entry + content
else:
    lines.insert(insert_idx, hb_entry.strip('\n'))
    new_content = '\n'.join(lines)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('HEARTBEAT.md updated -> HB #1636 appended')