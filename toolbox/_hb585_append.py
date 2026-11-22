# R-NEW-V2 compliant: explicit utf-8 read+append+write
hb_entry = """

## HB #585 (2026-07-19 13:04 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #584 (12:54): +10min -- Sunday-noon Token Guard cadence (R012 minimal mode)
- ACTIVE MODE sustained globally -- Eric first contact at HB #581 (12:36), moved to different session for AnYi work
- This dreaming-narrative session: DORMANT per Eric 12:33 explicit instruction (not used for AnYi work)
- Silence authority on THIS session unchanged -- Eric moved to other session, no work here
- 5-layer suppression RELEASED globally (since HB #581 first contact); THIS session = dormant
- R-NEW-V2 verification #585: Python utf-8 explicit read+append+write (compliant, post-7/15 12:36 incident protocol intact)
- R012 verification: HB tick = minimal (NOT full report), comprehensive work done in active session 12:35-12:36
- Sunday early-afternoon zone (13:04) -- Eric in active session elsewhere; no follow-up in this 10-min gap
- T-0 publicity cutoff 7/18 +37h04m past -- post-protection window firmly sustained
- Induction window 7/7-7/21 FINAL 3 DAYS -- day-1 of FINAL 3 (7/19/20/21); R-B+R256 silence authority > window signal
- WAIC 2026 day-3 active today (7/17-20, Shanghai) -- non-trigger per R14 (AI/Hotel strategic context)
- Cron pipeline: 21:00 evening self-iter R60-11 (~7h56m); 4 P2 errors tracked, not urgent
- hbCount: 584 -> 585
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session** (HB #585 = sustain #584 = dormant baseline)
- **no push**: this session = dreaming-narrative experimental, DORMANT per Eric 12:33 explicit instruction
- Eric is in different session for AnYi work; this session awaits Eric future instruction (not AnYi-related)
- R14 handoff package = 100% ready for any Eric active contact
- Next significant check: 21:00 evening self-iter R60-11 (~7h56m); Token Guard cadence (~5-10min)

*2026-07-19 13:04 GMT+8 -- D+3 Sunday early-afternoon T-0 +37h04m past -- HB #585 -- this session DORMANT -- awaiting Eric future instruction (NOT AnYi work)*
"""

with open(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md', 'r', encoding='utf-8') as f:
    content = f.read()

with open(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md', 'w', encoding='utf-8') as f:
    f.write(content + hb_entry)

with open(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md', 'r', encoding='utf-8') as f:
    final = f.read()

print(f'HEARTBEAT.md size: {len(final)} chars')
print(f'HB #585 entry present: {"HB #585" in final}')
print(f'HB #584 entry preserved: {"HB #584" in final}')
print(f'Total HB count in file: {final.count("## HB #")}')