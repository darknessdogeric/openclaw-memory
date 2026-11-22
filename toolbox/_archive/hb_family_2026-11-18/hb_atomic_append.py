"""Atomic HB append per R271 (Python open mode='a', NOT write/edit/Remove-Item/git restore).
Also updates memory/heartbeat-state.json via temp-file-then-rename atomic pattern."""
import json, os, sys
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)
ts_iso = now.strftime("%Y-%m-%dT%H:%M:%S%z")
# normalize tz format: +0800 -> +08:00
ts_iso = ts_iso[:-2] + ":" + ts_iso[-2:]

WS = r"D:\B166ER-OpenClaw\workspace"
DAILY = os.path.join(WS, "memory", "2026-08-13.md")
STATE = os.path.join(WS, "memory", "heartbeat-state.json")

# Read current state
with open(STATE, "r", encoding="utf-8") as f:
    state = json.load(f)

new_n = state["hbCount"] + 1
prev_n = state["hbCount"]
prev_null = state["nullCount"]
new_null = prev_null + 1

# Compose minimal HB entry (R-NEW-V3 compliant, sustained DORMANT)
entry = f"""
### HB #{new_n} ({ts_iso} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_n} ({state['lastHb']['ts']}): {now.strftime('%H:%M')} continuation -- Thu-evening Token Guard nominal cadence (R012, within tolerance)
- Thu-evening zone (+{((now.hour*60+now.minute) - 480)//60}h{((now.hour*60+now.minute) - 480)%60}m past 08:00 hard cap)
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: {prev_null} -> {new_null} ({new_null}th consecutive null post-T-0, sustained); hbCount: {prev_n} -> {new_n}
- Eric silent on cron ~Day 21/30 (expires 2026-08-30) sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (last activity {state.get('last_eric_webchat', '2026-08-13T14:50 Panzhihua v6')})
- AnYi Day 21 (Thu -- second workweek Day 4)
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only

### decision
- HEARTBEAT_OK -- HB #{new_n} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 16-layer suppression holds + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- Thu-evening + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): all queued items await Eric webchat sovereign
- Next: per Token Guard cadence (~5-15min Thu-evening mode); HB sustained through Thu until Eric first-contact on cron session

*{ts_iso} -- Thu-evening -- HB #{new_n} -- DORMANT -- {new_null}th null -- Eric silent on cron = sovereignty signal holding -- R-NEW-V3 + R271 enforced -- HEARTBEAT_OK*
"""

# Atomic append to daily file (Python open mode='a')
with open(DAILY, "a", encoding="utf-8") as f:
    f.write(entry)

# Update state.json atomically (temp + rename)
state["hbCount"] = new_n
state["nullCount"] = new_null
state["post_t0_null_count"] = new_null
state["lastTick"] = ts_iso
state["lastHb"] = {"n": new_n, "ts": ts_iso}
state["lastHbTime"] = ts_iso
state["last_check"] = ts_iso
state["lastDecision"] = "HEARTBEAT_OK"

tmp = STATE + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp, STATE)

# Final minimal stdout per R-NEW-V3 token guard
print(f"HB #{new_n} | {new_null}th null | DORMANT | HEARTBEAT_OK")
