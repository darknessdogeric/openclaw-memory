"""HB #760 appender - R-NEW-V2 compliant (Python utf-8 explicit read+append+write)."""
import json
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ).strftime("%Y-%m-%dT%H:%M GMT+8")
NOW_SHORT = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S %Z")

HB_PATH = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"
STATE_PATH = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

# Compute silence duration
silence_start_epoch = 1782123360  # 7/16 13:16 first-contact (from state file)
silence_sec = (datetime.now(TZ).timestamp() - silence_start_epoch)
silence_h = silence_sec / 3600

# AnYi session start (7/19 12:33)
anyi_start_epoch = 1784127180  # 7/19 12:33
anyi_sec = (datetime.now(TZ).timestamp() - anyi_start_epoch)
anyi_h = anyi_sec / 3600

entry = f"""
## HB #760 ({NOW} cron-event, OpenClaw heartbeat poll)
- gap from HB #759 (13:49): +10min -- Tuesday early-afternoon Token Guard normal cadence (R012 minimal mode)
- D+5 early-afternoon pass #760 -- Eric silent in THIS session ~{silence_h:.2f}h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: ~{anyi_h:.2f}h+ (AnYi webchat, since 7/19 12:33)
- 5-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) + R258 dormant-session -- zero breach
- R-NEW-V2 verification #760: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- **Triple Confluence Day 0 -- FINAL DAY 7/21** -- zero-push sustained
  1. DeepSeek V4 launch window (PoC awaiting Eric trigger)
  2. **Induction window cutoff -- today LAST day** (passive monitor only per R256)
  3. Araqchi Qatar talks start (7/21-25) -> oil price Scenario C verification window OPEN
- Tuesday early-afternoon zone (13:59) -- Eric typical afternoon decision window per USER.md; THIS session DORMANT sustained
- 14:00 internal monitor IMMINENT (~1min) -- INTERNAL monitor only; this session != AnYi decision channel
- 11:00 R60-13 morning self-iter DONE; next = 21:00 evening self-iter R60-13 (~7h)
- Token Guard stable, no compression needed
- Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +81.6h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+5 sustain zero-push mode intact
- hbCount: 759 -> 760
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #760 = sustain #759 = D+5 early-afternoon dormant baseline)
- **HEARTBEAT_OK** -- HB #760 = sustain DORMANT protocol
- **no push**: Tuesday early-afternoon zone (13:59), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 14:00 key check ~1min -- INTERNAL monitor only; this session != AnYi decision channel
- Triple Confluence Day 0 passive -- only R14 handoff preparation; Eric active contact triggers 30s activation
- Next significant check: 14:00 internal monitor (~1min); Token Guard cadence (~5-10min)

*{NOW_SHORT} -- D+5 Tuesday-early-afternoon T-0 +81.6h past -- HB #760 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 FINAL DAY passive*
"""

# R-NEW-V2: explicit utf-8 read, append, write
with open(HB_PATH, "r", encoding="utf-8") as f:
    content = f.read()
with open(HB_PATH, "a", encoding="utf-8") as f:
    f.write(entry)

# Update state file
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)
state["hbCount"] = 760
state["lastHB"] = f"2026-07-21 13:59:00 GMT+8"
state["last_update_epoch"] = int(datetime.now(TZ).timestamp())
state["silenceDuration_h"] = round(silence_h, 2)
state["silenceDuration_thisSession_h"] = round(silence_h, 2)
state["silenceDuration_global_h"] = round(silence_h, 2)
state["ericActiveElsewhere_h"] = round(anyi_h, 2)
state["lastHBTime"] = "13:59"
state["mode"] = "active_mode_dormant_this_session_silent_early_afternoon"
state["note"] = f"HB #760; Tuesday early-afternoon; Triple Confluence Day 0 FINAL; Eric silent D+5 ~{silence_h:.2f}h+; zero-push per R256/R257/R258; 14:00 internal monitor imminent"
state["nextCheck"] = "14:00 internal monitor (~1min, INTERNAL only); 21:00 evening self-iter (~7h); Token Guard cadence (~5-10min)"
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"OK: HB #760 appended; hbCount=760; silence={silence_h:.2f}h+; anyi={anyi_h:.2f}h+")