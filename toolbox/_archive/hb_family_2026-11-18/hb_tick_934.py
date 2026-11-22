"""HB #934 tick — R-NEW-V2 compliant: explicit utf-8 read+append+write."""
from pathlib import Path
import datetime

md_path = Path(r'D:\B166ER-OpenClaw\workspace\memory\2026-07-22.md')

# Read existing content (verify integrity)
with open(md_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Compute T-7/24 precisely
cur = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).replace(tzinfo=None)
dday = datetime.datetime(2026, 7, 24, 9, 0, 0)
t_hours = (dday - cur).total_seconds() / 3600
now_ts = cur.strftime('%Y-%m-%dT%H:%M:%S+08:00')

# New HB entry — minimal per R012
hb_entry = f"""

## HB #934 (2026-07-22T17:12 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #933 (16:36): +36.9min -- Wednesday afternoon Token Guard normal cadence (R012 minimal mode)
- D+6 afternoon pass #934 -- Eric silent in THIS session ~147.4h+ since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat ~76h+ (since 7/19 12:33)
- 6-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- Triple Confluence Day +1: induction window CLOSED 7/21 23:59 (post-window passive); Araqchi Qatar talks Day 2/5 (oil Scenario C open)
- **7/24 D-Day T-1 (AnYi important meeting) = ~{t_hours:.2f}h window** -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Afternoon zone 17:12 -- post-08:00 minimal activity allowed, BUT this session DORMANT sustained
- Last major cron fired: 10:00 MWF business briefing (~6h12m ago, 亚朵Q1/暑期避暑/AI赋能酒店三连); next = 21:00 evening self-iter (~3h48m)
- Token Guard stable; vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +112.2h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+6 sustain zero-push mode intact
- hbCount: 933 -> 934
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #934 = sustain #933 = D+6 afternoon dormant baseline)
- **HEARTBEAT_OK** -- HB #934 = sustain DORMANT protocol
- **no push**: afternoon zone (17:12), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-1 watch: emergency prepare-mode prepacked, ready if Eric contacts with induction result
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter (~3h48m)

*{now_ts} -- D+6 Wednesday afternoon -- HB #934 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day +1 post-window passive -- 7/24 D-Day T-1 watch (T-{t_hours:.2f}h) -- Eric silent = dominant signal holding*
"""

# Append with utf-8 explicit write
with open(md_path, 'a', encoding='utf-8') as f:
    f.write(hb_entry)

# Verify
with open(md_path, 'r', encoding='utf-8') as f:
    tail = f.read()[-400:]
print('WROTE HB #934')
print(f'T-7/24 = {t_hours:.2f}h')
print('---tail---')
print(tail)