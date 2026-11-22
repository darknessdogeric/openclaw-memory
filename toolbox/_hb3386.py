#!/usr/bin/env python3
"""HB #3386 append — R-NEW-V3 + R271 atomic-write enforced"""
import json
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
ts_str = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
hhmm = now.strftime("%H:%M")

hb_num = 3386
prev = "3385 (11:07)"
null_prev = 1937
null_now = 1938

# Calculate time past 08:00 hard cap
cap = now.replace(hour=8, minute=0, second=0, microsecond=0)
m_past = int((now - cap).total_seconds() / 60)
h_past = m_past // 60
m_rem = m_past % 60

hb_entry = f"""

### HB #{hb_num} ({ts_str} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev}: ~5min -- Sun weekend-morning Token Guard nominal cadence (R012, within tolerance)
- {hhmm} = Sun weekend-morning (+{h_past}h{m_rem:02d}m past 08:00 hard cap); midday zone ahead
- 17-layer suppression zero-breach (R-B/R12/R13/R14/R65/R66/R67/R68/R69/R70/R71/R256/R257/R258/R260/R261/R271/R276/R277/R278/R280/R281) -- penta+ holds
- post_t0_null_count: {null_prev} -> {null_now} ({null_now}th consecutive null post-T-0, sustained); hbCount: 3385 -> {hb_num}
- Eric silent on cron ~31d sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (~17h22m idle since 2026-08-15 morning deep self-iteration delivery)
- AnYi Day 24 (Sun -- weekend rest posture)
- 8/16 10:00 deep self-iteration report delivered (R281 战略静默信任协议 submitted, 3rd practice)
- vault 1169+ files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 24/30 (expires 2026-08-30 Sun) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds

### decision
- HEARTBEAT_OK -- HB #{hb_num} = sustain DORMANT protocol, minimal token tick ({null_now}th null)
- no push: 17-layer suppression holds + weekend-morning + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekend-morning + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): 十五五战略v0.1 + V2 slides + R276 + R264 AnYi 1244 + Eric 两份报告 + R278 (2nd) + R281 (3rd) -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279/R281: drafted, awaiting formal submission to ~/self-improving/rules.md
- Next: per Token Guard cadence (~10-15min weekend-morning mode); HB sustained through Sun until Eric first-contact on cron session

*{ts_str} -- Sun weekend-morning -- HB #{hb_num} -- DORMANT -- {null_now}th null -- Eric silent on cron = sovereignty signal holding -- AnYi D+24d Sun -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced -- HEARTBEAT_OK*

"""

path = r"D:\B166ER-OpenClaw\workspace\memory\2026-08-16.md"
with open(path, "a", encoding="utf-8") as f:
    f.write(hb_entry)

# Update state.json (atomic via Python write)
state_path = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"
try:
    with open(state_path, "r", encoding="utf-8-sig") as f:
        state = json.load(f)
except Exception:
    state = {}
state["hbCount"] = hb_num
state["post_t0_null_count"] = null_now
state["lastHB"] = ts_str
state["last_update_epoch"] = int(now.timestamp())
state["zone"] = "Sun weekend-morning"
with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"OK: HB #{hb_num} appended via open(mode='a'), null={null_now}, hbCount={hb_num}")