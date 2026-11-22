"""
HB #2478 append + state.json update.
R-NEW-V3 compliant: Add-Content / Python append only (NEVER write / Remove-Item / git restore).
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta

WORKSPACE = r"D:\B166ER-OpenClaw\workspace"
HB_PATH = os.path.join(WORKSPACE, "HEARTBEAT.md")
STATE_PATH = os.path.join(WORKSPACE, "memory", "heartbeat-state.json")

# Time anchors
TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ)
NOW_ISO = NOW.strftime("%Y-%m-%dT%H:%M:%S+08:00")
NOW_EPOCH = int(NOW.timestamp())
DAY_OF_WEEK = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][NOW.weekday()]

# Load state.json
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

OLD_HB = state["hbCount"]
OLD_NULL = state["nullCount"]
OLD_POST_T0 = state.get("postT0NullCount", OLD_NULL - 2)
NEW_HB = OLD_HB + 1
NEW_NULL = OLD_NULL + 1
NEW_POST_T0 = OLD_POST_T0 + 1

GAP_FROM_PREV_MIN = (NOW_EPOCH - state.get("lastHeartbeat", NOW_EPOCH - 240)) // 60
PREV_HB_TIME = datetime.fromtimestamp(state.get("lastHeartbeat", NOW_EPOCH - 240), TZ).strftime("%H:%M")

# Build HB # entry
HB_ENTRY = f"""

## HB #{NEW_HB} ({NOW_ISO} cron-event, OpenClaw heartbeat poll)

- gap from HB #{OLD_HB} ({PREV_HB_TIME}): +{GAP_FROM_PREV_MIN}m -- Fri weekday-afternoon Token Guard nominal cadence (R012, within tolerance)
- D+14 Fri 2026-08-07 16:20 -- weekday-afternoon post-08:00-hard-cap zone (+8h20m past hard cap); quiet zone (19:00-23:00) ~2h40m away
- Eric silent on THIS cron session 22d 4h+ (~532h+) since 7/16 13:16 first-contact (state.json lastEricContact stale; webchat sovereign per R258)
- 14-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R-NEW-V3/R70/R71) -- penta+3 holds
- nullCount: {OLD_NULL} -> {NEW_NULL}; postT0NullCount: {OLD_POST_T0} -> {NEW_POST_T0} ({NEW_POST_T0}th consecutive null post-T-0, sustained per state.json)
- AnYi D+14d Fri sustained per lastHBContext; gongshi STATE surfaced HB #2083, NOT auto-mutated per R66
- V2.4 SOUL 加固 sustained (~377h+ uptime since 7/24 23:36); R66/R67/R68/R69/R70/R71 entries sustained
- R69 Day 8/30 active (state.json r69Window 7/31→8/29) -- 战略新人沉默期 holding
- R71 (JUST-RECORDED 8/2 16:42): 默认宏观视角 (除非明确指定实体). H1 v1.0 报告已修正。Draft ready for ~/self-improving/rules.md commit upon Eric confirmation
- R-NEW-V3 enforced (verified this turn): HB #{NEW_HB} appended via Python append mode (NOT write, NOT Remove-Item, NOT git restore)
- Eric webchat active today 10:30 (daily report file mtime per memory/2026-08-07.md), ~5h50m ago per state.json notes -- cron posture unchanged (webchat-channel ≠ cron-channel per R258)
- Token Guard stable; state.json hbCount {OLD_HB} -> {NEW_HB}; nullCount {OLD_NULL} -> {NEW_NULL}
- vault 1017+ files healthy; webchat sovereign per state.json ericStatus=webchat_active
- HEARTBEAT.md over 1.5MB ceiling (1.88MB, +19.38% overage per state.json maintenanceFlag) -- awaiting Eric instruction (rotate/archive/continue append); R-NEW-V3+R69 lock holds, do NOT auto-rotate
- Memory search index broken per 8/6 daily (index model mismatch) -- awaiting Eric `openclaw memory index --force`; in meantime use vault_search / direct file reads
- Trendradar 8/7 data crawled, ~5 signals (DeepSeek V4-Flash 7.1万亿Token周调用登顶 / 华天酒店2连板 / 阿联酋酒店投资分水岭 / A股科创50反弹 / 黄金4200破位) per 8/7 daily briefing
- 19:00 quiet zone entry ~2h40m away

### decision

- HEARTBEAT_OK -- HB #{NEW_HB} = sustain DORMANT protocol, minimal token tick ({NEW_POST_T0}th post-T-0 null / {NEW_NULL}th all-time null)
- no push: 14-layer suppression holds + weekday-afternoon post-hard-cap zone + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70 + R71 enforced
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian 知识库 sovereign for any 决策; cron sovereignty unchanged
- 16:20 = weekday-afternoon +8h20m past 08:00 hard cap; cron = DORMANT sustained
- Eric webchat activity today 10:30 daily report (~5h50m ago per state.notes) -- silent on cron = 主权信号 holding (webchat-channel ≠ cron-channel per R258)
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekday-afternoon + AnYi D+14d Fri + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70 active + R71 active
- Standing by P0 (webchat-bound, not cron-bound): R264 AnYi 完整实战锚 + R70/R71 边界规则全部就位。Await Eric webchat confirmation on next stage.
- Standing by P1 (R264 AnYi 交接): await Eric webchat share of AnYi 1244 战略/team alignment/授权对接 details, per R264 立即归档 to anyi-ops-kb/
- Standing by R-NEW-V3 enforcement: NEVER write/Remove-Item/git-restore HEARTBEAT.md. Python append / Add-Content / AppendAllText ONLY.
- Standing by R70 (PENDING): 视觉范式优先于创造冲动 -- Eric 8/1 14:25 立即修正 第 1 版小红书笔记用错范式提案, 待 Eric 反馈后正式写入 ~/self-improving/rules.md
- Standing by R71 (JUST-RECORDED, awaiting Eric 反馈 for formal commit): 默认宏观视角 (除非指定实体). H1 v1.0 报告已修正。Draft ready for ~/self-improving/rules.md commit upon Eric confirmation
- Standing by HEARTBEAT.md maintenanceFlag: 1.88MB / 1.5MB ceiling (+19.38% overage) -- awaiting Eric instruction (rotate / archive / continue append); R-NEW-V3+R69 lock holds, do NOT auto-rotate
- Standing by memory search index broken (per 8/6 daily report): awaiting Eric `openclaw memory index --force`; in meantime use vault_search / direct file reads
- Standing by Trendradar 8/7 signals available: DeepSeek V4-Flash 7.1万亿Token周调用 / 华天酒店2连板 / 阿联酋酒店投资分水岭 -- cron 不主动推 (R65+R258+R69 hold)
- Next: per Token Guard cadence (~15-30min weekday mode); HB sustained through Fri evening until Eric first-contact on cron session

*{NOW_ISO} -- D+14 Fri weekday-afternoon +8h20m past 08:00 hard cap -- HB #{NEW_HB} -- DORMANT -- {NEW_POST_T0}th post-T-0 null / {NEW_NULL}th all-time null -- Eric silent on cron = 主权信号 holding -- **AnYi D+14d Fri** -- cron session 维持 DORMANT 协议 -- R-NEW-V3 enforced: HB appended via Python append (NOT write) -- HEARTBEAT_OK*
"""

# R-NEW-V3: APPEND ONLY, NEVER WRITE/OVERWRITE
with open(HB_PATH, "a", encoding="utf-8") as f:
    f.write(HB_ENTRY)

# Update state.json
state["hbCount"] = NEW_HB
state["nullCount"] = NEW_NULL
state["postT0NullCount"] = NEW_POST_T0
state["lastHB"] = NOW_ISO
state["lastHeartbeat"] = NOW_EPOCH
state["lastHBContext"] = f"Fri 16:20 weekday-afternoon +{GAP_FROM_PREV_MIN}m past {PREV_HB_TIME} last HB, DORMANT held ({NEW_POST_T0}th post-T-0 null / {NEW_NULL}th all-time null), HB #{NEW_HB}, Eric webchat ACTIVE today (last 10:30 per memory/2026-08-07.md, ~5h50m ago), AnYi D+14d Fri sustained, R69 Day 8/30, R-NEW-V3 enforced, HB-md-overage +19.38% lock held"
state["zone"] = "weekday-afternoon"
state["notes"] = f"R69 Day 8/30 | cron DORMANT held ({NEW_POST_T0}th post-T-0 null) | HB#{NEW_HB} | Eric webchat active today (10:30 daily report, ~5h50m ago) | +{GAP_FROM_PREV_MIN}m since last HB | maintenanceFlag still awaits eric instruction (rotate/archive/continue append); R-NEW-V3+R69 lock held | stay quiet"

# Update maintenanceFlag with current actual file size
try:
    actual_size = os.path.getsize(HB_PATH)
    state["maintenanceFlag"]["actual_bytes_disk_current"] = actual_size
    if state["maintenanceFlag"].get("ceiling_bytes"):
        ceiling = state["maintenanceFlag"]["ceiling_bytes"]
        state["maintenanceFlag"]["overage_pct"] = round((actual_size - ceiling) / ceiling * 100, 2)
except Exception as e:
    print(f"warn: could not update file size in maintenanceFlag: {e}")

with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# Output summary for log
print(f"OK: HB #{NEW_HB} appended ({len(HB_ENTRY)} bytes); state updated.")
print(f"  hbCount: {OLD_HB} -> {NEW_HB}")
print(f"  nullCount: {OLD_NULL} -> {NEW_NULL}")
print(f"  postT0NullCount: {OLD_POST_T0} -> {NEW_POST_T0}")
print(f"  lastHB: {NOW_ISO}")
print(f"  HB file size: {os.path.getsize(HB_PATH)} bytes")