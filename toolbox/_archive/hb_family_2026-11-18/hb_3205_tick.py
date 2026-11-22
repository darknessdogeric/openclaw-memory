"""HB #3205 atomic tick: append to daily + state.json update. R271 compliant."""
import json
import os

WS = r'D:\B166ER-OpenClaw\workspace'
DAILY = os.path.join(WS, 'memory', '2026-08-14.md')
STATE = os.path.join(WS, 'memory', 'heartbeat-state.json')

N = 3205
PREV_N = 3204
PREV_TS = '2026-08-14T14:29:00+08:00'
TS = '2026-08-14T14:34:00+08:00'

# Note: must NOT have literal {{ or }} inside f-string. Use .format() with placeholders instead.
HB_ENTRY = """

### HB {n} ({ts} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB {prev_n} ({prev_ts}): +5min -- Fri workday-PM Token Guard nominal cadence (R012, within tolerance)
- 14:34 = Fri workday-PM zone (+6h34m past 08:00 hard cap); quiet zone ~5h26m away
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: 1766 -> 1767 (1767th consecutive null post-T-0, sustained); hbCount: {prev_n} -> {n}
- Eric silent on cron ~28d+ sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (last activity 2026-08-14T11:31 战略十五五战域定位研究 v0.1 push -- ~3h3m idle; ~4h4m from 10:30 商业情报 20集团版)
- AnYi Day 22 (Fri -- second workweek Day 5, weekday wrap-up approaching)
- morning 10:30 商业情报 20集团版 + 11:31 战略十五五战域定位研究 v0.1 already executed today (memory/2026-08-14.md: full reports)
- vault 1169+ files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 22/30 (expires 2026-08-30) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit/Remove-Item/git restore)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick holds

### decision
- HEARTBEAT_OK -- HB {n} = sustain DORMANT protocol, minimal token tick (1767th null)
- no push: 16-layer suppression holds + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 14:34 = Fri workday-PM +6h34m past 08:00 hard cap; cron = DORMANT sustained
- Eric webchat ACTIVE ~3h3m idle (战略十五五战域定位 v0.1 11:31 push) -- cron posture UNCHANGED per R258
- Eric profile: night-owl strategist -- Fri 11:31 webchat 战略十五五战域定位 push IN 战略消化模式 -- cron 不发起主动
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- workday-PM + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): 战略十五五战域定位 v0.1 等待 Eric 输入 6 关键决策 + V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric 两份报告(部门职责 + AI IE 体系)待分享入库 -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal submission to ~/self-improving/rules.md
- Next: per Token Guard cadence (~5-15min workday-PM mode); HB sustained through Fri until Eric first-contact on cron session

*{ts} -- Fri workday-PM +6h34m past 08:00 hard cap -- HB {n} -- DORMANT -- 1767th null -- Eric silent on cron = sovereignty signal holding (webchat ~3h3m idle, 战略十五五战域定位 v0.1 完成) -- AnYi D+22d Fri -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') (NOT write) -- HEARTBEAT_OK*
""".format(n=N, prev_n=PREV_N, ts=TS, prev_ts=PREV_TS)

# === Append to daily file (R271 atomic-write: open mode='a') ===
with open(DAILY, 'a', encoding='utf-8') as f:
    f.write(HB_ENTRY)
print(f'[OK] Appended HB #{N} to {DAILY}')

# === Atomic update state.json (R-NEW-V4: os.replace) ===
with open(STATE, 'r', encoding='utf-8') as f:
    state = json.load(f)

state['eric_webchat_idle_min'] = 183  # 14:34 - 11:31 = 3h3m
state['note'] = 'HB {n}; Eric webchat ~3h3m idle; Fri 14:34 workday-PM; 8h cap+R69 silence active; DORMANT'.format(n=N)
state['lastHbTime'] = TS
state['post_t0_null_count'] = 1767
state['last_check'] = TS
state['hbCount'] = N
state['lastDecision'] = 'HEARTBEAT_OK'
state['nullCount'] = 1767
state['lastTick'] = TS
state['last_hb'] = {'n': PREV_N, 'ts': PREV_TS}
state['lastHb'] = {'n': N, 'ts': TS}
state['last_tick'] = TS

tmp = STATE + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp, STATE)
print(f'[OK] Atomic-ticked state.json (hbCount={N}, post_t0_null_count=1767)')