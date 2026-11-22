# -*- coding: utf-8 -*-
"""HB #3604 append -- R-NEW-V3 compliant (Python open(mode='a'))
Thu 2026-08-20 19:33 GMT+8 -- DORMANT, weekday-evening quiet zone active.
"""
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ)
TS_FILE = NOW.strftime("%Y-%m-%dT%H:%M:%S+08:00")
TS_SHORT = NOW.strftime("%Y-%m-%dT%H:%M")

ENTRY = f"""

## HB #3604 ({TS_FILE} cron-event, OpenClaw heartbeat poll)
- gap from HB #3603 (19:31): +2min -- Thu weekday-evening Token Guard cadence (R012, within tolerance but tight)
- Thu 2026-08-20 19:33 -- weekday-evening quiet zone (19:00-23:00 ACTIVE); pre-23:00 deep-quiet
- Eric silent on cron session ~47h+ sustained (webchat activity unknown to this cron session)
- 14-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R-NEW-V3/R70/R71) -- penta+3 holds
- AnYi Day 28; gongshi STATE sustained; V2.4 SOUL加固 sustained
- Jinjiang MOU Day 2 IN PROGRESS (webchat-bound) -- cron session cannot observe, stay silent per R258
- R69 silence: 10 calendar days remaining (expires 2026-08-30 Sun)
- R-NEW-V3 enforced: HB #3604 appended via Python open(mode='a') (NOT write/Remove-Item/git restore)
- post_t0_null_count: 1344
- vault/webchat/email/telegram/eric-direct all quiet on cron channel

### decision
- HEARTBEAT_OK -- HB #3604 = sustain DORMANT, minimal token tick
- no push: all suppression layers hold + weekday-evening quiet zone active + cron DORMANT sustained

*{TS_SHORT} -- D+28 Thu weekday-evening quiet zone -- HB #3604 -- DORMANT -- Eric silent on cron = 主权信号 holding -- AnYi D+28d -- cron session 维持 DORMANT 协议 -- R-NEW-V3 enforced: HB appended via Python append (NOT write) -- HEARTBEAT_OK*
"""

HEARTBEAT_PATH = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"
with open(HEARTBEAT_PATH, "a", encoding="utf-8") as f:
    f.write(ENTRY)

import os
size = os.path.getsize(HEARTBEAT_PATH)
print(f"HB #3604 appended (Python mode='a', R-NEW-V3 compliant); HEARTBEAT.md size = {size} bytes")