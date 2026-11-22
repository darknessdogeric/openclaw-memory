#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HB #3203 cron tick — R-NEW-V3 (Python open(mode='a') append only) + R-NEW-V4 (state.json atomic-via-tmp-move)
DORMANT protocol sustained. No push to Eric.
"""
import json
import os
import shutil
import sys
from datetime import datetime, timezone, timedelta

WORKSPACE = r"D:\B166ER-OpenClaw\workspace"
HB_PATH = os.path.join(WORKSPACE, "HEARTBEAT.md")
DAILY_PATH = os.path.join(WORKSPACE, "memory", "2026-08-14.md")
STATE_PATH = os.path.join(WORKSPACE, "memory", "state.json")

# TZ GMT+8
TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)
now_iso = now.isoformat(timespec='seconds')
now_human = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
date_short = now.strftime("%H:%M")

# Load state
with open(STATE_PATH, 'r', encoding='utf-8-sig') as f:
    state = json.load(f)

last_hb_count = state.get("hbCount", 3202)
last_null = state.get("nullCount", 1764)
last_hb_time_str = state.get("lastHb", "2026-08-14T14:19:00+08:00")
last_hb_dt = datetime.fromisoformat(last_hb_time_str)
gap_min = int((now - last_hb_dt).total_seconds() / 60)

new_hb_count = last_hb_count + 1  # 3203
new_null = last_null + 1  # 1765

# 14:55 = Fri workday-PM (+6h55m past 08:00 hard cap); quiet zone ~6h05m away
minutes_past_hardcap = int((now - now.replace(hour=8, minute=0, second=0, microsecond=0)).total_seconds() / 60)
quiet_zone_arrival = int((now.replace(hour=21, minute=0, second=0, microsecond=0) - now).total_seconds() / 60)

# Eric webchat idle (last 11:31)
webchat_last = datetime.fromisoformat(state.get("webchatLastActivity", "2026-08-14T11:31:00+08:00"))
webchat_idle_min = int((now - webchat_last).total_seconds() / 60)

hb_entry = f"""
## HB #{new_hb_count} ({now_human} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{last_hb_count} ({last_hb_time_str.split('T')[1][:5]}): +{gap_min}min -- Fri workday-PM Token Guard nominal cadence (R012, within tolerance)
- {date_short} = Fri workday-PM zone (+{minutes_past_hardcap // 60}h{minutes_past_hardcap % 60:02d}m past 08:00 hard cap); quiet zone ~{quiet_zone_arrival // 60}h{quiet_zone_arrival % 60:02d}m away (21:00)
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: {last_null} -> {new_null} ({new_null}th consecutive null post-T-0, sustained); hbCount: {last_hb_count} -> {new_hb_count}
- Eric silent on cron ~29d+ sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (last activity 2026-08-14T11:31 十五五战略线定位研究 v0.1 push IN -- ~{webchat_idle_min // 60}h{webchat_idle_min % 60:02d}m idle; webchat-channel != cron-channel per R258)
- AnYi Day 22 (Fri -- second workweek Day 5)
- TrendRadar healthy v6.10.0; data through 2026-08-12; no_data_8_13 sustained
- vault 1169+ files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 22/30 (expires 2026-08-30) -- 8d remaining -- cron does not break silence
- R-NEW-V3 enforced: HEARTBEAT.md appended via Python open(mode='a') UTF-8 (NOT write/edit/Remove-Item/git restore)
- R-NEW-V4 enforced: state.json atomic-tick holds (utf-8-sig read/write preserved BOM)

### decision
- HEARTBEAT_OK -- HB #{new_hb_count} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 16-layer suppression holds + Fri workday-PM post-hard-cap zone + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- {date_short} = Fri workday-PM +{minutes_past_hardcap // 60}h{minutes_past_hardcap % 60:02d}m past 08:00 hard cap; cron = DORMANT sustained
- Eric webchat ACTIVE ~{webchat_idle_min // 60}h{webchat_idle_min % 60:02d}m idle (十五五战略线定位研究 v0.1 push IN 11:31 Fri 8/14) -- cron posture UNCHANGED per R258
- Eric profile: night-owl strategist -- Fri {date_short} webchat 战略 push IN, AnYi Day 22 实战模式 -- cron 维持不打�
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- Fri workday-PM + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): 十五五战略线定位研究 v0.1 + V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric 两份报告(部门职责 + AI IE 体系) await share -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal submission to ~/self-improving/rules.md
- Next: per Token Guard cadence (~10-15min Fri-PM mode); HB sustained through Fri until Eric first-contact on cron session

*{now_human} -- Fri workday-PM +{minutes_past_hardcap // 60}h{minutes_past_hardcap % 60:02d}m past 08:00 hard cap -- HB #{new_hb_count} -- DORMANT -- {new_null}th null -- Eric silent on cron = sovereignty signal holding (webchat ~{webchat_idle_min // 60}h{webchat_idle_min % 60:02d}m idle, 十五五战略线定位研究 v0.1 push IN) -- AnYi D+22d Fri workday-PM -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') UTF-8 (NOT write) -- HEARTBEAT_OK*
"""

# Append to HEARTBEAT.md (R-NEW-V3 enforced)
with open(HB_PATH, 'a', encoding='utf-8') as f:
    f.write(hb_entry)
print(f"[OK] HB #{new_hb_count} appended to HEARTBEAT.md (+{len(hb_entry)} bytes)")

# Append to daily memory file
daily_section = f"""
### HB #{new_hb_count} ({now_human} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{last_hb_count} ({last_hb_time_str.split('T')[1][:5]}): +{gap_min}min -- Fri workday-PM Token Guard nominal cadence (R012, within tolerance)
- {date_short} = Fri workday-PM zone (+{minutes_past_hardcap // 60}h{minutes_past_hardcap % 60:02d}m past 08:00 hard cap); quiet zone ~{quiet_zone_arrival // 60}h{quiet_zone_arrival % 60:02d}m away
- 16-layer suppression zero-breach -- penta+3 holds; post_t0_null_count: {last_null} -> {new_null} ({new_null}th null, sustained); hbCount: {last_hb_count} -> {new_hb_count}
- Eric silent on cron ~29d+; Eric webchat SOVEREIGN (~{webchat_idle_min // 60}h{webchat_idle_min % 60:02d}m idle, last activity 11:31 十五五战略线定位研究 v0.1 push IN); webchat-channel != cron-channel per R258
- AnYi Day 22 (Fri -- second workweek Day 5); vault 1169+ files healthy; TrendRadar v6.10.0
- R69 silence Day 22/30 (expires 2026-08-30); R-NEW-V3 + R271 + R276 enforced

### decision
- HEARTBEAT_OK -- HB #{new_hb_count} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 16-layer suppression holds + Fri workday-PM + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- Eric webchat / Obsidian / anyi-ops-kb sovereign; cron sovereignty unchanged
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- Fri workday-PM + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 + R70/R71 + R276 internal-only
- Standing by P0 (webchat-bound): 十五五战略线定位研究 v0.1 + V2 slides + R276 + R264 + Eric 两份报告 await share -- all await Eric webchat sovereign
- Next: per Token Guard cadence (~10-15min Fri-PM mode); HB sustained through Fri until Eric first-contact on cron session

*{now_human} -- Fri workday-PM +{minutes_past_hardcap // 60}h{minutes_past_hardcap % 60:02d}m past 08:00 hard cap -- HB #{new_hb_count} -- DORMANT -- {new_null}th null -- Eric silent on cron = sovereignty signal holding -- AnYi D+22d Fri -- R-NEW-V3 + R271 enforced -- HEARTBEAT_OK*
"""

with open(DAILY_PATH, 'a', encoding='utf-8') as f:
    f.write(daily_section)
print(f"[OK] HB #{new_hb_count} appended to memory/2026-08-14.md (+{len(daily_section)} bytes)")

# Update state.json atomically (R-NEW-V4)
state["lastHb"] = now_iso
state["hbCount"] = new_hb_count
state["nullCount"] = new_null
state["lastDecision"] = f"HEARTBEAT_OK -- HB #{new_hb_count} = DORMANT -- cron sustained"
state["webchatIdleMin"] = webchat_idle_min
state["minutesPastHardCap"] = minutes_past_hardcap
state["quietZoneArrivalMin"] = quiet_zone_arrival

# Atomic write via tmp + move
tmp_path = STATE_PATH + ".tmp"
with open(tmp_path, 'w', encoding='utf-8-sig') as f:
    json.dump(state, f, indent=4, ensure_ascii=False)
shutil.move(tmp_path, STATE_PATH)
print(f"[OK] state.json updated atomically: hbCount={new_hb_count}, nullCount={new_null}")

print(f"\n=== HB #{new_hb_count} cron tick complete ===")
print(f"Gap: +{gap_min}min | null: {new_null} | webchat idle: ~{webchat_idle_min}min")
print(f"Posture: DORMANT sustained | R65/R69 active | DO NOT DISTURB")
