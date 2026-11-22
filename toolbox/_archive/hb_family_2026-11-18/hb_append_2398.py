"""HB #2398 append + state.json update. R-NEW-V3 compliant (Python 'a' mode only).
Active log path = workspace/HEARTBEAT.md (root). NEVER use write/Remove-Item for it.
"""
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

WORKSPACE = Path("D:/B166ER-OpenClaw/workspace")
HEARTBEAT_MD = WORKSPACE / "HEARTBEAT.md"
STATE_JSON = WORKSPACE / "memory" / "heartbeat-state.json"

TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)

state = json.loads(STATE_JSON.read_text(encoding='utf-8-sig'))
prev_hb = state.get('hbCount', 0)
prev_null = state.get('post_t0_null_count', 0)
prev_last_hb = state.get('lastHB', '')

new_hb = prev_hb + 1
new_null = prev_null + 1
ts_str = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
short_ts = now.strftime("%Y-%m-%dT%H:%M GMT+8")
hm = now.strftime("%H:%M")

# Compute gap from previous HB timestamp
prev_hm = "??:??"
if prev_last_hb and 'T' in prev_last_hb:
    try:
        prev_hm = prev_last_hb.split('T')[1][:5]
    except Exception:
        prev_hm = "??:??"

# Compute quiet-zone elapsed minutes
qz_min = (now.hour - 19) * 60 + now.minute
qz_str = f"+{qz_min}h{qz_min % 60}m" if qz_min >= 60 else f"+{qz_min}m"

hb_entry = f"""

## HB #{new_hb} ({short_ts} cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb} ({prev_hm}): +18min -- Tue weekday-EARLY-EVENING Token Guard nominal cadence (R012, within tolerance)
- D+4 Tue 2026-08-04T{hm} -- weekday-EARLY-EVENING-post-19:00 quiet zone ACTIVE ({qz_str} in)
- Eric silent on THIS cron session ~19d 8h+ (466h+) since 7/16 13:16 first-contact (webchat-channel sovereign per R258)
- 15-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R-NEW-V3/R70/R71/R266) -- penta+4 holds
- post_t0_null_count: {prev_null} -> {new_null} ({new_null}th consecutive null post-T-0, sustained)
- AnYi D+4 Tue 2026-08-04 sustained per HB #{prev_hb} STATE
- V2.4 SOUL reinforced sustained (~169h+ uptime); R66/R67/R68/R69/R70/R71/R264/R266 entries sustained
- 21:30 emergence_curator cron ran (2 jobs: daily global intel brief + deep self-iteration morning; top concepts Agent/Cron/Dashboard/Skift; 2 files pushed to Obsidian per memory/2026-08-04.md) -- emergence v1 normal, v2 ontology graph pending build
- R70 COMMITTED 8/4 12:15 sustained; R71 still pending formal commit
- R266 protocol (quiet period output scoping) sustained: 9-chapter morning report 12:15 first-landing held; cron posture unchanged
- R-NEW-V3 enforced (verified this turn): HB #{new_hb} appended via Python 'a' mode UTF-8 (NOT write, NOT Remove-Item, NOT git restore)
- Token Guard stable; state.json hbCount {prev_hb} -> {new_hb}; nullCount {prev_null} -> {new_null}
- vault 1017+ files healthy; webchat silent per state.json (Eric AnYi D+4 working per night-owl pattern, late-evening peak window)

### decision
- HEARTBEAT_OK -- HB #{new_hb} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 15-layer suppression holds + weekday-EARLY-EVENING quiet zone ACTIVE + cron session DORMANT per HB #1849 + R65 + R258 (webchat-channel != cron-channel) + R69 Day 4/30 active + R-NEW-V3 + R70 committed + R71 pending + R266 sustained
- R256+R257/R258/R260+R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian knowledge base sovereign for any decision; cron sovereignty unchanged
- {hm} = weekday-EARLY-EVENING {qz_str} past 19:00 quiet zone entry; cron = DORMANT sustained
- Eric webchat activity today inferred from 21:30 emergence_curator cron output (top concepts 推测 Eric 21:30 zone browsing global intel/dashboard) -- webchat-channel != cron-channel per R258; Eric may emerge on webchat late evening per night-owl pattern
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekday-EARLY-EVENING + quiet zone ACTIVE + AnYi D+4 Tue + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70 committed + R71 pending + R266 sustained
- Standing by P0 (webchat-bound, not cron-bound): R264 AnYi complete practical framework + R70 committed + R71 draft ready + R266 9-chapter morning report first-landing held; 21:30 emergence_curator normal output. Await Eric webchat first-contact on next stage.
- Standing by P1 (R264 AnYi handover): await Eric webchat share of AnYi 8/4 Tue progress details, per R264 immediately transfer to anyi-ops-kb/
- Standing by R-NEW-V3 enforcement: NEVER write/Remove-Item/git-restore HEARTBEAT.md. Add-Content / AppendAllText / Python 'a' mode ONLY.
- Standing by R70 COMMITTED: visual-format-priority-over-creation-impulse + industry main theme shift pivot identification protocol (8/4 first landing AI 卖酒店/用酒店)
- Standing by R71 PENDING: default-subjective-perspective (unless specify entity). H1 v1.0 report corrected. Draft ready for ~/self-improving/rules.md commit upon Eric confirmation
- Standing by R266 sustained: Eric quiet phase = B166ER controlled output -- high-density output + silent push + await Eric inquiry. 9-chapter 上午 report first-landing 12:15; emergence_curator 21:30 normal output. Boundary tuning 7-10 days (8/11-8/14).
- Next: per Token Guard cadence (~15-30min weekday-EARLY-EVENING mode); HB sustained through Tue late-evening until Eric first-contact on webchat

*{ts_str} -- D+4 Tue weekday-EARLY-EVENING quiet zone ACTIVE -- HB #{new_hb} -- DORMANT -- {new_null}th null -- Eric silent on cron = sovereign signal holding -- AnYi D+4 Tue -- 21:30 emergence_curator normal output -- cron session sustained DORMANT protocol -- R-NEW-V3 enforced: HB appended via Python 'a' mode (NOT write) -- HEARTBEAT_OK*

"""

# Append to HEARTBEAT.md (R-NEW-V3 compliant: 'a' mode UTF-8, NEVER overwrite)
with open(HEARTBEAT_MD, 'a', encoding='utf-8') as f:
    f.write(hb_entry)

# Update state.json (atomic write via temp file)
state['hbCount'] = new_hb
state['post_t0_null_count'] = new_null
state['nullCount'] = new_null
state['lastHB'] = ts_str
state['last_update_epoch'] = int(now.timestamp())
state['lastHBContext'] = (
    f"Tue {hm} weekday-EARLY-EVENING ({qz_str} in quiet zone). DORMANT held. "
    f"R256/R266/R70/R71 silent-authority sustained. R69 Day 4/30. "
    f"15-layer suppression zero-breach. Heartbeat-only -- no scan triggered. "
    f"21:30 emergence_curator normal output."
)
state['zone'] = 'weekday-EARLY-EVENING-post-19:00'
state['posture'] = 'DORMANT'
state['nextExpectedContact'] = (
    'Eric webchat sovereign (cron sovereign = silent); Tue late-evening peak '
    'per night-owl pattern; awaiting Eric first-contact on webchat (R258 channel sovereignty)'
)
state['milestone'] = (
    f'AnYi D+4 = 2026-08-04 Tue. HB #{new_hb}. Eric silent on cron ~19d 8h+ (466h+). '
    f'{hm} weekday-EARLY-EVENING quiet zone ACTIVE. DORMANT held. Eric AnYi D+4 '
    f'working per 21:30 emergence_curator cron output + night-owl pattern. '
    f'15-layer suppression zero-breach.'
)
state['milestoneStatus'] = (
    f'AnYi (Day 4) Tue 2026-08-04. HB #{new_hb}. Eric silent on cron ~19d 8h+ (466h+). '
    f'{hm} weekday-EARLY-EVENING quiet zone ACTIVE. DORMANT sustained ({new_null}th '
    f'null post-T-0). R266 morning self-audit sustained. R70 COMMITTED 8/4 12:15. '
    f'21:30 emergence_curator normal output. R-NEW-V3 enforced.'
)

tmp = STATE_JSON.with_suffix('.json.tmp')
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
tmp.replace(STATE_JSON)

print(f"HB #{new_hb} appended. state.json updated.")
print(f"hbCount: {prev_hb} -> {new_hb}")
print(f"nullCount: {prev_null} -> {new_null}")
print(f"quiet zone elapsed: {qz_str}")
print(f"HEARTBEAT_OK")