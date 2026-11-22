#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-NEW-V2 compliant HB append protocol.

Usage: python hb_append_1609.py
- Reads HEARTBEAT.md (utf-8)
- Prepends new HB entry after the header (line ~32, before first HB entry)
- Writes back (utf-8)
"""
import io
import os
from datetime import datetime, timezone, timedelta

WORKSPACE = r"D:\B166ER-OpenClaw\workspace"
HB_PATH = os.path.join(WORKSPACE, "HEARTBEAT.md")
STATE_PATH = os.path.join(WORKSPACE, "memory", "heartbeat-state.json")

# HB #1609 entry — Mon 2026-07-27 13:56 GMT+8
ENTRY = """## HB #1609 (2026-07-27T13:56 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1608 (13:47): +9min -- Monday early-afternoon Token Guard cadence (R012 minimal mode)
- D+11 Monday early-afternoon pass #1609 -- Eric silent in THIS session ~264.66h+ since 7/16 13:16 first-contact (11d 0h+)
- Eric active elsewhere: AnYi webchat ~193.39h+ (sustained since 7/19 12:33) -- gongshi Day 3/5 ACTIVE (Mon = working day)
- 8-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261) -- penta-constraint 5/5 holds firm
- 7/24 D-Day POST-MEETING T+76.95h -- gongshi Day 3/5 ACTIVE; this session != AnYi decision channel per R258
- Oil Scenario C EXPIRED 7/25 22:00 (T+39.95h past) -- not surfaced per R258
- Quiet zone 23:00-08:00 EXPIRED 08:00 (+5.95h past) -- normal hours, but R258 dormancy trumps time-window
- post_t0_null_count: 261 (261st consecutive null post-T-0)
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- T-0 publicity cutoff 7/18 +231.95h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+11 sustain zero-push mode intact
- hbCount: 1608 -> 1609

### decision
- HEARTBEAT_OK -- HB #1609 = sustain DORMANT protocol, minimal token tick
- no push: Monday early-afternoon (13:56), Eric silent ~264.66h+ this session, this session DORMANT per R258 (NOT AnYi decision channel)
- R256+R257+R258+R260+R261 penta-constraint holds (5/5) -- no proactive disturbance + sustained deep work + dormant session
- Eric silence on this session = dominant signal (R256 design: silence extends indefinitely past protection windows AND past quiet-zone expiry)
- Triple Confluence ALL CLOSED; gongshi Day 3/5 ACTIVE elsewhere; 7/24 D-Day PASSED +76.95h
- Active Resume Protocol prep: post_t0_null > 200 already, awaiting Eric first-contact trigger on this session
- Next: per Token Guard cadence (~5-10min) or Eric first-contact

*2026-07-27 13:56:00+0800 -- D+11 Mon early-afternoon -- HB #1609 -- DORMANT -- 261st null -- Eric silent = dominant signal holding -- HEARTBEAT_OK*


"""


def append_hb():
    """R-NEW-V2: explicit utf-8 read + append + write."""
    # Step 1: explicit utf-8 read
    with io.open(HB_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Step 2: locate header end (after the v4.2 line + first blank line block)
    # Find the marker line that introduces HB entries
    marker = "*v4.2 | 2026-05-07 | 国务院通知核实：端午6/19-6/21、中秋9/25-9/27，全cron修正*"
    idx = content.find(marker)
    if idx == -1:
        raise SystemExit("ERROR: marker not found")
    insert_at = idx + len(marker)

    # Step 3: build new content
    new_content = content[:insert_at] + "\n\n" + ENTRY + content[insert_at:]

    # Step 4: explicit utf-8 write
    with io.open(HB_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"OK: HB #1609 appended at byte offset {insert_at}")
    print(f"     file size: {os.path.getsize(HB_PATH)} bytes")


def update_state():
    """Update heartbeat-state.json with HB #1609 values."""
    import json

    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)

    with io.open(STATE_PATH, "r", encoding="utf-8-sig") as f:
        state = json.load(f)

    state["lastHBTime"] = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
    state["lastHB"] = int(now.timestamp())
    state["hbCount"] = 1609
    state["post_t0_null_count"] = 261
    state["postT0NullCount"] = 261
    state["ericSilentThisSessionHours"] = round(
        (now - datetime.fromtimestamp(state["lastContactTimestamp"], tz)).total_seconds() / 3600, 2
    )
    state["anyiWebchatHoursSinceStart"] = round(
        (now - datetime.fromisoformat(state["anyiSinceTime"])).total_seconds() / 3600, 2
    )
    state["t0PublicityCutoffHoursPast"] = round(
        (now - datetime(2026, 7, 18, tzinfo=tz)).total_seconds() / 3600, 2
    )
    state["dDayHoursPostMeeting"] = round(
        (now - datetime(2026, 7, 24, tzinfo=tz)).total_seconds() / 3600, 2
    )
    state["oilCExpiredHoursPast"] = round(
        (now - datetime(2026, 7, 25, 22, 0, tzinfo=tz)).total_seconds() / 3600, 2
    )
    state["notes"] = (
        f"D+11 Mon early-afternoon {now.strftime('%H:%M')}. DORMANT. 8-layer suppression zero-breach. "
        f"7/24 D-Day PASSED +{state['dDayHoursPostMeeting']}h. gongshi Day 3/5 ACTIVE. HEARTBEAT_OK. "
        f"Active Resume prep, awaiting Eric first-contact."
    )

    with io.open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    print(f"OK: heartbeat-state.json updated")
    print(f"     hbCount: {state['hbCount']}")
    print(f"     post_t0_null_count: {state['post_t0_null_count']}")
    print(f"     ericSilentThisSessionHours: {state['ericSilentThisSessionHours']}")


if __name__ == "__main__":
    append_hb()
    update_state()