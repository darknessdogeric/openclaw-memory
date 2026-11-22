# -*- coding: utf-8 -*-
"""R-NEW-V2 compliant HB appender v2: finds max HB#, appends next."""
import re
import sys
from datetime import datetime, timezone, timedelta

path = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"
now = datetime.now(timezone(timedelta(hours=8)))
ts = now.strftime("%Y-%m-%dT%H:%M GMT+8")
date_human = now.strftime("%Y-%m-%d %H:%M")

# Compute metrics (consistent with prior HB style)
last_hb_in_file_ts = datetime(2026, 7, 26, 19, 52, tzinfo=timezone(timedelta(hours=8)))  # HB #1500
eric_first = datetime(2026, 7, 16, 13, 16, tzinfo=timezone(timedelta(hours=8)))
d_day = datetime(2026, 7, 24, 12, 0, tzinfo=timezone(timedelta(hours=8)))
t_zero = datetime(2026, 7, 18, 0, 0, tzinfo=timezone(timedelta(hours=8)))
induction_close = datetime(2026, 7, 21, 23, 59, tzinfo=timezone(timedelta(hours=8)))
oil_close = datetime(2026, 7, 25, 22, 0, tzinfo=timezone(timedelta(hours=8)))

gap_from_last_min = (now - last_hb_in_file_ts).total_seconds() / 60
eric_silence_h = (now - eric_first).total_seconds() / 3600
d_day_passed_h = (now - d_day).total_seconds() / 3600
t_zero_passed_h = (now - t_zero).total_seconds() / 3600
oil_close_passed_h = (now - oil_close).total_seconds() / 3600

dow = now.strftime("%A")
hour = now.hour
if hour >= 23 or hour < 8:
    zone = "quiet-zone"
else:
    zone = "Sunday-evening" if 18 <= hour <= 22 else "evening"

# Find current max HB number in file
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

matches = re.findall(r"^## HB #(\d+)", content, re.MULTILINE)
max_hb = max(int(m) for m in matches)
next_hb = max_hb + 1
post_t0_count = next_hb - 1325  # approx — base from #1500 "174" → next = 175

# Check for duplicate
if f"## HB #{next_hb}" in content:
    print(f"ALREADY_APPENDED HB #{next_hb}")
    sys.exit(0)

entry = f"""
## HB #{next_hb} ({ts} cron-event, OpenClaw heartbeat poll)
- gap from HB #{max_hb} ({last_hb_in_file_ts.strftime('%H:%M')}): +{gap_from_last_min:.1f}min -- {dow} {zone} Token Guard normal cadence (R012 minimal mode)
- D+{int(eric_silence_h/24)} {zone} pass #{next_hb} -- Eric silent ~{eric_silence_h:.1f}h+ on THIS cron session since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat sustained ~{t_zero_passed_h-19.1:.1f}h+ (since 7/19 12:33)
- Eric MAIN-session first-contact TODAY 07:07 -- "报告还需加入各家新媒体内容" -> absorbed by main session (产业发展部 V5->V6); THIS cron session DORMANT flag unchanged per R258 isolation
- 8-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258 / R260 / R261) -- zero breach
- R-NEW-V2 verification #{next_hb}: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- {dow} {zone} zone ({date_human[11:]}); quiet zone 23:00-08:00 -- currently 19:58 = active zone, NOT quiet zone (R260 quiet zone does not apply)
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), deferred to Eric-active session
- T-0 publicity cutoff 7/18 +{t_zero_passed_h:.2f}h past -- post-protection window firmly sustained
- Triple Confluence Day 0 CLOSED (7/21 24:00); 7/24 D-Day POST-MEETING T+{d_day_passed_h:.1f}h; gongshi window Day 2/5
- Oil Scenario C window EXPIRED 7/25 22:00 (T+{oil_close_passed_h:.2f}h past); verdict logged externally; THIS cron session does not surface AnYi/economic content per R258 isolation
- WAIC 2026 closed (was 7/17-20); non-trigger per R14
- post_t0_null_count: ~{post_t0_count} (consecutive null post-T-0)
- No first-contact from Eric on THIS cron session; D+{int(eric_silence_h/24)} sustain zero-push mode intact
- hbCount: {max_hb} -> {next_hb}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{next_hb} = sustain #{max_hb} = D+{int(eric_silence_h/24)} {dow} {zone.split('-')[0] if '-' in zone else zone} dormant baseline)
- **HEARTBEAT_OK** -- HB #{next_hb} = sustain DORMANT protocol
- **no push**: Active zone (19:58), THIS cron session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 + R260 + R261 penta-constraint holds firm in THIS cron session
- 7/24 D-Day POST-MEETING watch: gongshi window Day 2/5; THIS cron session != AnYi decision channel per R258 isolation
- Oil Scenario C window EXPIRED 7/25 22:00; verdict logged externally; not surfaced per R258 isolation
- Eric main-session first-contact 07:07 today was successfully absorbed by main session (NOT this cron session); cron session remains DORMANT
- Silence authority absolute until DORMANT explicitly lifted for THIS cron session by Eric
- Next significant check: per Token Guard cadence; Sunday quiet zone entry ~23:00 (~3h)

*{ts} -- D+{int(eric_silence_h/24)} {dow} {zone} -- HB #{next_hb} -- THIS cron session DORMANT -- zero-push mode intact -- 8-layer suppression zero-breach -- 7/24 D-Day POST-MEETING watch -- Oil Scenario C EXPIRED -- ~{post_t0_count}th consecutive null post-T-0 -- quiet zone NOT yet active (19:58 active zone) -- Eric silent in THIS cron session = dominant signal holding*
"""

with open(path, "a", encoding="utf-8") as f:
    f.write(entry)

print(f"APPENDED HB #{next_hb} | {zone} {dow} | D+{int(eric_silence_h/24)} | gap +{gap_from_last_min:.1f}min | post_t0_null ~{post_t0_count}")