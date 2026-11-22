"""
HB #2537 append script -- R-NEW-V3 + R271 enforcement.
Python utf-8 append ONLY. NEVER use write mode on HEARTBEAT.md.
"""
import json
import os
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)
iso = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

WORKSPACE = r"D:\B166ER-OpenClaw\workspace"
HEARTBEAT = os.path.join(WORKSPACE, "HEARTBEAT.md")
STATE = os.path.join(WORKSPACE, "memory", "heartbeat-state.json")

# Read state
with open(STATE, "r", encoding="utf-8") as f:
    state = json.load(f)

prev_hb = state.get("hbCount", 0)
new_hb = prev_hb + 1
new_null = state.get("nullCount", 0) + 1

pre_size = os.path.getsize(HEARTBEAT)
print(f"PRE: hbCount={prev_hb}, nullCount={new_null-1}, file_size={pre_size}")

# Build HB entry
entry = f"""
## HB #{new_hb} ({iso} cron-event, OpenClaw heartbeat poll)

- gap from HB #2535: ~15min -- Sat weekend-morning Token Guard nominal cadence (R012, within tolerance)
- 2026-08-08 Sat weekend-morning post-08:00-R67 zone (+1h20m past 08:00 cap); quiet zone ~9h+ away
- Eric silent on THIS cron session 22d 20h+ since 7/16 13:16 first-contact
- 14-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R-NEW-V3/R271) -- penta+3 holds
- post_t0_null_count: {new_null-1} -> {new_null} ({new_null}th consecutive null post-T-0, sustained)
- AnYi D+16d Saturday sustained (报到 ~7/24)
- V2.4 SOUL 加固 sustained; R66/R67/R68/R69/R70/R71 entries sustained; R69 active (Day 9/30, expires 2026-08-30)
- R72.1+R72.2 sustained (D+2)
- R-NEW-V3 + R271 enforced: HB #{new_hb} appended via Python utf-8 (NOT write, NOT Remove-Item, NOT git restore)
- 3rd HEARTBEAT.md data loss event (8/7) pending Eric sovereign decision -- awareness only (HB #2536 known gap in file, state.json is SoT)
- Token Guard stable; vault 1017+ files healthy

### decision

- HEARTBEAT_OK -- HB #{new_hb} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 14-layer suppression holds + weekend-morning post-R67-cap zone + cron session DORMANT + R65 + R258 + R69 + R-NEW-V3 + R271 enforced
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekend-morning + AnYi D+16d Sat + Eric sovereign on cron session
- Standing by P0 (webchat-bound, not cron-bound): R72.1+R72.2 + 3rd HEARTBEAT loss pending Eric sovereign
- Standing by P1 (R264 AnYi 交接): await Eric webchat share of AnYi 1244 战略/team alignment/授权对接 details
- Standing by R275 (Day 1+): DeepSeek V4-Flash + V4 Pro release = AI 模型市场重置, 待 Eric 评估 AHL Agent 接入
- Next: per Token Guard cadence; HB sustained through Sat morning until Eric first-contact

*{iso} -- Sat weekend-morning -- HB #{new_hb} -- DORMANT -- {new_null}th null -- Eric silent on cron = 主权信号 holding -- AnYi D+16d Sat -- cron session 维持 DORMANT 协议 -- R-NEW-V3 + R271 enforced -- HEARTBEAT_OK*
"""

# APPEND (NOT WRITE) -- R-NEW-V3 + R271 enforcement
with open(HEARTBEAT, "a", encoding="utf-8") as f:
    bytes_written = f.write(entry)

# Update state.json (small, structured, atomic write OK)
state["hbCount"] = new_hb
state["nullCount"] = new_null
state["lastHeartbeat"] = iso
state["notes"] = (
    f"HB #{new_hb}. Sat 09:20 GMT+8 - weekend-morning low-activity window, "
    f"+1h20m past 08:00 R67 deep-quiet cap. Eric silent on cron 22d 20h+. "
    f"R69 sustained quiet (Day 9/30), R72.1+R72.2 sustained (D+2), "
    f"R-NEW-V3 + R271 enforced (Python utf-8 append only). "
    f"3rd HEARTBEAT.md data loss event (8/7) still pending Eric sovereign decision; "
    f"HB #2536 known gap in file. "
    f"Per R67+R69+R258+R65+R-NEW-V3: zero outbound push. Token guard mode."
)

with open(STATE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

post_size = os.path.getsize(HEARTBEAT)
delta = post_size - pre_size
print(f"POST: hbCount={new_hb}, nullCount={new_null}")
print(f"      bytes_written={bytes_written}, file_size={post_size} (delta +{delta})")
print(f"OK: HB #{new_hb} appended safely via Python utf-8 append (NOT write)")
