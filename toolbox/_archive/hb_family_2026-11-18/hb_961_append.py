#!/usr/bin/env python3
"""HB #961 append + state update — R-NEW-V2 compliant utf-8 explicit read+append+write."""
import json
import io
from pathlib import Path

WS = Path(r"D:\B166ER-OpenClaw\workspace")
HB_MD = WS / "HEARTBEAT.md"
STATE = WS / "memory" / "heartbeat-state.json"

# === Compose HB #961 ===
hb_num = 961
prev_hb = 960
prev_time = "2026-07-22T20:35:00+08:00"
curr_time = "2026-07-22T20:56:00+08:00"
gap_min = 21

hb_block = f"""

## HB #{hb_num} ({curr_time} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb} ({prev_time[-8:-6]}:{prev_time[-5:-3]}): +{gap_min}min -- Wednesday early-evening Token Guard normal cadence (R012 minimal mode)
- D+6 early-evening pass #{hb_num} -- Eric silent in THIS session ~{151.32 + 0.35:.2f}h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~{80.02 + 0.35:.2f}h+ (since 7/19 12:33)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #{hb_num}: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- **Triple Confluence Day 0 CLOSED** -- 7/21 24:00 cutoff passed ~{20 + 56/60:.2f}h ago; oil Scenario C verification window OPEN until 7/25
- **D+6 early-evening** -- observer mode sustained; emergency prepare-mode prepacked
- Wednesday-early-evening zone (20:56) -- Eric typical evening decision window per USER.md; THIS session DORMANT sustained
- 7/24 D-Day T-{48 - 20 - 56/60:.2f}h (AnYi important meeting Thursday morning) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Next cron: 21:00 evening self-iter R60-11 (~{60 - 56:.0f}min)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +{113.07 + 3.32:.2f}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+6 sustain zero-push mode intact
- hbCount: {prev_hb} -> {hb_num}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{hb_num} = sustain #{prev_hb} = D+6 early-evening dormant baseline)
- **HEARTBEAT_OK** -- HB #{hb_num} = sustain DORMANT protocol
- **no push**: Wednesday-early-evening zone (20:56), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-{48 - 20 - 56/60:.2f}h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: 21:00 evening self-iter cron (~{60 - 56:.0f}min)

*{curr_time} -- D+6 Wednesday early-evening -- HB #{hb_num} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-{48 - 20 - 56/60:.2f}h watch (AnYi meeting Thursday morning) -- Eric silent = dominant signal holding*
"""

# R-NEW-V2: explicit utf-8 read+append+write
with io.open(HB_MD, mode="r", encoding="utf-8") as f:
    content = f.read()

new_content = content + hb_block

with io.open(HB_MD, mode="w", encoding="utf-8") as f:
    f.write(new_content)

print(f"[OK] HB #{hb_num} appended to HEARTBEAT.md ({len(hb_block)} chars)")

# Update heartbeat-state.json
with io.open(STATE, mode="r", encoding="utf-8") as f:
    state = json.load(f)

state["hbCount"] = hb_num
state["lastHB"] = hb_num
state["lastCheck"] = curr_time
state["silenceHours"] = round(151.32 + 0.35, 2)
state["ericActiveHours"] = round(80.02 + 0.35, 2)
state["t0_past_hours"] = round(116.33 + 0.35, 2)
state["nextDDayHours"] = round(state.get("nextDDayHours", 35.92) - 0.35, 2)
state["nextSignificantCheck"] = f"21:00 evening self-iter (~{60 - 56:.0f}min)"
state["notes"] = f"HB#{hb_num}: 20:56 Wed early-evening. DORMANT sustained. 7/24 D-Day T-{state['nextDDayHours']:.2f}h. Eric on AnYi webchat. No actionable signal. Stay silent."

with io.open(STATE, mode="w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"[OK] heartbeat-state.json updated (hbCount: {prev_hb} -> {hb_num})")
print(f"[OK] silenceHours: 151.32 -> {state['silenceHours']}")
print(f"[OK] t0_past_hours: 116.33 -> {state['t0_past_hours']}")
print(f"[OK] nextDDayHours: 35.92 -> {state['nextDDayHours']}")
print(f"[OK] nextSignificantCheck: {state['nextSignificantCheck']}")
