#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix HB #2192 entry by replacing corrupted bytes with correct UTF-8."""
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

f = 'D:\\B166ER-OpenClaw\\workspace\\HEARTBEAT.md'

# Read raw bytes (file has mixed encoding, can't decode as UTF-8)
with open(f, 'rb') as fp:
    raw = fp.read()

print(f'File size: {len(raw)} bytes')

# Find my HB #2192 entry — use a unique marker that I'm confident is intact
# The marker: "## HB #2192 (2026-08-02T05:40" — this is ASCII, should be intact
marker = b'## HB #2192 (2026-08-02T05:40'
positions = []
start = 0
while True:
    pos = raw.find(marker, start)
    if pos < 0:
        break
    positions.append(pos)
    start = pos + 1

print(f'Found HB #2192 (8/2 05:40) marker at positions: {positions}')

# We want the LAST occurrence (my new entry at the end)
if not positions:
    print('ERROR: HB #2192 marker not found')
    sys.exit(1)

my_entry_start = positions[-1]
print(f'My entry starts at byte position: {my_entry_start}')

# Find the end of my entry — could be:
# (a) End of file (if my entry is the last)
# (b) Before the next "## HB #2" marker (if subsequent polls added entries)

# Look for "\n## HB #2" after my entry start + 10
next_marker_pattern = b'\n## HB #2'
next_pos = raw.find(next_marker_pattern, my_entry_start + 50)  # +50 to skip past my marker
if next_pos < 0:
    my_entry_end = len(raw)
    print(f'No next HB marker found, my entry extends to EOF: {my_entry_end}')
else:
    # The \n is part of the separator before the next entry; my entry ends just before it
    my_entry_end = next_pos
    print(f'Next HB marker found at: {next_pos}, my entry ends at: {my_entry_end}')

# Print the corrupted entry
corrupted = raw[my_entry_start:my_entry_end]
print('---CORRUPTED ENTRY (first 200 bytes hex)---')
print(corrupted[:200].hex(' '))
print('---CORRUPTED ENTRY (first 500 chars as ASCII / mojibake display)---')
# Display as if UTF-8 with errors=replace
print(corrupted[:500].decode('utf-8', errors='replace'))

# Now build the correct UTF-8 entry
correct_entry = '''\n## HB #2192 (2026-08-02T05:40 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #2191 (8/2 05:20): +20min -- Sun late-night Token Guard nominal cadence (R012, within tolerance)
- D+19 Sun 2026-08-02T05:40 -- **late-night-deep-quiet zone (23:00-08:00 hard)** -- absolute quiet; ~2h20m before 08:00 hard cap exit
- Eric silent on cron session 16d 16h+ (400h+) since 7/16 13:16 first-contact
- Eric silent on webchat as well (full dormant convergence per state.json)
- 12-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R-NEW-V3) -- hepta+1 holds
- post_t0_null_count: 795 -> 796 (796th consecutive null post-T-0, sustained)
- **R-NEW-V3 verified (revised)**: this HB entry uses Python UTF-8 native write (NOT write tool / NOT PowerShell 5.1 codepage munging); file has pre-existing mixed UTF-8/GB2312 from prior entries — flagged in P1
- AnYi 报到 D+10d Sunday sustained per HB-log; gongshi STATE surfaced HB #2083, NOT auto-mutated per R66
- V2.4 SOUL 加固 sustained (~184h+ uptime)
- R66/R67/R68/R69 entries sustained; R69 (战略新人沉默观察) 30-day window active (expires 2026-08-30)
- R70 (视觉范式优先于创造冲动) 已正式写入 ~/self-improving/rules.md per HB #2190 (Eric 8/1 15:25 反馈)
- Eric webchat last 8/1 22:50 area -- silent on cron AND webchat = 主权信号 holding (full dormant convergence, R258)
- Token Guard stable; vault 1017 files healthy; **B166ER-file-hbCount 2191 -> 2192** (gateway-level hbCount 2235+1=2236 sustained independently per state.json)
- 08:00 hard cap exit ~2h20m away; next milestone 06:49 (Token Guard)
- **R66 cross-verify note**: state.json hbCount 2235 != file HB #2192. state.json = OpenClaw gateway polling counter (faster cadence); HEARTBEAT.md file = B166ER response entries (per-poll LLM turn). Two independent counters, NOT state corruption. Filed for Eric awareness if drift grows.

### decision
- **HEARTBEAT_OK -- HB #2192 = sustain DORMANT protocol, minimal token tick** (796th null)
- **no push**: 12-layer suppression holds + **late-night-deep-quiet zone (23:00-08:00 hard)** + cron AND webchat both silent (full dormant convergence) + R65 explicit prohibition + R258 + R69 active + R-NEW-V3 verification mode
- R256+R257/R258/R260/R261/R65 penta+1 + R68+R69 hold -- no proactive disturbance
- Eric webchat / Obsidian 知识库 sovereign for any 决策; cron sovereignty unchanged
- 05:40 = **late-night-deep-quiet zone +2h20m before 08:00 hard cap exit**; cron = DORMANT sustained
- Eric 深夜/凌晨睡眠中 (per AnYi D+10d Sunday, Saturday 22:50 last webchat contact); 0 webchat activity since HB #2190
- Eric Saturday 22:50 mega-burst 已 全部 静默吸收完成 -- cron 通道 **不重复推送** (R65 + R258 + webchat主权 hold)
- **DO NOT DISTURB UNDER ANY CIRCUMSTANCE** -- late-night quiet zone + AnYi D+10d Sun + Eric sovereign on cron session + R65/R69 active
- Standing by P0 (webchat-bound, not cron-bound): R264 AnYi 完整实战链 (战略工作计划 -> 商业计划书 -> Q 预审稿 国央企风格 -> 内部计划书重写) 已跑通 -- 等待 Eric 在 webchat 确认下一阶段
- Standing by P1 (R264 AnYi 衔接): 等待 Eric 在 webchat/Obsidian 分享 AnYi 1244 战略 / 团队动向 / 权责对接 等具体内部内容, 按 R264 立即归档到 anyi-ops-kb/
- Standing by R-NEW-V3 verification: confirm HB entry uses Python UTF-8 native write (NOT write tool / NOT PowerShell 5.1 codepage munging) -- continuous verification mode + R-NEW-V3b sub-rule (use Python or Add-Content with [char] codepoints, NEVER raw Chinese in PowerShell 5.1 .ps1)
- R70 (视觉范式优先于创造冲动) 已正式写入 ~/self-improving/rules.md (per HB #2190, Eric 8/1 15:25 反馈)
- Next: per Token Guard cadence (~15-30min late-night mode); HB sustained through Sun night until 08:00 quiet zone exit / Mon 8/3 Day 6 first full workweek start

*2026-08-02 05:40 GMT+8 -- D+19 Sun late-night-deep-quiet zone (23:00-08:00 hard) +2h20m before hard cap exit -- HB #2192 -- DORMANT -- 796th null -- Eric silent 16d 16h+ on cron AND webchat (full dormant convergence) -- B166ER-file-hbCount 2192 (gateway hbCount 2236 independent) -- cron session 维持 DORMANT 协议 -- R-NEW-V3 verified (Python UTF-8 native write, NOT write tool, NOT PowerShell 5.1 codepage munging) -- HEARTBEAT_OK*
'''
correct_bytes = correct_entry.encode('utf-8')

# Replace corrupted section with correct UTF-8
new_raw = raw[:my_entry_start] + correct_bytes + raw[my_entry_end:]

# Verify the fix
test_marker = 'AnYi 报到 D+10d'.encode('utf-8')
if test_marker in new_raw:
    print('---FIX VERIFIED---')
    print(f'"AnYi 报到 D+10d" UTF-8 bytes found at position: {new_raw.find(test_marker)}')

# Write back atomically
import os
tmp = f + '.tmp'
with open(tmp, 'wb') as fp:
    fp.write(new_raw)
os.replace(tmp, f)

print(f'File rewritten. New size: {len(new_raw)} bytes (was {len(raw)}, delta {len(new_raw) - len(raw):+d})')
print('OK HB #2192 corrected UTF-8 entry written via Python.')