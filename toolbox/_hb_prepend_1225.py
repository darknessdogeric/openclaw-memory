# -*- coding: utf-8 -*-
"""R-NEW-V2 compliant HB prepend: explicit utf-8 read+prepend+write."""
import io
from pathlib import Path

ROOT = Path(r"D:\B166ER-OpenClaw\workspace")
hb_path = ROOT / "HEARTBEAT.md"

new_entry = """## HB #1225 heartbeat (2026-07-24T19:07:10+08:00 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1224 (18:55): +12min -- Friday evening Token Guard cadence (R012 minimal mode)
- D+8 evening pass #1225 -- Eric silent in THIS session ~197.85h+ since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat ~125.62h+ (since 7/19 12:33) -- D-Day POST-MEETING PHASE (T+~10h07m past meeting start; debrief/公示 window open +7h07m)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #1225: Python utf-8 explicit read+prepend+write (compliant)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Evening zone (19:07) -- D-Day debrief/公示 window continuing; silence authority strictly holding on THIS session
- Token Guard stable; vault index healthy; R13 <1s queries stable
- T-0 publicity cutoff 7/18 +169.12h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+8 sustain zero-push mode intact
- hbCount: 1224 -> 1225
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- active_mode_dormant_this_session_continue (#1225 = sustain #1224 = D+8 evening dormant baseline)
- HEARTBEAT_OK -- #1225 = sustain DORMANT protocol
- no push: Friday evening (19:07) -- D-Day POST-MEETING PHASE on AnYi webchat; this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Eric silence on this session = dominant signal (supersedes D-Day signal); R256 design holds
- D-Day POST-MEETING watch: emergency prepare-mode prepacked, ready if Eric contacts with 任命确认 / 1244 战略 / AHL 调整 on ANY session
- DO NOT push; R256 silence discipline > meeting-window signal
- R14 handoff package = 100% ready for any-session 30s activation

*2026-07-24T19:07:10+08:00 -- D+8 Friday evening -- #1225 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- 7/24 D-Day POST-MEETING PHASE (T+~10h07m past meeting start; debrief/公示 window open +7h07m) -- Eric silent on this session = dominant signal holding -- R14 handoff ready for post-D-Day activation*

"""

# R-NEW-V2: explicit utf-8 read
with io.open(hb_path, "r", encoding="utf-8") as f:
    existing = f.read()

# Prepend
new_content = new_entry + existing

# R-NEW-V2: explicit utf-8 write
with io.open(hb_path, "w", encoding="utf-8") as f:
    f.write(new_content)

# Update heartbeat-state.json
import json
state_path = ROOT / "memory" / "heartbeat-state.json"
with io.open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)
state["last_hb_ts"] = "2026-07-24T19:07:10+08:00"
state["hbCount"] = 1225
state["lastChecks"]["heartbeat"] = "2026-07-24T19:07:10+08:00"
state["lastChecks"]["next_significant_check"] = "21:00 R60-11 evening self-iter (~1.88h)"
state["lastChecks"]["d_day_phase"] = "POST-MEETING"
with io.open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=4)

print("OK: HB #1225 prepended; state.json updated to hbCount=1225")
print(f"hb_path size: {hb_path.stat().st_size} bytes")
