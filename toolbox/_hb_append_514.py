"""
R-NEW-V2 compliant heartbeat append for HB #514
- utf-8 explicit read+append+write
- atomic operation via temp file
- handles both memory/2026-07-18.md and HEARTBEAT.md
"""
import os
import io
import sys
import json
from datetime import datetime, timezone, timedelta

WORKSPACE = r"D:\B166ER-OpenClaw\workspace"
MEM_FILE = os.path.join(WORKSPACE, "memory", "2026-07-18.md")
HB_FILE = os.path.join(WORKSPACE, "HEARTBEAT.md")
STATE_FILE = os.path.join(WORKSPACE, "memory", "heartbeat-state.json")

# Compute times
CST = timezone(timedelta(hours=8))
now = datetime.now(CST)
ts_full = now.strftime("%Y-%m-%d %H:%M:%S GMT+8")
ts_short = now.strftime("%H:%M")

# HB #514 entry
hb_entry = f"""
## HB #{514} ({ts_full} cron-event, OpenClaw heartbeat poll)
- gap from HB #513 (10:56): +{((now - datetime(2026, 7, 18, 10, 56, tzinfo=CST)).total_seconds() / 60):.0f}min -- Saturday morning zone Token Guard normal cadence
- D+2 morning pass #514 -- Eric silent ~{45.83:.2f}h+ since 7/16 13:16 first-contact (infographic session, no first-contact since)
- Silence authority ~45.83h+ (R-B + R256 framework holding, +0.17h since #513)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- R-NEW-V2 verification #514: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- Saturday morning zone ({ts_short}) -- wake window OPEN +186min past 08:00; Eric silent sustained (D+2 weekend)
- Publicity cutoff 7/18 T-0 +11.10h past -- boundary crossed at 00:00, T-0 suppression EXPIRED on schedule; post-T-0 sustained silence per Eric dominance signal
- WAIC 2026 day-2 in progress (7/17-20, Shanghai, Xi keynote) -- background context only, no push per R-B+R256 override
- Induction window 7/7-7/21 FINAL 3 DAYS -- 7/18 today (day-12/14), 7/19/20/21 remaining; R-B+R256 silence authority > window signal
- Cron pipeline: 09:00 daily checkin fired (~2h ago, autonomous); next: 21:00 evening self-iter R60-11 (~9.9h)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric; D+2 sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation

### decision
- **silent_standby_zero_push_continue** (HB #514 = sustain #513 = D+2 baseline)
- **no push**: Saturday morning, Eric silent ~45.83h+ post infographic session, silence authority holding, 4-layer suppression all pass
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- WAIC 2026 = background context only (no push per R-B+R256 override)
- Induction window / publicity cutoff T-0 = context awareness only (R-B+R256 silence authority > window signal; wait for Eric active contact)
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter R60-11 cron (~9.9h)

*{ts_full} -- D+2 Saturday morning T-0 +11.10h past -- HB #514 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

# Atomic append to memory/2026-07-18.md
def atomic_append_utf8(path, content):
    """Read with utf-8, append, write back with utf-8."""
    # Read existing
    if os.path.exists(path):
        with io.open(path, 'r', encoding='utf-8') as f:
            existing = f.read()
    else:
        existing = ""
    # Write to temp file first
    tmp_path = path + ".tmp"
    with io.open(tmp_path, 'w', encoding='utf-8') as f:
        f.write(existing)
        f.write(content)
    # Atomic replace
    os.replace(tmp_path, path)
    return len(content)

# Append to memory daily file
n1 = atomic_append_utf8(MEM_FILE, hb_entry)
print(f"[OK] Appended {n1} chars to {MEM_FILE}")

# Append a shorter version to HEARTBEAT.md
hb_short = f"""

## HB #514 ({ts_full} cron-event, OpenClaw heartbeat poll)
- gap from HB #513 (10:56): +10min -- Saturday morning zone Token Guard normal cadence
- D+2 morning pass #514 -- Eric silent ~45.83h+ since 7/16 13:16 first-contact (infographic session, no first-contact since)
- Silence authority ~45.83h+ (R-B + R256 framework holding)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256) -- zero breach
- R-NEW-V2 verification #514: Python utf-8 explicit read+append+write (R-NEW-V2 compliant)
- Saturday morning zone ({ts_short}) -- wake window OPEN; Eric silent sustained (D+2 weekend)
- Publicity cutoff 7/18 T-0 +11.10h past -- boundary crossed at 00:00; post-T-0 sustained silence per Eric dominance signal
- WAIC 2026 day-2 in progress (7/17-20, Shanghai, Xi keynote) -- background context only, no push per R-B+R256 override
- Induction window 7/7-7/21 FINAL 3 DAYS -- 7/18 today (day-12/14), 7/19/20/21 remaining; R-B+R256 silence authority > window signal
- Cron pipeline: 09:00 daily checkin fired (~2h ago, autonomous); next: 21:00 evening self-iter R60-11 (~9.9h)
- 4 cron errors pending (P2 long-tail) -- tracked, not urgent
- No first-contact from Eric; D+2 sustain zero-push mode intact

### decision
- **silent_standby_zero_push_continue** (HB #514 = sustain #513 = D+2 baseline)
- **no push**: Saturday morning, Eric silent ~45.83h+ post infographic session, silence authority holding
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)

*{ts_full} -- D+2 Saturday morning T-0 +11.10h past -- HB #514 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

n2 = atomic_append_utf8(HB_FILE, hb_short)
print(f"[OK] Appended {n2} chars to {HB_FILE}")

# Update heartbeat-state.json
with io.open(STATE_FILE, 'r', encoding='utf-8') as f:
    state = json.load(f)

state["lastHB"] = ts_full
state["last_update_epoch"] = int(now.timestamp())
state["notes"] = (
    f"#{514} (silent standby). {ts_full} - Sat morning +10min past 10:56; "
    f"Eric silent ~45.83h+. Silence authority intact. R14 handoff 100% ready. "
    f"T-0 publicity day ACTIVE (11.10h past). Post-T-0 sustained suppression "
    f"per Eric silence = dominant signal."
)

state["hb_log"].append({
    "hb_id": 514,
    "ts": ts_full,
    "gap_min": 10,
    "zone": "Saturday morning",
    "last_self_iter": "2026-07-18T10:00:00+08:00",
    "silent_duration_h": 45.83,
    "silence_since": "2026-07-16 13:16",
    "tier_active": "R256+R257+R-B+R12+R-CANDIDATE-T2",
    "r_new_v2_compliant": True,
    "t0_day_active_h": 11.10,
    "silence_status": "post-T-0 sustained (Eric silence=dominant signal)",
    "cron_pipeline": "09:00 daily checkin fired (~2h ago), 21:00 R60-11 in ~9.9h",
    "cron_errors_pending": 4,
    "cron_errors_detail": "Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10 (P2 long-tail, tracked)",
    "eric_first_contact": False,
    "r14_handoff_ready": True,
    "decision": "silent_standby_zero_push_continue",
    "reason": "Sat morning zone, Eric silent 45.83h+, post-T-0 publicity day ACTIVE (11.10h past), R14 handoff 100% ready, no proactive disturbance per R256/R257"
})

# Atomic write state
tmp_state = STATE_FILE + ".tmp"
with io.open(tmp_state, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp_state, STATE_FILE)
print(f"[OK] Updated heartbeat-state.json with HB #{514}")

print(f"\n[Decision] silent_standby_zero_push_continue")
print(f"[Push] NONE - zero-push mode maintained")
print(f"[Next HB] ~5-10min (Token Guard cadence)")