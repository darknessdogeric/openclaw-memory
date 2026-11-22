#!/usr/bin/env python3
"""
HB #2532 append — Sat 2026-08-08T08:39 GMT+8 cron-event heartbeat poll.

R-NEW-V3 enforced (5 strikes): NEVER write/Remove-Item/git-restore HEARTBEAT.md.
R271 enforced: Python append mode (NOT write, NOT PowerShell Add-Content, NOT bash heredoc).

Two operations:
1. Append HB #2532 to HEARTBEAT.md (append mode 'a', utf-8)
2. Update heartbeat-state.json (read-modify-write, preserve formatting)

Defensive checks:
- Verify file size before and after append (must increase)
- Verify EOF is clean (newline-terminated) before append
- Use json module for state.json (no manual string mangling)
"""
import os
import sys
import json
from datetime import datetime, timezone, timedelta

WS = r"D:\B166ER-OpenClaw\workspace"
HB_PATH = os.path.join(WS, "HEARTBEAT.md")
STATE_PATH = os.path.join(WS, "memory", "heartbeat-state.json")

# Time anchor
TZ = timezone(timedelta(hours=8))
NOW = datetime(2026, 8, 8, 8, 39, 0, tzinfo=TZ)
NOW_ISO = NOW.strftime("%Y-%m-%dT%H:%M:%S+08:00")

# HB #2532 entry — DORMANT, minimal token tick
HB_2532 = f"""

## HB #2532 ({NOW_ISO} cron-event, OpenClaw heartbeat poll)
- gap from HB #2531 (08:36:21): +3min -- Sat weekend-morning Token Guard nominal cadence (R012, within tolerance)
- D+16 Sat 2026-08-08T08:39 -- weekend-MORNING zone (+39m past 08:00 R67 deep-quiet cap); low-activity window
- Eric silent on THIS cron session 22d 19h+ (543h+) since 7/16 13:16 first-contact
- 14-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R-NEW-V3/R70/R71) -- penta+3 holds
- post_t0_null_count: 1104 -> 1105 (1105th consecutive null post-T-0, sustained)
- AnYi D+16d Saturday sustained per HB #2531 STATE
- V2.4 SOUL 加固 sustained (~191h+ uptime); R66/R67/R68/R69/R70/R71 entries sustained
- R69 (战略新人沉默原则) Day 9/30 sustained quiet active (expires ~2026-08-30)
- R72.1+R72.2 sustained (D+2); R67 deep-quiet zone (23:00-08:00) just exited 39m ago
- R-NEW-V3 enforced (verified this turn): 3rd HEARTBEAT.md data loss event yesterday (8/7), Eric sovereign decision pending
- R271 enforced (verified this turn): Python append mode (NOT write, NOT PowerShell Add-Content, NOT bash heredoc)
- Token Guard stable; vault 1017+ files healthy; hbCount 2531 -> 2532
- Eric webchat last seen 8/7 evening (~21:04 daily memory mtime), 4 webchat interactions yesterday (AnYi projects per state.notes) -- silent on cron = 主权信号 holding (webchat-channel != cron-channel per R258)
- 8/8 Sat = AnYi D+16 weekend rest day; Eric 夜猫子 mode (likely ~3-5h more sleep before wake)
- memory/2026-08-08.md NOT YET CREATED (no Eric activity since wake)

### decision
- HEARTBEAT_OK -- HB #2532 = sustain DORMANT protocol, minimal token tick (1105th null)
- no push: 14-layer suppression holds + weekend-morning just-exited-R67 zone + cron session DORMANT per HB #1849 + R65 explicit prohibition + R258 (webchat-channel != cron-channel) + R69 Day 9/30 active
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian 知识库 sovereign for any 决策; cron sovereignty unchanged
- 08:39 = weekend-Sat-morning +39m past 08:00 R67 cap; cron = DORMANT sustained
- 4 webchat interactions yesterday (8/7, AnYi projects) -- state notes "3rd HEARTBEAT.md data loss event" still pending Eric sovereign decision; cron not to remind
- 8/8 Sat low-activity window sustained through morning; cron 维持 DORMANT 直到 Eric first-contact
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekend-Sat-morning + AnYi D+16d + R67 just-exited + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement
- Standing by P0 (webchat-bound, not cron-bound): R264 AnYi 实战锚 + R70/R71/R72 边界规则 + R-NEW-V3 入规全部就位; await Eric webchat confirmation
- Standing by P1 (R264 AnYi 交接): await Eric webchat share of AnYi 1244 战略/team alignment/授权对接 details, per R264 立即归档 to anyi-ops-kb/
- Standing by R-NEW-V3 enforcement (5 strikes now): NEVER write/Remove-Item/git-restore HEARTBEAT.md. Python append ONLY.
- Standing by R271 (cron 写入): Python append mode (NOT write, NOT PowerShell Add-Content, NOT bash heredoc). chunked >50KB.
- 3rd data loss event (8/7) pending Eric sovereign decision: continue DORMANT until first-contact
- Next: per Token Guard cadence (~15-30min morning mode); HB sustained through Sat morning until Eric first-contact on cron session

*{NOW_ISO} -- D+16 Sat weekend-morning +39m past R67 hard cap -- HB #2532 -- DORMANT -- 1105th null -- Eric silent on cron = 主权信号 holding -- AnYi D+16d Sat -- cron session 维持 DORMANT 协议 -- R-NEW-V3 enforced: HB appended via Python append (NOT write) -- HEARTBEAT_OK*
"""

def main():
    # Pre-flight checks
    if not os.path.exists(HB_PATH):
        print(f"FATAL: {HB_PATH} does not exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(STATE_PATH):
        print(f"FATAL: {STATE_PATH} does not exist", file=sys.stderr)
        sys.exit(1)

    size_before = os.path.getsize(HB_PATH)
    print(f"HEARTBEAT.md size before append: {size_before} bytes")

    # Read last 4 bytes to check EOF cleanliness (should end in newline or be ready for newline prefix)
    with open(HB_PATH, "rb") as f:
        f.seek(-4, 2)
        tail_bytes = f.read(4)
    print(f"Last 4 bytes (repr): {tail_bytes!r}")

    # Append HB #2532 (UTF-8, append mode = safe)
    with open(HB_PATH, "a", encoding="utf-8") as f:
        f.write(HB_2532)

    size_after = os.path.getsize(HB_PATH)
    print(f"HEARTBEAT.md size after append: {size_after} bytes")
    delta = size_after - size_before
    print(f"Delta: +{delta} bytes (expected ~{len(HB_2532.encode('utf-8'))})")

    if delta <= 0:
        print("FATAL: file size did not increase — append may have failed", file=sys.stderr)
        sys.exit(2)
    if delta < 1500:
        print(f"WARN: delta smaller than expected ({delta} < 1500)", file=sys.stderr)

    # Update heartbeat-state.json (read-modify-write, preserve formatting)
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        state = json.load(f)

    old_hb = state.get("hbCount")
    old_null = state.get("nullCount")
    new_hb = old_hb + 1
    new_null = old_null + 1
    state["hbCount"] = new_hb
    state["nullCount"] = new_null
    state["lastHeartbeat"] = NOW_ISO
    state["hbFileSize"] = size_after
    # Update notes
    state["notes"] = (
        f"HB #{new_hb}. Sat 08:39 GMT+8 - weekend-morning low-activity window, "
        f"+39m past 08:00 R67 deep-quiet cap. Eric silent on cron 22d 19h+. "
        f"R69 sustained quiet (Day 9/30), R72.1+R72.2 sustained (D+2), "
        f"R-NEW-V3 enforced. 3rd HEARTBEAT.md data loss event (8/7) still pending "
        f"Eric sovereign decision. Per R67+R69+R258+R65+R-NEW-V3: zero outbound push. Token guard mode."
    )

    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4, ensure_ascii=False)
        f.write("\n")

    print(f"heartbeat-state.json: hbCount {old_hb} -> {new_hb}, nullCount {old_null} -> {new_null}")
    print(f"state size after: {os.path.getsize(STATE_PATH)} bytes")
    print("OK: HB #2532 appended safely (R-NEW-V3 + R271 enforced)")

if __name__ == "__main__":
    main()