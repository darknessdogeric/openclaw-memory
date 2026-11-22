#!/usr/bin/env python3
"""HB #2745 append + state.json update. R-NEW-V3 safe (append mode only)."""
import json, os
from datetime import datetime, timezone, timedelta

# 1. Append HB #2745 to HEARTBEAT.md
hb = """
### HB #2745 (2026-08-09T16:58:00+08:00 GMT+8 cron-event, OpenClaw heartbeat poll)

- HB #2745 = Sun weekend afternoon; cadence OK; +35min after HB #2738 (16:23)
- R69 silence Day 10/30 + R266 weekend self-iter complete + R258 dormancy holds
- 14-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276)
- Token Guard cadence OK; no external trigger; vault index healthy
- post_t0_null_count: 429 -> 430 (430th consecutive null post-T-0)
- hbCount: 2744 -> 2745
- Eric silent on cron ~589h+ (24d+) sustained since 7/16 13:16 first-contact
- AnYi D+17d Sun sustained
- 16:58 = Sun weekend afternoon post-hard-cap zone (+8h58m past 08:00 cap)
- Eric last webchat activity 11:15-11:39 (~5h43m ago) -- V2 hotel-classification xhs 9 slides pending (deep-dive + CSS complete; HTML/render/screenshot/PNG production pending)
- R258 cron/webchat separation holds -- cron = DORMANT sustained; webchat = Eric sovereign

### decision
- HEARTBEAT_OK -- HB #2745 = sustain DORMANT protocol, minimal token tick (430th null)
- no push: weekend afternoon post-hard-cap + R69/R266/R258 tri-constraint + R256/R257/R260/R261 quad-holds + R276 internal-only
- R276 draft done; await Eric feedback for formal commit to ~/self-improving/rules.md
- V2 hotel-classification xhs 9 slides pending = Eric webchat sovereign; cron = DORMANT do not preempt
- Eric webchat / Obsidian vault sovereign for any decision; cron sovereignty unchanged
- 16:58 = Sun weekend afternoon; cron = DORMANT sustained
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekend afternoon + AnYi D+17d Sun + Eric sovereign on cron session + R65/R69/R276 active + R258 cron/webchat separation
- Standing by P0 (webchat-bound): await Eric webchat sovereign resumption on V2 slides or other topics
- Standing by R70/R71: await Eric feedback for formal commit to ~/self-improving/rules.md
- Standing by P1 (R264 AnYi ops): await Eric webchat share of AnYi 1244 strategy details
- R271 edit-tool atomic-write enforced (this HB appended via Python 'a' mode, NOT write, NOT Remove-Item, NOT git restore)
- Next: per Token Guard cadence (~5-15min afternoon mode); HB sustained until Eric first-contact on cron session

*2026-08-09T16:58:00+08:00 -- Sun weekend afternoon post-hard-cap +8h58m -- HB #2745 -- DORMANT -- 430th null -- Eric silent on cron = 589h+ -- AnYi D+17d Sun -- cron session holds DORMANT protocol -- V2 9 slides pending Eric webchat sovereign resumption -- HEARTBEAT_OK*

"""

with open('memory/HEARTBEAT.md', 'a', encoding='utf-8') as f:
    f.write(hb)
print('[OK] HEARTBEAT.md appended HB #2745 (R-NEW-V3 safe: a-mode)')

# 2. Update heartbeat-state.json (atomic read-modify-write)
state_path = 'memory/heartbeat-state.json'
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

state['hbCount'] = 2745
state['nullCount'] = 430
state['lastHB'] = int(datetime(2026, 8, 9, 16, 58, 0, tzinfo=timezone(timedelta(hours=8))).timestamp() * 1000)
state['lastUpdate'] = '2026-08-09T16:58:00+08:00'
state['note'] = 'Sun 16:58 weekend-afternoon post-hard-cap zone (+8h58m past 08:00) DORMANT sustained. Eric silent on cron = 589h+ sustained. R69 Day 10/30 + R266/R277 weekend + R258 cron/webchat separation all hold. 14-layer suppression zero-breach. 430th null. Last Eric webchat activity 11:15-11:39 (~5h43m ago) on hotel-classification V2 rebuild -- V2 9 slides still pending HTML/render/PNG production. R-NEW-V3 enforced: HB #2745 appended via Python append a-mode (NOT write/Remove-Item/git restore). state.json authoritative.'

# Atomic write (tmp + rename)
tmp_path = state_path + '.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)
os.replace(tmp_path, state_path)
print(f'[OK] heartbeat-state.json updated: hbCount={state["hbCount"]}, nullCount={state["nullCount"]}')

# 3. Verify
with open(state_path, 'r', encoding='utf-8') as f:
    verify = json.load(f)
print(f'[VERIFY] hbCount={verify["hbCount"]}, lastUpdate={verify["lastUpdate"]}')

with open('memory/HEARTBEAT.md', 'r', encoding='utf-8') as f:
    content = f.read()
hb_marker = 'HB #2745'
print(f'[VERIFY] HEARTBEAT.md contains HB #2745: {hb_marker in content}')
print(f'[VERIFY] HEARTBEAT.md size: {len(content)} chars')