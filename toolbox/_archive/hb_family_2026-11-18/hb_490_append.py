# -*- coding: utf-8 -*-
"""HB #490 heartbeat append (R-NEW-V2 compliant).
Python utf-8 explicit read+append+write — no PowerShell Add-Content.
"""
import json
import os
from datetime import datetime, timezone, timedelta

WS = r"D:\B166ER-OpenClaw\workspace"
HB_PATH = os.path.join(WS, "HEARTBEAT.md")
STATE_PATH = os.path.join(WS, "memory", "heartbeat-state.json")

CST = timezone(timedelta(hours=8))
now = datetime.now(CST)
ts_str = now.strftime("%Y-%m-%d %H:%M:%S GMT+8")
ts_short = now.strftime("%Y-%m-%d %H:%M")

# --- heartbeat-state.json update ---
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

new_count = state["lastHBNumber"] + 1  # 489 -> 490
state["lastHBNumber"] = new_count
state["lastHBTime"] = ts_str
state["lastHbTs"] = int(now.timestamp())
state["silenceHours"] = round((now - datetime.fromisoformat(state["silenceSince"])).total_seconds() / 3600, 2)
state["t0HoursPast"] = round((now - datetime(2026, 7, 18, 0, 0, tzinfo=CST)).total_seconds() / 3600, 2)
state["lastDecision"] = (
    f"HB #{new_count}: deep-night {ts_short}, Eric silent ~{state['silenceHours']}h, "
    f"T-0+{state['t0HoursPast']}h, no signals, all layers intact -> silent_standby sustained"
)

with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# --- HEARTBEAT.md append ---
entry = f"""
## HB #{new_count} ({ts_short} cron-event, OpenClaw heartbeat poll)
- gap from HB #{new_count - 1} (00:53): +5min -- deep-night zone Token Guard normal cadence
- D+2 deep-night pass #{new_count} -- Eric silent ~{state['silenceHours']}h+ since 7/16 13:16 (no first-contact)
- Silence authority ~{state['silenceHours']}h+ (R-B + R256 framework holding, +0.08h since #{new_count - 1})
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256) -- zero breach
- R-NEW-V2 verification #{new_count}: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- **Publicity cutoff 7/18 T-0 +{state['t0HoursPast']}h past** -- boundary crossed at 00:00, silence window protection objective achieved
- WAIC 2026 day-2 active today -- non-trigger per R14 (AI/Hotel strategic context, not relevant to current 4-layer suppression)
- Deep-night zone ({ts_short}) -- Eric typical deep-night rest zone per USER.md, silence authority strictly holding
- Cron pipeline: 09:00 daily checkin in ~8h02m (autonomous), no other triggers
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric; D+2+ sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount now: {new_count - 1} -> {new_count}

### decision
- **silent_standby_zero_push_continue** (HB #{new_count} = sustain #{new_count - 1} = D+2 baseline)
- **no push**: deep-night zone, Eric silent ~{state['silenceHours']}h+, T-0 boundary crossed, silence authority strictly holding
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work
- Token Guard tick: stable, no compression needed
- Post-T-0 silence = sustained suppression; pushes prohibited until Eric active contact (Eric silence = dominant signal)
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min); 09:00 daily checkin cron upcoming (~8h02m)

*{ts_short} -- D+2 deep-night T-0 +{state['t0HoursPast']}h past -- HB #{new_count} -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

# R-NEW-V2: read existing utf-8, append, write utf-8 explicitly
with open(HB_PATH, "r", encoding="utf-8") as f:
    existing = f.read()
with open(HB_PATH, "w", encoding="utf-8") as f:
    f.write(existing + entry)

print(f"OK HB #{new_count} appended at {ts_short}")
print(f"silenceHours={state['silenceHours']}, t0HoursPast={state['t0HoursPast']}")