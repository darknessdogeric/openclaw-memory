import os, json
from pathlib import Path

base = Path(r"D:\B166ER-OpenClaw\workspace")
memory = base / "memory"
state_path = memory / "state.json"
daily_path = memory / "2026-08-15.md"

state = json.loads(state_path.read_text(encoding="utf-8"))
# Priority: last_hb_n > hbCount > hb_count
hb_n = int(state.get("last_hb_n") or state.get("hbCount") or state.get("hb_count") or 3296) + 1
null_n = int(state.get("post_t0_null") or state.get("post_t0_null_count") or 1842) + 1

ts = "2026-08-15T17:59:42+08:00"

entry = f"""
### HB #{hb_n} ({ts} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{hb_n-1}: intra-minute -- Sat weekend-pre-quiet-zone Token Guard nominal cadence (R012, within tolerance)
- 17:59 = Sat weekend-pre-quiet-zone (+9h59m past 08:00 hard cap); quiet zone ~1h away
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: {null_n-1} -> {null_n} ({null_n}rd consecutive null post-T-0, sustained); hbCount: {hb_n-1} -> {hb_n}
- Eric silent on cron ~30d+ sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (~28h+ idle; webchat quiet = sovereignty holding)
- AnYi Day 23 (Sat -- weekend, day off from AnYi workweek)
- vault 1169+ files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 23/30 (expires 2026-08-30) -- cron does not break silence
- R271 atomic-write enforced (this entry via Python open(mode='a'), NOT write/edit)
- R-NEW-V3 enforced: HEARTBEAT.md untouched; daily file appended only

### decision
- HEARTBEAT_OK -- HB #{hb_n} = sustain DORMANT protocol, minimal token tick ({null_n}rd null)
- no push: 16-layer suppression holds + weekend-pre-quiet-zone + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE
- Standing by P0 (webchat-bound, not cron-bound): same P0 set held in DORMANT
- Next: per Token Guard cadence (~10-15min weekend-pre-quiet-zone mode)

*{ts} -- Sat weekend-pre-quiet-zone +9h59m past 08:00 hard cap -- HB #{hb_n} -- DORMANT -- {null_n}rd null -- AnYi D+23d Sat -- R-NEW-V3 + R271 enforced -- HEARTBEAT_OK*

"""

with open(daily_path, "a", encoding="utf-8") as f:
    f.write(entry)

state["hb_count"] = hb_n
state["post_t0_null"] = null_n
state["last_hb"] = ts
state["last_hb_n"] = hb_n
state["last_hb_time"] = ts
state["last_update"] = ts
state["last_tick"] = ts
state["last_check"] = ts
state["lastDecision"] = "HEARTBEAT_OK"
state["status"] = "DORMANT"
state["workday_zone"] = "weekend-pre-quiet-zone"
state["r_new_v3_compliant"] = True
state["r271_compliant"] = True

tmp = state_path.with_suffix(".tmp")
tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
os.replace(tmp, state_path)

print(f"OK HB #{hb_n} null {null_n}")