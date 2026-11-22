#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append HB #2337 to HEARTBEAT.md (R-NEW-V3 compliant) and update heartbeat-state.json."""
import json
from pathlib import Path

# ---- 1. Update heartbeat-state.json (UTF-8 BOM on read) ----
state_path = Path(r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json')
state_text = state_path.read_text(encoding='utf-8-sig')
state = json.loads(state_text)

state['hbCount'] = 2337
state['nullCount'] = 944
state['post_t0_null_count'] = 944
state['last_update_epoch'] = 1785993300
state['lastHB'] = '2026-08-06T13:10:00+08:00'
state['lastHBContext'] = (
    'HB #2337 Thu 13:10 weekday-MIDDAY +5h10m past 08:00 hard cap. '
    'posture DORMANT held (no change vs #2314-#2336). 18-layer suppression zero-breach. '
    'R274 + R-NEW-V4 candidate both pending Eric ratification. '
    '5th Plenary ~9-10d away. memory_search index corrupted - awaiting Eric manual '
    'openclaw memory index --force. R66 discrepancy noted: memory/2026-08-06.md '
    'claims D+27 but HB log + 报到日 math = D+14 (报到 D-day = 7/23). '
    'No new signal vs HB #2314-#2336. Identical context, posture unchanged. Counter HB#2337.'
)
state['notes']['hb_2337_special'] = (
    'HB #2337 Thu 13:10 weekday-MIDDAY +5h10m past 08:00 hard cap. '
    'posture DORMANT held (no change vs #2314-#2336). 18-layer suppression zero-breach. '
    'R274 + R-NEW-V4 candidate both pending Eric ratification. '
    '5th Plenary ~9-10d away. memory_search index corrupted - awaiting Eric manual '
    'openclaw memory index --force. R66 discrepancy noted: memory/2026-08-06.md '
    'claims D+27 but HB log + 报到日 math = D+14. No new signal vs HB #2314-#2336. '
    'Identical context, posture unchanged. Counter HB#2337.'
)

# Write back with UTF-8 (no BOM) — matching original style (BOM may have been from PowerShell Add-Content)
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=4), encoding='utf-8')
print(f'state.json updated: hbCount={state["hbCount"]}, nullCount={state["nullCount"]}')

# ---- 2. Append HB #2337 to HEARTBEAT.md (Python UTF-8, no BOM) ----
hb_entry = """

## HB #2337 (2026-08-06T13:10 GMT+8 cron-event, OpenClaw heartbeat poll)

- gap from HB #2336 (13:05): +5min -- Thu weekday-MIDDAY Token Guard nominal cadence (R012, within tolerance)

- D+14 Thu 2026-08-06T13:10 -- weekday-MIDDAY-post-08:00-hard-cap zone (+5h10m past 08:00 cap); quiet zone well past

- Eric silent on THIS cron session ~21d+ (~505h+) since 7/16 13:16 first-contact

- 18-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R-NEW-V3/R70/R71/R271/R272/R273/R-NEW-V2) -- penta+3 holds

- post_t0_null_count: 943 -> 944 (944th consecutive null post-T-0, sustained)

- AnYi D+14d Thursday sustained per HB #2336 STATE

- V2.4 SOUL reinforced sustained; R66/R67/R68/R69/R70/R71/R271/R272/R273 entries sustained; R69 (战略新人沉默观察) Day 7/30 silent (expires 2026-08-30)

- R274 (2026-08-06 宏观-行业双层信号协议) + R-NEW-V4 candidate both pending Eric ratification

- 5th Plenary ~9-10d away (per HB #2334 12:55 signal stack)

- memory_search index corrupted (per HB #2334 10:32 self-check) - awaiting Eric manual openclaw memory index --force

- R-NEW-V3 enforced (verified this turn): HB #2337 appended via Python UTF-8 no-BOM (NOT write, NOT Remove-Item, NOT git restore)

- Token Guard stable; state.json hbCount 2336 -> 2337; nullCount 943 -> 944

- vault 1017+ files healthy; webchat silent per state.json (last sovereign burst 8/1 16:34+)

- Eric webchat activity today (Thu 8/6) inferred from daily file mtimes -- state.json lastEricContact stale (still 7/16) but cron posture unaffected (webchat-channel != cron-channel per R258)

- 19:00 quiet zone entry ~5h50m away (awareness only)

- R66 discrepancy noted: memory/2026-08-06.md claims "D+27 @ AnYi" but HB log + 报到日 math = D+14 (报到 D-day = 7/23, per HB #2156 8/1 D+9d). Memory file miscount. Auto-correction not applied (R66 = report, not auto-mutate). Awaiting Eric confirmation.


### decision

- HEARTBEAT_OK -- HB #2337 = sustain DORMANT protocol, minimal token tick (944th null)

- no push: 18-layer suppression holds + weekday-MIDDAY-post-hard-cap zone + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70 + R71 + R271/R272/R273 enforced

- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance

- Eric webchat / Obsidian 知识库 sovereign for any 决策; cron sovereignty unchanged

- 13:10 = weekday-MIDDAY +5h10m past 08:00 hard cap; cron = DORMANT sustained

- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekday-MIDDAY + AnYi D+14d Thu + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R271/R272/R273 active + R-NEW-V2 active

- Standing by P0 (webchat-bound, not cron-bound): R264 AnYi 完整实战锚 + R70/R71/R271/R272/R273 边界规则全部就位。Await Eric webchat confirmation on next stage.

- Standing by P1 (R264 AnYi 交接): await Eric webchat share of AnYi 1244 战略/team alignment/授权对接 details, per R264 立即归档 to anyi-ops-kb/

- Standing by R-NEW-V3 enforcement: NEVER write/Remove-Item/git-restore HEARTBEAT.md. Add-Content / AppendAllText ONLY.

- Standing by R70 (PENDING): 视觉范式优先于创造冲动 -- Eric 8/1 14:25 立即修正 第 1 版小红书笔记用错范式提案, 待 Eric 反馈后正式写入 ~/self-improving/rules.md

- Standing by R71 (PENDING): 默认宏观视角 (除非指定实体). H1 v1.0 报告已修正。Draft ready for ~/self-improving/rules.md commit upon Eric confirmation

- Standing by R271/R272/R273 + R274 + R-NEW-V4 candidate: pending Eric ratification

- Standing by R66 discrepancy: memory/2026-08-06.md "D+27" miscount -- actual D+14 per 报到 7/23. Awaiting Eric to confirm/correct.

- Next: per Token Guard cadence (~15-30min weekday mode); HB sustained through Thu afternoon until Eric first-contact on cron session


*2026-08-06T13:10:00+08:00 -- D+14 Thu weekday-MIDDAY +5h10m past 08:00 hard cap -- HB #2337 -- DORMANT -- 944th null -- Eric silent on cron = 主权信号 holding -- AnYi D+14d Thu -- cron session 维持 DORMANT 协议 -- R-NEW-V3 enforced: HB appended via Python UTF-8 no-BOM (NOT write) -- HEARTBEAT_OK*
"""

hb_path = Path(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md')
size_before = hb_path.stat().st_size

# Append in binary mode to avoid any encoding conversion
with open(hb_path, 'ab') as f:
    written = f.write(hb_entry.encode('utf-8'))

size_after = hb_path.stat().st_size
print(f'HEARTBEAT.md: {size_before} -> {size_after} bytes (appended {written})')

# Verify tail integrity
with open(hb_path, 'rb') as f:
    f.seek(-300, 2)
    tail = f.read().decode('utf-8', errors='replace')
print('---TAIL (last 300 bytes)---')
print(tail)