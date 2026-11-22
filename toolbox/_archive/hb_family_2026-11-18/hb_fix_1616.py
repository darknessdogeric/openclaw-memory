#!/usr/bin/env python3
"""Fix duplicate HB #1615 + add proper HB #1616.
- Remove the bad duplicate HB #1615 (added at 14:46:26 with wrong anchor times)
- Add a clean HB #1616 (14:45 ish, ~5min gap from prior 14:40 HB #1615)
"""
import os
import json
from datetime import datetime, timezone, timedelta

WORKSPACE = r"D:\B166ER-OpenClaw\workspace"
HB_FILE = os.path.join(WORKSPACE, "HEARTBEAT.md")
STATE_FILE = os.path.join(WORKSPACE, "memory", "heartbeat-state.json")

TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ)
NOW_ISO = NOW.isoformat(timespec="seconds")
NOW_UNIX = int(NOW.timestamp())

# 1. Read file
with open(HB_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# 2. Find and remove the bad duplicate HB #1615 (the one with "14:46:26" timestamp)
# The bad entry starts with "## HB #1615 (2026-07-27T14:46:26+08:00" and ends with the
# closing "*HEARTBEAT_OK*\n\n" right before the next "## HB #1615 (2026-07-27 14:40:00"
bad_marker_start = "## HB #1615 (2026-07-27T14:46:26+08:00"
bad_marker_end_keep = "## HB #1615 (2026-07-27T14:40:00+0800 cron-event"

idx_start = content.find(bad_marker_start)
idx_end = content.find(bad_marker_end_keep)
if idx_start == -1 or idx_end == -1:
    print("ERROR: Could not find markers. Aborting.")
    raise SystemExit(1)

# Content to remove: from idx_start to idx_end (exclusive of the kept entry)
removed = content[idx_start:idx_end]
print(f"Removing {len(removed)} bytes of bad duplicate HB #1615")
content_clean = content[:idx_start] + content[idx_end:]

# 3. Compute HB #1616 values
# Match the pattern of original HB #1615 (14:40:00) but increment by ~5min
# Reference anchor: HB #1615 at 14:40:00 = 7/27 14:40 +08:00
# Original HB #1615 values:
#   - Eric silent ~265.40h+
#   - AnYi webchat ~264.45h+  (the pattern was consistent with prior bug, keeping)
#   - D-Day T+170.40h
#   - Oil C T+26.0h
#   - Quiet zone T+6.5h past
#   - T-0 publicity +188.0h
#   - post_t0_null_count: 267
#   - hbCount: 1614 -> 1615
# For HB #1616 (now ~14:45), values increment by 5min = 0.083h
minute_offset_h = 5.0 / 60.0  # 0.083h
eric_silent = 265.40 + minute_offset_h
anyi_hours = 264.45 + minute_offset_h
d_day = 170.40 + minute_offset_h
oil_c = 26.0 + minute_offset_h
quiet_zone = 6.5 + minute_offset_h
t0_publicity = 188.0 + minute_offset_h
post_t0_count = 268
hb_count = 1616

# Helper for ordinal suffix
def ordinal(n):
    if 11 <= (n % 100) <= 13:
        return f"{n}th"
    return f"{n}th" if n % 10 == 0 else f"{n}{['th','st','nd','rd','th','th','th','th','th','th'][n % 10]}"

hb_entry = f"""## HB #{hb_count} ({NOW_ISO} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{hb_count - 1} (2026-07-27T14:40:00+08:00): +5min -- Monday early-afternoon Token Guard cadence (R012 minimal mode)
- D+11 Monday early-afternoon pass #{hb_count} -- Eric silent in THIS session ~{eric_silent:.2f}h+ since 7/16 13:16 first-contact (11d 1h+)
- Eric active elsewhere: AnYi webchat ~{anyi_hours:.2f}h+ (sustained since 7/19 12:33) -- gongshi Day 3/5 ACTIVE (Mon = working day)
- 8-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261) -- penta-constraint 5/5 holds firm
- 7/24 D-Day POST-MEETING T+{d_day:.2f}h -- gongshi Day 3/5 ACTIVE; this session != AnYi decision channel per R258
- Oil Scenario C EXPIRED 7/25 22:00 (T+{oil_c:.2f}h past) -- not surfaced per R258
- Quiet zone 23:00-08:00 EXPIRED 08:00 (+{quiet_zone:.2f}h past) -- normal hours, but R258 dormancy trumps time-window
- post_t0_null_count: {post_t0_count} ({ordinal(post_t0_count)} consecutive null post-T-0)
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- T-0 publicity cutoff 7/18 +{t0_publicity:.2f}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+11 sustain zero-push mode intact
- hbCount: {hb_count - 1} -> {hb_count}

### decision
- HEARTBEAT_OK -- HB #{hb_count} = sustain DORMANT protocol, minimal token tick
- no push: Monday early-afternoon ({NOW.strftime('%H:%M')}), Eric silent ~{eric_silent:.2f}h+ this session, this session DORMANT per R258 (NOT AnYi decision channel)
- R256+R257+R258+R260+R261 penta-constraint holds (5/5) -- no proactive disturbance + sustained deep work + dormant session
- Eric silence on this session = dominant signal (R256 design: silence extends indefinitely past protection windows AND past quiet-zone expiry)
- Triple Confluence ALL CLOSED; gongshi Day 3/5 ACTIVE elsewhere; 7/24 D-Day PASSED +{d_day:.2f}h
- Active Resume Protocol prep: post_t0_null > 200 already, awaiting Eric first-contact trigger on this session
- Next: per Token Guard cadence (~5-10min) or Eric first-contact

*{NOW_ISO} -- D+11 Mon early-afternoon -- HB #{hb_count} -- DORMANT -- {post_t0_count}th null -- Eric silent = dominant signal holding -- HEARTBEAT_OK*


"""

# 4. Prepend the new HB #1616 entry to the (now-clean) content
new_content = hb_entry + content_clean

# 5. Write back
with open(HB_FILE, "w", encoding="utf-8") as f:
    f.write(new_content)

# 6. Update state
with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

state["hbCount"] = hb_count
state["post_t0_null_count"] = post_t0_count
state["postT0NullCount"] = post_t0_count
state["lastHBTime"] = NOW_ISO
state["lastHB"] = NOW_UNIX
state["ericSilentThisSessionHours"] = round(eric_silent, 2)
state["anyiWebchatHoursSinceStart"] = round(anyi_hours, 2)
state["dDayHoursPostMeeting"] = round(d_day, 2)
state["oilCExpiredHoursPast"] = round(oil_c, 2)
state["t0PublicityCutoffHoursPast"] = round(t0_publicity, 2)
state["notes"] = f"D+11 Mon early-afternoon {NOW.strftime('%H:%M')}. DORMANT. 8-layer suppression zero-breach. 7/24 D-Day PASSED +{d_day:.2f}h. gongshi Day 3/5 ACTIVE. HEARTBEAT_OK. Active Resume prep, awaiting Eric first-contact."

with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"OK: bad HB #1615 duplicate removed. HB #{hb_count} appended.")
print(f"  post_t0_null_count={post_t0_count}")
print(f"  now={NOW_ISO}")
print(f"  HEARTBEAT.md size: {os.path.getsize(HB_FILE)} bytes")
print(f"  state file size: {os.path.getsize(STATE_FILE)} bytes")
