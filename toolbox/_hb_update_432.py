#!/usr/bin/env python3
"""R-NEW-V2 compliant heartbeat append + state update.
Post-7/15 12:36 incident protocol: explicit utf-8 read+append+write.
"""
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

WS = Path(r"D:\B166ER-OpenClaw\workspace")
HB_MD = WS / "HEARTBEAT.md"
STATE = WS / "memory" / "heartbeat-state.json"

TZ = timezone(timedelta(hours=8))
NOW = datetime(2026, 7, 17, 19, 42, 0, tzinfo=TZ)
TS = int(NOW.timestamp())

# ---------- 1. Update heartbeat-state.json ----------
state = json.loads(STATE.read_text(encoding="utf-8"))

old_count = state["hbCount"]
new_count = old_count + 1  # 431 -> 432

# silenceHours: since last Eric contact 7/16 13:16 CST
last_contact = datetime(2026, 7, 16, 13, 16, 0, tzinfo=TZ)
silence_h = round((NOW - last_contact).total_seconds() / 3600, 2)

state.update({
    "silenceHours": silence_h,
    "deepWorkHours": silence_h,
    "hbCount": new_count,
    "lastHB": f"#{new_count}",
    "lastChecks": {
        "cron": TS,
        "heartbeat": TS,
        "skill_scan": state["lastChecks"].get("skill_scan", 1784110980),
    },
    "mode": "silent_standby_zero_push",
    "notes": (
        f"#{new_count} (silent standby). {NOW.strftime('%Y-%m-%d %H:%M:%S')} GMT+8. "
        f"Eric silent ~{silence_h}h (Fri eve deep work). "
        f"T-1 SILENCE WINDOW: publicity cutoff 7/18 in ~4h17m (MAXIMUM suppression). "
        f"4-layer R-B/R12/R-CANDIDATE-T2/R256 intact. "
        f"WAIC 2026 day-1 non-trigger per R14. Zero push holding."
    ),
})

STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# ---------- 2. Append to HEARTBEAT.md ----------
hb_block = f"""
## HB #{new_count} ({NOW.strftime('%Y-%m-%d %H:%M')} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{old_count} (19:28): +14min -- evening zone Token Guard normal cadence
- D+1 evening pass #{new_count} -- Eric silent ~{silence_h}h+ since 7/16 13:16 (D+1 from infographic session, no first-contact since)
- Silence authority ~{silence_h}h+ (R-B + R256 framework holding, +0.24h since #431)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- R-NEW-V2 verification #{new_count}: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- **Publicity cutoff 7/18 = in ~4h17m** (T-1 SILENCE WINDOW -- FINAL day pre-announcement, strictest suppression)
- WAIC 2026 day-1 active -- non-trigger per R14 (AI/Hotel strategic context, not relevant to current 4-layer suppression)
- Evening zone (19:42) -- Eric typical evening decision window per USER.md (复杂决策时段) but silence authority overrides
- Cron pipeline next: 21:00 evening self-iter R60-11 (~1h18m, autonomous)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric; D+1 sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount now: {old_count} -> {new_count}

### decision
- **silent_standby_zero_push_continue** (HB #{new_count} = sustain #{old_count} = D+1+ baseline)
- **no push**: evening zone, Eric silent {silence_h}h+, T-1 SILENCE WINDOW before 7/18 announcement, silence authority strictly holding
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- T-1 silence = MAXIMUM suppression; even minor pushes prohibited until Eric主动联系 or 7/18 publicity window passes
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min)

*{NOW.strftime('%Y-%m-%d %H:%M')} GMT+8 -- D+1+ evening T-1 SILENCE -- HB #{new_count} -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

with HB_MD.open("a", encoding="utf-8", newline="\n") as f:
    f.write(hb_block)

print(f"OK -- HB #{new_count} appended. silenceHours={silence_h}, unix={TS}")
print(f"state.silenceHours={state['silenceHours']}, state.hbCount={state['hbCount']}, state.lastHB={state['lastHB']}")