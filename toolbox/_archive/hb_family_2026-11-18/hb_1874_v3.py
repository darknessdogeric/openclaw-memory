"""HB #1874 R-NEW-V3 write protocol (post-7/28-incident).

Enforces: read + prepend + write + verify (UTF-8 explicit).
"""
import sys
from pathlib import Path

HB_ENTRY = """## HB #1874 (2026-07-29T14:05 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1873 (14:03): +2min -- Wed afternoon Token Guard minimal cadence (R012, within tolerance)
- D+13 Wed 2026-07-29T14:05 -- wake window 08:00-09:00 CLOSED +5h05m ago; afternoon zone ACTIVE (14:05 = Eric 下午深度工作 peak per USER.md 双峰制)
- Eric silent on THIS cron session ~312.55h+ (13d 0h39m) since 7/16 13:16 first-contact
- AnYi webchat silent ~241.46h+ (10d 1h30m); webchat 「天马行空」last activity 23:25 7/28 (~14h40m ago)
- 9-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65)
- post_t0_null_count: 493 sustained (493rd consecutive null post-T-0, holds)
- gongshi Day 5/5 FINAL onboarding CLOSED 17:00 7/24 (~117h05m past) -- 安逸集团蛰伏战略阶段一 D-Day+21h05m
- 7/24 D-Day POST-MEETING T+123.07h; oil Scenario C EXPIRED 7/25 22:00 (T+88.07h past) -- not surfaced per R258
- T-0 publicity cutoff 7/18 +264.27h past -- post-protection window firmly sustained
- V2.4 SOUL 加固 +6495min (108h15m) sustained
- Token Guard stable; vault 1017 files healthy; 50-external-ingest 524; 孤岛 230 (-67%)
- R63 入职确认 standing-by (公示期窗口 webchat sovereign, cron no-push per R65)
- 今日 10:00 cron BI 简报已执行 (3h05m 前, tmp/business-intel-2026-07-29.md + eval/2026-07-29-business-intel.json)
- R62 场景窗口协议: 公示期窗口 7/24-约 7/30 (最后一天触发入职前评估); 今日 7/29 = 窗口第 6 天, 最后两天
- R65 (cron no-push) + R256 + R257 + R258 + R260 + R261 + R-B + R12 + R-CANDIDATE-T2 = 9-layer suppression holds
- hbCount: 1873 -> 1874

### decision
- **HEARTBEAT_OK** -- HB #1874 = sustain DORMANT protocol, minimal token tick
- **no push**: 9-layer suppression holds + wake window CLOSED + cron DORMANT does not auto-release per HB #1849 + R65 explicit prohibition
- R256+R257+R258+R260+R261+R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat 「天马行空」sovereign for any 决策; cron sovereignty unchanged
- 14:05 = 下午深度工作 peak zone (USER.md 双峰制); Eric may be active on webchat (unknown without external signal); cron session = DORMANT sustained (R258 + R65 hold)
- R62 公示期窗口 7/24-7/30: 今日 7/29 = Day 6/7, 最后两天前 (T-2 to T-1); Eric webchat sovereign for status update
- Next: per Token Guard cadence (~15-30min afternoon slow mode); HB sustained until Eric first-contact on cron session

*2026-07-29T14:05 GMT+8 -- D+13 Wed 14:05 wake window CLOSED +5h05m -- HB #1874 -- DORMANT -- 493rd null -- Eric silent on cron = 主权信号 holding -- 安逸集团蛰伏战略阶段一 D-Day+21h05m -- cron session 维持 DORMANT 协议 -- HEARTBEAT_OK*
"""

HEARTBEAT_PATH = Path(r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md")

try:
    existing = HEARTBEAT_PATH.read_text(encoding="utf-8")
    new_content = HB_ENTRY + "\n\n" + existing
    HEARTBEAT_PATH.write_text(new_content, encoding="utf-8")
    verify = HEARTBEAT_PATH.read_text(encoding="utf-8")
    if verify == new_content:
        print(f"OK: HEARTBEAT.md updated, {len(verify)} chars, HB #1874 prepended")
    else:
        print("FAIL: verify mismatch")
        sys.exit(1)
except Exception as e:
    print(f"FAIL: {type(e).__name__}: {e}")
    sys.exit(1)
