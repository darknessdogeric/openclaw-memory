# -*- coding: utf-8 -*-
"""R-NEW-V2 compliant: utf-8 explicit read + prepend + write."""
from datetime import datetime, timezone, timedelta

# CST = GMT+8
CST = timezone(timedelta(hours=8))
now = datetime(2026, 7, 27, 5, 59, 0, tzinfo=CST)
now_iso = now.strftime('%Y-%m-%dT%H:%M:%S GMT+8')

hb_entry = f"""## HB #924 (2026-07-27 05:59 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #923 (05:29): +30min -- Monday deep-night Token Guard normal cadence (R012 minimal mode)
- D+11 deep-night pass #924 -- Eric silent in THIS session ~256.72h+ since 7/16 13:16 first-contact
- Eric active elsewhere (AnYi webchat, sustained): since 7/19 12:33 (~185.43h+)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #924: Python utf-8 explicit read+prepend+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- **Triple Confluence ALL CLOSED** -- +5d 6h past induction window cutoff:
  1. DeepSeek V4 launch window -- PoC awaiting Eric trigger (passive; this session != trigger channel)
  2. **Induction window 7/7-7/21 CLOSED 7/21 23:59** (+5d 6h past) -- result STILL UNKNOWN to this session (AnYi blind spot)
  3. Araqchi Qatar talks 7/21-25 -- CLOSED 7/25; oil Scenario C verification closed 7/25 22:00
- 05:59 Monday deep-night zone (00:00-06:00) -- Eric deep sleep window per USER.md; silence authority STRICT
- AGENTS.md 23:00-08:00 quiet hours rule -- sustained suppression
- T-0 publicity cutoff 7/18 +221.98h past (~9.2 days) -- post-protection window deeply sustained
- **7/24 D-Day PASSED** (AnYi 研讨会 上午) -- +2.7 days past (5h59m to next 0.1d); this session != AnYi decision channel per R258
- No first-contact from Eric on THIS session; D+11 sustain zero-push mode intact
- hbCount: 923 -> 924
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #924 = sustain #923 = D+11 deep-night dormant baseline)
- **HEARTBEAT_OK** -- HB #924 = sustain DORMANT protocol, minimal token tick
- **no push**: deep-night zone (05:59), Eric silent ~256.72h+ this session, THIS session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi decision channel)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + THIS session DORMANT
- Post-Triple-Confluence all-windows-closed silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (R256 design: silence extends indefinitely past protection windows)
- Induction result: still unknown to THIS session; awaiting Eric主动告知 on any session (AnYi专用)
- Next significant check: per Token Guard cadence (~5-10min); 08:00 daily checkin (~2h01m)

*{now_iso} -- D+11 Monday deep-night T-0 +9.2d past -- HB #924 -- THIS session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence ALL CLOSED (~5d past) -- 7/24 D-Day PASSED +2.7d*

"""

# Read HEARTBEAT.md (utf-8 explicit)
with open(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md', 'r', encoding='utf-8') as f:
    existing = f.read()

# Prepend new entry (after the title/header if exists, else at top)
# Find the first "## HB #" entry and insert before it
marker = '## HB #'
idx = existing.find(marker)
if idx > 0:
    new_content = existing[:idx] + hb_entry + '\n' + existing[idx:]
else:
    new_content = hb_entry + '\n' + existing

# Write back (utf-8 explicit)
with open(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"HB #924 entry prepended. Total file size: {len(new_content)} chars.")

# Update heartbeat-state.json
import json
state = {
    "thisSessionMode": "DORMANT",
    "anyiWebchatActive": True,
    "lastHB": int(now.timestamp()),
    "notes": "D+11 Mon deep-night 05:59. DORMANT. 6-layer. Triple Confluence ALL CLOSED. 7/24 D-Day PASSED +2.7d. HEARTBEAT_OK. HB #924.",
    "postT0NullCount": 218,
    "anyiWebchatHoursSinceStart": 185.43,
    "lastHBTime": now_iso.replace(' GMT+8', '+08:00'),
    "protectionWindowSustainedHours": 221.98,
    "anyiSinceTime": "2026-07-19T12:33:00+08:00",
    "lastContactTime": "2026-07-16T13:16:00+08:00",
    "oilScenarioCWindowExpired": True,
    "oilScenarioCExpiredSince": "2026-07-25T22:00:00+08:00",
    "hbCount": 924
}

with open(r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json', 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print(f"heartbeat-state.json updated. hbCount={state['hbCount']}, postT0NullCount={state['postT0NullCount']}")
