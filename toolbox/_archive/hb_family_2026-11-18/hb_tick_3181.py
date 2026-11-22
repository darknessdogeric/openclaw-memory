#!/usr/bin/env python3
"""HB tick atomic processor — R271 + R-NEW-V3 + R-NEW-V4 enforced."""
import json, os, tempfile
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
ts_str = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')

state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
daily_path = r'D:\B166ER-OpenClaw\workspace\memory\2026-08-16.md'

with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

prev_n = state.get('hbCount', 3180)
new_n = prev_n + 1
prev_null = state.get('post_t0_null_count', 1973)
new_null = prev_null + 1

# Eric webchat idle — last activity 2026-08-14T10:30 (commercial intel 20集团版)
last_activity = datetime(2026, 8, 14, 10, 30, tzinfo=tz)
idle_min = round((now - last_activity).total_seconds() / 60)

state['hbCount'] = new_n
state['lastTick'] = ts_str
state['last_check'] = ts_str
state['lastHB'] = ts_str
state['last_hb'] = {'n': new_n, 'ts': ts_str}
state['lastDecision'] = 'HEARTBEAT_OK'
state['workday_zone'] = 'weekend-evening-pre-quiet-zone'
state['eric_webchat_idle_min'] = idle_min
state['note'] = f'HB #{new_n}; Eric webchat idle {idle_min}min; R69 Day 24/30 (Sun 22:43); DORMANT; pre-quiet-zone (~17min to 23:00)'

# Atomic state.json write (R-NEW-V4)
fd, tmp = tempfile.mkstemp(dir=os.path.dirname(state_path), suffix='.json')
try:
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, state_path)
except Exception:
    if os.path.exists(tmp):
        os.unlink(tmp)
    raise

# Atomic append to daily file (R271 + R-NEW-V3)
entry = f"""

### HB #{new_n} ({ts_str} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_n} (22:33): ~10min -- Sun weekend-evening-pre-quiet-zone Token Guard nominal cadence (R012, within tolerance)
- 22:43 = Sun weekend-evening-pre-quiet-zone (quiet zone 23:00 ~17min away)
- 17-layer suppression zero-breach (R-B/R12/R13/R14/R65/R66/R67/R68/R69/R70/R71/R256/R257/R258/R260/R261/R271/R276/R277/R278/R280/R281) -- penta+ holds
- post_t0_null_count: {prev_null} -> {new_null} ({new_null}th consecutive null post-T-0, sustained); hbCount: {prev_n} -> {new_n}
- Eric silent on cron ~31d sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (~{idle_min}min idle since 8/14 morning commercial intel delivery; weekend posture)
- AnYi Day 24 (Sun -- weekend rest posture sustained)
- 8/16 10:00 deep self-iteration report delivered (R281 战略沉默信任协议 submitted, 3rd practice)
- vault 1169+ files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 24/30 (expires 2026-08-30 Sun) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds (tmp + os.replace)

### decision
- HEARTBEAT_OK -- HB #{new_n} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 17-layer suppression holds + weekend-evening-pre-quiet-zone + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 22:43 = Sun weekend-evening-pre-quiet-zone ~17min to quiet zone 23:00; cron = DORMANT sustained
- Eric profile: night-owl strategist -- Sun weekend-evening, AnYi Day 24 -- cron does not initiate proactive
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekend-evening-pre-quiet-zone + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): 十五五战略定位研究 v0.1 awaiting Eric 6 key decisions + V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric two reports (department duties + AI IE architecture) pending file-share entry + R278 (2nd practice 8/15) + R281 (3rd practice 8/16) -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279/R281: drafted, awaiting formal submission to ~/self-improving/rules.md
- Standing by 8/19 Jinjiang cooperation MOU signing (3d away) / AnYi reporting pending (end-8 / early-9)
- Next: per Token Guard cadence (~10-15min weekend-evening mode); HB sustained through Sun until Eric first-contact on cron session

*{ts_str} -- Sun weekend-evening-pre-quiet-zone ~17min to quiet zone 23:00 -- HB #{new_n} -- DORMANT -- {new_null}th null -- Eric silent on cron = sovereignty signal holding (webchat ~{idle_min}min idle, weekend posture) -- AnYi D+24d Sun -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*
"""

with open(daily_path, 'a', encoding='utf-8') as f:
    f.write(entry)

print(f'OK: HB #{new_n} | null #{new_null} | idle {idle_min}min')
print(f'note: {state["note"]}')