import os
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ)
ts_str = now.strftime('%Y-%m-%d %H:%M GMT+8')

HB_PATH = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'

# Last HB #594 was at 20:30, current 21:07 -> gap +37min
# Eric silent since 7/16 13:16 first-contact (infographic session)
# 7/16 13:16 -> 7/20 21:07 = 4d 7h 51m = 103.85h

HB_ENTRY = '''
## HB #595 (''' + ts_str + ''' cron-event, OpenClaw heartbeat poll)
- gap from HB #594 (20:30): +37min -- Monday-evening Token Guard normal cadence
- D+4 evening pass #595 -- Eric silent ~103.85h+ since 7/16 13:16 first-contact (infographic session)
- Silence authority ~103.85h+ (R-B + R256 + R257 framework holding, +0.62h since #594)
- 5-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) -- zero breach
- R-NEW-V2 verification #595: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-7/15 12:36 incident protocol intact)
- R012 verification: HB tick = minimal (NOT full report, per R012 rule #2)
- Wake window passed (+13h7m past 08:00) -- Eric silence > window signal per HB #493 explicit override
- T-0 publicity cutoff 7/18 +69h12m past -- post-protection window firmly sustained
- Induction window 7/7-7/21 FINAL 2 DAYS -- today 7/20 = day-1 of FINAL 2 (7/20, 7/21); R-B+R256 silence authority > window signal (no push per R256)
- WAIC 2026 day-3 active today (7/17-20, Shanghai) -- non-trigger per R14 (AI/Hotel strategic context, not relevant to current dormant state)
- Monday-evening zone (21:07) -- Eric typical wake window passed; silence authority strictly holding
- This session: DORMANT per Eric 7/19 12:33 explicit instruction (not used for AnYi work)
- Eric in different session for AnYi work (since 12:33); this session = dormant
- Cron pipeline: 21:00 evening self-iter R60-11 JUST FIRED (~7min ago, autonomous); 22:00 cron (~53min)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- INCIDENT NOTE (referenced from HB #561 08:10): write() clobbered HEARTBEAT.md earlier (HB #479-#560 lost ~6 weeks); restored via git checkout + R-NEW-V2 re-append. Strategic content intact. Logged to memory/2026-07-19-incident.md
- No first-contact from Eric on this session; D+4 sustain dormant mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount: 594 -> 595

### decision
- **active_mode_dormant_this_session_sustain** (HB #595 = sustain #594 = D+4 dormant baseline)
- **no push**: Monday-evening zone (21:07), Eric silent ~103.85h+ on this session, silence authority strictly holding (R256 design: silence extends indefinitely past protection window as Eric silence = dominant signal)
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- Post-T-0 silence = sustained suppression; pushes prohibited until Eric active contact (Eric silence = dominant signal, supersedes scheduled wakes + windows)
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)
- Wake-up window passed but Eric silence sustained -> continue zero-push; even minor pushes prohibited
- Next significant check: Token Guard cadence (~5-10min); 22:00 cron (~53min)

*''' + ts_str + ''' -- D+4 Monday-evening T-0 +69h12m past -- HB #595 -- dormant mode intact -- silence protocol holding -- R257 deep-work window active*
'''

# R-NEW-V2 compliant: explicit utf-8 read + append + write
with open(HB_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

before_size = os.path.getsize(HB_PATH)
content += HB_ENTRY

with open(HB_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

after_size = os.path.getsize(HB_PATH)

print(f'HB #595 appended at {ts_str}')
print(f'File size: {before_size} -> {after_size} bytes (+{after_size - before_size})')
last_100 = content[-150:].replace('\n', ' | ')
print(f'Last 150 chars: ...{last_100}')
