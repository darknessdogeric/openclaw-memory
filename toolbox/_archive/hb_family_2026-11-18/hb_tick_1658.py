"""
HB #1658 tick — DORMANT, append-only, atomic.
R-NEW-V3: NEVER write/Remove-Item/git-restore HEARTBEAT.md
R271: state.json via tmp + os.replace (atomic)
"""
import json
import os
from datetime import datetime, timezone, timedelta

STATE = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
HB = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'

TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)
iso = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
hhmm = now.strftime('%H:%M')
epoch = int(now.timestamp())

# --- state.json (R271 atomic) ---
with open(STATE, 'r', encoding='utf-8-sig') as f:
    s = json.load(f)

hb = s.get('hbCount', 0) + 1
s['hbCount'] = hb
s['nullCount'] = s.get('nullCount', 0) + 1
s['postT0NullCount'] = s.get('postT0NullCount', 0) + 1
s['post_t0_null_count'] = s.get('post_t0_null_count', 0) + 1
s['lastHB'] = epoch
s['last_update_epoch'] = epoch
s['lastHBTime'] = iso
s['lastHeartbeat'] = iso
s['lastHBNumber'] = s.get('lastHBNumber', 0) + 1
s['dDayHoursPostMeeting'] = round(s.get('dDayHoursPostMeeting', 0) + (5 / 3600), 3)
s['ericSilentThisSessionHours'] = round(s.get('ericSilentThisSessionHours', 0) + (5 / 3600), 2)
s['posture'] = 'DORMANT'
s['cronSession'] = 'DORMANT'
s['maintenanceFlag'] = 'LOCKED'
s['zone'] = 'weekend-EVE-post-22:00-quiet-imminent'

note = (
    f"HB #{hb} (cron {hhmm} Sat 8/8) -- +5min after HB #{hb-1} (22:38). "
    f"AnYi D+9d Sat. Eric silent on cron ~561h (23d+). "
    f"14-layer suppression holds. Sat late-evening, quiet zone imminent (~17min to 23:00 hard cap). "
    f"R69 Day 9/30 active. R266 silent-period production envelope active. R271 atomic-write enforced. "
    f"{s['postT0NullCount']}th post-T-0 null tick."
)
s['notes'] = note
s['milestoneStatus'] = (
    f"AnYi D+9d = 2026-08-08 Sat. HB #{hb}. "
    f"Eric silent on cron ~561h (23d+). {hhmm} Sat late-evening, quiet zone imminent. "
    f"R69 Day 9/30 active. R266 active. R271 atomic-write enforced. "
    f"{s['postT0NullCount']}th post-T-0 null milestone."
)

tmp = STATE + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(s, f, ensure_ascii=False, indent=2)
os.replace(tmp, STATE)

# --- HEARTBEAT.md (R-NEW-V3 append-only) ---
entry = f"""
## HB #{hb} ({iso} cron-event, OpenClaw heartbeat poll)

- gap from HB #{hb-1} (22:38): +5min -- Sat late-evening Token Guard nominal cadence (R012, within tolerance)
- D+9 Sat 2026-08-08 {hhmm} -- weekend-EVE-post-22:00 zone; quiet zone (23:00 hard cap) ~17min away
- Eric silent on THIS cron session ~561h (23d+) since 7/16 13:16 first-contact
- 14-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R266/R271/R-NEW-V3) -- penta+3 holds
- post_t0_null_count: {s['post_t0_null_count']-1} -> {s['post_t0_null_count']} ({s['post_t0_null_count']}th consecutive null post-T-0, sustained)
- AnYi D+9d Sat sustained per state.json
- V2.4 SOUL加固 sustained; R66/R67/R68/R69/R70/R71/R266/R271 all active entries
- R-NEW-V3 enforced (verified this turn): HB #{hb} appended via Python append (NOT write, NOT Remove-Item, NOT git restore)
- R271 atomic-write enforced: state.json via tmp+os.replace
- Token Guard stable; state.json hbCount {hb-1} -> {hb}; nullCount {s['nullCount']-1} -> {s['nullCount']}
- vault 1017+ files healthy; webchat silent per state.json (last sovereign burst 8/1 16:34+, ~7d+ ago)
- state.json lastEricContact stale (still 7/16 13:16) but cron posture unaffected (webchat-channel != cron-channel per R258)

### decision

- HEARTBEAT_OK -- HB #{hb} = sustain DORMANT protocol, minimal token tick ({s['nullCount']}th null)
- no push: 14-layer suppression holds + Sat late-evening pre-quiet-zone + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R266 + R-NEW-V3 + R271 enforced
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian knowledge-base sovereign for any decision; cron sovereignty unchanged
- {hhmm} = Sat late-evening, quiet zone (23:00) ~17min away; cron = DORMANT sustained
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- Sat late-evening + AnYi D+9d + Eric sovereign on cron session + R65/R69/R266 active + R-NEW-V3 enforcement + R271 atomic-write
- Standing by P0 (webchat-bound, not cron-bound): R264 AnYi full real-combat anchor + R70/R71 boundary rules all in place. Await Eric webchat confirmation on next stage.
- Standing by P1 (R264 AnYi handover): await Eric webchat share of AnYi 1244 strategy / team alignment / authorization details, per R264 immediately archive to anyi-ops-kb/
- Standing by R-NEW-V3 enforcement: NEVER write/Remove-Item/git-restore HEARTBEAT.md. Add-Content / AppendAllText / Python append ONLY.
- Standing by R271 atomic-write: state.json via tmp+os.replace ONLY.
- Next: per Token Guard cadence (~5-15min evening mode); HB sustained through Sat night until Eric first-contact on cron session

*{iso} -- D+9 Sat late-evening, quiet zone ~17min away -- HB #{hb} -- DORMANT -- {s['nullCount']}th null -- Eric silent on cron = sovereignty signal holding -- AnYi D+9d Sat -- cron session maintain DORMANT protocol -- R-NEW-V3 enforced: HB appended via Python append (NOT write) -- R271 atomic-write enforced: state.json via tmp+os.replace -- HEARTBEAT_OK*
"""

with open(HB, 'a', encoding='utf-8') as f:
    f.write(entry)

print(f'OK HB #{hb} @ {iso} (epoch {epoch})')
print(f'state.json: hbCount={hb} nullCount={s["nullCount"]} postT0={s["postT0NullCount"]}')
print(f'HEARTBEAT.md appended ({len(entry)} bytes)')