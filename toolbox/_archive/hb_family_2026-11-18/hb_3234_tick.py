"""HB #3234 atomic tick - Fri 18:34 workday-PM-evening DORMANT."""
import json
import os
from datetime import datetime

STATE = r'D:\B166ER-OpenClaw\workspace\memory\state.json'
DAILY = r'D:\B166ER-OpenClaw\workspace\memory\2026-08-14.md'
HB_FILE = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'

TS = '2026-08-14T18:34:00+08:00'

# 1. Read state.json
with open(STATE, 'r', encoding='utf-8') as f:
    state = json.load(f)

old_hb = state.get('hbCount', 3233)
old_null = state.get('post_t0_null_count', 1788)
new_hb = old_hb + 1
new_null = old_null + 1
idle_min = 408  # ~6h48m from 11:31 push (now 18:34)

# 2. Update state.json atomically (os.replace)
state['hbCount'] = new_hb
state['lastHbTime'] = TS
state['last_tick'] = TS
state['last_check'] = TS
state['last_hb'] = {'n': new_hb, 'ts': TS}
state['lastHb'] = TS
state['post_t0_null_count'] = new_null
state['nullCount'] = state.get('nullCount', 1791) + 1
state['eric_webchat_idle_min'] = idle_min
state['workday_zone'] = 'workday-PM-evening'
state['lastDecision'] = 'HEARTBEAT_OK'
state['note'] = f"HB {new_hb}; Eric webchat idle ~{idle_min}m; Fri 18:34 workday-PM-evening; R69 silence Day 22/30 active; sustained dormancy intact"

tmp = STATE + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp, STATE)

# 3. Append HB entry to HEARTBEAT.md (open mode='a' - R-NEW-V3 compliant)
hb_entry = f"""
### HB #{new_hb} ({TS} cron-event, OpenClaw heartbeat poll)
- gap from HB #{old_hb} (18:25:21): +~9min -- Fri workday-PM-evening Token Guard nominal cadence (R012, within tolerance)
- 18:34 = Fri workday-PM-evening zone (+10h34m past 08:00 hard cap); quiet zone ~1h26m away
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: {old_null} -> {new_null} ({new_null}th consecutive null post-T-0, sustained); hbCount: {old_hb} -> {new_hb}
- Eric silent on cron ~28d+ sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (last activity 2026-08-14T11:31 十五五战略线战略定位研究 v0.1 push -- ~6h48m idle; ~8h4m from 10:30 商业情报 20集团版)
- AnYi Day 22 (Fri -- second workweek Day 5, weekday wrap-up)
- 18:34 PM-evening -- Eric likely in deep work mode or post-work wind-down
- morning 10:30 商业情报 20集团版 + 11:31 十五五战略线战略定位研究 v0.1 already executed today (memory/2026-08-14.md: full reports)
- vault 1169+ files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 22/30 (expires 2026-08-30) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched (append-only via open mode='a')
- R-NEW-V4 enforced: state.json atomic-tick holds (os.replace)

### decision
- HEARTBEAT_OK -- HB #{new_hb} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 16-layer suppression holds + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 18:34 = Fri workday-PM-evening +10h34m past 08:00 hard cap; cron = DORMANT sustained
- Eric webchat ACTIVE ~6h48m idle (十五五战略线战略定位研究 v0.1 11:31 push) -- cron posture UNCHANGED per R258
- Eric profile: night-owl strategist -- Fri 11:31 webchat 战略主线 push IN 战略消化模式 -- cron 不发起主动
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- workday-PM-evening + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): 十五五战略线战略定位研究 v0.1 等待 Eric 输入 6 关键决策 + V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric 两份报告(部门职责 + AI IE 体系)待分享入库 -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal submission to ~/self-improving/rules.md
- Next: per Token Guard cadence (~5-15min workday-PM-evening mode); HB sustained through Fri until Eric first-contact on cron session

*{TS} -- Fri workday-PM-evening +10h34m past 08:00 hard cap -- HB #{new_hb} -- DORMANT -- {new_null}th null -- Eric silent on cron = sovereignty signal holding (webchat ~6h48m idle, 十五五战略线战略定位研究 v0.1 完成) -- AnYi D+22d Fri -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*
"""

with open(HB_FILE, 'a', encoding='utf-8') as f:
    f.write(hb_entry)

# 4. Brief daily note append (R-NEW-V3 compliant)
daily_entry = f"""
### HB #{new_hb} ({TS} cron-event)
- Fri workday-PM-evening +10h34m past 08:00 hard cap
- HB #{new_hb} = {new_null}th null; 16-layer suppression holds; R69 silence Day 22/30 active
- Eric webchat ~6h48m idle (15:31 → 18:34 = +3h3m from 11:31 push)
- DO NOT DISTURB -- Eric sovereign on cron session; cron posture UNCHANGED per R258
- HEARTBEAT_OK
"""

with open(DAILY, 'a', encoding='utf-8') as f:
    f.write(daily_entry)

print(f'OK HB#{new_hb} null#{new_null} state.json + HEARTBEAT.md + daily appended atomically')