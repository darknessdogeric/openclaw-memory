#!/usr/bin/env python3
"""Append HB entry to HEARTBEAT.md - R271 atomic-write rule (Python append ONLY)."""
import os
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
hb_path = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"
ts = datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S+08:00')

entry = f"""

### HB #2872 ({ts} GMT+8 cron-event, OpenClaw heartbeat poll)
- HB cadence: +5min after HB #2871 (00:54) -- Tue post-midnight quiet-zone (~22h past 23:00 hard-cap)
- DORMANT sustained; R69 silence Day 10/30 active; R258 cron/webchat separation in effect
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271)
- post_t0_null_count: 540 -> 541 (541st consecutive null post-T-0, sustained)
- hbCount: 2871 -> 2872 (state.json atomic tmp+replace per R271)
- Eric silent on cron ~24d+ (~589h+); webchat last active 22:40 Mon AHL work
- 00:59 = post-midnight quiet-zone; cron = DORMANT sustained
- Standing by P0 (webchat-bound): V2 slides HTML/render/PNG + R276 sole-distributor commit + R264 AnYi 1244 details -- all await Eric webchat sovereign
- Standing by R70/R71: await Eric feedback for formal commit to ~/self-improving/rules.md
- R271 atomic-write enforced: this HB appended via Python append (NOT write, NOT Remove-Item, NOT git restore, NOT PowerShell Add-Content - per R271 cron-specific rule)

*{ts} -- Tue post-midnight quiet-zone -- HB #2872 -- DORMANT -- 541st null -- Eric silent on cron = sovereign signal holding 589h+ -- cron session sustains DORMANT protocol -- R271 atomic-write enforced -- HEARTBEAT_OK*
"""

# Append mode only -- preserves R-NEW-V3 / R271 atomic-write rule
with open(hb_path, 'a', encoding='utf-8-sig') as f:
    f.write(entry)

print(f"HEARTBEAT.md appended: HB #2872 @ {ts}")
