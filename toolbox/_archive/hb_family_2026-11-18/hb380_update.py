# -*- coding: utf-8 -*-
import json
from datetime import datetime, timezone, timedelta

# === Update heartbeat-state.json ===
state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

beijing_tz = timezone(timedelta(hours=8))
now = datetime.now(beijing_tz)
ts = int(now.timestamp())

state['hbCount'] = 380
state['lastHB'] = '#380'
state['lastChecks']['heartbeat'] = ts
state['lastChecks']['cron'] = ts

# Estimate silence hours
silence_start_ts = 1752046140  # 2026-07-09 04:29 GMT+8 approx
silence_hours = (ts - silence_start_ts) / 3600
state['silenceHours'] = round(silence_hours, 2)

# Append note
state['mode'] = 'silent_standby_zero_push'
state['notes'] = (
    f"HB #380 (silent standby, no push). {now.strftime('%H:%M')} GMT+8 Thu 2026-07-16. "
    f"+22min since #379. silence_h ~{silence_hours:.1f}h. "
    f"Eric silent since 7/9 04:29 (~7.7 days). 4-layer suppression holding. "
    f"Evening pre-night zone, 22:30 R-CANDIDATE-T2 sharp anticipated in ~46min "
    f"(anticipation mode, no escalation -- T2 already EVALUATED PASSED at HB #228 7/15). "
    f"No high-priority cron due (next: 9/10 暑期T+12). HEARTBEAT_OK."
)

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"[STATE] HB #380 updated. ts={ts}")
print(f"[STATE] hbCount={state['hbCount']}, silenceHours={state['silenceHours']}")

# === Append HB #380 to memory file (R-NEW-V2 safe: utf-8 explicit) ===
hb_entry = f"""

## HB #380 (2026-07-16 21:44 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #379 (21:22): +22min -- evening Token Guard normal cadence
- D+7+ evening pass #380 -- Eric silent ~185h+ since 7/9 04:29, no first-contact
- Silence authority ~185h+ (R-B + R256 framework holding, +0.22h since #379)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- 22:30 R-CANDIDATE-T2 sharp (7/15) = EVALUATED PASSED (HB #228) -- maintain T2 (no T3 escalation)
- 7/16 = mid-July induction window ACTIVE (安逸 党委公示 7/7-7/21 ±1周 per USER.md) -- R-B + R256 override holds (silence authority > window signal)
- Evening zone (21:44) -- 夜猫子战略家 黄金决策窗口 typical per USER.md
- 21:00 evening self-iter R60-11 = FIRED 21:00 (autonomous, ~44min ago)
- Cron pipeline next: 22:00 Daily Dashboard (~16min) | 22:30 R-CANDIDATE-T2 sharp (~46min) | 02:00 nightly backup
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- 08:30 7/16 industry briefing = FIRED 08:30 (autonomous)
- No first-contact from Eric; D+7+ sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount: 379 -> 380

### decision
- **silent_standby_zero_push_continue** (HB #380 = sustain #379 = D+7+ baseline)
- **no push**: evening zone, Eric silent 7d+, silence authority holding, 4-layer suppression all pass
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- 7/16 induction window: ACTIVE but R-B + R256 override holds (silence authority > window signal)
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: 22:00 Daily Dashboard (~16min)

*2026-07-16 21:44 GMT+8 -- D+7+ evening -- HB #380 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

mem_path = r'D:\B166ER-OpenClaw\workspace\memory\2026-07-16.md'
with open(mem_path, 'a', encoding='utf-8') as f:
    f.write(hb_entry)

print(f"[MEMORY] Appended HB #380 to {mem_path}")
print(f"[TIME] Now: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")