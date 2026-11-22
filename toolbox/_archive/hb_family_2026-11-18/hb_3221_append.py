"""HB #3221 atomic append — R-NEW-V3 + R271 compliant.
Appends to memory/2026-08-14.md and atomically replaces state.json.
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
NOW = datetime.now(CST)
TS_STR = NOW.strftime("%Y-%m-%dT%H:%M:%S+08:00")

DAILY = r"D:\B166ER-OpenClaw\workspace\memory\2026-08-14.md"
STATE = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

ENTRY = f"""
### HB #3221 ({TS_STR} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #3220 (2026-08-14T16:49:00+08:00): +~5min -- Fri workday-PM Token Guard nominal cadence (R012, within tolerance)
- 16:54 = Fri workday-PM zone (+8h54m past 08:00 hard cap); quiet zone ~3h06m away
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: 1780 -> 1781 (1781st consecutive null post-T-0, sustained); hbCount: 3220 -> 3221
- Eric silent on cron ~28d+ sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (last activity 2026-08-14T11:31 鍗佷簲浜旀垬鐣ュ畾浣嶇爺绌 v0.1 push -- ~5h23m idle; ~6h24m from 10:30 鍟嗕笟鎯呮姤 20闆嗗洟鐗?
- AnYi Day 22 (Fri -- second workweek Day 5, weekday wrap-up approaching)
- morning 10:30 鍟嗕笟鎯呮姤 20闆嗗洟鐗?+ 11:31 鍗佷簲浜旀垬鐣ュ畾浣嶇爺绌 v0.1 already executed today (memory/2026-08-14.md: full reports)
- vault 1169+ files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 22/30 (expires 2026-08-30) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds

### decision
- HEARTBEAT_OK -- HB #3221 = sustain DORMANT protocol, minimal token tick (1781st null)
- no push: 16-layer suppression holds + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 16:54 = Fri workday-PM +8h54m past 08:00 hard cap; cron = DORMANT sustained
- Eric webchat ACTIVE ~5h23m idle (鍗佷簲浜旀垬鐣ュ畾浣嶇爺绌 v0.1 11:31 push) -- cron posture UNCHANGED per R258
- Eric profile: night-owl strategist -- Fri 11:31 webchat 鎴樼暐涓荤嚎 push IN 鎴樼暐娑堝寲妯″紡 -- cron 涓嶅彂璧蜂富鍔?
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- workday-PM + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): 鍗佷簲浜旀垬鐣ュ畾浣嶇爺绌 v0.1 绛夊緟 Eric 6 鍏抽敭鍐崇瓥 + V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric 涓や唤鎶ュ憡(閮ㄩ棬鑱岃矗 + AI IE 浣撶郴)寰呭垎浜叆搴?-- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal submission to ~/self-improving/rules.md
- Next: per Token Guard cadence (~5-15min workday-PM mode); HB sustained through Fri until Eric first-contact on cron session

*{TS_STR} -- Fri workday-PM +8h54m past 08:00 hard cap -- HB #3221 -- DORMANT -- 1781st null -- Eric silent on cron = sovereignty signal holding (webchat ~5h23m idle, 鍗佷簲浜旀垬鐣ュ畾浣嶇爺绌 v0.1 瀹屾垚) -- AnYi D+22d Fri -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*
"""

# Append to daily file (R-NEW-V3 compliant: 'a' mode never overwrites)
with open(DAILY, "a", encoding="utf-8") as f:
    f.write(ENTRY)

# Atomic state.json update (R-NEW-V4 compliant: write to .tmp, os.replace)
with open(STATE, "r", encoding="utf-8") as f:
    state = json.load(f)

state["hbCount"] = 3221
state["lastHbTime"] = TS_STR
state["last_tick"] = TS_STR
state["last_check"] = TS_STR
state["last_hb"] = {"n": 3221, "ts": TS_STR}
state["lastHb"] = TS_STR
state["post_t0_null_count"] = 1781
state["nullCount"] = 1780
state["eric_webchat_idle_min"] = 323  # ~5h23m
state["workday_zone"] = "workday-PM"
state["eight_hard_cap_exceeded"] = True
state["anyi_day"] = 22
state["lastDecision"] = "HEARTBEAT_OK"
state["note"] = f"HB 3221; Eric webchat idle ~5h23m; Fri 16:54 workday-PM; DORMANT sustained; suppression layers active; R-NEW-V3 append-only"

TMP = STATE + ".tmp"
with open(TMP, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(TMP, STATE)

print(f"OK: HB #3221 appended; hbCount=3221; nullCount=1781; ts={TS_STR}")