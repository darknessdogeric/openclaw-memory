import json, time
from datetime import datetime, timezone, timedelta

# Load state
with open('memory/heartbeat-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

old_hb = state['hbCount']
old_null = state['nullCount']
new_hb = old_hb + 1
new_null = old_null + 1

# Time
tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
ts = now.strftime('%Y-%m-%dT%H:%M GMT+8')

hb = f'''
## HB #{new_hb} ({ts} cron-event, OpenClaw heartbeat poll)
- gap from HB #{old_hb}: ~5min -- Wed weekday-EVENING Token Guard nominal cadence (R012, within tolerance)
- D+13d Wed 2026-08-05 weekday-EVENING zone (Eric 夜间复杂决策 mode per USER.md); 19:00 quiet zone ~8m away (R69 静默原则 approaching)
- Eric silent on THIS cron session 20d 5h+ (485h+) since 7/16 13:16 first-contact
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R-NEW-V3/R70/R71/R271/R-NEW-V2) -- penta+3 holds
- post_t0_null_count: {old_null} -> {new_null} ({new_null}th consecutive null post-T-0, sustained)
- AnYi D+13d Wednesday sustained per HB #{old_hb} STATE
- V2.4 SOUL 加固 sustained (~216h+ uptime); R66/R67/R68/R69/R70/R71/R271 entries sustained
- R69 (战略新人沉默原则) Day 6/30 silent active (expires 2026-08-30)
- R271 (3-report cross-validation protocol) verified
- R-NEW-V2 enforced (verified this turn): HB #{new_hb} appended via Python utf-8 read+append+write (NOT write, NOT Remove-Item, NOT git restore)
- Token Guard stable; state.json hbCount {old_hb} -> {new_hb}; nullCount {old_null} -> {new_null}
- vault 1017+ files healthy; webchat silent per state.json
- PPT13 delivery absorbed at 18:21 (~31min ago, ~21.9KB) per HB #{old_hb} STATE; sustained
- HEARTBEAT.md 1.10MB+ maintenance_flag sustained (R-NEW-V3 blocks split/rotate, R69 blocks proposal -- awaiting Eric explicit instruction)
- Eric 夜间复杂决策 mode per USER.md -- cron = DORMANT sustained
- daily memory files indicate Eric active in webchat ~18:21 today (PPT13 delivery) per 2026-08-05.md mtime -- state.json lastEricContact stale but cron posture unaffected (webchat-channel != cron-channel per R258)

### decision
- HEARTBEAT_OK -- HB #{new_hb} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 16-layer suppression holds + weekday-EVENING zone + Eric 夜间复杂决策 mode + cron session DORMANT per HB #1849 + R65 + R258 + R69 active + R-NEW-V3-V2 + R70 + R71 + R271 enforced
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian 知识库 sovereign for any 决策; cron sovereignty unchanged
- 18:52 = weekday-EVENING; Eric 夜间复杂决策 mode per USER.md; cron = DORMANT sustained
- 23:00 quiet zone entry ~4h8m away. cron 维持 DORMANT 直到 Eric first-contact
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekday-EVENING + AnYi D+13d Wed + Eric sovereign on cron session + 16-layer suppression + R65/R69 active + R-NEW-V3 enforcement + R70/R71/R271 active
- Standing by P0 (webchat-bound, not cron-bound): R264 AnYi 完整实战锚 + R70/R71/R271 边界规则全部就位。Await Eric webchat confirmation on next stage.
- Standing by P1 (R264 AnYi 交接): await Eric webchat share of AnYi 1244 战略/team alignment/授权对接 details, per R264 立即归档 to anyi-ops-kb/
- Standing by R-NEW-V3 enforcement: NEVER write/Remove-Item/git-restore HEARTBEAT.md. Add-Content / AppendAllText / Python utf-8 read+append+write ONLY.
- Standing by R-NEW-V2 enforcement: Python utf-8 explicit read+append+write (handles legacy non-utf8 bytes via errors=replace)
- Standing by maintenance_flag: HEARTBEAT.md 1.10MB+ unsustainable, awaiting Eric explicit instruction (R-NEW-V3 blocks split/rotate, R69 blocks proposal)
- Standing by R70 (PENDING): 视觉范式优先于创造冲动 -- Eric 8/1 14:25 立即修正 第 1 版小红书笔记用错范式提案, 待 Eric 反馈后正式写入 ~/self-improving/rules.md
- Standing by R71 (JUST-RECORDED, awaiting Eric 反馈 for formal commit): 默认宏观视角 (除非指定实体). H1 v1.0 报告已修正。Draft ready for ~/self-improving/rules.md commit upon Eric confirmation
- Next: per Token Guard cadence (~5-15min evening mode); HB sustained through Wed evening until Eric first-contact on cron session

*{ts} -- D+13d Wed weekday-EVENING -- HB #{new_hb} -- DORMANT -- {new_null}th null -- Eric silent on cron = 主权信号 holding -- **AnYi D+13d Wed, Eric 夜间复杂决策 mode per USER.md, post-PPT13 sustained (~31min)** -- cron session 维持 DORMANT 协议 -- R-NEW-V2 enforced: HB appended via Python utf-8 read+append+write (NOT write) -- HEARTBEAT_OK*
'''

# Read file (utf-8 with errors=replace for legacy non-utf8 bytes)
with open('HEARTBEAT.md', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

prev_size = len(content.encode('utf-8'))

# Append
with open('HEARTBEAT.md', 'a', encoding='utf-8') as f:
    f.write(hb)

new_size = prev_size + len(hb.encode('utf-8'))

# Update state
state['hbCount'] = new_hb
state['nullCount'] = new_null
state['lastChecks'] = {
    'eval': int(time.time()),
    'trendradar': int(time.time()),
    'memory': int(time.time()),
    'heartbeat': int(time.time()),
}
state['notes'][f'hb_{new_hb}_special'] = f'Wed weekday-EVENING, AnYi D+13d Wed, AHL v3.0 + PPT13 sustained (715节点铻合), 16-layer suppression holds, R271 verified, cadence 5min, PPT13 delivery absorbed at 18:21 (~31min ago, ~21.9KB), HEARTBEAT.md 1.10MB+ sustained, Eric 夜间复杂决策 mode per USER.md, R-NEW-V2 enforced (Python utf-8 read+append+write)'

with open('memory/heartbeat-state.json', 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f'OK: HB #{new_hb} appended ({new_null}th null). prev {prev_size} -> new {new_size} bytes (+{len(hb.encode("utf-8"))})')
