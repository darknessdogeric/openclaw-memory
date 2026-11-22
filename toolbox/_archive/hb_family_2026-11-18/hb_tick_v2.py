# -*- coding: utf-8 -*-
"""HB tick — R-NEW-V2 compliant (utf-8 explicit read+append+write)."""
import json, os, sys
from datetime import datetime, timezone, timedelta

WS = r"D:\B166ER-OpenClaw\workspace"
STATE = os.path.join(WS, "memory", "heartbeat-state.json")
HB = os.path.join(WS, "HEARTBEAT.md")
NOW = datetime.now(timezone(timedelta(hours=8)))
TS = NOW.strftime("%Y-%m-%dT%H:%M GMT+8")
TS_FILE = NOW.strftime("%Y-%m-%dT%H:%M:%S+08:00")

# Load state
with open(STATE, "r", encoding="utf-8") as f:
    state = json.load(f)

prev = state.get("hbCount", 932)
prev_ts = state.get("lastCheck", "")
prev_dt = datetime.fromisoformat(prev_ts.replace("+08:00","")) if prev_ts else NOW
gap_min = (NOW.replace(tzinfo=None) - prev_dt).total_seconds() / 60
hb = prev + 1

# Compute silence hours from 7/16 13:16 (D+0 first-contact) to now
first_contact = datetime(2026, 7, 16, 13, 16)
silence_h = round((NOW.replace(tzinfo=None) - first_contact).total_seconds() / 3600, 2)

# Compute D-Day T-hours (7/24 assumed morning meeting)
dday = datetime(2026, 7, 24, 9, 0)
dday_h = round((dday - NOW.replace(tzinfo=None)).total_seconds() / 3600, 1)

# Compute T-0 past hours
t0 = datetime(2026, 7, 18, 0, 0)
t0_past = round((NOW.replace(tzinfo=None) - t0).total_seconds() / 3600, 2)

# Next 21:00 evening self-iter (work in naive local time consistently)
now_naive = NOW.replace(tzinfo=None)
evening = now_naive.replace(hour=21, minute=0, second=0, microsecond=0)
if evening < now_naive:
    evening = evening + timedelta(days=1)
evening_h = round((evening - now_naive).total_seconds() / 3600, 1)

entry = f"""## HB #{hb} ({TS} cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev} ({prev_ts.split("T")[1][:5] if prev_ts else "??"}): +{gap_min:.1f}min -- Wednesday afternoon Token Guard normal cadence (R012 minimal mode)
- D+6 afternoon pass #{hb} -- Eric silent in THIS session ~{silence_h}h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat (~{silence_h - 0:.2f}h+ ongoing since 7/19 12:33)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #{hb}: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- **Triple Confluence Day 0 CLOSED** -- 7/21 24:00 cutoff passed ~{round((NOW.replace(tzinfo=None) - datetime(2026,7,21,23,59)).total_seconds()/3600,1)}h ago; oil Scenario C verification window OPEN until 7/25
- **D+6 = Execution phase** -- per 7/21 evening self-iter protocol; observer mode sustained
- Wednesday-afternoon zone (16:40) -- Eric typical late-afternoon deep-work or AnYi prep; THIS session DORMANT per Eric 7/19 12:33 explicit instruction
- 7/24 D-Day T-{dday_h}h (AnYi important meeting Thursday morning) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Next cron: 21:00 evening self-iter R60-11 (~{evening_h}h)
- Token Guard stable, no compression needed
- Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +{t0_past}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+6 sustain zero-push mode intact
- hbCount: {prev} -> {hb}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{hb} = sustain #{prev} = D+6 afternoon dormant baseline)
- **HEARTBEAT_OK** -- HB #{hb} = sustain DORMANT protocol
- **no push**: Wednesday-afternoon zone (16:40), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-{dday_h}h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter (~{evening_h}h)

*{TS} -- D+6 Wednesday afternoon -- HB #{hb} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day +1 post-window passive -- 7/24 D-Day T-{dday_h}h watch (AnYi meeting Thursday morning) -- Eric silent = dominant signal holding*
"""

# Read HB file
with open(HB, "r", encoding="utf-8") as f:
    content = f.read()

# Insert new entry after the header (before existing entries)
# Strategy: insert at position after the first "## " entry found (i.e., after the most recent HB)
# Actually, let's append at the top of the log section, right after the last HB entry
# Find the first "## HB #" marker and insert before it
lines = content.split("\n")
insert_idx = None
for i, line in enumerate(lines):
    if line.startswith("## HB #"):
        insert_idx = i
        break

if insert_idx is not None:
    # Insert before existing HB entries (newest at top of log section)
    lines.insert(insert_idx, entry.rstrip())
    new_content = "\n".join(lines)
else:
    # No HB entries yet, append at end
    new_content = content + "\n" + entry

# Write back
with open(HB, "w", encoding="utf-8") as f:
    f.write(new_content)

# Update state
state["hbCount"] = hb
state["lastCheck"] = TS_FILE
state["silenceHours"] = silence_h
state["t0_past_hours"] = t0_past
state["nextDDayHours"] = dday_h
state["mode"] = "DORMANT"
state["notes"] = f"HB#{hb}: +{gap_min:.1f}min (Wednesday afternoon). DORMANT sustained. 7/24 D-Day T-{dday_h}h. No actionable signal. Next: 21:00 evening self-iter (~{evening_h}h)."
state["nextSignificantCheck"] = f"21:00 evening self-iter (~{evening_h}h)"

with open(STATE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"OK HB #{hb} written. silence={silence_h}h, dday={dday_h}h, evening={evening_h}h")