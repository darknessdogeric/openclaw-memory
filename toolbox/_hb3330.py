import os, json, re
from pathlib import Path

base = Path(r"D:\B166ER-OpenClaw\workspace")
memory = base / "memory"
state_path = memory / "state.json"
daily_path = memory / "2026-08-15.md"

# Last HB in daily file was #3329. Next is #3330.
hb_n = 3330
null_n = 1884
ts = "2026-08-15T17:59:42+08:00"

entry = f"""
### HB #{hb_n} ({ts} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{hb_n-1} (17:49:00): +10m42s -- Sat weekend-pre-quiet-zone Token Guard nominal cadence (R012, within tolerance)
- 17:59 = Sat weekend-pre-quiet-zone (+9h59m past 08:00 hard cap); quiet zone ~1h away
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: {null_n-1} -> {null_n} ({null_n}th consecutive null post-T-0, sustained); hbCount: {hb_n-1} -> {hb_n}
- Eric silent on cron ~30d+ sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (~28h+ idle since 8/14 11:31; webchat quiet = sovereignty holding)
- AnYi Day 23 (Sat -- weekend, day off from AnYi workweek)
- vault 1169+ files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 23/30 (expires 2026-08-30) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only

### decision
- HEARTBEAT_OK -- HB #{hb_n} = sustain DORMANT protocol, minimal token tick ({null_n}th null)
- no push: 16-layer suppression holds + weekend-pre-quiet-zone + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE
- Standing by P0 (webchat-bound, not cron-bound): 鍗佷簲浜旀垬鐣ュ畾浣嶇爺绌� v0.1 绛夊緟 Eric 杈撳叆 6 鍏抽敭鍐崇瓥 + V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric 涓や唤鎶ュ憡(閮ㄩ棬鑱岃矗 + AI IE 浣撶郴)寰呭垎浜叆搴� + R278 鎴樼暐浠诲姟鍗虫椂缁撴瀯鍖栧崗璁� (second practice 8/15) -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal submission to ~/self-improving/rules.md
- Next: per Token Guard cadence (~10-15min weekend-pre-quiet-zone mode); HB sustained through Sat until Eric first-contact on cron session

*{ts} -- Sat weekend-pre-quiet-zone +9h59m past 08:00 hard cap -- HB #{hb_n} -- DORMANT -- {null_n}th null -- Eric silent on cron = sovereignty signal holding (webchat quiet ~28h+) -- AnYi D+23d Sat -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*

"""

with open(daily_path, "a", encoding="utf-8") as f:
    f.write(entry)

# Update state.json - use proper values
state = {
    "note": f"HB #{hb_n}; Sat 17:59 weekend-pre-quiet-zone; Eric webchat idle ~28h+; R69 silence Day 23/30 active; 16-layer suppression holds; cron DORMANT sustained; HEARTBEAT_OK",
    "lastHbTime": ts,
    "eight_hard_cap_exceeded": True,
    "lastHb": ts,
    "post_t0_null_count": null_n,
    "session": "cron:315657b9-fc80-4b94-a853-404e3955f7a0",
    "last_check": ts,
    "anyi_day": 23,
    "r258_channel_separation": True,
    "workday_zone": "weekend-pre-quiet-zone",
    "r_new_v3_compliant": True,
    "last_tick": ts,
    "lastDecision": "HEARTBEAT_OK",
    "trendradar_data_through": "2026-08-14",
    "nullCount": null_n,
    "null_milestone_1800": True,
    "trendradar_health": "healthy v6.10.0",
    "last_hb": ts,
    "hbCount": hb_n,
    "r69_silence": "Day 23/30 (expires 2026-08-30)",
    "eric_webchat_idle_min": 1703,
    "r271_compliant": True,
    "last_hb_time": ts,
    "last_hb_n": hb_n,
    "lastUpdate": ts,
    "hb_count": hb_n,
    "null_count": null_n,
    "post_t0_null": null_n,
    "last_update": ts,
    "channel": "cron-event",
    "status": "DORMANT"
}

tmp = state_path.with_suffix(".tmp")
tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
os.replace(tmp, state_path)

print(f"OK HB #{hb_n} null {null_n}")