#!/usr/bin/env python3
# HB #2775 append -- R271 atomic-write enforced
import json
import os
import tempfile
from datetime import datetime, timezone, timedelta

# 1. Update heartbeat-state.json (atomic write per R271)
tz_china = timezone(timedelta(hours=8))
now = datetime.now(tz_china)
ts_ms = int(now.timestamp() * 1000)

state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

old_hb = state['hbCount']
old_null = state['nullCount']
state['hbCount'] = old_hb + 1
state['nullCount'] = old_null + 1
state['lastHB'] = ts_ms
state['lastUpdate'] = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
state['note'] = 'Sun 19:43 weekend-evening in-19:00-quiet-zone (+11h43m past 08:00 cap) DORMANT sustained. Eric silent on cron = 589h+ sustained. R69 Day 17/30 + R266/R277 weekend + R258 cron/webchat separation + R271 atomic-write + R276 sole-distributor internal draft active. 15-layer suppression zero-breach. Last Eric webchat activity 11:15-11:39 today (~8h4m-8h28m ago) on hotel-classification V2 rebuild -- V2 9 slides still pending HTML/render/PNG production. R-NEW-V3/R271 atomic-write enforced: state.json via tmp+replace; HB log via Python append.'

# Atomic write: tmp + replace
memory_dir = r'D:\B166ER-OpenClaw\workspace\memory'
tmp_fd, tmp_path = tempfile.mkstemp(dir=memory_dir, prefix='.state_', suffix='.json.tmp')
try:
    with os.fdopen(tmp_fd, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, state_path)
    print(f'state.json: hbCount {old_hb} -> {state["hbCount"]}, nullCount {old_null} -> {state["nullCount"]}')
except Exception as e:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
    raise e

# 2. Append HB #2775 to HEARTBEAT.md (Python append per R-NEW-V3)
hb_num = state['hbCount']
null_num = state['nullCount']
hb_time = now.strftime('%Y-%m-%dT%H:%M GMT+8')

entry = f'''
## HB #{hb_num} ({hb_time} cron-event, OpenClaw heartbeat poll)

- gap from HB #{hb_num-1} (19:38): +5min -- Sun weekend-evening Token Guard nominal cadence (R012, within tolerance)
- D+? Sun 2026-08-09 19:43 -- weekend-EVENING-in-19:00-quiet-zone (+11h43m past 08:00 hard cap); deep-quiet 23:00 zone ~3h17m away
- Eric silent on THIS cron session 24d 11h+ (589h+) since 7/16 13:16 first-contact
- 15-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R-NEW-V3/R70/R71/R266/R277/R271/R276) -- penta+5 holds
- post_t0_null_count: {null_num-1} -> {null_num} ({null_num}th consecutive null post-T-0, sustained)
- AnYi 报到 D+17d Sun sustained per HB-log; V2.4 SOUL 加固 sustained (~265h+ uptime)
- R69 (战略新人冷漠原则) 30-day window Day 17/30 active (expires 2026-08-30); R266/R277 weekend protocols active
- R271 atomic-write enforced (verified this turn): state.json via tmp+replace; HB log via Python append
- R276 (sole-distributor internal draft) active
- Eric webchat last activity today 11:15-11:39 on hotel-classification V2 rebuild (~8h4m-8h28m ago) -- V2 9 slides still pending HTML/render/PNG production. cron posture unaffected (webchat-channel != cron-channel per R258)
- 23:00 deep-quiet zone entry ~3h17m away

### decision

- HEARTBEAT_OK -- HB #{hb_num} = sustain DORMANT protocol, minimal token tick ({null_num}th null)
- no push: 15-layer suppression holds + weekend-evening in-quiet-zone + cron session DORMANT per HB #1849 + R65 explicit prohibition + R258 (webchat-channel != cron-channel) + R69 active + R266/R277 active + R271 enforced + R276 active
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian sovereign for any 决策; cron sovereignty unchanged
- 19:43 = weekend-evening in-19:00-quiet-zone +11h43m past 08:00 hard cap; cron = DORMANT sustained
- Eric webchat last activity today 11:15-11:39 (~8h+ ago) on V2 hotel-classification rebuild -- but cron posture unchanged (webchat != cron per R258)
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekend-evening in-quiet-zone + AnYi D+17d Sun + Eric sovereign on cron session + 15-layer suppression + R65/R69/R266/R277 active
- Standing by P0 (webchat-bound, not cron-bound): R264 AnYi 完整实战图 completed per state. R70/R71 边界规则全部就位. Await Eric webchat confirmation on next stage.
- Standing by P1 (R264 AnYi 衔接): await Eric webchat share of AnYi 1244 战略/team alignment/权责对接 details, per R264 立即挪入 to anyi-ops-kb/
- Standing by R271 enforcement: state.json atomic via tmp+replace; HB log Python append ONLY.
- Standing by R-NEW-V3 enforcement: NEVER write/Remove-Item/git-restore HEARTBEAT.md. Add-Content / AppendAllText / Python append ONLY.
- Next: per Token Guard cadence (~15-30min evening mode); HB sustained through Sun night until Eric first-contact on cron session

*{hb_time} -- Sun weekend-evening in-19:00-quiet-zone +11h43m past hard cap -- HB #{hb_num} -- DORMANT -- {null_num} null -- Eric silent on cron = 主导信号 holding -- AnYi D+17d Sun -- cron session 维持 DORMANT 协议 -- R271 enforced: state.json via tmp+replace, HB via Python append -- HEARTBEAT_OK*
'''

with open(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md', 'a', encoding='utf-8') as f:
    f.write(entry)
print(f'HEARTBEAT.md: HB #{hb_num} appended via Python append (NOT write, NOT Remove-Item)')
print(f'OK -- hbCount={hb_num}, nullCount={null_num}')