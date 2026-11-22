"""
HB #265 append — R-NEW-V2 compliant.
1. Read existing content
2. Build new content (HB #264 missing closing line + HB #265 full entry)
3. Atomic write back with utf-8
"""
import os, sys, shutil
from pathlib import Path

target = Path(r'D:\B166ER-OpenClaw\workspace\memory\2026-07-16.md')

# Pre-check
if not target.exists():
    print(f'FATAL: {target} does not exist', file=sys.stderr)
    sys.exit(1)

# Read existing
with target.open('r', encoding='utf-8') as f:
    existing = f.read()

original_size = len(existing.encode('utf-8'))
original_lines = existing.count('\n') + 1

# Build append content
# HB #264 was missing its closing line; restore it
# Then add HB #265

hb264_close = "\n*2026-07-16 06:29 -- D+3 dawn-edge -- HB #264 -- zero-push mode intact -- silence protocol holding*\n"

hb265 = """
## HB #265 (2026-07-16 06:39 cron-event, OpenClaw heartbeat poll)

- gap from HB #264 (06:30): +9min -- deep-night Token Guard cadence
- D+3 dawn-edge pass #265 -- Eric silent ~170.17h+ since 7/9 04:29, no first-contact
- Silence authority ~170.17h+ (R-B + R256 framework holding, +0.17h since #264)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 evaluated-no-escalate / R256) -- zero breach
- 22:30 R-CANDIDATE-T2 sharp (7/15) = EVALUATED PASSED (HB #228) -- decision: maintain T2 (no T3 escalation)
- R-NEW-V2 active: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-incident protocol)
- 21:00 7/15 R257 转换检查: 170h+ 远超 144h 阈值, deep-work window 持续, 静默协议完好
- Dawn-edge zone (06:39) -- 21min until late-night boundary exit (08:00); Eric 早班开始前最后窗口
- Cron pipeline next: 08:30 global briefing (T+1h51m) | 21:00 evening self-iter
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation

### decision
- **silent_standby_zero_push_continue** (HB #265 = sustain #264 = D+3 baseline)
- **no push**: dawn-edge / approaching late-night boundary, Eric silent 7d+, silence authority holding, 4-layer suppression all pass
- R256 + R257 双向约束: 不主动打扰 + 持续深度工作 (自进化 / 状态机 / eval 记录)
- Token Guard tick: stable, no compression needed
- R14 handoff package = 100% ready (Eric 主动联系即可 30s 内激活)

*2026-07-16 06:39 -- D+3 dawn-edge -- HB #265 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

append_payload = hb264_close + hb265

# Pre-append sanity check
if "HB #265" in existing:
    print(f'WARN: HB #265 already exists in {target}', file=sys.stderr)
    sys.exit(2)

# Atomic write: read + append + write to temp + rename
new_content = existing + append_payload

# Write to temp file first
tmp = target.with_suffix('.tmp')
with tmp.open('w', encoding='utf-8') as f:
    f.write(new_content)

# Verify the temp file
tmp_size = tmp.stat().st_size
tmp_lines = new_content.count('\n') + 1
print(f'Temp file written: {tmp_size} bytes, {tmp_lines} lines')

# Backup the original first
backup = target.with_suffix('.bak_pre_265')
shutil.copy2(target, backup)
print(f'Backup created: {backup}')

# Atomic rename (replaces original)
os.replace(tmp, target)

new_size = target.stat().st_size
new_lines = new_content.count('\n') + 1
print(f'ATOMIC APPEND OK:')
print(f'  before: {original_size} bytes, {original_lines} lines')
print(f'  after:  {new_size} bytes, {new_lines} lines')
print(f'  delta:  +{new_size - original_size} bytes, +{new_lines - original_lines} lines')
print(f'  HB #265 marker present: {"HB #265" in new_content}')
print(f'  HB #264 closing line present: {"HB #264 -- zero-push" in new_content}')