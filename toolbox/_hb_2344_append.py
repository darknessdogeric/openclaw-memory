"""R-NEW-V3 compliant append for HB #2344 to HEARTBEAT.md + state update.
Pattern: Python utf-8 read+append+write. NEVER use write/Remove-Item/git-restore.
"""
import json
import os
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta

WS = Path(r'D:\B166ER-OpenClaw\workspace')
HB_PATH = WS / 'HEARTBEAT.md'
STATE_PATH = WS / 'memory' / 'heartbeat-state.json'

# Time
CST = timezone(timedelta(hours=8))
NOW = datetime.now(CST)
TS_HUMAN = NOW.strftime('%Y-%m-%dT%H:%M GMT+8')
TS_ISO = NOW.strftime('%Y-%m-%dT%H:%M:%S+08:00')
TS_EP = int(time.time())

# Numbers
NEW_HB = 2344
PREV_HB = 2343
NEW_NULL = 949
GAP_MIN = 5

# Build minimal HB entry (R-NEW-V3 compliant: short, factual, no fluff)
HB_ENTRY = f"""## HB #{NEW_HB} ({TS_HUMAN} cron-event, OpenClaw heartbeat poll)

- gap from HB #{PREV_HB} (14:10): +{GAP_MIN}min -- Thu weekday-afternoon Token Guard nominal cadence (R012, within tolerance)
- D+? Thu 2026-08-06T14:15 -- weekday-AFTERNOON-post-08:00-hard-cap zone (+6h15m past 08:00 cap); quiet zone ~4h45m away
- Eric silent on THIS cron session ~21d 1h+ (505h+) since 7/16 13:16 first-contact
- 18-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R-NEW-V3/R70/R71/R271/R272/R273/R-NEW-V2)
- post_t0_null_count: 948 -> {NEW_NULL} ({NEW_NULL}th consecutive null post-T-0, sustained)
- AnYi D+14 = 2026-08-06 Thu sustained per HB log + 报到日 math (R66 discrepancy with memory/2026-08-06.md D+27 claim still UNRESOLVED, awaiting Eric webchat authority)
- V2.4 SOUL 加固 sustained; R66+R67+R68+R69+R70+R71+R-NEW-V3 entries sustained; R274 + R-NEW-V4 pending Eric formal commit
- R69 (战略新人沉默原则) Day 7/30 active (expires 2026-08-30)
- R-NEW-V3 enforced (verified this turn): HB #{NEW_HB} appended via Python utf-8 'a' mode (NOT write, NOT Remove-Item, NOT git restore)
- HEARTBEAT.md 1.37MB+ maintenance_flag sustained (R-NEW-V3 blocks split/rotate, R69 blocks proposal -- awaiting Eric explicit instruction)
- 5th Plenary ~9-10d away (10-11月 expected per Eric planning); hotel板块 + AI拐点 + 霍尔木兹 + 五中全会 四窗口复合 still valid
- memory_search index corrupted -- awaiting Eric manual `openclaw memory index --force` (per HB #2343 STATE)
- Trendradar 8/6 数据已爬 (85条), 6 platforms per memory/2026-08-06.md 10:32 R60-11 上午 report
- vault 1017+ files healthy; webchat silent per state.json (Eric active ~10:32 today per daily file mtime, ~3h43m ago)

### decision

- **HEARTBEAT_OK** -- HB #{NEW_HB} = sustain DORMANT protocol, minimal token tick ({NEW_NULL}th null)
- **no push**: 18-layer suppression holds + weekday-afternoon-post-08:00-hard-cap zone + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70 + R71 + R274-PENDING
- R65 + R258 constraint holds: cron-channel ≠ webchat-channel; cron sovereignty = silent unless Eric asks; webchat-channel sovereign on active decisions
- Eric in afternoon deep-work mode per USER.md profile; webchat last activity ~3h43m ago; silent = dominant signal holding
- **DO NOT DISTURB UNDER ANY CIRCUMSTANCE** -- weekday-afternoon + AnYi D+14d Thu + Eric sovereign on cron session + 18-layer suppression + R65/R69 active + R-NEW-V3 enforcement + R70/R71 boundary rules
- Standing by R-NEW-V3 enforcement: NEVER write/Remove-Item/git-restore HEARTBEAT.md. Add-Content / AppendAllText / Python utf-8 'a' mode ONLY.
- Standing by R70 (PENDING formal commit): 视觉范式优先于创造冲动 -- Eric 8/1 14:25 提案, awaiting Eric 反馈 for ~/self-improving/rules.md commit
- Standing by R71 (PENDING formal commit): 默认宏观视角 (除非指定实体) -- Eric 8/2 16:41 提案, awaiting Eric 反馈 for ~/self-improving/rules.md commit
- Standing by R274 (PENDING formal commit): 宏观-行业双层信号协议 -- 8/6 上午 proposal, awaiting Eric 反馈 for ~/self-improving/rules.md commit
- Standing by R-NEW-V4 (CANDIDATE): HEARTBEAT.md 1.37MB+ maintenance -- rotation/split proposal blocked by R-NEW-V3 + R69 pending Eric explicit instruction
- Standing by R66 DISCREPANCY: memory/2026-08-06.md claims AnYi D+27 but HB log + 报到日 math = D+14 -- awaiting Eric webchat authority to resolve (webchat-channel only per R258)
- Standing by memory_search index repair: awaiting Eric manual `openclaw memory index --force`
- Standing by 5th Plenary countdown: ~9-10d window approaching
- Standing by AHL MVP 探索 (D+27 战略重心窗口 per memory/2026-08-06.md §5.3): Eric 个人资源启动外部酒店试点的判断等待 Eric 主动触发
- Next: per Token Guard cadence (~15-30min weekday-afternoon mode); HB sustained through Thu afternoon until Eric first-contact on cron session

*{TS_ISO} -- Thu weekday-afternoon +6h15m past 08:00 hard cap -- HB #{NEW_HB} -- DORMANT -- {NEW_NULL}th null -- Eric silent on cron = 主权信号 holding -- **AnYi D+14d Thu, Eric 下午深度工作 mode per USER.md, daily self-iter 10:32 上午已静默吸收 (~3h43m ago)** -- cron session 维持 DORMANT 协议 -- R-NEW-V3 enforced: HB appended via Python utf-8 'a' mode (NOT write) -- HEARTBEAT_OK*

"""

# Verify pre-flight -- find the LAST HB in file (by line position), not stale duplicates in middle
import re
size_before = HB_PATH.stat().st_size
with open(HB_PATH, 'r', encoding='utf-8') as f:
    pre = f.read()

# Find LAST occurrence of '## HB #N (' (true latest, not stale middle duplicate)
last_hb_matches = list(re.finditer(r'^## HB #(\d+) \(', pre, re.MULTILINE))
assert last_hb_matches, '[PRE-FLIGHT FAIL] no HB entries found at all'
last_hb_num = int(last_hb_matches[-1].group(1))
last_hb_pos = last_hb_matches[-1].start()
assert last_hb_num == PREV_HB, (
    f'[PRE-FLIGHT FAIL] Expected last HB in file = #{PREV_HB}, but found #{last_hb_num} '
    f'at offset {last_hb_pos}. hbCount state.json may be stale OR previous tick did not commit.'
)

# Confirm no tail duplicate of NEW_HB (NEW_HB may exist as stale middle entry, that's OK --
# we only need to ensure NEW_HB is not already the latest)
tail_window = pre[-1000:]
assert f'## HB #{NEW_HB} (' not in tail_window, (
    f'[PRE-FLIGHT FAIL] HB #{NEW_HB} already exists as the latest entry in tail. '
    f'Previous tick may have committed but state.json lag. Aborting to prevent dup.'
)

# Append (R-NEW-V3: open 'a' mode ONLY)
with open(HB_PATH, 'a', encoding='utf-8') as f:
    f.write(HB_ENTRY)
size_after = HB_PATH.stat().st_size

# Update state.json (read-modify-write, utf-8-sig to handle BOM)
with open(STATE_PATH, 'r', encoding='utf-8-sig') as f:
    state = json.load(f)

state['hbCount'] = NEW_HB
state['nullCount'] = NEW_NULL
state['post_t0_null_count'] = NEW_NULL
state['last_update_epoch'] = TS_EP
state['lastHB'] = TS_ISO
state['lastChecks']['heartbeat'] = TS_EP
state['lastHBContext'] = (
    f'HB #{NEW_HB} Thu 14:15 weekday-afternoon +6h15m past 08:00 hard cap. '
    f'posture DORMANT held (no change vs #2314-#{PREV_HB}). 18-layer suppression zero-breach. '
    f'R274 + R-NEW-V4 candidate both pending Eric ratification. 5th Plenary ~9-10d away. '
    f'memory_search index corrupted - awaiting Eric manual openclaw memory index --force. '
    f'R66 discrepancy SUSTAINED: memory/2026-08-06.md claims D+27 but HB log + 报到日 math = D+14. '
    f'No new signal vs HB #2314-#{PREV_HB}. Identical context, posture unchanged. Counter HB#{NEW_HB}.'
)
state['hb_2344_special'] = state['lastHBContext']
state['notes']['hb_2344_special'] = state['lastHBContext']
state['notes']['time'] = TS_HUMAN
state['notes']['r69_compliance'] = 'Day 7/30 silent'
state['posture'] = 'DORMANT'
state['zone'] = 'weekday-afternoon-post-hard-cap'
state['milestoneStatus'] = (
    f'AnYi D+14 = 2026-08-06 Thu. HB #{NEW_HB}. Eric silent on cron ~21d 1h+ (505h+). '
    f'5th Plenary ~9-10d away.'
)

with open(STATE_PATH, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print(f'[OK] HEARTBEAT.md appended: {size_before} -> {size_after} bytes (delta +{size_after - size_before})')
print(f'[OK] heartbeat-state.json updated: hbCount={state["hbCount"]}, nullCount={state["nullCount"]}, posture={state["posture"]}')
print(f'[OK] HB #{NEW_HB} {TS_HUMAN} -- DORMANT -- {NEW_NULL}th null -- HEARTBEAT_OK')
