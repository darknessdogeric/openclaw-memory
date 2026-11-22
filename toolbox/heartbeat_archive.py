"""R268 HEARTBEAT.md Archive Maintenance
Triggered when file size hits 1.2MB+ threshold.
Run: python toolbox/heartbeat_archive.py
"""
import re
from pathlib import Path

WORKSPACE = Path('D:/B166ER-OpenClaw/workspace')
HB_FILE = WORKSPACE / 'HEARTBEAT.md'

CUTOFF_DATE = '2026-07-22'  # Keep last 5 days in main file

def main():
    content = HB_FILE.read_text(encoding='utf-8')
    print(f'Read {HB_FILE.name}: {len(content)} chars')

    # Split by '## HB #' delimiters (keep delimiter attached to next block)
    parts = re.split(r'(?=^## HB #\d+)', content, flags=re.MULTILINE)
    header_or_empty = parts[0]
    hb_blocks = parts[1:]

    date_pattern = re.compile(r'## HB #(\d+)\s+\((\d{4}-\d{2}-\d{2})')

    archive_blocks = []
    keep_blocks = []
    for blk in hb_blocks:
        m = date_pattern.search(blk)
        if m:
            date = m.group(2)
            if date < CUTOFF_DATE:
                archive_blocks.append(blk)
            else:
                keep_blocks.append(blk)
        else:
            keep_blocks.append(blk)

    # Archive file
    archive_filename = 'HEARTBEAT_archive_2026-07-19_to_2026-07-21.md'
    archive_header = """# HEARTBEAT Archive: 2026-07-19 to 2026-07-21

> Auto-archived by R268 maintenance on 2026-07-27 02:33 GMT+8
> Source: HEARTBEAT.md (file size triggered 1.2MB+ threshold)
> This file retains HB entries from 7/19 to 7/21 (320 entries)
> Main file HEARTBEAT.md retains entries from 7/22+ (158 entries)
> Cutoff policy: keep last 5 days in main file, archive older
> Context: Session DORMANT per Eric 7/19 12:33 explicit instruction

---
"""
    archive_content = archive_header + ''.join(archive_blocks)
    archive_path = WORKSPACE / archive_filename
    archive_path.write_text(archive_content, encoding='utf-8')

    print(f'Archive written: {archive_filename}')
    print(f'  Size: {len(archive_content)} chars ({len(archive_content)/1024:.1f}KB)')
    print(f'  Blocks: {len(archive_blocks)}')

    # Rewrite main file
    main_content = header_or_empty + ''.join(keep_blocks)
    HB_FILE.write_text(main_content, encoding='utf-8')

    print()
    print('Main file rewritten:')
    print(f'  Size: {len(main_content)} chars ({len(main_content)/1024:.1f}KB)')
    print(f'  Blocks: {len(keep_blocks)}')
    threshold_kb = 1.2 * 1024
    current_kb = len(main_content) / 1024
    status = 'UNDER threshold OK' if len(main_content) < 1.2*1024*1024 else 'OVER threshold FAIL'
    print(f'  Threshold check: 1.2MB = {threshold_kb:.1f}KB, current = {current_kb:.1f}KB')
    print(f'  Status: {status}')

    print()
    print('=== Final file state ===')
    for f in WORKSPACE.glob('HEARTBEAT*.md'):
        print(f'  {f.name}: {f.stat().st_size/1024:.1f}KB')

if __name__ == '__main__':
    main()
