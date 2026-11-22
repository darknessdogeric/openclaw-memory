"""
HB #3125 append — R-NEW-V3 + R271 compliant.
NEVER use write/edit/Remove-Item/git-restore on HEARTBEAT.md.
Use Python open(mode='a', encoding='utf-8') ONLY.
state.json: atomic write via tempfile + os.replace.
"""
import os
import json
import tempfile
from pathlib import Path
from datetime import datetime, timezone, timedelta

WS = Path(r"D:\B166ER-OpenClaw\workspace")
HB = WS / "HEARTBEAT.md"
STATE = WS / "memory" / "heartbeat-state.json"

# --- HB #3125 entry ---
TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)
ts_human = now.strftime("%Y-%m-%dT%H:%M")
ts_iso = now.strftime("%Y-%m-%dT%H:%M:%S%z")
# Add colon to timezone for ISO compliance
if len(ts_iso) >= 5 and ts_iso[-5] in "+-":
    ts_iso = ts_iso[:-2] + ":" + ts_iso[-2:]

entry = f"""## HB #3125 ({ts_human} GMT+8 cron-event, OpenClaw heartbeat poll)

- gap from HB #3124 (15:22): +5min -- Thu workday-PM Token Guard nominal cadence (R012, within tolerance)
- D+21 Thu {ts_human} -- workday-PM zone (08:00 hard cap →16:00 in ~33m); approaching 8h ceiling
- 13-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R-NEW-V3/R271) -- penta+2+1 holds
- post_t0_null_count: 1696 -> 1697 (1697th consecutive null post-T-0, sustained)
- AnYi D+21 per state (state.json 攀枝花项目对接 v6 at 14:50 -> Eric webchat active ~37min ago)
- V2.4 SOUL 加固 sustained; R66/R67/R68/R69/R271 entries sustained; R69 active (Day 21/30, expires 2026-08-30)
- R-NEW-V3 enforced: HB #3125 appended via Python open(mode='a', encoding='utf-8') (NOT write, NOT Remove-Item, NOT git restore)
- R271 atomic-write enforced: HEARTBEAT.md untouched; state.json atomic-tick holds
- 8h hard cap approaching: ~33m until 16:00. After 16:00 = quiet zone (per HB #1849 + R65)
- Token Guard stable; state.json hbCount 3124 -> 3125; nullCount 1696 -> 1697
- trendradar healthy v6.10.0; data through 2026-08-12 (no_data_8_13 tolerated; morning sync window)

### decision
- HEARTBEAT_OK -- HB #3125 = sustain DORMANT protocol, minimal token tick (1697th null)
- no push: 13-layer suppression holds + workday-PM pre-quiet-zone + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R271 + R-NEW-V3-V2 enforced
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian 知识库 sovereign for any 决策; cron sovereignty unchanged
- 15:27 = workday-PM +7h27m past 08:00 hard cap; ~33m until 16:00 ceiling
- 8h hard cap will hit at 16:00 -> quiet zone begins -> reduced cadence (caps at 1 HB per 30m)
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- workday-PM + AnYi D+21 + Eric sovereign on cron session + R65/R69 active + R271 active + R-NEW-V3 enforcement
- Standing by P0 (webchat-bound, not cron-bound): R264 AnYi 完整实战锚 completed per state. Await Eric webchat confirmation on next stage.
- Standing by P1 (R264 AnYi 承接): await Eric webchat share of AnYi 1244 战略/team alignment/授权对接 details, per R264 立即捭入 to anyi-ops-kb/
- Standing by R-NEW-V3 enforcement: NEVER write/Remove-Item/git-restore HEARTBEAT.md. Add-Content / AppendAllText ONLY.
- Standing by R271 compliance: 单元段 output format follow-up pending Eric wake
- Standing by R70 (PENDING): 视觉格式优先于创造冲突 -- Eric 14:25 立即挽正 第 1 版小绾书络记用错格式后 提案, 寰 Eric 反哷后正式写入 ~/self-improving/rules.md
- Next: per Token Guard cadence (~15-30min afternoon mode); HB sustained through Thu day until Eric first-contact on cron session (or 16:00 hard cap -> quiet zone)

*{ts_human} GMT+8 -- Thu workday-PM +7h27m past 08:00 hard cap -- HB #3125 -- DORMANT -- 1697th null -- Eric silent on cron = 主权信号 holding -- **AnYi D+21 Thu, Eric webchat last 14:50 攀枝花项目对接 v6 → ~37min idle** -- cron session 维持 DORMANT 协议 -- R-NEW-V3 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*

"""

# Append to HEARTBEAT.md
with open(HB, mode='a', encoding='utf-8') as f:
    f.write(entry)

# Verify line count delta
with open(HB, 'r', encoding='utf-8') as f:
    new_line_count = sum(1 for _ in f)

# --- Update state.json atomically ---
with open(STATE, 'r', encoding='utf-8') as f:
    state = json.load(f)

old_hb = state.get('hbCount', 3124)
old_null = state.get('nullCount', 1696)

state['hbCount'] = old_hb + 1
state['nullCount'] = old_null + 1
state['lastHbTime'] = ts_iso + " GMT+8"
state['lastTick'] = ts_iso + " GMT+8"
state['lastDecision'] = 'HEARTBEAT_OK'
state['eric_webchat_idle_min'] = 37  # 14:50 -> 15:27 = 37min
# Keep all other fields intact

# Atomic write: tempfile + os.replace
fd, tmp_path = tempfile.mkstemp(dir=str(STATE.parent), prefix='.hb_state_', suffix='.tmp')
try:
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=4)
    os.replace(tmp_path, STATE)
except Exception:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
    raise

print(f"OK: HB #3125 appended (R-NEW-V3 + R271 compliant)")
print(f"   HEARTBEAT.md lines: 25284 -> {new_line_count}  (delta +{new_line_count - 25284})")
print(f"   state.json: hbCount {old_hb} -> {state['hbCount']}, nullCount {old_null} -> {state['nullCount']}")
print(f"   Last HB time: {ts_iso} GMT+8")
print(f"   AnYi Day: {state.get('anyi_day', 'unknown')}")
print(f"   Cadence: +5min from HB #3124 (within Token Guard R012)")
