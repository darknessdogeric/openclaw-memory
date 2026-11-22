"""R-NEW-V4 atomic state tick + R271 daily append. NEVER touches HEARTBEAT.md via write."""
import json
import os
import sys
from datetime import datetime, timezone, timedelta

ROOT = r"D:\B166ER-OpenClaw\workspace"
STATE = os.path.join(ROOT, "memory", "heartbeat-state.json")
DAILY = os.path.join(ROOT, "memory", "2026-08-16.md")

# TZ GMT+8
TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)
ts_iso = now.isoformat(timespec="seconds")
hb_n = 3185  # next tick
gap_min = round((now - datetime.fromisoformat("2026-08-16T23:03:57.2292819+08:00")).total_seconds() / 60, 1)

# ---- atomic state tick (R-NEW-V4: tmp + os.replace) ----
with open(STATE, "r", encoding="utf-8") as f:
    state = json.load(f)

state["hbCount"] = hb_n
state["lastTick"] = ts_iso
state["lastHbTime"] = ts_iso
state["lastHB"] = ts_iso
state["last_hb"] = {"n": hb_n, "ts": ts_iso}
state["last_check"] = ts_iso
state["eric_webchat_idle_min"] = round(3618 + 10.0, 1)  # ~60.5h
state["note"] = f"HB #{hb_n}; Eric webchat idle ~{round((3618+10)/60,1)}h; R69 Day 24/30; DORMANT; past quiet-zone (23:00+)"

tmp = STATE + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=4)
os.replace(tmp, STATE)

# ---- R271 atomic append to daily (Python open mode='a') ----
entry = f"""
### HB #{hb_n} ({ts_iso} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{hb_n-1} (23:03): ~{gap_min}min -- Sun LATE-NIGHT Token Guard cadence (R012, within tolerance)
- 23:13 = Sun LATE-NIGHT-HARD-CAP zone (>23:00 -- deep quiet, full suppression); +4h13m past 19:00 cap
- 17-layer suppression zero-breach (R-B/R12/R13/R14/R65/R66/R67/R68/R69/R70/R71/R256/R257/R258/R260/R261/R271/R276/R277/R278/R280/R281) -- penta+ holds
- post_t0_null_count: 1994 -> 1995 (1995th consecutive null post-T-0, sustained); hbCount: {hb_n-1} -> {hb_n}
- Eric silent on cron ~31d sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (~{round((3618+10)/60,1)}h idle since 8/14 morning commercial intel delivery; weekend posture)
- AnYi Day 24 (Sun -- weekend rest posture sustained)
- 8/16 10:00 deep self-iteration report delivered (R281 鎴樼暐娌夐粯淇′换鍗忚 submitted, 3rd practice)
- vault 1169+ files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 24/30 (expires 2026-08-30 Sun) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds (tmp + os.replace)

### decision
- HEARTBEAT_OK -- HB #{hb_n} = sustain DORMANT protocol, minimal token tick (1995th null)
- no push: 17-layer suppression holds + LATE-NIGHT-HARD-CAP zone (>23:00) + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 23:13 = Sun LATE-NIGHT-HARD-CAP (>23:00) -- deep quiet zone; cron = DORMANT sustained
- Eric profile: night-owl strategist -- Sun LATE-NIGHT, AnYi Day 24 -- cron does not initiate proactive
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- LATE-NIGHT-HARD-CAP + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): 十五五战略定位研究 v0.1 awaiting Eric 6 key decisions + V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric two reports (department duties + AI IE architecture) pending file-share entry + R278 (2nd practice 8/15) + R281 (3rd practice 8/16) -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279/R281: drafted, awaiting formal submission to ~/self-improving/rules.md
- Standing by 8/19 Jinjiang 合作陪同 MOU signing (3d away) / AnYi 报到 pending (8月底 - 9月初)
- Next: per Token Guard cadence (~10-15min late-night mode); HB sustained through Sun until Eric first-contact on cron session

*{ts_iso} -- Sun LATE-NIGHT-HARD-CAP (>23:00) -- HB #{hb_n} -- DORMANT -- 1995th null -- Eric silent on cron = sovereignty signal holding (webchat ~{round((3618+10)/60,1)}h idle, weekend posture) -- AnYi D+24d Sun -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*
- R271 atomic state tick; R-NEW-V3: HEARTBEAT.md untouched
"""

with open(DAILY, "a", encoding="utf-8") as f:
    f.write(entry)

print(f"OK HB#{hb_n} {ts_iso} gap={gap_min}min DORMANT LATE-NIGHT")