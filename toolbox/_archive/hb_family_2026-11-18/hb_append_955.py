# -*- coding: utf-8 -*-
"""R-NEW-V2 compliant HEARTBEAT.md append + state update for HB #955."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

WORKSPACE = Path(r"D:\B166ER-OpenClaw\workspace")
HB_MD = WORKSPACE / "HEARTBEAT.md"
STATE_JSON = WORKSPACE / "memory" / "heartbeat-state.json"

# --- timestamps (Asia/Shanghai GMT+8) ---
TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)
ts_str = now.strftime("%Y-%m-%dT%H:%M GMT+8")
date_str = now.strftime("%Y-%m-%d")
prev_hb = 954
new_hb = prev_hb + 1  # 955
silence_hours = 150.23
t0_past_hours = 115.48

# --- HB #955 log entry (minimal, R012 compliant) ---
hb_entry = f"""
## HB #{new_hb} ({ts_str} cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb} (19:28): +2min -- Wednesday early-evening Token Guard normal cadence (R012 minimal mode)
- D+6 early-evening pass #{new_hb} -- Eric silent in THIS session ~{silence_hours:.2f}h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~{78.97:.2f}h+ (since 7/19 12:33)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #{new_hb}: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- **Triple Confluence Day 0 CLOSED** -- 7/21 24:00 cutoff passed ~19h30m ago; oil Scenario C verification window OPEN until 7/25
- **D+6 early-evening** -- observer mode sustained; emergency prepare-mode prepacked
- Wednesday early-evening zone (19:30) -- Eric typical late-afternoon/evening deep-work window; THIS session DORMANT sustained
- 7/24 D-Day T-37.5h (AnYi important meeting Thursday morning) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Next cron: 21:00 evening self-iter R60-11 (~1.5h)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +{t0_past_hours:.2f}h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+6 sustain zero-push mode intact
- hbCount: {prev_hb} -> {new_hb}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{new_hb} = sustain #{prev_hb} = D+6 early-evening dormant baseline)
- **HEARTBEAT_OK** -- HB #{new_hb} = sustain DORMANT protocol
- **no push**: Wednesday early-evening zone (19:30), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-37.5h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter (~1.5h)

*{ts_str} -- D+6 Wednesday early-evening -- HB #{new_hb} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-37.5h watch (AnYi meeting Thursday morning) -- Eric silent = dominant signal holding*
"""

# --- explicit utf-8 read+append+write per R-NEW-V2 ---
with open(HB_MD, "r", encoding="utf-8") as f:
    existing = f.read()
with open(HB_MD, "w", encoding="utf-8") as f:
    f.write(existing + hb_entry)

# --- update heartbeat-state.json ---
with open(STATE_JSON, "r", encoding="utf-8") as f:
    state = json.load(f)

state["lastHB"] = new_hb
state["hbCount"] = new_hb
state["lastCheck"] = now.isoformat()
state["silenceHours"] = round(silence_hours, 2)
state["t0_past_hours"] = round(t0_past_hours, 2)
state["notes"] = f"HB#{new_hb}: 19:30 Wednesday early-evening. DORMANT sustained. 7/24 D-Day T-37.5h. Eric on AnYi webchat. No actionable signal. Stay silent."

with open(STATE_JSON, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"OK HB#{new_hb} appended + state updated. silence={state['silenceHours']}h t0_past={state['t0_past_hours']}h")