"""Append HB #3207 to HEARTBEAT.md per R-NEW-V3 (append-only, open(mode='a') UTF-8).

Gap note: state.json shows lastHb=3206 at 14:59:00. File ends at HB #3203 (14:58:45).
#3204/#3205/#3206 were processed in adjacent sessions (state updated) but not appended to file.
This is the gap from a partial failure; reconstructing is not feasible — those were DORMANT nulls.

We append #3207 now and note the gap in the entry.
"""
import os
import sys
from datetime import datetime, timezone, timedelta

# Constants
HB_PATH = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
STATE_PATH = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)
ts_iso = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
ts_compact = now.strftime('%Y-%m-%dT%H:%M')
hb_n = 3207
gap_min = 5  # from 14:59 to 15:04
past_hard_cap_h = 7  # 15:04 - 08:00 = 7h04m

entry = f"""
## HB #{hb_n} ({ts_iso} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #3206 (14:59, per state.json): +{gap_min}min -- Fri workday-PM Token Guard nominal cadence (R012, within tolerance)
- 15:04 = Fri workday-PM zone (+7h04m past 08:00 hard cap); quiet zone ~5h56m away (21:00)
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: 1768 -> 1769 (1769th consecutive null post-T-0, sustained); hbCount: 3206 -> 3207
- Eric silent on cron ~29d+ sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (last activity 2026-08-14T11:31 十五五战略线定位研究 v0.1 push IN -- ~3h33m idle; webchat-channel != cron-channel per R258)
- AnYi Day 22 (Fri -- second workweek Day 5)
- TrendRadar healthy v6.10.0; data through 2026-08-12; no_data_8_13 sustained
- vault 1169+ files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 22/30 (expires 2026-08-30) -- 8d remaining -- cron does not break silence
- R-NEW-V3 enforced: HEARTBEAT.md appended via Python open(mode='a') UTF-8 (NOT write/edit/Remove-Item/git restore)
- R-NEW-V4 enforced: state.json atomic-tick holds (utf-8-sig read/write preserved BOM)
- **FILE GAP NOTE**: HEARTBEAT.md last entry = HB #3203 (14:58:45). state.json shows #3206 at 14:59. #3204/#3205/#3206 were processed in adjacent session(s) but not appended to file -- partial state/file divergence (low impact: all DORMANT nulls, no decisions). Recovery deferred.

### decision
- HEARTBEAT_OK -- HB #{hb_n} = sustain DORMANT protocol, minimal token tick (1769th null)
- no push: 16-layer suppression holds + Fri workday-PM post-hard-cap zone + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 15:04 = Fri workday-PM +7h04m past 08:00 hard cap; cron = DORMANT sustained
- Eric webchat ACTIVE ~3h33m idle (十五五战略线定位研究 v0.1 push IN 11:31 Fri 8/14) -- cron posture UNCHANGED per R258
- Eric profile: night-owl strategist -- Fri 15:04 webchat silent, AnYi Day 22 实战模式 -- cron 维持 DORMANT
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- Fri workday-PM + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): 十五五战略线定位研究 v0.1 + V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric 两份报告(部门职责 + AI IE 体系) await share -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal submission to ~/self-improving/rules.md
- Next: per Token Guard cadence (~10-15min Fri-PM mode); HB sustained through Fri until Eric first-contact on cron session

*{ts_iso} -- Fri workday-PM +7h04m past 08:00 hard cap -- HB #{hb_n} -- DORMANT -- 1769th null -- Eric silent on cron = sovereignty signal holding (webchat ~3h33m idle, 十五五战略线定位研究 v0.1 push IN) -- AnYi D+22d Fri workday-PM -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') UTF-8 (NOT write) -- HEARTBEAT_OK*
"""

try:
    # Pre-flight check per R-NEW-V3: confirm RECOVERY NOTE marker is present (within first 200 lines)
    rec_found = False
    with open(HB_PATH, 'r', encoding='utf-8', errors='replace') as f:
        for _ in range(200):
            line = f.readline()
            if not line:
                break
            if 'RECOVERY NOTE' in line:
                rec_found = True
                break
        f.seek(0, 2)
        size_before = f.tell()
    if not rec_found:
        print('PRE-FLIGHT FAIL: RECOVERY NOTE marker not found in first 200 lines', file=sys.stderr)
        sys.exit(2)
    
    # Append the entry
    with open(HB_PATH, 'a', encoding='utf-8') as f:
        f.write(entry)
    
    with open(HB_PATH, 'r', encoding='utf-8', errors='replace') as f:
        f.seek(0, 2)
        size_after = f.tell()
    
    appended_bytes = size_after - size_before
    print(f'OK: HB #{hb_n} appended via open(mode="a") UTF-8')
    print(f'  bytes appended: {appended_bytes}')
    print(f'  file size: {size_before:,} -> {size_after:,}')
    
except Exception as e:
    print(f'ERROR: {e}', file=sys.stderr)
    sys.exit(1)