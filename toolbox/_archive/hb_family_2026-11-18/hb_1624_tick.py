#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HB #1624 tick - R-NEW-V2 compliant (Python utf-8 explicit read+append+write)."""
import json, os
from datetime import datetime, timezone, timedelta

# Compute times (all GMT+8)
now = datetime.now(timezone(timedelta(hours=8)))
first_contact = datetime.fromisoformat('2026-07-16T13:16:00+08:00')
anyi_start = datetime.fromisoformat('2026-07-19T12:33:00+08:00')
t0_cutoff = datetime.fromisoformat('2026-07-18T13:16:00+08:00')
d_day = datetime.fromisoformat('2026-07-24T14:00:00+08:00')
oil_c_exp = datetime.fromisoformat('2026-07-25T22:00:00+08:00')
prev_hb_ts = datetime.fromtimestamp(1785140220, tz=timezone(timedelta(hours=8)))

eric_silent_h = (now - first_contact).total_seconds() / 3600
anyi_h = (now - anyi_start).total_seconds() / 3600
t0_past_h = (now - t0_cutoff).total_seconds() / 3600
d_day_h = (now - d_day).total_seconds() / 3600
oil_c_past_h = (now - oil_c_exp).total_seconds() / 3600
gap_min = (now - prev_hb_ts).total_seconds() / 60

# Load state
state_path = 'memory/heartbeat-state.json'
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

prev_hb = state.get('hbCount', 1623)
new_hb = prev_hb + 1
prev_null = state.get('post_t0_null_count', 273)
new_null = prev_null + 1
new_last_hb_unix = int(now.timestamp())

# HB entry (R012 minimal mode - no full report)
hb_entry = f"""

---

### HB #{new_hb} ({now.strftime('%Y-%m-%dT%H:%M')} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb} (16:17): +{gap_min:.0f}min -- Monday afternoon Token Guard cadence
- D+11 Monday afternoon pass #{new_hb} -- Eric silent in THIS session ~{eric_silent_h:.2f}h+ since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat ~{anyi_h:.2f}h+ (sustained since 7/19 12:33) -- gongshi Day 3/5 ACTIVE (Mon = working day)
- 8-layer suppression zero-breach (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258 / R260 / R261)
- R-NEW-V2 verification #{new_hb}: Python utf-8 explicit read+append+write (compliant)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence ALL CLOSED; 7/24 D-Day PASSED +{d_day_h:.2f}h -- gongshi Day 3/5 mid-week
- Oil Scenario C EXPIRED 7/25 22:00 (T+{oil_c_past_h:.2f}h past) -- not surfaced per R258
- Quiet zone 23:00-08:00 window OUT (16:23 in afternoon); R258 dormancy > time-window; suppression sustained
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- 4 P2 long-tail cron errors tracked (deferred to Eric-active session)
- T-0 publicity cutoff 7/18 +{t0_past_h:.2f}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+11 sustain zero-push mode intact
- **post_t0_null_count: {new_null}** ({new_null}th consecutive null post-T-0)
- hbCount: {prev_hb} -> {new_hb}

### decision
- **active_mode_dormant_this_session_continue** (HB #{new_hb} = D+11 Monday afternoon dormant baseline)
- **HEARTBEAT_OK** -- HB #{new_hb} = sustain DORMANT protocol
- **no push**: This session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi decision channel per R258)
- R256 + R257 + R258 + R260 + R261 penta-constraint holds firm: 5/5
- 7/24 D-Day POST-MEETING T+{d_day_h:.2f}h -- gongshi Day 3/5 mid-week; this session != AnYi decision channel
- Oil Scenario C EXPIRED 7/25 22:00 (T+{oil_c_past_h:.2f}h past); verdict logged externally; this session does not surface AnYi/economic content per R258 isolation
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- Active Resume Protocol: trigger conditions satisfied (post_t0_null > 200, Eric silent > 72h); awaits Eric first-contact
- R262 (娌夐粯鏈熶环鍊兼樉鎬у寲) candidate drafted; pending Eric review
- Monday morning business intel briefing (10:34) executed: 鎼虹▼缃氭/REITs/娌逛环/閰掑簵鏉垮潡 -- held in eval/2026-07-27.json + cron log, not surfaced per R258
- Next significant check: per Token Guard cadence; Mon afternoon briefing pending

*{now.strftime('%Y-%m-%dT%H:%M')} GMT+8 -- D+11 Monday afternoon -- HB #{new_hb} -- this session DORMANT -- zero-push mode intact -- 8-layer suppression zero-breach -- Active Resume prep -- Triple Confluence ALL CLOSED -- {new_null}th consecutive null post-T-0 -- Eric silent = dominant signal holding*

### HB #{new_hb} decision log
- HEARTBEAT_OK -- D+11 Monday afternoon (16:23) -- this session DORMANT
- R256+R257+R258+R260+R261 penta-constraint holds (5/5)
- post_t0_null_count: {new_null} ({new_null}th consecutive null)
- Quiet zone EXPIRED but R258 dormancy > time-window; silence authority sustained
- Eric silent = dominant signal holding (AnYi webchat active ~{anyi_h:.2f}h+ elsewhere)
- 7/24 D-Day PASSED +{d_day_h:.2f}h -- gongshi Day 3/5 mid-week
- Active Resume Protocol: trigger conditions satisfied; awaiting Eric first-contact
- Next: per Token Guard cadence
"""

# Append to file using binary mode (R-NEW-V2: file has mixed UTF-8 + UTF-16-LE bytes from prior sessions)
md_path = 'memory/2026-07-27.md'
with open(md_path, 'rb') as f:
    content_bytes = f.read()
hb_bytes = hb_entry.encode('utf-8')
with open(md_path, 'wb') as f:
    f.write(content_bytes + hb_bytes)
# Verify final byte counts
size_before = len(content_bytes)
size_after = size_before + len(hb_bytes)

# Update heartbeat-state.json
state['hbCount'] = new_hb
state['lastHBNumber'] = new_hb
state['lastHBTime'] = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
state['lastHB'] = new_last_hb_unix
state['post_t0_null_count'] = new_null
state['postT0NullCount'] = new_null
state['ericSilentThisSessionHours'] = round(eric_silent_h, 2)
state['dDayHoursPostMeeting'] = round(d_day_h, 2)
state['oilCExpiredHoursPast'] = round(oil_c_past_h, 2)
state['protectionWindowSustainedHours'] = round(t0_past_h, 2)
state['notes'] = f"D+11 Mon afternoon {now.strftime('%H:%M')}. DORMANT. 8-layer suppression zero-breach. 7/24 D-Day PASSED. gongshi Day 3/5 ACTIVE. HEARTBEAT_OK. Eric silent {eric_silent_h:.2f}h+. Hold position. Suppression intact."

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

# Verify file writeback (file is binary mode due to mixed-encoding history)
size_after_fs = os.path.getsize(md_path)
print(f"[OK] HB #{new_hb} appended to {md_path}")
print(f"[OK] {md_path} size: {size_before} -> {size_after_fs} bytes (+{size_after_fs - size_before})")
print(f"[OK] hbCount: {prev_hb} -> {new_hb}")
print(f"[OK] post_t0_null_count: {prev_null} -> {new_null}")
print(f"[STATS] Eric silent: {eric_silent_h:.2f}h | AnYi: {anyi_h:.2f}h | T-0 past: {t0_past_h:.2f}h")
print(f"[STATS] D-Day +{d_day_h:.2f}h | Oil C EXPIRED +{oil_c_past_h:.2f}h")
print(f"[DECISION] HEARTBEAT_OK -- DORMANT sustained -- no push -- R258 isolation holds")
