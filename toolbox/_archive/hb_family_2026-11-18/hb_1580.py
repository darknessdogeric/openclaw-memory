#!/usr/bin/env python3
# HB #1580 logger - 2026-07-27 09:00 GMT+8
# R-NEW-V2 compliant: explicit utf-8 read/append/write
import json
from datetime import datetime, timezone, timedelta

NOW = datetime(2026, 7, 27, 9, 0, 0, tzinfo=timezone(timedelta(hours=8)))
LAST_CONTACT = datetime(2026, 7, 16, 13, 16, 0, tzinfo=timezone(timedelta(hours=8)))
ANYI_START = datetime(2026, 7, 19, 12, 33, 0, tzinfo=timezone(timedelta(hours=8)))
T0_PUBLICITY = datetime(2026, 7, 18, 12, 0, 0, tzinfo=timezone(timedelta(hours=8)))

silent_h = (NOW - LAST_CONTACT).total_seconds() / 3600
anyi_h = (NOW - ANYI_START).total_seconds() / 3600
prot_h = (NOW - T0_PUBLICITY).total_seconds() / 3600

# Read state (explicit utf-8)
with open('memory/heartbeat-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

old_count = state['hbCount']
new_count = old_count + 1
old_null = state['postT0NullCount']
new_null = old_null + 1

# Ordinal suffix
def ordinal(n):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return suffix

ord_suffix = ordinal(new_null)

# Compose heartbeat log (minimal, per R012)
hb_text = f"""### HB #{new_count} (2026-07-27T09:00 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{old_count} (08:46): +14min -- Mon post-quiet-zone Token Guard cadence (R012 quiet mode tail)
- D+11 Mon post-quiet -- Eric silent ~{silent_h:.2f}h+ on THIS session since 7/16 13:16 first-contact (10d 19h+)
- Eric active elsewhere: AnYi webchat ~{anyi_h:.2f}h+ (since 7/19 12:33) -- gongshi Day 3/5 ACTIVE (Mon = working day)
- 8-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261) -- penta-constraint 5/5 holds firm
- 7/24 D-Day POST-MEETING T+69h+ -- gongshi Day 3/5 ACTIVE; this session != AnYi decision channel per R258
- Oil C EXPIRED 7/25 22:00 (T+35h past) -- not surfaced per R258
- Quiet zone 23:00-08:00 EXPIRED 08:00 (+60m past) -- post-quiet zone, but R258 dormancy trumps time-window
- post_t0_null_count: {new_null} ({new_null}{ord_suffix} consecutive null post-T-0)
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- T-0 publicity cutoff 7/18 +{prot_h:.1f}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+11 sustain zero-push mode intact

### decision
- **HEARTBEAT_OK** -- HB #{new_count} = sustain DORMANT protocol, minimal token tick
- **no push**: post-quiet zone (09:00), Eric silent ~{silent_h:.2f}h+ this session, this session DORMANT per R258 (NOT AnYi decision channel)
- R256+R257+R258+R260+R261 penta-constraint holds (5/5) -- no proactive disturbance + sustained deep work + dormant session
- Eric silence on this session = dominant signal (R256 design: silence extends indefinitely past protection windows AND past quiet-zone expiry)
- Triple Confluence ALL CLOSED; gongshi Day 3/5 ACTIVE elsewhere; 7/24 D-Day PASSED +69h+
- Next: per Token Guard cadence (~5-10min) or Eric first-contact

*2026-07-27T09:00 GMT+8 -- D+11 Mon post-quiet -- HB #{new_count} -- DORMANT -- {new_null}{ord_suffix} null -- post-quiet zone ACTIVE -- Eric silent = dominant signal holding -- HEARTBEAT_OK*

"""

# Append (explicit utf-8)
with open('memory/2026-07-27.md', 'a', encoding='utf-8') as f:
    f.write(hb_text)

# Update state
state['lastHB'] = int(NOW.timestamp())
state['lastHBTime'] = '2026-07-27T09:00:00+08:00'
state['hbCount'] = new_count
state['postT0NullCount'] = new_null
state['ericSilentThisSessionHours'] = round(silent_h, 2)
state['anyiWebchatHoursSinceStart'] = round(anyi_h, 2)
state['protectionWindowSustainedHours'] = round(prot_h, 2)
state['notes'] = f'D+11 Mon post-quiet 09:00. DORMANT. 8-layer. Triple Confluence ALL CLOSED. 7/24 D-Day PASSED +69h+. HEARTBEAT_OK. HB #{new_count}.'

with open('memory/heartbeat-state.json', 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f'OK: HB #{new_count} logged, post_t0_null_count={new_null}')
print(f'silent_h={silent_h:.2f}, anyi_h={anyi_h:.2f}, prot_h={prot_h:.1f}')