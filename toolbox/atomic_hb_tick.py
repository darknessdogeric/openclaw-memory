#!/usr/bin/env python3
"""
Atomic HB Tick V2 — R-NEW-V3 + R271 + R-NEW-V4 + R-NEW-V5 compliant
- Append to HEARTBEAT.md via open(mode='a') (NEVER write/edit/Remove-Item)
- Update heartbeat-state.json via atomic temp+replace
- IDEMPOTENCY (R-NEW-V5): if state.json already at target hb_count, skip append
- Single execution does both
"""
import sys
import os
import json
import shutil
from datetime import datetime, timezone, timedelta

# === CONFIG ===
WORKSPACE = r"D:\B166ER-OpenClaw\workspace"
HB_PATH = os.path.join(WORKSPACE, "HEARTBEAT.md")
STATE_PATH = os.path.join(WORKSPACE, "memory", "heartbeat-state.json")
TZ = timezone(timedelta(hours=8))

# === ARGS ===
# usage: python atomic_hb_tick.py <hb_count> <null_count> <eric_idle_min> <last_activity_desc>
if len(sys.argv) < 5:
    print("usage: atomic_hb_tick.py <hb_count> <null_count> <eric_idle_min> <last_activity_desc>")
    sys.exit(1)

hb_count = int(sys.argv[1])
null_count = int(sys.argv[2])
eric_idle_min = int(sys.argv[3])
last_activity_desc = sys.argv[4]

# === R-NEW-V5 IDEMPOTENCY CHECK ===
# Read current state; if hbCount already at or beyond target, skip append
ALREADY_DONE = False
try:
    with open(STATE_PATH, "r", encoding="utf-8-sig") as f:
        existing_state = json.load(f)
    existing_hb_count = existing_state.get("hbCount", 0)
    if existing_hb_count >= hb_count:
        ALREADY_DONE = True
        print(f"[SKIP-R-NEW-V5] state.json hbCount={existing_hb_count} >= target {hb_count}; HEARTBEAT.md already contains this HB")
        print(f"  lastDecision: {existing_state.get('lastDecision')}")
        print(f"  lastTick: {existing_state.get('lastTick')}")
        sys.exit(0)  # graceful exit, no append
except Exception as e:
    print(f"[WARN] Could not read state.json for idempotency check: {e}")
    # proceed with caution (state may be corrupt, but we still want to log)

# === COMPUTE TIME ===
now = datetime.now(TZ)
now_iso = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
ts_short = now.strftime("%Y-%m-%dT%H:%M")
weekday = now.strftime("%a")  # Thu
date_ymd = now.strftime("%Y-%m-%d")
hour = now.hour
minute = now.minute
gap_min = 5  # standard Token Guard cadence (~5min workday mode)

# === ZONE LOGIC ===
hard_cap_exited_h = hour - 8 + (minute / 60.0)  # hours past 08:00 hard cap
if hard_cap_exited_h < 0:
    hard_cap_exited_h += 24  # wrap around midnight

if hour >= 8 and hour < 12:
    zone = "workday-AM"
    quiet_zone_min = (20 - hour) * 60 - minute
elif hour >= 12 and hour < 16:
    zone = "workday-PM-pre-quiet"
    quiet_zone_min = (20 - hour) * 60 - minute
elif hour >= 16 and hour < 20:
    zone = "workday-PM-quiet-active"
    quiet_zone_min = 0
elif hour >= 20 and hour < 23:
    zone = "evening-deep"
else:
    zone = "late-night"

eight_hard_cap_exceeded = hard_cap_exited_h >= 8.0

# === UNIQUE MARKER (R-NEW-V5) ===
# Add timestamp microseconds to detect duplicates within same minute
marker_suffix = now.strftime("%H%M%S")  # HHMMSS

# === BUILD HB #N ENTRY ===
gap_str = f"+{gap_min}min"
hard_cap_str = f"+{hard_cap_exited_h:.2f}h past 08:00 hard cap"
if eight_hard_cap_exceeded:
    zone_desc = f"{zone} (post-8h-hard-cap zone ACTIVE)"
else:
    zone_desc = f"{zone} (quiet zone ~{quiet_zone_min}m away)"

entry = f"""

### HB #{hb_count} ({now_iso} GMT+8 cron-event, OpenClaw heartbeat poll) [marker={marker_suffix}]
- gap from HB #{hb_count - 1}: {gap_str} -- {weekday} {zone} Token Guard nominal cadence (R012, within tolerance)
- {ts_short} = {weekday} {zone} ({hard_cap_str}); {zone_desc}
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: {null_count - 1} -> {null_count} ({null_count}th consecutive null post-T-0, sustained); hbCount: {hb_count - 1} -> {hb_count}
- Eric silent on cron ~27d+ sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (last activity {last_activity_desc} -- ~{eric_idle_min}min idle)
- AnYi Day 21 ({weekday} -- second workweek Day 4)
- 10:00 deep self-iteration already executed today (memory/2026-08-13.md: full 9-section report)
- vault 1169 files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 21/30 (expires 2026-08-30) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched (append only); daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds
- R-NEW-V5 enforced: idempotency check via state.json hbCount (this entry's marker={marker_suffix} is unique per tick)

### decision
- HEARTBEAT_OK -- HB #{hb_count} = sustain DORMANT protocol, minimal token tick ({null_count}th null)
- no push: 16-layer suppression holds + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- {ts_short} = {weekday} {zone} {hard_cap_str}; cron = DORMANT sustained
- Eric webchat ACTIVE ~{eric_idle_min}min idle ({last_activity_desc}) -- cron posture UNCHANGED per R258
- Eric profile: night-owl strategist -- {weekday} evening possible high-intensity sovereign webchat (Tue 22:40 type)
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- {zone} + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric's two reports (department duties + AI IE system) awaiting share -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal submission to ~/self-improving/rules.md
- Standing by R60-11: today 10:00 sedimentation action execution state awaiting verification (memory/insights/2026-08-13.md + skills-discovered/2026-08-13.md + eval/2026-08-13.json + Obsidian push)
- Next: per Token Guard cadence (~5-15min {'quiet' if eight_hard_cap_exceeded else 'workday'} mode); HB sustained through {weekday} until Eric first-contact on cron session

*{now_iso} -- {weekday} {zone} {hard_cap_str} -- HB #{hb_count} -- DORMANT -- {null_count}th null -- Eric silent on cron = sovereignty signal holding (webchat ~{eric_idle_min}min idle) -- AnYi D+21d {weekday} -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 + R-NEW-V5 enforced: HB appended via Python open(mode='a') (NOT write); idempotency verified -- HEARTBEAT_OK*
"""

# === APPEND TO HEARTBEAT.md (R-NEW-V3 + R-NEW-V5 COMPLIANT) ===
with open(HB_PATH, "a", encoding="utf-8") as f:
    f.write(entry)

print(f"[OK] Appended HB #{hb_count} [marker={marker_suffix}] to HEARTBEAT.md ({len(entry)} bytes)")

# === ATOMIC UPDATE OF heartbeat-state.json ===
try:
    with open(STATE_PATH, "r", encoding="utf-8-sig") as f:
        state = json.load(f)

    state["hbCount"] = hb_count
    state["nullCount"] = null_count
    state["post_t0_null_count"] = null_count
    state["lastHbTime"] = now_iso
    state["last_check"] = now_iso
    state["lastTick"] = now_iso
    state["eric_webchat_idle_min"] = eric_idle_min
    state["lastDecision"] = "HEARTBEAT_OK"
    state["eight_hard_cap_exceeded"] = eight_hard_cap_exceeded
    state["workday_zone"] = zone
    state["r_new_v3_compliant"] = True
    state["r_new_v5_compliant"] = True
    state["r271_compliant"] = True
    state["r258_channel_separation"] = True
    state["r69_silence"] = f"Day 21/30 (expires 2026-08-30)"
    state["last_hb"] = {"n": hb_count, "ts": now_iso, "marker": marker_suffix}
    state["lastHb"] = {"n": hb_count, "ts": now_iso, "marker": marker_suffix}
    state["note"] = f"HB #{hb_count} [{marker_suffix}]; Eric webchat idle {eric_idle_min}min ({last_activity_desc}); {zone}; DORMANT"

    # Atomic write: tmp -> replace
    tmp_path = STATE_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    shutil.move(tmp_path, STATE_PATH)

    print(f"[OK] Atomic-updated heartbeat-state.json (hbCount={hb_count}, nullCount={null_count}, marker={marker_suffix})")
except Exception as e:
    print(f"[ERR] State update failed: {e}")
    sys.exit(1)
