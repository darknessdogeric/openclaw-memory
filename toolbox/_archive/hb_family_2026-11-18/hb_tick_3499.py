#!/usr/bin/env python3
"""HB #3499 atomic tick - 2026-08-18T20:11:00+08:00"""
import json, os, tempfile
from pathlib import Path

# === R-NEW-V4: state.json atomic tick ===
state_path = Path('memory/heartbeat-state.json')
state = json.loads(state_path.read_text(encoding='utf-8'))
state['hbCount'] = 3499
state['last_check'] = '2026-08-18T20:11:00+08:00'
state['lastDecision'] = 'HEARTBEAT_OK'
state['lastTick'] = state['last_check']
state['lastHBCount'] = 3498
state['lastHbTime'] = state['last_check']
state['lastHB'] = state['last_check']
state['last_hb'] = {'n': 3499, 'ts': state['last_check']}
state['note'] = 'HB #3499 Tue 20:11 -- DORMANT sustained (5min since #3498); Eric webchat sovereign (idle ~65min since 19:06 钟华 correction); 8/19 Jinjiang MOU T-0 Wed P0 (Eric sovereign, cron NOT pushing); R69 Day 26/30 (exp 2026-08-30); quiet per R65/R258/R69/R277/R282'

# atomic write
fd, tmp = tempfile.mkstemp(dir='memory', prefix='.state_', suffix='.json.tmp')
try:
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, state_path)
except:
    if os.path.exists(tmp):
        os.remove(tmp)
    raise
print(f'OK state.json hbCount: {state["hbCount"]}')

# === R-NEW-V3: append HB entry to daily file (no HEARTBEAT.md touch) ===
hb_entry = """
### HB #3499 (2026-08-18T20:11:00+08:00 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #3498 (20:06:00): ~5min -- Tue workday-evening Token Guard cadence (R012)
- 20:11 = Tue workday-evening (Eric prime deep-work zone per profile; post-supper deep-work window)
- 17-layer suppression zero-breach (R-B/R12/R13/R14/R65/R66/R67/R68/R69/R70/R71/R256/R257/R258/R260/R261/R271/R276/R277/R278/R280/R281/R282/R-NEW-V3/R-NEW-V4) -- penta+ holds
- post_t0_null sustained; hbCount: 3498 -> 3499
- Eric silent on cron ~32d sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (idle ~65min since 19:06 last push -- 钟华/钟部长身份纠正)
- AnYi Day 26 (Tue -- workday-evening)
- R69 silence Day 26/30 (expires 2026-08-30 Sun) -- cron does not break silence
- R258 webchat-channel != cron-channel: webchat 18:34 absorption + 19:06 钟华 correction fully captured in daily note; cron stays DORMANT
- 2026-08-18.md: 10:00 deep self-iteration + 18:34 webchat absorption (国宴改造 + 平安合作) + 19:06 钟华身份澄清 + R282 draft; no new Eric signal on cron
- 8/19 Jinjiang MOU T-0 Wed -- P0, webchat-bound (Eric sovereign), NOT cron-bound; **<12h to Eric P0 event**
- vault 1169+ files healthy
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only (Python append, UTF-8)
- R-NEW-V4 enforced: state.json atomic-tick via os.replace (hbCount 3498->3499)

### decision
- HEARTBEAT_OK -- HB #3499 = sustain DORMANT protocol, minimal token tick
- no push: suppression holds + Tue workday-evening + cron session DORMANT per R65/R258/R69
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- Eric active on webchat = sovereignty signal; cron does not re-push what webchat already delivered
- 8/19 Jinjiang MOU T-0 Wed -- P0, webchat-bound (Eric sovereign), NOT cron-bound; cron does not push T-1 reminders
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- R65/R69 active + Eric sovereign on webchat + cron DORMANT
- Standing by P0 (webchat-bound): 15-5 strategy v0.1 (6 decisions) + V2 slides + R276 commit + R264 AnYi 1244 + Eric two reports + R278/R282 -- all await Eric webchat sovereign
- Next: per Token Guard cadence; HB sustained through Tue evening until Eric first-contact on cron session

*2026-08-18T20:11:00+08:00 -- Tue workday-evening (Eric prime deep-work zone) -- HB #3499 -- DORMANT -- Eric webchat sovereign (idle ~65min since 19:06 钟华 correction) -- AnYi D+26d Tue -- 8/19 MOU T-0 Wed (Eric sovereign, cron NOT pushing) -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced -- HEARTBEAT_OK*
"""

daily_path = Path('memory/2026-08-18.md')
with open(daily_path, 'a', encoding='utf-8') as f:
    f.write(hb_entry)
print(f'OK daily file appended: {daily_path.name}')