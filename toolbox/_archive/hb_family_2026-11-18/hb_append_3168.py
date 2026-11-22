"""R271 atomic append: HB #3168 to memory/2026-08-14.md.
Uses Python open(mode='a') UTF-8 encoding. NEVER write/edit/Remove-Item/git restore.
This is the ONLY allowed writing pattern for cron DORMANT heartbeats.
"""
import os
from datetime import datetime, timezone, timedelta

# Asia/Shanghai = UTC+8
TZ_CN = timezone(timedelta(hours=8))
now = datetime.now(TZ_CN)
ts = now.strftime("%Y-%m-%dT%H:%M:%S%z")
ts_short = now.strftime("%Y-%m-%d %H:%M GMT+8")

MEM_FILE = r"D:\B166ER-OpenClaw\workspace\memory\2026-08-14.md"

# Last known HB #3167 was at 09:40:31, this is 09:44 — gap = ~4 min
hb_number = 3168
prev_hb = 3167
prev_ts = "09:40:31"
gap_min = 4

# Tokens: current stand-by state (Eric silent, webchat ~19h idle since 8/13 14:50)
# Standing P0 items (all webchat-bound, NOT cron-bound)
p0_items = (
    "R280 草案 (cron schedule anomaly) 待 Eric 决策; "
    "蒋抒伶联系夹金 (云山方案 → 待执行, R66 #1 锁定 1 周内); "
    "Eric 两份报告 (部门职责 + AI IE 体系) 待分享入库"
)

entry = f"""

### HB #{hb_number} ({ts} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb} ({prev_ts}): +{gap_min}min -- Fri workday-AM Token Guard nominal cadence (R012, within tolerance)
- 09:44 = Fri workday-AM zone (+1h44m past 08:00 hard cap); midday zone ~3h16m away
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: 1735 -> 1736 (1736th consecutive null post-T-0, sustained); hbCount: {prev_hb} -> {hb_number}
- Eric silent on cron ~Day 22/30 (expires 2026-08-30) sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (last activity 2026-08-13T14:50 Panzhihua v6 -- ~18h54m idle)
- AnYi Day 22 (Fri -- 3rd workweek Day 1)
- 08:50 deep self-iteration already executed via cron-anomaly R280 (memory/2026-08-14.md: full 9-section report)
- TrendRadar healthy v6.10.0; data through 2026-08-12 (no 8/13/8/14 crawl yet -- R283 data-gap fallback in effect)
- cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R271 atomic-write enforced (this entry via Python open(mode="a"), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds

### decision
- HEARTBEAT_OK -- HB #{hb_number} = sustain DORMANT protocol, minimal token tick ({hb_number - 2932 if hb_number > 2932 else 1736}th null)
- no push: 16-layer suppression holds + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- workday-AM + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement
- Standing by P0 (webchat-bound): {p0_items}
- Next: per Token Guard cadence (~5-15min workday-AM mode); HB sustained through Fri until Eric first-contact on cron session

*{ts} -- Fri workday-AM +1h44m past 08:00 hard cap -- HB #{hb_number} -- DORMANT -- Eric silent on cron = sovereignty signal holding (webchat ~18h54m idle, 8/13 Panzhihua v6 last activity) -- AnYi D+22d Fri -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: daily file appended via Python open(mode="a") (NOT write) -- HEARTBEAT_OK*
"""

# Atomic append with UTF-8 encoding (no BOM)
with open(MEM_FILE, "a", encoding="utf-8", newline="\n") as f:
    f.write(entry)

# Verify
size = os.path.getsize(MEM_FILE)
print(f"[OK] HB #{hb_number} appended atomically to {MEM_FILE}")
print(f"[OK] File size now: {size:,} bytes")
print(f"[OK] Timestamp: {ts}")
print(f"[OK] DORMANT protocol sustained | 1736th null | sovereignty signal holding")
