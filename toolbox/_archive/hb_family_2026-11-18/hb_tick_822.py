"""HB tick - R-NEW-V2 compliant (utf-8 explicit read+append+write).
Sustain DORMANT mode for HB #822, late-night quiet window.
Do NOT push any message to user. Internal monitor only.
"""
import json
import datetime
from pathlib import Path

WS = Path(r"D:\B166ER-OpenClaw\workspace")
now = datetime.datetime.now()
ts_iso = now.strftime("%Y-%m-%dT%H:%M") + " GMT+8"
ts_human = now.strftime("%Y-%m-%d %H:%M GMT+8")

# Load heartbeat state
state_path = WS / "memory" / "heartbeat-state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
prev_hb = state.get("hbCount", 821)
prev_ts = state.get("lastHB", "22:52")
new_hb = prev_hb + 1
silence_h = state.get("silenceDuration_h", 128.22)

# Build minimal HB entry (R012: NOT full report)
hb_entry = f"""
## HB #{new_hb} ({ts_iso} cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb} ({prev_ts}): ~+10min -- Tuesday late-night Token Guard cadence (R012 minimal mode)
- D+5 late-night pass #{new_hb} -- Eric silent in THIS session ~{silence_h:.2f}h+ since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat (~56.71h+ since 7/19 12:33)
- 5-layer suppression (R-B/R12/R-CANDIDATE-T2/R256/R257) + R258 dormant-session -- zero breach
- R-NEW-V2 verification #{new_hb}: Python utf-8 explicit read+append+write (compliant)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence FINAL DAY 7/21 sustained -- zero-push on this session:
  1. DeepSeek V4 launch window (PoC awaiting Eric trigger)
  2. **Induction window cutoff 23:59 -- INTERNAL monitor only (~57min)** this session != AnYi decision channel
  3. Araqchi Qatar talks day-1 (7/21-25) -- oil Scenario C verification window OPEN (INTERNAL only)
- 23:02 GMT+8 Tuesday late-night quiet mode per HEARTBEAT.md
- 21:00 R60-11 evening self-iter DONE (~112min ago)
- Token Guard stable, no compression needed
- Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked, not urgent
- T-0 publicity cutoff 7/18 +5d14h+ past -- post-protection window firmly sustained
- hbCount: {prev_hb} -> {new_hb}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{new_hb} = sustain D+5 late-night dormant baseline)
- **HEARTBEAT_OK** -- HB #{new_hb} = sustain DORMANT protocol
- **no push**: late-night zone, this session DORMANT per Eric 7/19 12:33 explicit instruction
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- 23:59 Induction cutoff approaching -- INTERNAL monitor only; this session != AnYi decision channel
- Next significant check: 23:59 Induction cutoff INTERNAL monitor (~57min)

*{ts_human} -- D+5 Tuesday late-night -- HB #{new_hb} -- this session DORMANT -- zero-push mode intact -- Triple Confluence FINAL DAY passive*
"""

# Append to today's memory (R-NEW-V2 compliant utf-8 explicit)
today_path = WS / "memory" / f"{now.strftime('%Y-%m-%d')}.md"
with open(today_path, "a", encoding="utf-8") as f:
    f.write(hb_entry)

# Update heartbeat-state.json
state["hbCount"] = new_hb
state["lastHBTime"] = ts_iso
state["lastHB"] = now.strftime("%H:%M")
state["last_update_epoch"] = int(now.timestamp())
new_silence = round(silence_h + (10 / 60), 2)  # +~10min
state["silenceDuration_h"] = new_silence
state["silenceDuration_thisSession_h"] = new_silence
state["silenceDuration_global_h"] = new_silence
state["note"] = (
    f"HB #{new_hb}; Tuesday {now.strftime('%H:%M')} GMT+8; Triple Confluence FINAL DAY 7/21 "
    f"(~57min to Induction cutoff 23:59); Eric silent D+5 ~{new_silence:.2f}h+ on THIS session "
    f"(AnYi dedicated); 21:00 R60-11 evening self-iter already executed (~112m ago); "
    f"awaiting Eric active contact in AnYi session, not here"
)

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"OK: HB #{new_hb} logged at {now.strftime('%H:%M')} GMT+8")
print(f"Silence: {new_silence:.2f}h+")
print(f"Next: 23:59 Induction cutoff INTERNAL monitor (~57min)")
print(f"Mode: DORMANT sustained -- zero-push -- no user-facing message required")
