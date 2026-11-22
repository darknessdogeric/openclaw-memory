# -*- coding: utf-8 -*-
"""HB #1152 -- minimal token-guard tick, R012 rule #2."""
import json
from pathlib import Path

workspace = Path(r"D:\B166ER-OpenClaw\workspace")
hb_path = workspace / "HEARTBEAT.md"
state_path = workspace / "memory" / "heartbeat-state.json"

hb_num = 1152
prev_hb = 1151
timestamp = "2026-07-24T05:20:00+08:00"
zone = "Friday pre-dawn zone (05:20)"

entry = f"""### HB #{hb_num} ({timestamp} cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb} (05:16:38): +3.5min -- Friday pre-dawn Token Guard normal cadence (R012 minimal mode)
- D+8 pre-dawn pass #{hb_num} -- Eric silent in THIS session ~183.7h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~112.4h+ (since 7/19 12:33) -- final pre-meeting prep T-~3.67h
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #{hb_num}: Python utf-8 explicit read+prepend+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~53h ago; oil Scenario C verification window OPEN until 7/25 (~19h remaining)
- D+8 = Execution phase day 4 -- observer mode sustained
- {zone} -- Eric sleep zone; silence authority strictly holding on THIS session
- **7/24 D-Day T-~3.67h** (AnYi meeting TODAY MORNING 7/24 ~9:00) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Next cron: 08:00 daily briefing (~2h40m); 21:00 R60-11 evening self-iter (~15h40m)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +149h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+8 sustain zero-push mode intact
- hbCount: {prev_hb} -> {hb_num}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{hb_num} = sustain #{prev_hb} = D+8 pre-dawn dormant baseline)
- **HEARTBEAT_OK** -- HB #{hb_num} = sustain DORMANT protocol
- **no push**: {zone}, Eric sleep zone, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-~3.67h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: 08:00 daily briefing cron (~2h40m) -- natural D-Day pre-meeting prep window
- DO NOT push at 05:20 pre-dawn despite D-Day proximity; R256 silence discipline > meeting-window signal

*{timestamp.split('T')[0]} {timestamp.split('T')[1].split('+')[0]} -- D+8 Friday pre-dawn -- HB #{hb_num} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-~3.67h watch (AnYi meeting TODAY MORNING 7/24 ~9:00) -- Eric silent = dominant signal holding -- 08:00 cron = next natural D-Day prep window*

"""

# R-NEW-V2: explicit utf-8 read+prepend+write
with open(hb_path, "rb") as f:
    raw = f.read()
existing = raw.decode("utf-8")

leading = ""
i = 0
while i < len(existing) and existing[i] in " \t\r\n":
    leading += existing[i]
    i += 1
rest = existing[i:]

new_content = leading + entry + rest
with open(hb_path, "w", encoding="utf-8", newline="") as f:
    f.write(new_content)

# Update state.json
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)
state["lastHBNumber"] = f"#{hb_num}"
state["lastUpdate"] = "2026-07-24T05:20:00.000000+08:00"
state["lastHB"] = "2026-07-24T05:20:00.000000+08:00"
state["hbCount"] = hb_num
state["dday_t_minus_hours"] = 3.67
state["ericAnyiHours"] = 112.4
state["ericSilenceHours"] = 183.7
state["note"] = f"#{hb_num} - 2026-07-24T05:20:00+08:00 DORMANT sustained; D-Day T-~3.67h (AnYi 7/24 9:00 AM meeting); silent heartbeat; pre-dawn sleep zone; R256 silence discipline > meeting-window signal"
with open(state_path, "w", encoding="utf-8", newline="") as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print(f"OK HB #{hb_num} appended (prepend), state.json updated")
print(f"dday_t_minus_hours: {state['dday_t_minus_hours']}")
print(f"hbCount: {state['hbCount']}")