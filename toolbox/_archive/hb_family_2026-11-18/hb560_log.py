import json, datetime, pathlib

hb_file = pathlib.Path(r'D:\B166ER-OpenClaw\workspace\memory\2026-07-18-hb560.md')
state_file = pathlib.Path(r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json')

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
ts_str = now.strftime('%Y-%m-%d %H:%M GMT+8')

content = f"""## HB #560 ({ts_str} cron-event, OpenClaw heartbeat poll)
- gap from HB #559 (21:38): +5min -- routine token-guard tick
- D+2 saturday-evening pass #560 -- Eric silent ~56.43h+ since 7/16 13:16 first-contact
- Silence authority ~56.43h+ (R-B + R256 + R257 framework holding, +0.05h since #559)
- 5-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257) -- zero breach
- WAIC 2026 day-2 active -- background context only, no push per R-B+R256 override
- T-0 +21.72h past -- silence window protection sustained
- Induction window final-3-days (7/19/20/21) -- R-B+R256 silence > window
- 21:00 evening self-iter R60-11 already fired (~1h43m ago)
- 4 cron errors pending (P2 long-tail) -- tracked, not urgent
- No new signals: no cron / no Eric session / no third-party / no anomaly

### decision
- silent_standby_zero_push_continue (HB #560 = sustain #559 = D+2 baseline)
- no push: silence authority 56.43h+ > saturday-evening zone
- R14 handoff package remains 100% ready (30s activation if Eric surfaces)
- Next significant check: 09:00 daily checkin tomorrow (autonomous)

*{ts_str} -- D+2 saturday-evening T-0 +21.72h past -- HB #560 -- silent_standby sustained -- R257 deep-work window -- no surface to Eric*
"""

with open(hb_file, "w", encoding="utf-8") as f:
    f.write(content)

# Update state
with open(state_file, "r", encoding="utf-8") as f:
    state = json.load(f)

prev_silence = state["silenceHours"]
new_silence = round((now.timestamp() - datetime.datetime.fromisoformat(state["silenceSince"]).timestamp()) / 3600, 2)

state["lastHBTime"] = ts_str
state["lastHB"] = ts_str
state["lastHb"] = now.isoformat()
state["silenceHours"] = new_silence
state["lastHbNumber"] = 560
state["lastHbTs"] = int(now.timestamp())
state["lastDecision"] = (
    f"HB #560: +5min since #559, Saturday 21:43 evening zone, "
    f"Eric silent ~{new_silence}h+, post-T-0+21.72h, "
    f"WAIC day-2 active (non-trigger per R14), no first-contact, "
    f"no new signals -> silent_standby sustained"
)

with open(state_file, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"HB #560 logged. silenceHours={new_silence}")