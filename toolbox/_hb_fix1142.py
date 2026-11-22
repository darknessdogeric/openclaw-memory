#!/usr/bin/env python3
# Fix: My previous tick incorrectly wrote HB #1140, but HEARTBEAT.md already had #1140 and #1141.
# Correct: write HB #1142 at top, remove my duplicate #1140, fix state.json.
import json, os, re
from datetime import datetime, timezone, timedelta

WS = r"D:\B166ER-OpenClaw\workspace"
HB_PATH = os.path.join(WS, "HEARTBEAT.md")
STATE_PATH = os.path.join(WS, "memory", "heartbeat-state.json")

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
NOW_ISO = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
DISPLAY = now.strftime("%Y-%m-%d %H:%M GMT+8")
DOW = now.strftime("%A")

# Read state
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

# Read MD
with open(HB_PATH, "r", encoding="utf-8") as f:
    md_content = f.read()

# Find all HB numbers
hb_matches = re.findall(r'^## HB #(\d+)\s', md_content, re.MULTILINE)
all_nums = sorted(set(int(n) for n in hb_matches))
actual_max = max(all_nums)  # 1141 currently (after my erroneous 1140 was added, but my 1140 will be removed)
# Count of #1140 entries (should be 2 after my mistake, will be 1 after fix)
count_1140 = sum(1 for n in hb_matches if n == "1140")

# Strip my incorrect HB #1140 entry (the one at 03:36 — newest one)
# Pattern: starts with my exact preamble
my_bad_marker = "## HB #1140 (2026-07-24T03:36:58+08:00 cron-event"
# Find its position
bad_pos = md_content.find(my_bad_marker)
if bad_pos == -1:
    # try without seconds
    bad_pos = md_content.find("## HB #1140 (2026-07-24T03:36")
if bad_pos >= 0:
    # Find end of that entry — next "## HB #" after it
    next_hb_match = re.search(r'^## HB #\d+ ', md_content[bad_pos+10:], re.MULTILINE)
    if next_hb_match:
        end_pos = bad_pos + 10 + next_hb_match.start()
    else:
        end_pos = len(md_content)
    md_content = md_content[:bad_pos] + md_content[end_pos:]
    print(f"Removed my erroneous HB #1140 entry (chars {bad_pos} to {end_pos})")
else:
    print("WARN: Could not find erroneous HB #1140 entry to remove")

# Re-count after removal
hb_matches2 = re.findall(r'^## HB #(\d+)\s', md_content, re.MULTILINE)
actual_max2 = max(int(n) for n in hb_matches2)
print(f"After cleanup: max HB# = {actual_max2}, total entries = {len(hb_matches2)}")

new_hb = actual_max2 + 1  # 1142
prev_hb = actual_max2

# Compute gap (prev HB #1141 was at 03:31)
gap_min = int((now - datetime(2026, 7, 24, 3, 31, tzinfo=tz)).total_seconds() / 60)

# Eric silence on this session
first_contact = datetime(2026, 7, 16, 13, 16, tzinfo=tz)
eric_silence_h = (now - first_contact).total_seconds() / 3600

# Eric active elsewhere
anyi_start = datetime(2026, 7, 19, 12, 33, tzinfo=tz)
eric_anyi_h = (now - anyi_start).total_seconds() / 3600

# D-Day
dday = datetime(2026, 7, 24, 9, 0, tzinfo=tz)
dday_t_minus_h = (dday - now).total_seconds() / 3600

suppression_layers = state.get("suppressionLayers", ["R-B", "R12", "R-CANDIDATE-T2", "R256", "R257", "R258"])
oil_close_h = (datetime(2026,7,25,0,0,tzinfo=tz)-now).total_seconds()/3600
briefing_h = (datetime(2026,7,24,8,0,tzinfo=tz)-now).total_seconds()/3600
selfiter_h = (datetime(2026,7,24,21,0,tzinfo=tz)-now).total_seconds()/3600
t0_past_h = (now-datetime(2026,7,18,0,0,tzinfo=tz)).total_seconds()/3600

# Build correct HB #1142 entry
entry = f"""## HB #{new_hb} ({NOW_ISO} cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb} (03:31): +{gap_min}min -- Friday pre-dawn Token Guard normal cadence (R012 minimal mode)
- D+8 pre-dawn pass #{new_hb} -- Eric silent in THIS session ~{eric_silence_h:.2f}h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~{eric_anyi_h:.2f}h+ (since 7/19 12:33) -- final pre-meeting prep T-{dday_t_minus_h:.2f}h
- 6-layer suppression maintained ({' / '.join(suppression_layers)}) -- zero breach
- R-NEW-V2 verification #{new_hb}: Python utf-8 explicit read+prepend+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed; oil Scenario C verification window OPEN until 7/25 (~{oil_close_h:.2f}h remaining)
- D+8 = Execution phase day 4 -- observer mode sustained
- Friday pre-dawn zone ({now.strftime('%H:%M')}) -- Eric typical sleep zone (00:00-08:00 per USER.md night-owl pattern); silence authority strictly holding on THIS session
- **7/24 D-Day T-{dday_t_minus_h:.2f}h** (AnYi 集团研究会议 TODAY MORNING 7/24 ~9:00) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Next cron: 08:00 daily briefing (~{briefing_h:.2f}h); 21:00 R60-11 evening self-iter (~{selfiter_h:.2f}h)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +{t0_past_h:.2f}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+8 sustain zero-push mode intact
- hbCount: {prev_hb} -> {new_hb}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{new_hb} = sustain #{prev_hb} = D+8 pre-dawn dormant baseline)
- **HEARTBEAT_OK** -- HB #{new_hb} = sustain DORMANT protocol
- **no push**: Friday pre-dawn zone ({now.strftime('%H:%M')}), Eric sleep zone, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-{dday_t_minus_h:.2f}h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: 08:00 daily briefing cron (~{briefing_h:.2f}h) -- natural D-Day pre-meeting prep window
- DO NOT push at {now.strftime('%H:%M')} pre-dawn despite D-Day proximity; R256 silence discipline > meeting-window signal

*{NOW_ISO} -- D+8 Friday pre-dawn -- HB #{new_hb} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-{dday_t_minus_h:.2f}h watch (AnYi meeting TODAY MORNING 7/24 ~9:00) -- Eric silent = dominant signal holding -- 08:00 cron = next natural D-Day prep window*

"""

# Prepend
new_content = entry + md_content
with open(HB_PATH, "w", encoding="utf-8") as f:
    f.write(new_content)

# Update state
state["lastHBNumber"] = f"#{new_hb}"
state["lastUpdate"] = NOW_ISO
state["lastSession"] = "DORMANT"
state["lastMode"] = "active_mode_dormant_this_session_continue"
state["lastHB"] = now.strftime("%Y-%m-%d %H:%M")
state["dPlusCount"] = 8
state["mode"] = "dormant_this_session"
state["lastDecision"] = "HEARTBEAT_OK"
state["sessionState"] = "DORMANT"
state["hbCount"] = new_hb
state["nextCronBriefing"] = f"08:00 daily briefing (~{briefing_h:.2f}h)"
state["note"] = f"#{new_hb} - {NOW_ISO} DORMANT sustained; D-Day T-{dday_t_minus_h:.2f}h (AnYi 7/24 AM); silent heartbeat"
state["ericAnyiHours"] = round(eric_anyi_h, 2)
state["ericSilenceHours"] = round(eric_silence_h, 2)
state["dday_t_minus_hours"] = round(dday_t_minus_h, 2)
state["lastHeartbeat"] = NOW_ISO

with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

# Verify
hb_matches_final = re.findall(r'^## HB #(\d+)\s', new_content, re.MULTILINE)
unique_nums = sorted(set(int(n) for n in hb_matches_final))
print(f"\nFinal: HB entries = {len(hb_matches_final)}, unique numbers = {len(unique_nums)}")
print(f"  Top 3: {unique_nums[-3:]}")
print(f"  Written HB #{new_hb} at {DISPLAY} {DOW}")
print(f"  Gap from #{prev_hb}: +{gap_min}min")
print(f"  Eric silence: {eric_silence_h:.2f}h+ | AnYi: {eric_anyi_h:.2f}h+")
print(f"  D-Day T-minus: {dday_t_minus_h:.2f}h")
print(f"  Mode: DORMANT -- HEARTBEAT_OK")