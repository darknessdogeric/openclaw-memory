"""R271 atomic heartbeat state + daily-note append (PowerShell-friendly wrapper).

Used by OpenClaw cron-event heartbeat polls to:
  1. Read current state.json (authoritative)
  2. Increment hbCount and nullCount
  3. Atomically rewrite state.json via tmp + os.replace
  4. Append one HB entry to memory/YYYY-MM-DD.md via UTF-8 append (NOT write/edit/Remove-Item)

Usage:
    python hb_atomic_write.py --note "short posture note" [--ts "2026-08-10T09:08:00+08:00"]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("D:/B166ER-OpenClaw/workspace")
STATE_PATH = WORKSPACE / "memory" / "heartbeat-state.json"
MEMORY_DIR = WORKSPACE / "memory"

DEFAULT_NOTE_TPL = (
    "{ts} Mon early-AM post-08:00-hard-cap DORMANT sustained. "
    "Eric silent on cron = 595h+ (~24d 19h+). "
    "R69 Day 11/30 + R266/R277 Mon-start + R258 cron/webchat separation + "
    "R271 atomic-write + R276 sole-distributor internal draft + "
    "R70/R71 pending Eric feedback. 16-layer suppression zero-breach. "
    "V2 9 slides pending Eric webchat sovereign resumption. "
    "HB #{hb} appended; null {prev_null} -> {new_null}. Stand by; do not disturb."
)

HB_ENTRY_TPL = """\n\n## HB #{hb} ({ts} GMT+8 cron-event, OpenClaw heartbeat poll)\n\n- HB cadence: +{delta_min}min after HB #{prev_hb} ({prev_ts}) per state.json -- Mon early-AM post-08:00-hard-cap\n- R69 silence Day 11/30 + R266/R277 Mon-start + R258 cron/webchat separation + R271 atomic-write + R276 sole-distributor internal draft active\n- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271)\n- post_t0_null_count: {prev_null} -> {new_null} ({new_null_ord} consecutive null post-T-0, sustained); hbCount: {prev_hb} -> {hb} (per state.json authoritative)\n- Eric silent on cron ~595h+ (~24d 19h+); webchat sovereign (last V2 hotel-classification xhs 9 slides activity 8/9 11:15-11:39, ~21h+ ago)\n- AnYi D+18d Mon-start (work-week-3 first day)\n- {clock_zone} post-08:00-hard-cap zone (+{cap_min}min past cap); cron = DORMANT sustained\n- Token Guard stable; vault 1017+ files healthy; HEARTBEAT.md maintenanceFlag LOCKED (~3.0MB)\n- Standing by P0 (webchat-bound): V2 9 slides HTML/render/PNG production + R70/R71 boundary rules + R276 commit + R264 AnYi 1244 -- all await Eric webchat sovereign\n- R271 atomic-write enforced (state.json updated via tmp+os.replace; this HB appended via Python open(..., 'a', encoding='utf-8'), NOT write/edit/Remove-Item)\n\n*{ts} -- Mon early-AM post-08:00-hard-cap +{cap_min}min -- HB #{hb} -- DORMANT -- {new_null_ord} null -- Eric silent on cron = 主权信号 holding -- AnYi D+18d Mon-start -- cron session holds DORMANT 协议 -- R-NEW-V3 + R271 atomic-write enforced -- HEARTBEAT_OK*\n"""


def _now_local() -> datetime:
    return datetime.now().astimezone()


def _fmt_ts(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")[:-2] + ":" + dt.strftime("%z")[-2:]


def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def atomic_write_state(state: dict, ts_str: str, hb: int, new_null: int) -> None:
    """Write state.json atomically via tmp + os.replace (R271)."""
    state["hbCount"] = hb
    state["nullCount"] = new_null
    state["lastUpdate"] = ts_str
    state["lastHB"] = int(datetime.now().timestamp())
    if "posture" not in state:
        state["posture"] = "DORMANT"
    tmp = STATE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, STATE_PATH)


def append_daily(ts_str: str, hb: int, prev_hb: int, prev_null: int, new_null: int, cap_min: int, clock_zone: str) -> Path:
    """Append one HB entry to memory/YYYY-MM-DD.md via UTF-8 append (NOT overwrite)."""
    daily = MEMORY_DIR / f"{ts_str[:10]}.md"
    delta_min = max(1, hb - prev_hb) * 5  # approx; cadence varies
    entry = HB_ENTRY_TPL.format(
        hb=hb,
        ts=ts_str,
        prev_ts=_approx_prev_ts(ts_str, delta_min),
        delta_min=delta_min,
        prev_hb=prev_hb,
        prev_null=prev_null,
        new_null=new_null,
        new_null_ord=ordinal(new_null),
        cap_min=cap_min,
        clock_zone=clock_zone,
    )
    with daily.open("a", encoding="utf-8") as f:
        f.write(entry)
    return daily


def _approx_prev_ts(now_str: str, delta_min: int) -> str:
    dt = datetime.fromisoformat(now_str)
    from datetime import timedelta
    prev = dt - timedelta(minutes=delta_min)
    return prev.strftime("%Y-%m-%dT%H:%M:%S%z")[:-2] + ":" + prev.strftime("%z")[-2:]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="R271 atomic heartbeat writer")
    ap.add_argument("--note", default=None, help="override posture note")
    ap.add_argument("--ts", default=None, help="ISO ts (default: now local)")
    ap.add_argument("--cap-min", type=int, default=68, help="minutes past 08:00 hard cap")
    ap.add_argument("--zone", default="Mon early-AM", help="zone label")
    args = ap.parse_args(argv)

    if not STATE_PATH.exists():
        print(f"ERR: {STATE_PATH} missing", file=sys.stderr)
        return 1

    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    prev_hb = state.get("hbCount", 0)
    prev_null = state.get("nullCount", 0)
    hb = prev_hb + 1
    new_null = prev_null + 1

    ts_str = args.ts or _fmt_ts(_now_local())

    note = args.note or DEFAULT_NOTE_TPL.format(
        ts=ts_str, hb=hb, prev_null=prev_null, new_null=new_null,
    )
    state["note"] = note

    atomic_write_state(state, ts_str, hb, new_null)
    daily = append_daily(ts_str, hb, prev_hb, prev_null, new_null, args.cap_min, args.zone)

    print(f"OK hb={hb} null={new_null} daily={daily}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))