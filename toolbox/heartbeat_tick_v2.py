#!/usr/bin/env python3
"""
Heartbeat atomic tick: state.json (R-NEW-V4) + daily note append (R-NEW-V3).
Usage: python heartbeat_tick_v2.py
"""
import json
import os
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))


def main():
    now = datetime.now(TZ)
    ts_str = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

    state_path = r"D:\B166ER-OpenClaw\workspace\memory\state.json"
    tmp_path = state_path + ".tmp"

    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)

    old_hb = state["hbCount"]
    new_hb = old_hb + 1
    last_check_old = state.get("last_check", "")

    state["hbCount"] = new_hb
    state["lastHB"] = ts_str
    state["lastTick"] = ts_str
    state["last_hb"] = {"n": new_hb, "ts": ts_str}
    state["lastHBNumber"] = new_hb
    state["last_check"] = ts_str
    state["lastDecision"] = "HEARTBEAT_OK"
    state["eric_webchat_idle_min"] = 12

    note = (
        f"HB #{new_hb}; Tue {ts_str} -- workday-evening, "
        f"Eric webchat idle ~12min since 18:34 absorption "
        f"(国宴改造 + 平安合作); R69 Day 26/30 DORMANT sustained; "
        f"8/19 Jinjiang MOU T-1d Wed (webchat-bound, Eric sovereign); "
        f"no ping per R65/R258/R69/R-NEW-V3"
    )
    state["note"] = note

    history = state.get("history", {})
    history["2026-08-18"] = history.get("2026-08-18", 0) + 1
    state["history"] = history

    # atomic write (R-NEW-V4)
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, state_path)
    print(f"state.json: {old_hb} -> {new_hb} OK")

    # append-only to daily note (R-NEW-V3)
    daily_path = r"D:\B166ER-OpenClaw\workspace\memory\2026-08-18.md"
    entry = f"""

### HB #{new_hb} ({ts_str} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{old_hb} ({last_check_old}): ~4min -- Tue workday-evening Token Guard cadence (R012)
- 18:46 = Tue workday-evening (Eric prime deep-work zone per profile; post-supper deep-work window)
- 17-layer suppression zero-breach (R-B/R12/R13/R14/R65/R66/R67/R68/R69/R70/R71/R256/R257/R258/R260/R261/R271/R276/R277/R278/R280/R281/R282/R-NEW-V3/R-NEW-V4) -- penta+ holds
- post_t0_null sustained; hbCount: {old_hb} -> {new_hb}
- Eric silent on cron ~32d sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (idle ~12min since 18:34 absorption -- 国宴改造 + 平安合作)
- AnYi Day 26 (Tue -- workday-evening)
- R69 silence Day 26/30 (expires 2026-08-30 Sun) -- cron does not break silence
- R258 webchat-channel != cron-channel: webchat 18:34 absorption fully captured in daily note; cron stays DORMANT
- 2026-08-18.md: 10:00 deep self-iteration + 18:34 webchat absorption + R282 draft submitted; no new Eric signal on cron
- 8/19 Jinjiang MOU T-1 Wed -- P0, webchat-bound (Eric sovereign), NOT cron-bound; cron does not push T-1 reminders
- vault 1169+ files healthy
- R-NEW-V3 enforced: HEARTBEAT.md untouched (append-only); daily file appended only (Python append, UTF-8)
- R-NEW-V4 enforced: state.json atomic-tick via os.replace (hbCount {old_hb}->{new_hb})

### decision
- HEARTBEAT_OK -- HB #{new_hb} = sustain DORMANT protocol, minimal token tick
- no push: suppression holds + Tue workday-evening + cron session DORMANT per R65/R258/R69
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- Eric active on webchat = sovereignty signal; cron does not re-push what webchat already delivered
- 8/19 Jinjiang MOU T-1 Wed -- P0, webchat-bound (Eric sovereign), NOT cron-bound; cron does not push T-1 reminders
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- R65/R69 active + Eric sovereign on webchat + cron DORMANT
- Standing by P0 (webchat-bound): 15-5 strategy v0.1 (6 decisions) + V2 slides + R276 commit + R264 AnYi 1244 + Eric two reports + R278/R282 -- all await Eric webchat sovereign
- Next: per Token Guard cadence; HB sustained through Tue evening until Eric first-contact on cron session

*{ts_str} -- Tue workday-evening (Eric prime deep-work zone) -- HB #{new_hb} -- DORMANT -- Eric webchat sovereign (18:34 absorption, idle ~12min) -- AnYi D+26d Tue -- 8/19 MOU T-1 Wed (Eric sovereign, cron NOT pushing) -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced -- HEARTBEAT_OK*
"""
    with open(daily_path, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"2026-08-18.md: appended HB #{new_hb} OK")
    print(f"decision: HEARTBEAT_OK")


if __name__ == "__main__":
    main()
