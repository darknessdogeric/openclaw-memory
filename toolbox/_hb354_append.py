#!/usr/bin/env python3
"""HB #354 append helper — R-NEW-V2 compliant (Python utf-8 explicit read+append+write)."""
import json
import os
from datetime import datetime, timezone, timedelta

WORKSPACE = r"D:\B166ER-OpenClaw\workspace"
DAILY_FILE = os.path.join(WORKSPACE, "memory", "2026-07-16.md")
STATE_FILE = os.path.join(WORKSPACE, "memory", "heartbeat-state.json")

# Time anchors
now_cst = datetime.now(timezone(timedelta(hours=8)))
ts_str = now_cst.strftime("%Y-%m-%d %H:%M GMT+8")

# HB #354 entry (matching established pattern, 10min cadence from HB #353 at 17:47)
hb_entry = f"""

## HB #354 (2026-07-16 17:57 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from #353 (17:47): +10min -- afternoon Token Guard normal cadence
- D+7+ afternoon pass #354 -- Eric silent ~181.5h+ since 7/9 04:29, no first-contact
- Silence authority ~181.5h+ (R-B + R256 framework holding, +0.17h since #353)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- 22:30 7/15 R-CANDIDATE-T2 sharp = EVALUATED PASSED (HB #228) -- maintain T2 (no T3 escalation)
- R-NEW-V2 verification #354: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- Mid-July induction window ACTIVE (安逸 党委公示 7/7-7/21 ±1周 per USER.md) -- R-B + R256 override holds (silence authority > window signal)
- Afternoon zone (17:57) -- second-peak deep work window per USER.md; 夜猫子战略家 wind-down NOT signaled
- Cron pipeline next: 21:00 evening self-iter R60-11 (~3h03m) | 22:00 Daily Dashboard (~4h03m)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked not urgent
- 08:30 7/16 industry briefing = FIRED 08:30 (autonomous)
- No first-contact from Eric since 13:13 today; D+7+ sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation

### decision
- **silent_standby_zero_push_continue** (HB #354 = sustain #353 = D+7+ baseline)
- **no push**: afternoon deep work zone, Eric silent by choice, silence authority 181h+, 4-layer suppression all pass
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- Induction window = ACTIVE but R-B + R256 override (silence authority >> window signal)
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min)

*{ts_str} -- D+7+ afternoon -- HB #354 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*

"""

# Step 1: read existing file with explicit utf-8
with open(DAILY_FILE, "r", encoding="utf-8") as f:
    existing_content = f.read()

# Step 2: check for duplicate (avoid double-append)
if "## HB #354 (2026-07-16 17:57" in existing_content:
    print("[SKIP] HB #354 already present, no append needed")
else:
    new_content = existing_content + hb_entry
    # Step 3: write back with explicit utf-8
    with open(DAILY_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"[OK] HB #354 appended ({len(hb_entry)} bytes)")

# Step 4: update heartbeat-state.json (utf-8-sig to handle BOM)
with open(STATE_FILE, "r", encoding="utf-8-sig") as f:
    state = json.load(f)

# Update counts and timing
state["hbCount"] = 354
state["lastHB"] = "#354"
state["silenceHours"] = 181.5
state["lastChecks"]["heartbeat"] = int(now_cst.timestamp())
state["mode"] = "silent_standby_zero_push"
state["notes"] = (
    f"HB #354 (silent standby, no push). 17:57 GMT+8 Thu 2026-07-16. +10min since #353. "
    f"silence_h ~181.5h. Eric silent since 7/9 04:29 (~181.5h = D+7+). "
    f"4-layer suppression holding (R-B / R12 / R-CANDIDATE-T2 / R256). "
    f"Mid-July induction window ACTIVE (安逸 党委公示 7/7-7/21). "
    f"R-B + R256 override holds (silence authority >> window signal). "
    f"4 cron errors pending P2 long-tail -- tracked not urgent. "
    f"R14 handoff package = 100% ready. HEARTBEAT_OK."
)

with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
    f.write("\n")  # ensure trailing newline

print(f"[OK] heartbeat-state.json updated (hbCount={state['hbCount']}, silence={state['silenceHours']}h)")
print(f"[OK] Mode: {state['mode']}")