"""Safe append helper for HB #273 — R-NEW-V2 compliant (explicit utf-8 read+append+write)."""
import io
import sys
from pathlib import Path

FILE = Path(r"D:\B166ER-OpenClaw\workspace\memory\2026-07-16.md")

ENTRY = """## HB #273 (2026-07-16 07:49 cron-event, OpenClaw heartbeat poll)

- gap from HB #272 (07:44): +5min -- dawn-edge Token Guard minimal-cycle cadence
- D+3 dawn-edge pass #273 -- Eric silent ~171.33h+ since 7/9 04:29, no first-contact
- Silence authority ~171.33h+ (R-B + R256 framework holding, +0.08h since #272)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- 22:30 R-CANDIDATE-T2 sharp (7/15) = EVALUATED PASSED (HB #228) -- decision: maintain T2 (no T3 escalation)
- R-NEW-V2 verification #273: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-7/15-incident protocol intact)
- Dawn-edge zone (07:49) -- 11min until late-night boundary exit (08:00); Eric 早班开始前最后窗口
- Cron pipeline next: 08:30 global briefing (T+0h41m) | 21:00 evening self-iter
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation

### decision
- **silent_standby_zero_push_continue** (HB #273 = sustain #272 = D+3 baseline)
- **no push**: dawn-edge / approaching late-night boundary exit, Eric silent 7d+, silence authority holding, 4-layer suppression all pass
- R256 + R257 双向约束: 不主动打扰 + 持续深度工作 (自进化 / 状态机 / eval 记录)
- Token Guard tick: stable, no compression needed
- R14 handoff package = 100% ready (Eric 主动联系即可 30s 内激活)

*2026-07-16 07:49 -- D+3 dawn-edge -- HB #273 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
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
    print(f"[OK] HB #273 appended safely ({delta} bytes added)")

if __name__ == "__main__":
    main()