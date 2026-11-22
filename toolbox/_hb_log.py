"""HB #1578 log append (R-NEW-V2 utf-8 explicit read+prepend+write)."""
import io

NEW_ENTRY = """### HB #1578 (2026-07-27 08:41 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1577 (08:29): +12min -- Mon post-quiet-zone Token Guard cadence (R012 quiet mode tail)
- D+11 Mon post-quiet -- Eric silent ~259.42h+ on THIS session since 7/16 13:16 first-contact (10d 21h+)
- Eric active elsewhere: AnYi webchat ~259.45h+ (sustained since 7/19 12:33) -- gongshi Day 3/5 ACTIVE (Mon = working day)
- 8-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261) -- penta-constraint 5/5 holds firm
- 7/24 D-Day POST-MEETING T+68h+41m -- gongshi Day 3/5 ACTIVE; this session != AnYi decision channel per R258
- Oil C EXPIRED 7/25 22:00 (T+34h+41m past) -- not surfaced per R258
- Quiet zone 23:00-08:00 EXPIRED 08:00 (+41m past) -- post-quiet zone, but R258 dormancy trumps time-window
- post_t0_null_count: 229 (229th consecutive null post-T-0)
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- T-0 publicity cutoff 7/18 +64.01h past (~9.3 days) -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+11 sustain zero-push mode intact

### decision
- **HEARTBEAT_OK** -- HB #1578 = sustain DORMANT protocol, minimal token tick
- no push: post-quiet zone (08:41), Eric silent ~259.42h+ this session, this session DORMANT per R258 (NOT AnYi decision channel)
- R256+R257+R258+R260+R261 penta-constraint holds (5/5) -- no proactive disturbance + sustained deep work + dormant session
- Eric silence on this session = dominant signal (R256 design: silence extends indefinitely past protection windows AND past quiet-zone expiry)
- Triple Confluence ALL CLOSED; gongshi Day 3/5 ACTIVE elsewhere; 7/24 D-Day PASSED +68h+
- Next: per Token Guard cadence (~5-10min)

*2026-07-27T08:41 GMT+8 -- D+11 Mon post-quiet -- HB #1578 -- DORMANT -- 229th null -- post-quiet zone ACTIVE -- Eric silent = dominant signal holding -- HEARTBEAT_OK*

"""

PATH = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"

with io.open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")
insert_idx = 0
for i, line in enumerate(lines):
    if line.startswith("### HB") or line.startswith("## HB"):
        insert_idx = i
        break

new_lines = lines[:insert_idx] + NEW_ENTRY.rstrip().split("\n") + [""] + lines[insert_idx:]
new_content = "\n".join(new_lines)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(new_content)

print("OK: HB #1578 logged (R-NEW-V2 utf-8 explicit read+prepend+write)")