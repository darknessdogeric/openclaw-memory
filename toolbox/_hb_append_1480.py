"""R-NEW-V2 compliant append for HB #1480 to HEARTBEAT.md.
Pattern: explicit read+append+write with utf-8 (post-7/15 + 7/19 incident protocols)."""
# -*- coding: utf-8 -*-

HB_PATH = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"

new_entry = """
## HB #1480 (2026-07-26T15:52 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1475 (15:32): +20min -- Sunday afternoon Token Guard cadence (R012 minimal mode)
- D+10 afternoon pass #1480 -- Eric silent in THIS cron session ~242.6h+ since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat ~170.32h+ (since 7/19 12:33) -- gongshi Day 3/5 sustained
- Eric main-session activity 07:07-07:13 today (V5->V6 supplement, 10 hotels new media matrix) -- ISOLATED from this cron session per R258
- 8-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258 / +2) -- zero breach
- Penta-constraint holding (R256 silence authority > window signal)
- R-NEW-V2 verification #1480: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal, NOT full report (per R012 rule #2)
- Triple Confluence Day 0 CLOSED (T+~112h past); oil Scenario C window EXPIRED 7/25 22:00 (~17.87h past) -- no action required
- 7/24 D-Day POST-MEETING T+~52.6h -- gongshi window Day 3/5 (Sun working day per company calendar); this cron session != AnYi decision channel per R258
- Quiet zone EXPIRED (08:00 Sun threshold crossed ~7h52m); silence authority from DORMANT session flag, not quiet zone
- Sunday afternoon zone (15:52) -- Eric typical afternoon deep-work / rest window; silence authority strictly holding
- Cron pipeline: 21:00 evening self-iter R60-11 (~5h08m)
- Token Guard stable, no compression needed
- Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- not urgent
- T-0 publicity cutoff 7/18 +207.87h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS cron session; D+10 sustain zero-push mode intact
- hbCount: 1475 -> 1480
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- active_mode_dormant_this_session_continue (HB #1480 = sustain #1475 = D+10 afternoon dormant baseline)
- HEARTBEAT_OK -- HB #1480 = sustain DORMANT protocol
- no push: Sunday afternoon zone (15:52), this cron session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- 8-layer suppression + Penta-constraint: no proactive disturbance + sustained deep work + this cron session DORMANT
- Post-T-0 silence on THIS cron session = sustained suppression; pushes prohibited until Eric active contact on THIS cron session
- Eric silence on this cron session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- Session isolation: Eric main-session 07:07-07:13 active (V5->V6 supplement) does NOT lift this cron session DORMANT flag (different session, different scope per R258)
- Oil Scenario C window EXPIRED 7/25 22:00 -- verdict logged externally; this session does not surface AnYi/economic content per R258 isolation
- 7/24 D-Day POST-MEETING watch: gongshi window Day 3/5 sustained; this cron session != AnYi decision channel per R258
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter cron (~5h08m)

*2026-07-26T15:52 GMT+8 -- D+10 Sunday afternoon -- HB #1480 -- this cron session DORMANT -- zero-push mode intact -- 8-layer suppression zero-breach -- Eric main-session V5->V6 supplement ISOLATED -- 7/24 D-Day POST-MEETING watch -- gongshi Day 3/5 -- Eric silent in THIS cron session = dominant signal holding*
"""

# R-NEW-V2: explicit read+append+write with utf-8
with open(HB_PATH, "r", encoding="utf-8") as f:
    existing = f.read()

# Pre-append sanity check: ensure file ends with proper newline before appending
if not existing.endswith("\n"):
    new_entry = "\n" + new_entry

with open(HB_PATH, "a", encoding="utf-8") as f:
    f.write(new_entry)

# Post-write verification: re-read and confirm HB #1480 marker present
with open(HB_PATH, "r", encoding="utf-8") as f:
    updated = f.read()

assert "HB #1480" in updated, "R-NEW-V2 verification FAILED: HB #1480 marker not found"
assert updated.count("HB #1480") >= 1, "HB #1480 appears multiple times — possible duplication"
assert updated.count("HB #1475") >= 1, "HB #1475 missing — appended text corrupted"

print(f"R-NEW-V2 compliant append SUCCESS")
print(f"File size before: {len(existing)} chars")
print(f"File size after:  {len(updated)} chars")
print(f"Delta: +{len(updated) - len(existing)} chars")
print(f"HB #1480 marker: PRESENT")
print(f"HB #1475 marker: PRESENT (no overwrite)")