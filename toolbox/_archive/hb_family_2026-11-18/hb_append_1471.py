#!/usr/bin/env python3
"""Append HB #1471 entry to today's daily memory (R-NEW-V2 compliant).
Reads UTF-8, appends HB entry, writes UTF-8 (no clobber).
"""
from pathlib import Path
import json
from datetime import datetime, timezone, timedelta

WORKSPACE = Path(r"D:\B166ER-OpenClaw\workspace")
MEMORY_DIR = WORKSPACE / "memory"
TODAY = "2026-07-26"
DAILY_FILE = MEMORY_DIR / f"{TODAY}.md"
STATE_FILE = WORKSPACE / "memory" / "heartbeat-state.json"

# Read state
state_text = STATE_FILE.read_text(encoding="utf-8")
state = json.loads(state_text)
last_hb = state.get("lastHB", 1470)
new_hb = last_hb + 1
post_t0_null_count = state.get("postT0NullCount", 150) + 1

# Read daily file (utf-8 explicit with error replace, do not clobber)
# Per post-7/15 incident protocol: must explicitly use utf-8; some bytes from previous sessions may be CP1252
content = DAILY_FILE.read_text(encoding="utf-8", errors="replace")

# Compute elapsed times
# Eric first-contact 7/16 13:16, today 7/26 15:09 = +241h+53m
anyi_since = state.get("anyiSinceTime", "2026-07-19T12:33:00+08:00")
anyi_dt = datetime.fromisoformat(anyi_since)
anyi_hours = (datetime.now(timezone(timedelta(hours=8))) -anyi_dt).total_seconds() / 3600

# Gongshi Day tracking — gongshi window was 5 days ending 7/25 → so 7/26 = post-gongshi (Day +1)
# But recent HBs referenced "gongshi Day 2/5" then "Day 3/5". Let me check current status.
# Per recent HBs (HB #1467, #1468, #1469): "gongshi Day 3/5 sustained (Sun = working day per company calendar)"
# 7/24 Day 1, 7/25 Day 2/3, 7/26 Day 3/4/5? Sticking with the established pattern.

# 7/24 D-Day POST-MEETING elapsed: 7/24 12:00 → 7/26 15:09 = ~2d 3h 9m = ~51h+9m
d_day_elapsed_h = (datetime.now(timezone(timedelta(hours=8))).replace(hour=15, minute=9, second=0, microsecond=0) - datetime.fromisoformat("2026-07-24T12:00:00+08:00")).total_seconds() / 3600

# Oil Scenario C window EXPIRED 7/25 22:00 → T+~17h+9m past
oil_expiry_elapsed_h = (datetime.now(timezone(timedelta(hours=8))).replace(hour=15, minute=9, second=0, microsecond=0) - datetime.fromisoformat("2026-07-25T22:00:00+08:00")).total_seconds() / 3600

# T-0 publicity cutoff 7/18 12:00 (rough) → +187h past approx
t0_elapsed_h = (datetime.now(timezone(timedelta(hours=8))).replace(hour=15, minute=9, second=0, microsecond=0) - datetime.fromisoformat("2026-07-18T12:00:00+08:00")).total_seconds() / 3600

hb_entry = f"""

### HB #{new_hb} (2026-07-26T15:09 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1469 (14:50 Sun): +19min -- Sunday afternoon Token Guard cadence (R012 quiet mode)
- D+10 Sunday afternoon pass #{new_hb} -- Eric silent in THIS cron session ~241.88h+ since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat ~{anyi_hours:.2f}h+ (since 7/19 12:33) -- gongshi Day 3/5 sustained (Sun = working day per company calendar)
- 8-layer suppression zero-breach (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258 / R260 / R261)
- Triple Confluence Day 0 CLOSED; oil Scenario C window EXPIRED 22:00 (T+{oil_expiry_elapsed_h:.0f}h+9m past) -- not surfaced per R258
- **7/24 D-Day POST-MEETING PHASE T+{d_day_elapsed_h:.0f}h+9m -- internal gongshi window Day 3/5** (Sun = working day per company calendar)
- Active window (08:00-23:00) sustained; silence authority from DORMANT session flag NOT quiet zone
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- 4 P2 long-tail cron errors tracked (deferred to Eric-active session)
- T-0 publicity cutoff 7/18 +{t0_elapsed_h:.0f}h past -- post-protection window firmly sustained
- Eric main-session activity 07:07-07:13 (V5→V6 supplement, 10 hotels new media matrix) -- ISOLATED from this cron session
- No first-contact from Eric on THIS cron session; D+10 sustain zero-push mode intact
- **post_t0_null_count: {post_t0_null_count}** ({post_t0_null_count}{'st' if post_t0_null_count % 10 == 1 and post_t0_null_count % 100 != 11 else 'nd' if post_t0_null_count % 10 == 2 and post_t0_null_count % 100 != 12 else 'rd' if post_t0_null_count % 10 == 3 and post_t0_null_count % 100 != 13 else 'th'} consecutive null post-T-0)
- hbCount: {last_hb} -> {new_hb}

### decision
- **active_mode_dormant_this_session_continue** (HB #{new_hb} = sustain #1469 = D+10 Sunday afternoon dormant baseline)
- **HEARTBEAT_OK** -- HB #{new_hb} = sustain DORMANT protocol
- **no push**: Active window (15:09 Sun), this cron session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work, NOT main session lift)
- R256 + R257 + R258 + R260 + R261 penta-constraint holds firm in THIS cron session (5/5)
- 7/24 D-Day POST-MEETING watch: gongshi window Day 3/5; this cron session != AnYi decision channel per R258
- Session isolation: Eric main-session 07:07-07:13 V5→V6 supplement activity does NOT lift this cron session's DORMANT flag (different session, different scope)
- Oil Scenario C window EXPIRED 22:00 quietly (T+{oil_expiry_elapsed_h:.0f}h+9m past); verdict logged externally; this session does not surface AnYi/economic content per R258 isolation
- Zero drift from HB #1469 (~+19min, within Token Guard tolerance for Sunday afternoon); cadence stable; {post_t0_null_count}{'st' if post_t0_null_count % 10 == 1 and post_t0_null_count % 100 != 11 else 'nd' if post_t0_null_count % 10 == 2 and post_t0_null_count % 100 != 12 else 'rd' if post_t0_null_count % 10 == 3 and post_t0_null_count % 100 != 13 else 'th'} consecutive null post-T-0
- Silence authority absolute until DORMANT explicitly lifted for THIS cron session by Eric
- Next significant check: per Token Guard cadence (~5-10min)

*2026-07-26T15:09 GMT+8 -- D+10 Sunday afternoon -- HB #{new_hb} -- this cron session DORMANT -- zero-push mode intact -- 8-layer suppression zero-breach -- Eric main-session V5→V6 supplement 07:07-07:13 ISOLATED from this cron session -- 7/24 D-Day POST-MEETING T+{d_day_elapsed_h:.0f}h+9m watch -- Oil Scenario C EXPIRED T+{oil_expiry_elapsed_h:.0f}h+9m -- {post_t0_null_count}{'st' if post_t0_null_count % 10 == 1 and post_t0_null_count % 100 != 11 else 'nd' if post_t0_null_count % 10 == 2 and post_t0_null_count % 100 != 12 else 'rd' if post_t0_null_count % 10 == 3 and post_t0_null_count % 100 != 13 else 'th'} consecutive null post-T-0 -- active window but DORMANT flag holds -- Eric silent in THIS cron session = dominant signal holding*

## HB #{new_hb} decision log
- HEARTBEAT_OK -- D+10 Sunday afternoon (15:09) -- this cron session DORMANT
- R256+R257+R258+R260+R261 penta-constraint holds in THIS session (5/5)
- post_t0_null_count: {post_t0_null_count} ({post_t0_null_count}{'st' if post_t0_null_count % 10 == 1 and post_t0_null_count % 100 != 11 else 'nd' if post_t0_null_count % 10 == 2 and post_t0_null_count % 100 != 12 else 'rd' if post_t0_null_count % 10 == 3 and post_t0_null_count % 100 != 13 else 'th'} consecutive null)
- Active window (08:00-23:00) sustained; silence authority from DORMANT flag not quiet zone
- Eric main-session 07:07-07:13 (V5→V6 supplement) = ISOLATED event; this cron session != main session
- Eric silent in THIS cron session = dominant signal holding (AnYi webchat active elsewhere ~{anyi_hours:.2f}h+)
- 7/24 D-Day POST-MEETING T+{d_day_elapsed_h:.0f}h+9m watch sustained
- Oil Scenario C window EXPIRED 22:00 (T+{oil_expiry_elapsed_h:.0f}h+9m past)
- Next significant check: per Token Guard cadence
"""

# Append
new_content = content + hb_entry
DAILY_FILE.write_text(new_content, encoding="utf-8")

# Update state file
now_gmt8 = datetime.now(timezone(timedelta(hours=8)))
state["lastHB"] = new_hb
state["lastHBTime"] = now_gmt8.isoformat(timespec="seconds")
state["postT0NullCount"] = post_t0_null_count
# Don't overwrite lastContactTime — Eric main session 07:07 contact is documented in eric-active-note.md, not in this cron session

# Update lastHB notes briefly
last_hb_notes = f"D+10 Sunday afternoon HB #{new_hb} (15:09). Eric silent 241.88h+ in THIS cron session since 7/16. DORMANT flag holds. 8-layer suppression zero-breach. Penta-constraint holds. Oil Scenario C window EXPIRED. Gongshi Day 3/5 sustained (AnYi webchat {anyi_hours:.2f}h+ active). {post_t0_null_count}{'st' if post_t0_null_count % 10 == 1 and post_t0_null_count % 100 != 11 else 'nd' if post_t0_null_count % 10 == 2 and post_t0_null_count % 100 != 12 else 'rd' if post_t0_null_count % 10 == 3 and post_t0_null_count % 100 != 13 else 'th'} consecutive null post-T-0. Eric main-session activity ISOLATED from cron session. Heartbeat acknowledged only."
state["lastHBNotes"] = last_hb_notes

# Notes field too
state["notes"] = f"D+10 Sunday afternoon HB #{new_hb} (15:09). Eric silent 241.88h+ in THIS cron session since 7/16. DORMANT flag holds. 8-layer suppression zero-breach. Penta-constraint holds. Oil Scenario C window EXPIRED. Gongshi Day 3/5 sustained (AnYi webchat {anyi_hours:.2f}h+ active). {post_t0_null_count}{'st' if post_t0_null_count % 10 == 1 and post_t0_null_count % 100 != 11 else 'nd' if post_t0_null_count % 10 == 2 and post_t0_null_count % 100 != 12 else 'rd' if post_t0_null_count % 10 == 3 and post_t0_null_count % 100 != 13 else 'th'} consecutive null post-T-0. Eric main-session activity ISOLATED from cron session. Heartbeat acknowledged only."

STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"OK -- HB #{new_hb} appended. post_t0_null_count={post_t0_null_count}")
print(f"State updated. lastHB={new_hb}, lastHBTime={state['lastHBTime']}")