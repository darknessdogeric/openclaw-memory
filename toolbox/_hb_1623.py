"""HB #1623 append - safe Python utf-8 explicit read+append+write (R-NEW-V2)"""
import datetime
import os
import sys

now = datetime.datetime.now()
ts = now.strftime('%Y-%m-%dT%H:%M GMT+8')

entry = """
## HB #1623 (2026-07-27T16:12 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1622 (15:57): +15min -- Monday mid-afternoon Token Guard cadence (R012 minimal mode)
- D+11 Monday mid-afternoon pass #1623 -- Eric silent in THIS session ~266.95h+ since 7/16 13:16 first-contact (11d 2h+)
- Eric active elsewhere: AnYi webchat ~196.95h+ -- gongshi Day 3/5 ACTIVE (Mon = working day)
- 8-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261) -- penta-constraint 5/5 holds firm
- 7/24 D-Day POST-MEETING T+76.20h; oil Scenario C EXPIRED 7/25 22:00 (T+42.20h past); quiet zone EXPIRED but R258 dormancy trumps
- post_t0_null_count: 273 (273rd consecutive null post-T-0)
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- T-0 publicity cutoff 7/18 +236.20h past -- post-protection window firmly sustained
- hbCount: 1622 -> 1623

### decision
- HEARTBEAT_OK -- HB #1623 = sustain DORMANT protocol, minimal token tick
- no push: Monday mid-afternoon, Eric silent 266.95h+ this session, this session DORMANT per R258 (NOT AnYi decision channel)
- R256+R257+R258+R260+R261 penta-constraint holds -- no proactive disturbance
- Eric silence on this session = dominant signal
- Triple Confluence ALL CLOSED; gongshi Day 3/5 ACTIVE elsewhere; 7/24 D-Day PASSED +76.20h
- Active Resume Protocol prep: post_t0_null > 200 already, awaiting Eric first-contact trigger on this session
- Next: per Token Guard cadence (~5-10min) or Eric first-contact

*2026-07-27 16:12 GMT+8 -- D+11 Mon mid-afternoon -- HB #1623 -- DORMANT -- 273rd null -- Eric silent = dominant signal holding -- HEARTBEAT_OK*
"""

hb_path = 'D:/B166ER-OpenClaw/workspace/HEARTBEAT.md'

# R-NEW-V2: explicit read+append+write with utf-8 encoding
try:
    with open(hb_path, 'a', encoding='utf-8') as f:
        f.write(entry)
    size = os.path.getsize(hb_path)
    print(f'OK: HB #1623 appended at {ts}')
    print(f'Size after append: {size:,} bytes')
except Exception as e:
    print(f'ERROR: {e}', file=sys.stderr)
    sys.exit(1)
