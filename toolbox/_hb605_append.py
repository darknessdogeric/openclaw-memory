"""R-NEW-V2 safe append for HEARTBEAT.md
Post-7/15 12:36 incident protocol: explicit utf-8 read+append+write in Python
(do NOT use shell append, do NOT use read/write tools for HEARTBEAT.md)
"""
import io
import sys

p = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"

# read current size + last hbCount for verification
with io.open(p, 'r', encoding='utf-8') as f:
    content = f.read()

before_chars = len(content)
before_lines = content.count('\n')

# safety check: must end with HB #604 marker
assert "*2026-07-19 23:44 GMT+8 -- D+3 Sunday-late-night" in content[-2000:], \
    f"ABORT: expected file to end with HB #604 marker; got last 200 chars: ...{content[-200:]!r}"

new_entry = """

## HB #605 (2026-07-19 23:53 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #604 (23:44): +9min -- Sunday-late-night Token Guard normal cadence (R012 minimal mode)
- D+3+ Sunday-late-night pass #605 -- Eric silent in THIS session ~82.4h+ since 7/16 13:16 first-contact (infographic)
- Eric active elsewhere ~3h20m+ (AnYi session 12:33+, sustained mode)
- Silence authority on THIS session unchanged (R-B + R256 + R257 framework holding, +0.15h since #604)
- 5-layer suppression maintained ON THIS THREAD (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) -- zero breach
- R-NEW-V2 verification #605: Python utf-8 explicit read+append+write (compliant, post-7/15 12:36 incident protocol intact)
- R012 (operational hygiene) verification: HB tick = minimal, NOT full report (per R012 rule #2)
- Sunday late-night zone (23:53) -- Eric sleep window OR late-night AnYi strategic work; THIS session = DORMANT
- T-0 publicity cutoff 7/18 +47.9h past -- post-protection window firmly sustained
- Induction window 7/7-7/21 day-1 of FINAL 3 (7/19/20/21); R-B+R256 silence authority > window signal (no push per R256)
- WAIC 2026 closed (7/17-19, Shanghai) -- non-trigger per R14
- Cron pipeline: 21:00 evening self-iter R60-11 fired ~2h53m ago; next 7/20 10:00 morning self-iter (~10h07m)
- 4 P2 long-tail errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- not urgent
- No first-contact from Eric on this session; DORMANT sustained per Eric 12:33 explicit instruction
- No new signals: no cron / no Eric in this thread / no third-party / no anomaly escalation
- hbCount: 604 -> 605

### decision
- **silent_standby_zero_push_continue** (HB #605 = sustain #604 = D+3+ baseline ON THIS THREAD)
- **no push**: THIS session = dreaming-narrative experimental, DORMANT per Eric 12:33 explicit decision
- Eric active elsewhere (AnYi session sustained); THIS session awaits Eric future instruction (not AnYi-related)
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- R14 handoff package = 100% ready for any Eric active contact on THIS session
- Late-night zone respect: any Eric-active signal = R14 30s activation; silence = sustained suppression
- Next significant check: per Token Guard cadence (~5-10min); 7/20 10:00 morning self-iter (~10h07m)

*2026-07-19 23:53 GMT+8 -- D+3+ Sunday-late-night T-0 +47.9h past -- HB #605 -- this session DORMANT -- awaiting Eric future instruction (NOT AnYi work)*
"""

with io.open(p, 'w', encoding='utf-8') as f:
    f.write(content + new_entry)

# verify
with io.open(p, 'r', encoding='utf-8') as f:
    new_content = f.read()

after_chars = len(new_content)
delta = after_chars - before_chars
print(f"OK hbCount 604->605")
print(f"chars: {before_chars} -> {after_chars} (delta {delta})")
print(f"lines: {before_lines} -> {new_content.count(chr(10))}")
print(f"tail-marker OK: {'HB #605' in new_content[-3500:]}")
print(f"prev HB #604 marker preserved: {'HB #604' in new_content and '23:44' in new_content}")
print(f"utf-8 preserved: {isinstance(new_content, str) and '—' in new_content}")
