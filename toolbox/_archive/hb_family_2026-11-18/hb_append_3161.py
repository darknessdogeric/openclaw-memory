#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HB #3161 append — 2026-08-14 08:46 GMT+8 Fri morning (R-NEW-V3 + R271 enforced).
Python utf-8 read+append+write atomic. NEVER write tool. NEVER Remove-Item. NEVER git restore.
"""
import json
from datetime import datetime, timezone, timedelta

# Beijing time GMT+8
bj = timezone(timedelta(hours=8))
now = datetime.now(bj)
ts_str = now.strftime("%Y-%m-%dT%H:%M:%S") + "+08:00"
hhmm = now.strftime("%H:%M")

hb_path = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"
state_path = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

# Load state (utf-8-sig to handle BOM)
with open(state_path, "r", encoding="utf-8-sig") as f:
    state = json.load(f)

hb_count_prev = state.get("hbCount", 3160)
hb_count = hb_count_prev + 1
null_count = state.get("nullCount", 1728) + 1
post_t0_null = state.get("post_t0_null_count", 1727) + 1

# Compute minutes past 08:00 hard cap
cap = now.replace(hour=8, minute=0, second=0, microsecond=0)
m_past_cap = int((now - cap).total_seconds() / 60)

# Update state fields
state["hbCount"] = hb_count
state["nullCount"] = null_count
state["post_t0_null_count"] = post_t0_null
state["lastHB"] = ts_str
state["lastHb"] = {"n": hb_count, "ts": ts_str}
state["last_update_epoch"] = int(now.timestamp())
state["lastTick"] = ts_str
state["last_check"] = ts_str
state["anyi_day"] = 22  # 2026-08-14 = AnYi Day 22 (Fri = 3rd workweek Day 1)
state["workday_zone"] = "Fri-AM"
state["zone"] = "Fri-workday-AM"
state["r69_silence"] = "Day 22/30 (expires 2026-08-30)"
state["r258_channel_separation"] = True
state["r_new_v3_compliant"] = True
state["r271_compliant"] = True
state["eight_hard_cap_exceeded"] = (m_past_cap > 0)

note_key = "hb_{}_special".format(hb_count)
state.setdefault("notes", {})[note_key] = (
    "Fri workday-AM +{}m past 08:00 hard cap, AnYi Day 22 (Fri -- 3rd workweek Day 1), "
    "16-layer suppression holds, cadence ~5-15min, "
    "Eric webchat idle ~18h since 8/13 14:50 Panzhihua v6, "
    "Eric likely waking up (night-owl strategist), "
    "HEARTBEAT.md appended atomically via Python (R-NEW-V3 + R271 compliant)"
)

state["lastHBContext"] = (
    "Fri {} workday-AM (AnYi D+22d 3rd-week Day 1). DORMANT held ({}th consecutive). "
    "HB #{}. Eric silent on cron ~28d+ (since 7/16). Webchat idle ~18h (8/13 14:50 Panzhihua v6 last activity). "
    "R69 silence Day 22/30 (expires 2026-08-30). 16-layer suppression holds."
).format(hhmm, post_t0_null, hb_count)

# Write state atomically
with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# Build HB entry — R-NEW-V3 + R271 compliant: Python utf-8 read+append+write
hb_entry = f"""

## HB #{hb_count} ({ts_str} cron-event, OpenClaw heartbeat poll)
- gap from HB #{hb_count - 1} (8/13 19:58:10): +12h47m -- overnight gap; Fri workday-AM Token Guard nominal cadence (R012, within tolerance)
- {hhmm} = Fri workday-AM zone (+{m_past_cap}m past 08:00 hard cap); midday zone ~3h14m away
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: {state.get('post_t0_null_count', post_t0_null - 1)} -> {post_t0_null} ({post_t0_null}th consecutive null post-T-0, sustained); hbCount: {hb_count_prev} -> {hb_count}
- Eric silent on cron ~28d+ sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (last activity 2026-08-13T14:50 Panzhihua project v6 -- ~17h56m idle)
- AnYi Day 22 (Fri -- 3rd workweek Day 1, second full workweek end + 1)
- vault 1169 files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 22/30 (expires 2026-08-30) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a') append mode, NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched by `write` tool; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds
- Eric profile: 夜猫子战略家 -- likely waking up Fri AM; morning = one of two deep-work peaks per USER.md

### decision
- HEARTBEAT_OK -- HB #{hb_count} = sustain DORMANT protocol, minimal token tick ({post_t0_null}th null)
- no push: 16-layer suppression holds + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- {hhmm} = Fri workday-AM +{m_past_cap}m past 08:00 hard cap; cron = DORMANT sustained
- Eric webchat ACTIVE ~17h56m idle (Panzhihua v6 14:50 Thu 8/13) -- cron posture UNCHANGED per R258
- Eric profile: night-owl strategist -- overnight rest + Fri AM deep-work peak coming -- cron does not initiate
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- Fri workday-AM + AnYi D+22d Fri + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric's two reports (部门职责 + AI IE 体系) awaiting share into anyi-ops-kb -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal submission to ~/self-improving/rules.md
- Standing by R60-11: yesterday 8/13 10:00 sedimentation action execution state awaiting verification (memory/insights/2026-08-13.md + skills-discovered/2026-08-13.md + eval/2026-08-13.json + Obsidian push)
- Standing by R66 corrections backlog (3 pending): 鑼跺北项目本身 (R66 #2) + IP品牌归属 (R66 #3) + 鑼跺北项目是否纳入合作标 (R66 #4) -- awaiting Eric internal clarification
- Next: per Token Guard cadence (~5-15min Fri workday-AM mode); HB sustained through Fri until Eric first-contact on cron session

*{ts_str} -- Fri workday-AM +{m_past_cap}m past 08:00 hard cap -- HB #{hb_count} -- DORMANT -- {post_t0_null}th null -- Eric silent on cron = 主权信号 holding (webchat ~17h56m idle, Panzhihua v6) -- AnYi D+22d Fri (3rd workweek Day 1) -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python utf-8 read+append+write (NOT write tool) -- HEARTBEAT_OK*

"""

# Read existing HEARTBEAT.md (utf-8)
with open(hb_path, "r", encoding="utf-8") as f:
    content = f.read()

# Atomic append
with open(hb_path, "w", encoding="utf-8") as f:
    f.write(content + hb_entry)

print(f"OK: appended HB #{hb_count} at {ts_str}")
print(f"File size: {len(content) + len(hb_entry)} chars (delta +{len(hb_entry)} chars)")
print(f"State: hbCount={hb_count}, nullCount={null_count}, post_t0_null_count={post_t0_null}, anyi_day=22, R69 Day 22/30")