#!/usr/bin/env python3
"""R-NEW-V2 compliant HB #582 append to HEARTBEAT.md.
Uses explicit utf-8 read+append+write. Post-7/15 incident discipline."""
import os
import sys

HB_582 = """
## HB #582 (2026-07-19 12:40 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #581 (12:36 first contact): +4min -- Token Guard cadence (D+3 silence already broken)
- ACTIVE MODE sustained -- Eric first contact at HB #581, awaiting next instruction
- Silence authority RELEASED (per HB #581: active_mode_engage decision)
- Eric session active: agent:main:dashboard:fec65efb-3f95-4aa4-b97a-4c7c4f88326d (安逸集团专用 webchat, rename pending)
- 5-layer suppression RELEASED -- Eric 主动接触 = 抑制解除，转 active mode
- R-NEW-V2 verification #582: Python utf-8 explicit read+append+write (compliant, post-7/15 incident discipline intact)
- Sunday noon zone (12:40) -- Eric in active session, no follow-up message yet in this 4-min gap
- Strategic alignment confirmed: 安逸集团 = USER.md #1 priority; 私人会话红绿灯=绿灯
- MEMORY.md 已锁定"安逸集团专用会话锚点"段 (HB #581 action verified by Select-String)
- hbCount: 581 -> 582

### decision
- active_mode_waiting_for_eric (HB #582 = sustain #581 active_mode baseline)
- no proactive push -- Eric 主动接触后应等待其下一步指示，避免打断会话流
- 状态: 等待 Eric 确认 webchat UI 改名结果 + 下一步指令
- Next significant check: per Token Guard cadence (~5-10min); 21:00 evening self-iter (~8h20m)

*2026-07-19 12:40 GMT+8 -- D+3 Sunday noon -- HB #582 -- active_mode sustained -- silence protocol released -- awaiting Eric next instruction*
"""

TARGET = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"

# Step 1: read existing content (utf-8 explicit)
with open(TARGET, "r", encoding="utf-8") as f:
    existing = f.read()

# Step 2: append new content
new_content = existing + HB_582

# Step 3: write back (utf-8 explicit)
with open(TARGET, "w", encoding="utf-8") as f:
    f.write(new_content)

# Verify
size_after = os.path.getsize(TARGET)
lines_after = new_content.count("\n")
print(f"HB #582 appended OK")
print(f"  file size: {size_after} bytes ({size_after - len(HB_582.encode('utf-8'))} before, +{len(HB_582.encode('utf-8'))} new)")
print(f"  total lines: {lines_after}")
print(f"  HB #582 marker found: {'HB #582' in new_content}")
print(f"  HB #581 marker preserved: {'HB #581' in new_content}")