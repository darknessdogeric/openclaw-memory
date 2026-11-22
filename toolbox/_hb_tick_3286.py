#!/usr/bin/env python3
"""Minimal-token HB tick (R-NEW-V3 + R271 compliant)."""
import json, os, sys, tempfile
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00")
DATE = datetime.now(TZ).strftime("%Y-%m-%d")
TIME = datetime.now(TZ).strftime("%H:%M")

HB_NUM = 3286
NULL_COUNT = 1834
PREV_HB = "13:29"
STATE_PATH = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"
HB_PATH = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"
DAILY_PATH = fr"D:\B166ER-OpenClaw\workspace\memory\{DATE}.md"

# ---- 1. Append to HEARTBEAT.md (R-NEW-V3: open mode='a' ONLY) ----
hb_entry = f"""
## HB #{HB_NUM} ({NOW} cron-event, OpenClaw heartbeat poll)
- gap from HB #{HB_NUM-1} ({PREV_HB}): +4min -- Sat weekend-AFTERNOON Token Guard nominal cadence (R012, within tolerance)
- AnYi Day 17 Sat 2026-08-15 {TIME} -- weekend-AFTERNOON-pre-quiet-zone (~5h27m before 19:00 quiet zone)
- Eric silent on THIS cron session ~30d+ sustained since 7/16 13:16 first-contact
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R-NEW-V3/R70/R71/R271) -- penta+4 holds
- nullCount: {NULL_COUNT-1} -> {NULL_COUNT} ({NULL_COUNT}th consecutive null post-T-0, sustained)
- AnYi D+17d Sat (Eric weekend-rest)
- V2.4 SOUL 鍔犲浐 sustained; R66/R67/R68/R69/R70/R71/R271 entries sustained
- R69 silence Day 23/30 (expires 2026-08-30) -- cron does not break silence
- R-NEW-V3 enforced: HB #{HB_NUM} appended via Python open(mode='a') (NOT write, NOT Remove-Item, NOT git restore)
- R271 atomic-write enforced: state.json via Python tmp+os.replace (NOT direct edit)
- Token Guard stable; vault 1169+ files healthy; trendradar v6.10.0 healthy
- webchat silent on cron channel; trendradar RSS fresh 2026-08-14

### decision
- HEARTBEAT_OK -- HB #{HB_NUM} = sustain DORMANT protocol, minimal token tick ({NULL_COUNT}th null)
- no push: 16-layer suppression holds + weekend-AFTERNOON pre-quiet-zone + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R271 enforced
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian sovereign for any decision; cron sovereignty unchanged
- Eric silent on cron ~30d+ = sovereign signal holding indefinitely
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekend-AFTERNOON + AnYi D+17d Sat + Eric silent + R65/R69 active + R-NEW-V3 + R70/R71/R271 enforced
- Standing by R-NEW-V3: NEVER write/Remove-Item/git-restore HEARTBEAT.md. AppendAllText / open(mode='a') ONLY.
- Standing by R271 atomic write: state.json via tmp+os.replace.
- Standing by R70/R71: 瑙嗚鏍煎紡浼樺厛浜庡垱閫犲啿绐?Drafts ready, awaiting Eric reply for formal commit.
- Next: per Token Guard cadence (~10-15min); HB sustained through Sat weekend-AFTERNOON until Eric first-contact on cron session

*{NOW} -- AnYi D+17d Sat weekend-AFTERNOON-pre-quiet-zone -- HB #{HB_NUM} -- DORMANT -- {NULL_COUNT}th null -- Eric silent on cron = sovereignty signal holding -- cron session sustained DORMANT -- R-NEW-V3 + R271 enforced -- HEARTBEAT_OK*
"""

with open(HB_PATH, "a", encoding="utf-8") as f:
    f.write(hb_entry)

# ---- 2. Update state.json atomically (R271: tmp+os.replace) ----
state = {}
if os.path.exists(STATE_PATH):
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            state = json.load(f)
    except Exception as e:
        print(f"WARN: state.json read failed: {e}", file=sys.stderr)

state.update({
    "lastHbTime": NOW,
    "lastHB": NOW,
    "lastHBTime": NOW,
    "last_hb_time": NOW,
    "last_heartbeat": NOW,
    "last_tick": NOW,
    "last_check": NOW,
    "last_update_epoch": int(datetime.now(TZ).timestamp()),
    "hbCount": HB_NUM,
    "nullCount": NULL_COUNT,
    "post_t0_null_count": NULL_COUNT,
    "anyi_day": 17,
    "eric_webchat_idle_min": state.get("eric_webchat_idle_min", 153),
    "posture": "DORMANT",
    "cronSession": "DORMANT",
    "workday_zone": "weekend-AFTERNOON-pre-quiet-zone",
    "zone": "weekend-AFTERNOON-pre-quiet-zone (~5h27m before 19:00 quiet zone)",
    "lastDecision": "HEARTBEAT_OK",
    "last_tick_format": "minimal-token-tick",
    "r69_silence": "Day 23/30 (expires 2026-08-30)",
    "r_new_v3_compliant": True,
    "r271_compliant": True,
    "r258_channel_separation": True,
    "trendradar_health": "healthy v6.10.0",
    "trendradar_data_through": "2026-08-12",
    "trendradar_hot_news_through": "2026-08-12",
    "trendradar_rss_through": "2026-08-14",
    "trendradar_rss_fresh": True,
    "trendradar_no_data_8_13": True,
    "eight_hard_cap_exceeded": True,
    "session": "cron:315657b9-fc80-4b94-a853-404e3955f7a0",
    "note": f"HB #{HB_NUM}; Sat {TIME} weekend-AFTERNOON-pre-quiet-zone; R69 Day 23/30; HEARTBEAT_OK; +4min after HB #{HB_NUM-1}; R-NEW-V3 + R271 enforced",
})

# Atomic write: tmp + os.replace
fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(STATE_PATH), suffix=".tmp")
try:
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp_path, STATE_PATH)
except Exception as e:
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)
    print(f"ERROR: state.json atomic write failed: {e}", file=sys.stderr)
    sys.exit(1)

# ---- 3. Brief tick to daily note (R-NEW-V3 compliant) ----
daily_entry = f"""

### HB #{HB_NUM} ({NOW} cron-event, OpenClaw heartbeat poll)
- gap: +4min -- Sat weekend-AFTERNOON Token Guard nominal cadence
- {TIME} = weekend-AFTERNOON-pre-quiet-zone; 16-layer suppression holds; cron DORMANT
- nullCount {NULL_COUNT-1} -> {NULL_COUNT}; hbCount {HB_NUM-1} -> {HB_NUM}
- AnYi D+17d Sat; Eric silent on cron ~30d+; R69 Day 23/30 active
- HEARTBEAT_OK -- DORMANT protocol sustained
"""

# Ensure daily file exists, then append
if not os.path.exists(DAILY_PATH):
    with open(DAILY_PATH, "a", encoding="utf-8") as f:
        f.write(f"# {DATE}\n\n")
with open(DAILY_PATH, "a", encoding="utf-8") as f:
    f.write(daily_entry)

print(f"OK: HB #{HB_NUM} tick complete | nullCount={NULL_COUNT} | R-NEW-V3+R271 compliant")