#!/usr/bin/env python3
"""Audit the OpenClaw skill library health."""
import json
import os
import subprocess

OPENCLAW_CMD = r'C:\Users\ericz\.openclaw\tmp\agent-cli\openclaw.cmd'
SKILLS_JSON = os.path.join(os.path.dirname(__file__), '..', 'skills_raw.json')


def main():
    # Run the official command
    result = subprocess.run([OPENCLAW_CMD, 'skills', 'list', '--json'], capture_output=True)
    raw = result.stdout
    # Detect BOM
    if raw[:2] == b'\xff\xfe':
        # LE BOM
        raw = raw[2:]
        text = raw.decode('utf-16-le')
    elif raw[:2] == b'\xfe\xff':
        # BE BOM
        raw = raw[2:]
        text = raw.decode('utf-16-be')
    elif raw[:3] == b'\xef\xbb\xbf':
        # UTF-8 BOM
        raw = raw[3:]
        text = raw.decode('utf-8')
    else:
        # Try utf-8 first, fallback to utf-16-le
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError:
            text = raw.decode('utf-16-le', errors='ignore')

    # Save normalized UTF-8 copy for inspection
    with open(SKILLS_JSON, 'w', encoding='utf-8') as f:
        f.write(text)

    # Parse JSON
    data = json.loads(text)
    skills = data.get('skills', [])

    # Stats
    print(f'TOTAL SKILLS: {len(skills)}')
    print()

    by_source = {}
    eligible = 0
    disabled_list = []
    for s in skills:
        src = s.get('source', 'unknown')
        by_source[src] = by_source.get(src, 0) + 1
        if s.get('eligible'):
            eligible += 1
        else:
            m = s.get('missing', {})
            reasons = []
            if m.get('bins'):
                reasons.append('bins=' + ','.join(m['bins']))
            if m.get('anyBins'):
                reasons.append('anyBins=' + ','.join(m['anyBins']))
            if m.get('env'):
                reasons.append('env=' + ','.join(m['env']))
            if m.get('os'):
                reasons.append('os=' + ','.join(m['os']))
            disabled_list.append('  - ' + s['name'] + ': ' + (' / '.join(reasons) if reasons else 'unknown'))

    print('=== BY SOURCE ===')
    for src, cnt in sorted(by_source.items(), key=lambda x: -x[1]):
        print(f'  {src}: {cnt}')
    print()

    disabled = len(skills) - eligible
    print('=== ELIGIBILITY ===')
    pct = 100 * eligible // len(skills) if skills else 0
    print(f'  Eligible: {eligible} / {len(skills)} ({pct}%)')
    print(f'  Disabled: {disabled}')
    print()

    if disabled_list:
        print('=== DISABLED SKILLS (need fixes) ===')
        for d in disabled_list:
            print(d)


if __name__ == '__main__':
    main()