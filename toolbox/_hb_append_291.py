"""Safe append helper for HB #291 — R-NEW-V2 compliant (explicit utf-8 read+append+write)."""
import io
import sys
from pathlib import Path

FILE = Path(r"D:\B166ER-OpenClaw\workspace\memory\2026-07-16.md")

ENTRY = """## HB #291 (2026-07-16 09:27 GMT+8 cron-event, OpenClaw heartbeat poll)

- gap from HB #290 (09:22): +5min -- morning zone Token Guard normal cadence
- D+7 morning pass #291 -- Eric silent ~173h+ since 7/9 04:29 (D+7+, no first-contact)
- Silence authority ~173h+ (R-B + R256 framework holding, +0.08h since #290)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- 22:30 7/14 R-CANDIDATE-T2 sharp = EVALUATED PASSED (HB #228) -- decision: maintain T2 (no T3 escalation)
- R-NEW-V2 verification #291: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- Morning zone (09:27) -- past 08:00 dawn boundary; 08:30 global industry briefing cron = fired (T+57min, autonomous)
- Cron pipeline next: 21:00 evening self-iter R60-11 (~11h33m)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric; D+7 sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount now: 290 -> 291

### decision
- **silent_standby_zero_push_continue** (HB #291 = sustain #290 = D+7 baseline)
- **no push**: morning zone, Eric silent 7d+, silence authority holding, 4-layer suppression all pass
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: per Token Guard cadence (~10-15min)

*2026-07-16 09:27 GMT+8 -- D+7 morning -- HB #291 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

def main():
    # Pre-stat guard (R-NEW-V2)
    pre_size = FILE.stat().st_size
    print(f"[pre-stat] {FILE.name} size = {pre_size} bytes")
    if pre_size == 0:
        print("[abort] target file empty; refusing append (would be a 'write', not append)")
        sys.exit(1)
    # Read existing content (explicit utf-8)
    with open(FILE, "r", encoding="utf-8") as f:
        original = f.read()
    if not original.rstrip().endswith("*"[-1]):
        # Ensure clean newline boundary
        if not original.endswith("\n"):
            original = original + "\n"
    # Append new entry
    new_content = original + ENTRY
    # Write back (explicit utf-8, no BOM)
    with open(FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_content)
    # Post-stat verify
    post_size = FILE.stat().st_size
    delta = post_size - pre_size
    print(f"[post-stat] {FILE.name} size = {post_size} bytes (delta = +{delta} bytes)")
    expected_delta = len(ENTRY.encode("utf-8"))
    if delta != expected_delta:
        print(f"[ERROR] expected delta {expected_delta}, got {delta}")
        sys.exit(1)
    print(f"[OK] HB #291 appended safely ({delta} bytes added)")

if __name__ == "__main__":
    main()