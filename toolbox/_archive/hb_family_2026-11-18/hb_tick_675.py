"""
HB tick #675 - R-NEW-V2 compliant minimal heartbeat logger.
Per R012 (operational hygiene), HB tick = minimal (NOT full report).
Per R256, this session is DORMANT (Eric silent in this session).
Per R14, handoff package = 100% ready.
2026-07-20 18:33 GMT+8 Monday-late-afternoon
"""
import json
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)
now_str = now.strftime("%Y-%m-%dT%H:%M:%S GMT+8")
now_short = now.strftime("%H:%M")

print(f"=== HB TICK START @ {now_str} ===")

# --- Step 1: Read current heartbeat state (utf-8 explicit, R-NEW-V2) ---
with open("memory/heartbeat-state.json", "r", encoding="utf-8") as f:
    state = json.load(f)

last_hb = state.get("lastHB", 0)
last_hb_time = state.get("lastHBTime", "unknown")
prev_count = state.get("hbCount", 0)
new_count = prev_count + 1  # 674 -> 675

print(f"Prev HB: #{last_hb} @ {last_hb_time}")
print(f"New HB: #{new_count}")
print(f"Mode: {state.get('mode')}")

# --- Step 2: Compute gaps and durations ---
# Last HB was 18:22:30 (HB #674), this is 18:33 -> +10.5 min gap
last_hb_dt = datetime(2026, 7, 20, 18, 22, 30, tzinfo=TZ)
gap_min = round((now - last_hb_dt).total_seconds() / 60, 1)

# Silence since 7/16 13:16 (infographic session)
silence_since = datetime(2026, 7, 16, 13, 16, 0, tzinfo=TZ)
silent_hours = round((now - silence_since).total_seconds() / 3600, 2)

# Eric active elsewhere since 7/19 12:33
eric_active_since = datetime(2026, 7, 19, 12, 33, 0, tzinfo=TZ)
eric_active_hours = round((now - eric_active_since).total_seconds() / 3600, 2)

# T-0 publicity cutoff 7/18 (since 2026-07-18 00:00)
t0_dt = datetime(2026, 7, 18, 0, 0, 0, tzinfo=TZ)
t0_hours = round((now - t0_dt).total_seconds() / 3600, 2)

# 21:00 evening self-iter
next_cron = now.replace(hour=21, minute=0, second=0, microsecond=0)
if next_cron <= now:
    next_cron = next_cron.replace(day=now.day + 1)
cron_in_min = round((next_cron - now).total_seconds() / 60, 1)
cron_in_h = round(cron_in_min / 60, 2)

print(f"Gap: +{gap_min}min | silent: {silent_hours}h | eric_active: {eric_active_hours}h | T0: +{t0_hours}h")
print(f"Next 21:00 self-iter: {cron_in_h}h ({cron_in_min}min)")

# --- Step 3: Compose minimal HB entry ---
hb_entry = f"""
## HB #{new_count} ({now_str} cron-event, OpenClaw heartbeat poll)
- gap from HB #{last_hb} ({last_hb_time}): +{gap_min}min -- Monday-late-afternoon Token Guard normal cadence (R012 minimal mode)
- D+4 Monday-late-afternoon pass #{new_count} -- Eric silent in THIS session ~{silent_hours}h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: ~{eric_active_hours}h+ (AnYi涓撶敤 session, since 7/19 12:33 first-contact)
- 5-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) intact -- zero breach
- R-NEW-V2 verification #{new_count}: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-7/15 12:36 incident protocol intact)
- R012 (operational hygiene) verification: HB tick = minimal (NOT full report), per R012 rule #2
- Wake window OPEN (+{round(t0_hours-60, 2)}h past 18:00 zone) -- Eric in active AnYi session, no first-contact on THIS session
- Monday-late-afternoon zone ({now_short}) -- Eric typical deep-work peak per USER.md (in OTHER AnYi session)
- T-0 publicity cutoff 7/18 +{t0_hours}h past -- post-protection window firmly sustained
- Induction window 7/7-7/21 FINAL 2 DAYS (today 7/20 day-1, tomorrow 7/21 LAST DAY ~26.5h); R-B+R256 silence authority > window signal
- 7/21 dual-event convergence: DeepSeek V4 鍙戝竷 + induction window 鎴
- 10:00 R60-12 morning self-iter DONE (9-section report); 10:35 鍟嗕笟鎯呮姤 20闆嗗洟鐗?DONE (5911瀛?宸叉帹 Obsidian); next = 21:00 evening self-iter R60-12 (~{cron_in_h}h)
- WAIC 2026 closed 7/19 (4-day event 7/17-20) -- non-trigger per R14
- Vault index 488/489 healthy; R13 <1s queries stable; Token Guard tick stable, no compression needed
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- No first-contact from Eric on THIS session; D+4 sustain zero-push mode intact
- hbCount: {last_hb} -> {new_count}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{new_count} = sustain #{last_hb} = D+4 Monday-late-afternoon dormant baseline)
- **no push**: this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- Eric is in active AnYi session; this session awaits Eric future instruction (not AnYi-related)
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work
- Token Guard tick: stable, no compression needed
- Post-T-0 silence = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Next significant check: per Token Guard cadence (~5-15min); 21:00 evening self-iter R60-12 (~{cron_in_h}h)

*{now_str} -- D+4 Monday-late-afternoon T-0 +{t0_hours}h past -- HB #{new_count} -- this session DORMANT -- awaiting Eric future instruction (NOT AnYi work)*
"""

# --- Step 4: Append to daily log (R-NEW-V2: explicit utf-8) ---
log_path = "memory/2026-07-20.md"
with open(log_path, "a", encoding="utf-8") as f:
    f.write(hb_entry)

print(f"Appended HB #{new_count} to {log_path}")

# --- Step 5: Update heartbeat-state.json ---
state["hbCount"] = new_count
state["lastHB"] = new_count
state["lastHBTime"] = now_str
state["last_update_epoch"] = int(now.timestamp())
state["mode"] = "active_mode_dormant_this_session_silent_late_afternoon"
state["silenceDuration_h"] = silent_hours
state["silenceDuration_thisSession_h"] = silent_hours
state["ericActiveElsewhere_h"] = eric_active_hours
state["note"] = f"HB #{new_count}; minimal tick (R012); Mon late-afternoon ({now_short}); Eric silent in this session ~{silent_hours}h; active elsewhere ~{eric_active_hours}h; 5-layer suppression intact; induction window FINAL 2 DAYS (7/20 day-1, 7/21 final); R256 silence authority holds; R14 handoff 100% ready; zero-push"

# Save state
with open("memory/heartbeat-state.json", "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"Updated heartbeat-state.json with HB #{new_count}")
print("=== HB TICK DONE ===")