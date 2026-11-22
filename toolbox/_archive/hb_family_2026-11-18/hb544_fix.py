#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""HB #544 fixup -- restore correct hb_id after bad #513 over-write"""
import json, os, re, time
from pathlib import Path
from datetime import datetime, timezone, timedelta

WS = Path(r"D:\B166ER-OpenClaw\workspace")
MEM = WS / "memory"
TODAY = MEM / "2026-07-18.md"
HBSTATE = MEM / "heartbeat-state.json"

NOW = datetime.now(timezone(timedelta(hours=8)))
NOW_TS = NOW.strftime("%Y-%m-%d %H:%M GMT+8")

# ---- read heartbeat-state.json (utf-8 explicit) ----
with open(HBSTATE, "r", encoding="utf-8") as f:
    hb = json.load(f)

# Identify the bad HB #513 entry (last in log) and fix it
last_log = hb["hb_log"][-1]
assert last_log["hb_id"] == 513, f"Expected last hb_id 513, got {last_log['hb_id']}"

# Correct HB # is 544 (continuing from previous lastHB=543)
correct_hb_id = 544
last_log["hb_id"] = correct_hb_id
last_log["ts"] = NOW_TS

# Fix top-level counters
hb["lastHB"] = correct_hb_id
hb["chainHb"] = hb["chainHb"] + 1  # was 513, now 514
# chain_hb increments per log entry; the bad entry had wrong chain_hb. Set correctly.
hb["chain_hb"] = 473  # this is the next correct chain_hb for #544
hb["hb_log"][-1] = last_log

# Update last_check fields
hb["last_heartbeat"] = NOW_TS
hb["lastChecks"]["heartbeat"] = int(NOW.timestamp())
hb["lastCheck"] = NOW.isoformat()
hb["last_update_epoch"] = int(NOW.timestamp())
hb["notes"] = f"#{correct_hb_id} (silent standby). {NOW_TS} - saturday-afternoon, Eric silent 49.79h+, T-0 publicity day ACTIVE (+15.06h past), R14 handoff 100% ready, no proactive disturbance per R256/R257"

# Fix chain_hb inside last log entry to match top-level
hb["hb_log"][-1]["chain_hb"] = hb["chain_hb"]

# ---- atomic write ----
tmp = HBSTATE.with_suffix(".tmp")
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(hb, f, ensure_ascii=False, indent=2)
    f.flush()
    os.fsync(f.fileno())
os.replace(tmp, HBSTATE)

# ---- Fix memory file: replace #513 entry text with #544 entry ----
with open(TODAY, "r", encoding="utf-8") as f:
    today_content = f.read()

# Replace any "HB #513" references with "HB #544"
fixed_content = today_content.replace("HB #513", "HB #544")
fixed_content = fixed_content.replace("# 513", "# 544")
fixed_content = fixed_content.replace("= 513", "= 544")
fixed_content = fixed_content.replace("-> 513", "-> 544")
# Fix ts line
fixed_content = fixed_content.replace("2026-07-18 15:02 GMT+8 cron-event, OpenClaw heartbeat poll)",
                                       "2026-07-18 15:02 GMT+8 cron-event, OpenClaw heartbeat poll [FIXED #513->#544]")
# Fix chain_hb references from "472 -> 473" to "472 -> 473" already, but ensure it's not "513"
fixed_content = re.sub(r'512 -> 513(?!\d)', '512 -> 514', fixed_content)
fixed_content = re.sub(r'473(?=\D|$)', '473', fixed_content)  # ensure chain_hb stays 473

# Verify the changes happened
assert "HB #544" in fixed_content, "HB #544 not found after replacement"
n_replacements = today_content.count("513") - fixed_content.count("513")
print(f"Replaced {n_replacements} '513' references with '544'")

# atomic write
tmp_md = TODAY.with_suffix(".md.tmp")
with open(tmp_md, "w", encoding="utf-8") as f:
    f.write(fixed_content)
    f.flush()
    os.fsync(f.fileno())
os.replace(tmp_md, TODAY)

print(f"FIX OK -- HB #{correct_hb_id} restored (chainHb 514, chain_hb 473)")
print(f"hb_log last entry: hb_id={hb['hb_log'][-1]['hb_id']}, ts={hb['hb_log'][-1]['ts']}")
print(f"top-level: lastHB={hb['lastHB']}, chainHb={hb['chainHb']}, chain_hb={hb['chain_hb']}")
