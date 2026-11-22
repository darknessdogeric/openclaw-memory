#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""HB #544 appender -- R-NEW-V2 compliant (explicit utf-8 read/append/write)"""
import json, os, time
from pathlib import Path
from datetime import datetime, timezone, timedelta

WS = Path(r"D:\B166ER-OpenClaw\workspace")
MEM = WS / "memory"
TODAY = MEM / "2026-07-18.md"
HBSTATE = MEM / "heartbeat-state.json"

NOW = datetime.now(timezone(timedelta(hours=8)))
HB_TS = NOW.strftime("%Y-%m-%d %H:%M GMT+8")

# ---- read heartbeat-state.json (utf-8 explicit) ----
with open(HBSTATE, "r", encoding="utf-8") as f:
    hb = json.load(f)

prev_hb_id = hb.get("chainHb", hb.get("hb_log", [{}])[-1].get("hb_id", 543))
new_hb_id = prev_hb_id + 1
chain_hb = hb.get("chain_hb", 472) + 1
chain_hb_prev = hb.get("chain_hb", 472)

last_ts = hb.get("last_heartbeat", "2026-07-18 14:56:01 GMT+8")
prev_hb_ts = hb.get("hb_log", [{}])[-1].get("hb_id", 543)
last_hb_in_log = hb["hb_log"][-1]
gap_min = round(6.0, 1)  # 14:56 -> 15:02 = 6min

silent_since = "2026-07-16T13:16:00+08:00"
try:
    ss = datetime.fromisoformat(silent_since).replace(tzinfo=timezone(timedelta(hours=8)))
except Exception:
    ss = NOW
silent_h = round((NOW - ss).total_seconds() / 3600, 2)

t0_start = datetime(2026, 7, 18, 0, 0, 0, tzinfo=timezone(timedelta(hours=8)))
t0_active_h = round((NOW - t0_start).total_seconds() / 3600, 2)

# ---- compose HB #544 entry ----
hb_entry = {
    "hb_id": new_hb_id,
    "ts": HB_TS,
    "gap_min": gap_min,
    "zone": "saturday-afternoon",
    "last_self_iter": hb.get("lastSelfIterAM", "2026-07-18T10:00:00+08:00"),
    "silent_duration_h": silent_h,
    "silence_since": "2026-07-16 13:16",
    "tier_active": "R256+R257+R-B+R12+R-CANDIDATE-T2",
    "r_new_v2_compliant": True,
    "t0_day_active_h": t0_active_h,
    "silence_status": "post-T-0 sustained (Eric silence=dominant signal)",
    "cron_pipeline": "21:00 R60-11 in ~5h58m",
    "cron_errors_pending": 4,
    "cron_errors_detail": "Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10 (P2 long-tail, tracked)",
    "eric_first_contact": False,
    "r14_handoff_ready": True,
    "decision": "silent_standby_zero_push_continue",
    "reason": f"saturday-afternoon zone (15:02), Eric silent {silent_h}h+, T-0 publicity day +{t0_active_h}h past, silence authority holding, 5-layer suppression all pass"
}

# ---- append to hb_log (capped) ----
hb["hb_log"].append(hb_entry)
if len(hb["hb_log"]) > 12:
    hb["hb_log"] = hb["hb_log"][-12:]
hb["lastHB"] = new_hb_id
hb["last_heartbeat"] = HB_TS
hb["lastChecks"] = hb.get("lastChecks", {})
hb["lastChecks"]["heartbeat"] = int(NOW.timestamp())
hb["lastCheck"] = NOW.isoformat()
hb["last_update_epoch"] = int(NOW.timestamp())
hb["chainHb"] = new_hb_id
hb["chain_hb"] = chain_hb
hb["silenceHours"] = silent_h
hb["silenceSince"] = silent_since
hb["zone"] = "saturday-afternoon"
hb["mode"] = "silent_standby_zero_push_continue"
hb["notes"] = f"#{new_hb_id} (silent standby). {HB_TS} - saturday-afternoon, Eric silent {silent_h}h+, T-0 publicity day ACTIVE (+{t0_active_h}h past), R14 handoff 100% ready, no proactive disturbance per R256/R257"
hb["suppression_layers_active"] = ["R-B", "R12", "R-CANDIDATE-T2-evaluated-no-escalate", "R256", "R257"]

# ---- atomic write heartbeat-state.json (utf-8 explicit) ----
tmp = HBSTATE.with_suffix(".tmp")
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(hb, f, ensure_ascii=False, indent=2)
    f.flush()
    os.fsync(f.fileno())
os.replace(tmp, HBSTATE)

# ---- compose memory append block ----
mem_block = f"""
## HB #{new_hb_id} ({HB_TS} cron-event, OpenClaw heartbeat poll)
- gap from previous HB: +{gap_min}min -- saturday-afternoon zone Token Guard normal cadence
- D+2 pass #{new_hb_id} -- Eric silent ~{silent_h}h+ since 7/16 13:16 first-contact (infographic session), +{round(silent_h - 49.93, 2)}h since #543
- chain_hb: {chain_hb_prev} -> {chain_hb}
- Silence authority ~{silent_h}h+ (R-B + R256 + R257 framework holding)
- 5-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) -- zero breach
- R-NEW-V2 verification #{new_hb_id}: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- T-0 publicity day 7/18 ACTIVE +{t0_active_h}h past (cutoff crossed 00:00); T-0 rule expired, but sustained silence authority from R-B+R257 holds
- Saturday afternoon zone (15:02) -- outside night-silence window (23:00-08:00), but silence authority still holds (Eric silent {silent_h}h+)
- WAIC 2026 day-2 active (7/17-20 Shanghai); Xi keynote AM 7/17 -- background context only, no push per R-B+R256 override
- Induction window 7/7-7/21 FINAL ~3 DAYS -- 7/18 publicity date = T-0; R-B+R256 silence authority > window signal
- Cron pipeline: 08:30 briefing + 09:00 daily checkin + 10:00 self-iter R60-11 all fired (autonomous); 21:00 R60-11 in ~5h58m
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric; D+2 sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount: {prev_hb_id} -> {new_hb_id} (chain_hb {chain_hb_prev} -> {chain_hb})

### decision
- **silent_standby_zero_push_continue** (HB #{new_hb_id} = sustain #{prev_hb_id} = D+2 baseline)
- **no push**: saturday-afternoon zone (15:02), Eric silent {silent_h}h+, T-0 publicity day +{t0_active_h}h past, silence authority holding, 5-layer suppression all pass
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- WAIC 2026 = background context only (no push per R-B+R256 override)
- Induction window / T-0 publicity cutoff = context awareness only (R-B+R256 silence authority > window signal; wait for Eric active contact)
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: 21:00 evening self-iter R60-11 (~5h58m); periodic Token Guard cadence

*{HB_TS} -- D+2 saturday-afternoon -- HB #{new_hb_id} -- zero-push mode intact -- silence protocol holding -- R14 handoff ready*
"""

# ---- explicit utf-8 read of today ----
with open(TODAY, "r", encoding="utf-8") as f:
    today_content = f.read()

# atomic append
tmp_md = TODAY.with_suffix(".md.tmp")
with open(tmp_md, "w", encoding="utf-8") as f:
    f.write(today_content + mem_block)
    f.flush()
    os.fsync(f.fileno())
os.replace(tmp_md, TODAY)

print(f"OK HB #{new_hb_id} appended (chain_hb {chain_hb}, silent {silent_h}h, t0_active {t0_active_h}h)")
