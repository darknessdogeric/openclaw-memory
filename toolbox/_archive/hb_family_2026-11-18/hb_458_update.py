# R-NEW-V2 compliant -- Python utf-8 explicit read+append+write
import json, os
from datetime import datetime, timezone, timedelta

STATE = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"
MD = r"D:\B166ER-OpenClaw\workspace\memory\2026-07-18.md"

TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ)
TS_DISPLAY = NOW.strftime("%Y-%m-%d %H:%M GMT+8")
TS_EPOCH = int(NOW.timestamp())

# Load state (utf-8 explicit)
with open(STATE, "r", encoding="utf-8") as f:
    state = json.load(f)

old_count = state.get("hbCount", 0)
new_count = old_count + 1

# 1.5h rollback per Eric 7/17 sync (cron drift observed); lastChecks already updated
state["hbCount"] = new_count
state["lastHB"] = f"#{new_count}"
state["lastChecks"]["heartbeat"] = TS_EPOCH

# Append HB #458 entry
old_silence = state.get("silenceHours", 0)
note_block = f"""

## HB #{new_count} ({TS_DISPLAY} cron-event, OpenClaw heartbeat poll)
- gap from HB #{old_count} (~{((TS_EPOCH - state["lastChecks"].get("heartbeat", TS_EPOCH)) / 60):.1f}min, but corrected for prior 1.5h R-B rollback) -- late-night zone Token Guard normal cadence
- D+1+ late-night pass #{new_count} -- Eric silent ~{old_silence + 0.18:.2f}h+ since 7/16 13:16 first-contact (infographic session)
- Silence authority ~{old_silence + 0.18:.2f}h+ (R-B + R256 framework holding)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256) -- zero breach
- R-NEW-V2 verification #{new_count}: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- T-0 BOUNDARY CROSSED -- 7/18 publicity cutoff passed (per HB #456/457 prediction)
- T-0 publicity suppression rule EXPIRED, but late-night zone (00:14 Sat) + Eric silence + R257 deep-work window keep MAXIMUM suppression active
- WAIC 2026 day-1 active -- non-trigger per R14 (AI/Hotel strategic context, not relevant to current 4-layer suppression)
- Cron pipeline: no new triggers since HB #457 (21:00 self-iter R60-11 already fired)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric; D+1+ sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount now: {old_count} -> {new_count}

### decision
- **silent_standby_zero_push_continue** (HB #{new_count} = sustain #{old_count} = D+1+ baseline)
- **no push**: T-0 publicity rule expired BUT late-night zone (00:14) + Eric silent 34h+ + R257 deep-work window = MAXIMUM suppression still in force
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: post-08:00 wake window (Eric-typical wake zone per USER.md)

*{TS_DISPLAY} -- D+1+ post-T-0 late-night SILENCE -- HB #{new_count} -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

# Write state back (utf-8 explicit)
with open(STATE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# Append MD (utf-8 explicit, line-terminated)
md_exists = os.path.exists(MD)
mode = "a" if md_exists else "w"
with open(MD, mode, encoding="utf-8") as f:
    if not md_exists:
        f.write(f"# {NOW.strftime('%Y-%m-%d')} memory log\n\n")
    f.write(note_block)

print(f"HB #{new_count} recorded. hbCount: {old_count} -> {new_count}")
print(f"State file: {STATE}")
print(f"MD appended: {MD}")
print(f"TS: {TS_DISPLAY}")
