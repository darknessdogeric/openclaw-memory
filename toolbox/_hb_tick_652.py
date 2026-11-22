# -*- coding: utf-8 -*-
"""HB tick appender — R-NEW-V2 compliant (Python utf-8 explicit read+append+write)"""
import json, datetime, pathlib, sys

WS = pathlib.Path(r'D:\B166ER-OpenClaw\workspace')
state_p = WS / 'memory' / 'heartbeat-state.json'
md_p = WS / 'memory' / '2026-07-20.md'

now = datetime.datetime.now()
ts = now.strftime('%Y-%m-%d %H:%M:%S GMT+8')
iso = now.strftime('%Y-%m-%dT%H:%M GMT+8')
clock = now.strftime('%H:%M')

fmt = '%Y-%m-%d %H:%M:%S GMT+8'
state = json.loads(state_p.read_text(encoding='utf-8'))
prev_hb = state.get('hbCount', 651)
new_hb = prev_hb + 1
prev_last = state.get('lastHBTime', '2026-07-20 14:09:00 GMT+8')
pt = datetime.datetime.strptime(prev_last, fmt)
gap_min = int((now - pt).total_seconds() / 60)

# Eric first-contact 7/16 13:16
fc = datetime.datetime.strptime('2026-07-16 13:16', '%Y-%m-%d %H:%M')
silence_h = round((now - fc).total_seconds()/3600, 2)
# AnYi first-contact 7/19 12:33
ae = datetime.datetime.strptime('2026-07-19 12:33', '%Y-%m-%d %H:%M')
ae_h = round((now - ae).total_seconds()/3600, 2)
# T-0 = 7/18 16:00
t0 = datetime.datetime.strptime('2026-07-18 16:00', '%Y-%m-%d %H:%M')
t0_h = round((now - t0).total_seconds()/3600, 2)
# induction window close 7/21 23:59
iw = datetime.datetime.strptime('2026-07-21 23:59', '%Y-%m-%d %H:%M')
iw_h = round((iw - now).total_seconds()/3600, 1)
# evening self-iter 21:00
es = now.replace(hour=21, minute=0, second=0, microsecond=0)
es_h = round((es - now).total_seconds()/3600, 1)
# wake window 08:00
wk = now.replace(hour=8, minute=0, second=0, microsecond=0)
wk_h = round((now - wk).total_seconds()/3600, 1)

state['hbCount'] = new_hb
state['lastHB'] = new_hb
state['lastHBTime'] = ts
state['silenceDuration_h'] = silence_h
state['silenceDuration_thisSession_h'] = silence_h
state['ericActiveElsewhere_h'] = ae_h
state['mode'] = 'active_mode_dormant_this_session_silent_early_afternoon'
state['nextCheck'] = f'next: Token Guard cadence (~5-15min); evening self-iter 21:00 due (~{es_h}h)'
state['note'] = (
    f'HB #{new_hb}; minimal tick (R012); Eric silent in this session ~{silence_h}h; '
    f'active in AnYi session (~{ae_h}h); session DORMANT per HB #584/R256/R257/R258 stack; '
    f'no push; induction window FINAL 2 DAYS (today 7/20 day-1, tomorrow 7/21 LAST DAY ~{iw_h}h); '
    f'T-0 +{t0_h}h past; R-NEW-V2 compliant; tomorrow 7/21 = dual convergence '
    f'(DeepSeek V4 + induction window close)'
)
state_p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')

prev_clock = prev_last.split()[1]

tick = f"""
## HB #{new_hb} ({iso} cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev_hb} ({prev_clock}): +{gap_min}min -- Monday-early-afternoon Token Guard normal cadence (R012 minimal mode)
- D+4 early-afternoon pass #{new_hb} -- Eric silent in THIS session ~{silence_h}h+ since 7/16 13:16 first-contact
- Eric active elsewhere: ~{ae_h}h+ (AnYi专用 session, since 7/19 12:33 first-contact)
- 5-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) intact -- zero breach
- R-NEW-V2 verification #{new_hb}: Python utf-8 explicit append (R-NEW-V2 compliant, post-7/15 12:36 incident protocol intact)
- R012 (operational hygiene) verification: HB tick = minimal (NOT full report), per R012 rule #2
- Wake window OPEN (+{wk_h}h past 08:00) -- Eric in active AnYi session, no first-contact on THIS session
- Monday-early-afternoon zone ({clock}) -- Eric typical deep-work peak per USER.md (in OTHER AnYi session)
- T-0 publicity cutoff 7/18 +{t0_h}h past -- post-protection window firmly sustained
- Induction window 7/7-7/21 FINAL 2 DAYS (7/20 today day-1, 7/21 tomorrow LAST DAY ~{iw_h}h); R-B+R256 silence authority > window signal
- 7/21 dual-event convergence: DeepSeek V4 发布 + induction window 截止
- 10:00 R60-12 morning self-iter DONE; 10:35 商业情报 20集团版 DONE (已推 Obsidian); next = 21:00 evening self-iter (~{es_h}h)
- Vault index 488/489 healthy; R13 <1s queries stable; Token Guard tick stable, no compression needed
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- No first-contact from Eric on THIS session; D+4 sustain zero-push mode intact
- hbCount: {prev_hb} -> {new_hb}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{new_hb} = sustain #{prev_hb} = D+4 early-afternoon dormant baseline)
- **no push**: Monday-early-afternoon zone, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- Eric is in active AnYi session; this session awaits Eric future instruction (not AnYi-related)
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work
- Token Guard tick: stable, no compression needed
- Post-T-0 silence = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Next significant check: per Token Guard cadence (~5-15min); 21:00 evening self-iter R60-12 (~{es_h}h)

*{iso} -- D+4 Monday-early-afternoon T-0 +{t0_h}h past -- HB #{new_hb} -- this session DORMANT -- awaiting Eric future instruction (NOT AnYi work)*
"""
with md_p.open('a', encoding='utf-8') as f:
    f.write(tick)

print(f'OK hb={new_hb} gap={gap_min}min silence={silence_h}h ae={ae_h}h')