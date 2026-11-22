#!/usr/bin/env python3
"""R-NEW-V2 compliant HB log appender. Explicit utf-8 read+append+write.
Avoids 7/19 08:10 write() clobber incident. 2026-07-19 protocol."""
import io
from pathlib import Path

HB_PATH = Path(r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md")
STATE_PATH = Path(r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json")

NEW_HB = r"""

## HB #935 (2026-07-22T17:05 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #934 (16:50): +14.5min -- Wednesday afternoon Token Guard normal cadence (R012 minimal mode)
- D+6 afternoon pass #935 -- Eric silent in THIS session ~147.82h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~76.32h+ (since 7/19 12:33)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #935: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day +1 post-window passive; Araqchi Qatar talks (7/21-25) Day 2/5 -> oil Scenario C verification window OPEN until 7/25
- Wednesday afternoon zone (17:05) -- Eric typical late-afternoon deep-work or approaching evening transition; THIS session DORMANT sustained
- 7/24 D-Day T-39.92h (AnYi important meeting Thursday morning) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- 10:00 MWF daily briefing fired ~7h05m ago (autonomous, BI brief committed to memory/2026-07-22.md: 亚朵Q1+47.5%/零售38.1% + 暑期避暑+230%/AI降本20-30% 三连)
- Next cron: 21:00 evening self-iter R60-11 (~3h55m)
- Token Guard stable, no compression needed
- Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +112.83h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+6 sustain zero-push mode intact
- hbCount: 934 -> 935
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #935 = sustain #934 = D+6 afternoon dormant baseline)
- **HEARTBEAT_OK** -- HB #935 = sustain DORMANT protocol
- **no push**: Wednesday afternoon zone (17:05), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-39.92h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter (~3h55m)

*2026-07-22T17:05 GMT+8 -- D+6 Wednesday afternoon -- HB #935 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day +1 post-window passive -- 7/24 D-Day T-39.92h watch (AnYi meeting Thursday morning) -- Eric silent = dominant signal holding*
"""

# R-NEW-V2 compliant: explicit utf-8 read+append+write
def append_hb():
    with io.open(HB_PATH, "r", encoding="utf-8") as f:
        existing = f.read()
    with io.open(HB_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(existing)
        if not existing.endswith("\n"):
            f.write("\n")
        f.write(NEW_HB.lstrip("\n"))
    print(f"OK: HB #935 appended ({len(NEW_HB)} bytes)")

def update_state():
    import json
    with io.open(STATE_PATH, "r", encoding="utf-8") as f:
        state = json.load(f)
    state["hbCount"] = 935
    state["lastHB"] = 934
    state["lastCheck"] = "2026-07-22T17:05:00+08:00"
    state["silenceHours"] = 147.82
    state["ericActiveHours"] = 76.32
    state["t0_past_hours"] = 112.83
    state["nextDDayHours"] = 39.92
    state["notes"] = "HB#935: +14.5min from #934 (Wednesday afternoon). DORMANT sustained. 7/24 D-Day T-39.92h. 21:00 evening self-iter (~3h55m). No actionable signal."
    state["nextSignificantCheck"] = "21:00 evening self-iter (~3h55m)"
    with io.open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"OK: heartbeat-state.json updated (hbCount=935)")

if __name__ == "__main__":
    append_hb()
    update_state()
    print("OK: R-NEW-V2 HB #935 update complete")
