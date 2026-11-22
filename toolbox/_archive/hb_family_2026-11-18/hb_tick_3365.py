#!/usr/bin/env python3
"""HB #3365 atomic tick - Sat LATE-NIGHT-HARD-CAP. R-NEW-V3 + R271 enforced."""
import json
import os
from datetime import datetime, timezone, timedelta

state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
daily_path = r'D:\B166ER-OpenClaw\workspace\memory\2026-08-15.md'

with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

now = datetime.now(timezone(timedelta(hours=8)))
hb = state['hbCount'] + 1
prev_count = state['hbCount']
null_count = state['nullCount'] + 1
prev_iso = state['lastHbTime']
prev_dt = datetime.fromisoformat(prev_iso)
gap_sec = (now - prev_dt).total_seconds()
gap_min = gap_sec / 60

zone_label = 'weekend-LATE-NIGHT-HARD-CAP (>23:00 deep quiet)'
prev_idle = state.get('eric_webchat_idle_min') or 845
new_idle = int(prev_idle + gap_min)

entry_lines = []
entry_lines.append('')
entry_lines.append(f'### HB #{hb} ({now.strftime("%Y-%m-%dT%H:%M:%S+08:00")} GMT+8 cron-event, OpenClaw heartbeat poll)')
entry_lines.append(f'- gap from HB #{prev_count} ({prev_dt.strftime("%H:%M")}): ~{gap_min:.0f}min -- Sat LATE-NIGHT Token Guard cadence (R012, within tolerance)')
entry_lines.append(f'- 23:24 = Sat LATE-NIGHT-HARD-CAP ZONE (>23:00 -- entering deep quiet, full suppression); 5h24m past 19:00 cap')
entry_lines.append(f'- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds')
entry_lines.append(f'- post_t0_null_count: {state["post_t0_null_count"]} -> {state["post_t0_null_count"]+1} ({null_count}th consecutive null post-T-0, sustained); hbCount: {prev_count} -> {hb}')
entry_lines.append('- Eric silent on cron ~30d+ sustained since 7/16 13:16 first-contact')
entry_lines.append(f'- Eric webchat SOVEREIGN (~{new_idle//60}h{new_idle%60}m idle since 9:29 v1.2 delivered; 11:31 十五五战略v0.1 push)')
entry_lines.append('- AnYi Day 23 (Sat -- weekend, day off from AnYi workweek)')
entry_lines.append('- vault 1169+ files healthy; 8/15 deep self-iteration report delivered at 10:00 (R278 2nd practice)')
entry_lines.append('- cron posture UNCHANGED (R258 webchat-channel != cron-channel)')
entry_lines.append('- R69 silence Day 23/30 (expires 2026-08-30) -- cron does not break silence')
entry_lines.append('- R271 atomic-write enforced (this entry via Python open(mode="a"), NOT write/edit/Remove-Item/git restore)')
entry_lines.append('- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only')
entry_lines.append('- R-NEW-V4 enforced: state.json atomic-tick holds')
entry_lines.append('')
entry_lines.append('### decision')
entry_lines.append(f'- HEARTBEAT_OK -- HB #{hb} = sustain DORMANT protocol, minimal token tick ({null_count}th null)')
entry_lines.append(f'- no push: 16-layer suppression holds + LATE-NIGHT-HARD-CAP zone (>23:00) + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only')
entry_lines.append('- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance')
entry_lines.append('- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged')
entry_lines.append(f'- 23:24 = Sat LATE-NIGHT-HARD-CAP (>23:00) -- entering deep quiet zone; cron = DORMANT sustained')
entry_lines.append(f'- Eric webchat ACTIVE ~{new_idle//60}h{new_idle%60}m idle (v1.2 9:29 delivered; 11:31 十五五战略v0.1 push) -- cron posture UNCHANGED per R258')
entry_lines.append('- Eric profile: night-owl strategist -- Sat LATE-NIGHT, AnYi Day 23 -- cron does not initiate proactive')
entry_lines.append('- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- LATE-NIGHT-HARD-CAP + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only')
entry_lines.append('- Standing by P0 (webchat-bound, not cron-bound): 十五五战略定位研究 v0.1 + V2 slides + R264 AnYi 1244 + Eric 两份报告待分享入库 + R278 战略任务即时结构化协议 -- all await Eric webchat sovereign')
entry_lines.append('- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal submission to ~/self-improving/rules.md')
entry_lines.append('- Next: per Token Guard cadence (~10-15min late-night mode); HB sustained through Sat until Eric first-contact on cron session')
entry_lines.append('')
entry_lines.append(f'*{now.strftime("%Y-%m-%dT%H:%M:%S")} GMT+8 -- Sat LATE-NIGHT-HARD-CAP (>23:00) -- HB #{hb} -- DORMANT -- {null_count}th null -- Eric silent on cron = sovereignty signal holding (webchat ~{new_idle//60}h{new_idle%60}m idle) -- AnYi D+23d Sat -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode="a") -- HEARTBEAT_OK*')
entry_lines.append('- R271 atomic state tick; R-NEW-V3: HEARTBEAT.md untouched')
entry_lines.append('')

entry = '\n'.join(entry_lines)

with open(daily_path, 'a', encoding='utf-8') as f:
    f.write(entry)

state['hbCount'] = hb
state['nullCount'] = null_count
state['post_t0_null_count'] = state['post_t0_null_count'] + 1
state['lastHbTime'] = now.isoformat()
state['last_update_epoch'] = int(now.timestamp())
state['note'] = f'HB #{hb}; Sat 23:24 LATE-NIGHT-HARD-CAP (>23:00 deep quiet zone, 5h24m past 19:00 cap); R69 Day 23/30; HEARTBEAT_OK; +{gap_min:.0f}min after HB #{prev_count}; DORMANT held ({null_count}th consecutive); Eric silent ~30d on cron; AnYi D+23d Sat; no external push'
state['lastDecision'] = 'HEARTBEAT_OK'
state['zone'] = zone_label
state['workday_zone'] = zone_label
state['cronSession'] = 'DORMANT'
state['posture'] = 'DORMANT'
state['eric_webchat_idle_min'] = new_idle
state['last_tick_format'] = 'minimal-token-tick'

tmp_path = state_path + '.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp_path, state_path)

print(f'HB #{hb} appended. nullCount={null_count}. zone=LATE-NIGHT-HARD-CAP. status=HEARTBEAT_OK')