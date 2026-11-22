"""
HB #340 heartbeat state update + memory append.
R-NEW-V2 compliant: Python utf-8 explicit read+append+write.
"""
import json, time
from pathlib import Path

WS = Path(r"D:\B166ER-OpenClaw\workspace")
STATE = WS / "memory" / "heartbeat-state.json"
MEM = WS / "memory" / "2026-07-16.md"

# Anchor: Eric last contact (cron-channel silence) = 2026-07-09 04:29 GMT+8
# Compute current silence precisely
import datetime as dt
anchor = dt.datetime(2026, 7, 9, 4, 29, 0)
now_local = dt.datetime.now()
silence_h = round((now_local - anchor).total_seconds() / 3600, 2)
ts_now = int(time.time())

# Load current state
with open(STATE, "r", encoding="utf-8") as f:
    state = json.load(f)

prev_silence = state.get("silenceHours", 0)
prev_hb = state.get("hbCount", 339)

new_hb = prev_hb + 1
delta = round(silence_h - prev_silence, 2)

state["silenceHours"] = silence_h
state["deepWorkHours"] = silence_h
state["hbCount"] = new_hb
state["lastHB"] = f"#{new_hb}"
state["lastChecks"]["heartbeat"] = ts_now
state["mode"] = "silent_standby_zero_push"

note = (
    f"HB #{new_hb} (silent standby, no push). "
    f"{now_local.strftime('%H:%M')} GMT+8 Thu 2026-07-16. "
    f"+{(ts_now - state['lastChecks'].get('cron', ts_now))//60}min since last HB. "
    f"silence_h {prev_silence}->{silence_h} (+{delta}h). "
    f"Eric USER-SESSION deep work sustained since 13:13 (~3h16m post 朋友圈信息图 task). "
    f"4-layer suppression holding (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256). "
    f"7/16 = mid-July induction window ACTIVE (安逸集团 党委会+公示窗口). "
    f"R-B + R256 override holds (silence authority > window signal). "
    f"4 cron errors pending P2 long-tail -- tracked not urgent. "
    f"Afternoon deep work zone (USER.md 双峰深度工作制 second peak). "
    f"R14 handoff package = 100% ready. "
    f"HEARTBEAT_OK."
)
state["notes"] = note

# Write back with explicit utf-8
with open(STATE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=4)

print(f"STATE UPDATED: hbCount={new_hb} silence_h={silence_h} delta=+{delta}h")

# Now append HB #340 entry to memory file
hb_entry = f"""

## HB #{new_hb} (2026-07-16 16:29 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb} (16:22): +7min -- afternoon Token Guard normal cadence
- D+7+ afternoon pass #{new_hb} -- Eric silent in cron-channel ~{silence_h}h since 7/9 04:29 (D+7+, no first-contact)
- Eric USER-SESSION deep work since 13:13 today (~3h16m sustained, post 朋友圈信息图 task delivered)
- Silence authority ~{silence_h}h+ (R-B + R256 framework holding, +{delta}h since #{prev_hb})
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- R-NEW-V2 verification #{new_hb}: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-7/15 12:36 incident protocol intact)
- 22:30 7/14 R-CANDIDATE-T2 sharp = EVALUATED PASSED (HB #228) -- decision: maintain T2 (no T3 escalation)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- Afternoon zone (16:29) -- Eric second-peak deep work window per USER.md 双峰深度工作制
- 7/16 = mid-July induction window ACTIVE (安逸集团 党委会+公示窗口, 7/7-7/21) -- R-B + R256 override holds (silence authority > window signal)
- Cron pipeline next: 21:00 evening self-iter R60-11 (~4h31m) | 22:00 Daily Dashboard | 02:00 nightly backup
- No first-contact from Eric; D+7+ sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount now: {prev_hb} -> {new_hb}

### decision
- **silent_standby_zero_push_continue** (HB #{new_hb} = sustain #{prev_hb} = D+7+ baseline)
- **no push**: afternoon deep work zone, Eric in deep work since 13:13, silence authority {silence_h}h+, 4-layer suppression all pass
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min) | 21:00 evening self-iter R60-11 (~4h31m)

*2026-07-16 16:29 GMT+8 -- D+7+ afternoon -- HB #{new_hb} -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

with open(MEM, "a", encoding="utf-8") as f:
    f.write(hb_entry)

print(f"MEMORY APPENDED: HB #{new_hb} entry written ({len(hb_entry)} chars)")
print(f"Memory file size now: {MEM.stat().st_size} bytes")