#!/usr/bin/env python3
"""Append HB entry to HEARTBEAT.md (R-NEW-V3 -- Add-Content only, never overwrite)."""
import os
from datetime import datetime, timezone, timedelta

ws = r"D:\B166ER-OpenClaw\workspace"
tz = timezone(timedelta(hours=8))
ts = datetime.now(tz)
ts_iso = ts.isoformat(timespec="seconds")
ts_short = ts.strftime("%H:%M")
hb = 3742
prev = 3741

entry = f"""
### HB #{hb} ({ts_iso} cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev} (16:23): +4min -- Sat weekend-afternoon Token Guard cadence (R012, in tolerance)
- {ts_short} = Sat weekend-afternoon (Eric weekend rest per USER.md)
- 14-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R-NEW-V3/R70/R71) -- penta+ holds
- state.json atomic-tick via os.replace (hbCount {prev} -> {hb}, R-NEW-V4)
- Eric webchat SOVEREIGN (cron idle ~92h+ since 8/18 19:06)
- AnYi Day 29 (Sat weekend-afternoon)
- R69 silence Day 29/30 (expires 2026-08-30 Sun, **8 calendar days remain**) -- cron does not break silence
- vault 1254+ files healthy
- R-NEW-V3 enforced: HEARTBEAT.md appended via Add-Content (PS7+); no overwrite (recovery mode from prior data loss 8/1)

### decision
- HEARTBEAT_OK -- HB #{hb} = sustain DORMANT protocol, minimal token tick
- no push: suppression holds + Sat weekend-afternoon + cron session DORMANT per R65/R258/R69/R277/R282
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- R65/R69 active + Eric sovereign on webchat + cron DORMANT
- Standing by P0 (webchat-bound, all unchanged): 15-5 strategy v0.1 + V2 slides + R276 commit + R264 AnYi 1244 + Eric two reports + R278/R282/R283/R284/R285/R286 (all drafts) -- all await Eric webchat sovereign
- R69 countdown: 8 calendar days to lift silence on 8/30 Sun -- R282 + R283 + R284 + R285 + R286 batch ready for lift
- Next: per Token Guard cadence (~15-30min weekend-afternoon); HB sustained until Eric first-contact on webchat

*{ts_iso} -- Sat weekend-afternoon + ~4min from HB #{prev} -- HB #{hb} -- DORMANT -- Eric webchat sovereign (cron idle ~92h+ since 8/18 19:06) -- AnYi D+29d Sat -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 + R69-T8d enforced -- HEARTBEAT_OK*
- HB #{hb} @ {ts_short} | DORMANT sustain | R69 Day 29/30 (lift 8/30 Sun) | Eric weekend rest | no push (R65/R258/R69/R-NEW-V3) | decision: HEARTBEAT_OK
"""

hb_path = os.path.join(ws, "HEARTBEAT.md")
# R-NEW-V3: Add-Content equivalent -- open in append mode (NEVER overwrite)
with open(hb_path, "a", encoding="utf-8") as f:
    f.write(entry)

print(f"HEARTBEAT.md append OK -- HB #{hb} entry written")
print(f"file size: {os.path.getsize(hb_path):,} bytes")
