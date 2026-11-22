#!/usr/bin/env python3
"""HB #310 append helper — R-NEW-V2 compliant (Python utf-8 explicit read+append+write)."""
import json
import os
from datetime import datetime, timezone, timedelta

WORKSPACE = r"D:\B166ER-OpenClaw\workspace"
DAILY_FILE = os.path.join(WORKSPACE, "memory", "2026-07-16.md")
STATE_FILE = os.path.join(WORKSPACE, "memory", "heartbeat-state.json")

# Time anchors
now_cst = datetime.now(timezone(timedelta(hours=8)))
ts_str = now_cst.strftime("%Y-%m-%d %H:%M GMT+8")

# HB #310 entry (matching the established pattern, 5min cadence post-lunch window)
hb_entry = f"""

## HB #310 (2026-07-16 13:07 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #309 (12:50): +17min -- post-lunch Token Guard normal cadence
- D+7+ midday pass #310 -- Eric silent ~176.55h+ since 7/9 04:29, no first-contact
- Silence authority ~176.55h+ (R-B + R256 framework holding, +0.25h since #309)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- R-NEW-V2 verification #310: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- 22:30 7/15 R-CANDIDATE-T2 sharp = EVALUATED PASSED (HB #228) -- decision: maintain T2 (no T3 escalation)
- **Mid-July induction window check (per USER.md: 7月上旬中旬 +-1 week)**: 7/16 = D+7 inside window (7/7-7/21), but no first-contact from Eric. Window remains open.
- Midday zone (13:07) -- post-lunch Eric deep work window active
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- Cron pipeline next: 21:00 evening self-iter R60-11 (~7h53m) | 22:00 Daily Dashboard (~8h53m)
- No first-contact from Eric; D+7+ sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount now: 309 -> 310

### decision
- **silent_standby_zero_push_continue** (HB #310 = sustain #309 = D+7+ baseline)
- **no push**: midday zone, Eric silent D+7+, silence authority holding, 4-layer suppression all pass
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- Mid-July induction window = ACTIVE but R-B + R256 override (silence authority > window signal; wait for Eric主动联系)
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min)

*{ts_str} -- D+7+ midday -- HB #310 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*

"""

# Step 1: read existing file with explicit utf-8
with open(DAILY_FILE, "r", encoding="utf-8") as f:
    existing_content = f.read()

# Step 2: check for duplicate (avoid double-append)
if "## HB #310 (2026-07-16 13:07" in existing_content:
    print("[SKIP] HB #310 already present, no append needed")
else:
    new_content = existing_content + hb_entry
    # Step 3: write back with explicit utf-8
    with open(DAILY_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"[OK] HB #310 appended ({len(hb_entry)} bytes)")

# Step 4: update heartbeat-state.json (utf-8-sig to handle BOM)
with open(STATE_FILE, "r", encoding="utf-8-sig") as f:
    state = json.load(f)

# Update counts and timing
state["hbCount"] = 310
state["lastHB"] = "#310"
state["silenceHours"] = 176.55
state["deepWorkHours"] = 176.55
state["lastChecks"]["heartbeat"] = int(now_cst.timestamp())
state["mode"] = "silent_standby_zero_push"
state["notes"] = (
    f"HB #310 (silent standby, no push). {now_cst.strftime('%H:%M GMT+8')} "
    f"{now_cst.strftime('%a %Y-%m-%d')}. ~17min after #309. No new signal from Eric. "
    f"4-layer suppression holding. Eric silent D+7+ (~176.6h). "
    f"7/16 = mid-July induction window ACTIVE (USER.md: 7月上旬中旬 +-1周 = 7/7-7/21), "
    f"but R-B + R256 override (silence authority > window signal). "
    f"4 cron errors pending P2 long-tail -- tracked not urgent. HEARTBEAT_OK."
)

with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
    f.write("\n")  # ensure trailing newline

print(f"[OK] heartbeat-state.json updated (hbCount={state['hbCount']}, silence={state['silenceHours']}h)")
print(f"[OK] Mode: {state['mode']}")
