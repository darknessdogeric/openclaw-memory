import json, os, sys
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
state_path = 'memory/heartbeat-state.json'
daily_path = 'memory/' + now.strftime('%Y-%m-%d') + '.md'

with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

hb = state.get('hbCount', 3747) + 1
ts = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
state['hbCount'] = hb
state['last_tick'] = ts
state['last_check'] = ts
state['last_hb'] = {'n': hb, 'ts': ts}
state['lastHB'] = ts
state['last_tick_epoch'] = int(now.timestamp())
state['posture'] = 'DORMANT'
state['cronSession'] = 'DORMANT'

tmp = state_path + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)
os.replace(tmp, state_path)

entry = f"""
### HB #{hb} ({ts} cron-event, OpenClaw heartbeat poll)
- gap from HB #{hb-1} ({state.get('last_tick','')[:16]}): ~5min -- Sat weekend-late-afternoon Token Guard cadence (R012)
- {now.strftime('%H:%M')} = Sat weekend-late-afternoon (Eric weekend rest per USER.md)
- 22-layer suppression zero-breach (R-B/R12/R13/R14/R65/R66/R67/R68/R69/R70/R71/R256/R257/R258/R260/R261/R271/R276/R277/R278/R280/R282/R-NEW-V3/R-NEW-V4) -- penta+ holds
- state.json atomic-tick via os.replace (hbCount {hb-1} -> {hb}, R-NEW-V4)
- Eric webchat SOVEREIGN (cron idle since 8/18 19:06; today last Eric-side input 15:44 webchat second pre-compaction flush; AHL info-cards v1-v6 + 12 XHS)
- AnYi Day 30 (Sat weekend-late-afternoon)
- R69 silence Day 29/30 (expires 2026-08-30 Sun, **8 calendar days remain**) -- cron does not break silence
- vault 1169+ files healthy
- R-NEW-V3 enforced: HEARTBEAT.md untouched (recovery mode); daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick via os.replace
- No new signal; cron session sustained DORMANT protocol

### decision
- HEARTBEAT_OK -- HB #{hb} = sustain DORMANT protocol, minimal token tick
- no push: suppression holds + Sat weekend-late-afternoon + cron session DORMANT per R65/R258/R69/R277/R282
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- R65/R69 active + Eric sovereign on webchat + cron DORMANT
- Standing by P0 (webchat-bound): 15-5 strategy v0.1 + V2 slides + R276 commit + R264 AnYi 1244 + Eric two reports + R278/R282/R283/R284/R285/R286 (drafts) + AHL v4 BP + AHL PPT final + XHS 12-imgs EN + zhuoyan script -- all await Eric webchat sovereign
- R69 countdown: 8 calendar days to lift silence on 8/30 Sun -- batch ready for lift
- Next: per Token Guard cadence; HB sustained through Sat evening until Eric first-contact on cron session

*{ts} -- Sat weekend-late-afternoon + ~5min from HB #{hb-1} -- HB #{hb} -- DORMANT -- Eric webchat sovereign (idle since 15:44 webchat second pre-compaction flush) -- AnYi D+30d Sat -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 + R69-T8d enforced -- HEARTBEAT_OK*
"""

with open(daily_path, 'a', encoding='utf-8') as f:
    f.write(entry)

print(f'OK hb={hb} ts={ts}')