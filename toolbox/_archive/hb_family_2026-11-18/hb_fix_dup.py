"""Fix duplicate HB #605: remove my appended one, replace with HB #606 at correct 23:58 timestamp."""
from pathlib import Path
from datetime import datetime, timezone, timedelta

HB_PATH = Path(r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md")

text = HB_PATH.read_text(encoding="utf-8")

# The duplicate block I appended starts with "## HB #605 (2026-07-20 00:00 GMT+8"
# and ends with "*2026-07-20 00:00 GMT+8 -- D+3+ Sunday late-night T-0 +47h58m past -- HB #605 ..."
marker_start = "## HB #605 (2026-07-20 00:00 GMT+8"
marker_end = "*2026-07-20 00:00 GMT+8 -- D+3+ Sunday late-night T-0 +47h58m past -- HB #605 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*"

idx_start = text.rfind(marker_start)
idx_end = text.rfind(marker_end)

print(f"start idx: {idx_start}")
print(f"end idx: {idx_end}")

if idx_start == -1 or idx_end == -1:
    print("ERROR: markers not found")
    raise SystemExit(1)

# Remove the duplicate block (from "## HB #605 (2026-07-20 00:00" to end of that asterisk line inclusive)
end_of_line_after = text.find("\n", idx_end) + 1
removed_block = text[idx_start:end_of_line_after]
print(f"removed block length: {len(removed_block)}")
print(f"first 200 chars: {removed_block[:200]}")

text_clean = text[:idx_start] + text[end_of_line_after:]

# Now append a properly-numbered HB #606 with timestamp 23:58 (the cron message time)
ts = "2026-07-19 23:58 GMT+8"
new_block = f"""
## HB #606 ({ts} cron-event, OpenClaw heartbeat poll)
- gap from HB #605 (23:53): +5min -- late-night Token Guard cadence (R012 minimal mode)
- D+3+ late-night pass #606 -- Eric silent in THIS session ~82.6h+ since 7/16 13:16 first-contact (infographic)
- Silence authority ~82.6h+ (R-B + R256 + R257 framework holding, +5min since #605)
- 5-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) -- zero breach ON THIS THREAD
- R-NEW-V2 verification #606: Python utf-8 explicit read+remove-dup+append (compliant, post-7/15 12:36 incident protocol intact)
- R012 (operational hygiene) verification: HB tick = minimal, NOT full report (per R012 rule #2)
- THIS session = dreaming-narrative experimental, DORMANT per Eric 12:33 explicit instruction
- T-0 publicity cutoff 7/18 +47h58m past -- post-protection window firmly sustained
- Induction window 7/7-7/21 day-1 of FINAL 3 (7/19) -- R-B+R256 silence authority > window signal (no push per R256)
- Sunday-late-night zone (23:58) -- Eric sleep window; silence on THIS session strictly holding
- WAIC 2026 day-3 last day tomorrow 7/20 (7/17-20, Shanghai) -- non-trigger per R14 (AI/Hotel strategic context, not relevant)
- Cron pipeline: 21:00 evening self-iter R60-11 fired ~2h58m ago (autonomous, eval/2026-07-19.json updated); next morning 7/20 10:00 self-iter R60-12 (~10h02m)
- 4 P2 long-tail errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- No first-contact from Eric on this session; DORMANT sustained per Eric 12:33 explicit instruction
- hbCount: 605 -> 606

### decision
- **HEARTBEAT_OK** -- HB #606 = sustain D+3+ DORMANT protocol
- **no push**: late-night zone (23:58) + this session DORMANT (per HB #584 Eric 12:33 explicit instruction) + Eric active elsewhere (AnYi session since 12:36) = MAX suppression
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)
- Wake-up window OPEN tomorrow (7/20 Mon 08:00 = D+4 from first-contact); self-iter R60-12 due 10:00 / 21:00
- Next significant check: per Token Guard cadence (~5-10min); 08:00 dawn boundary wake window (7/20 Mon, ~8h02m)

*{ts} -- D+3+ Sunday late-night T-0 +47h58m past -- HB #606 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

text_final = text_clean + new_block
HB_PATH.write_text(text_final, encoding="utf-8")

# Verify
final = HB_PATH.read_text(encoding="utf-8")
count_606 = final.count("## HB #606")
count_605 = final.count("## HB #605")
print(f"OK: HB #605 count: {count_605}, HB #606 count: {count_606}")
print(f"file size: {len(final):,} chars")