"""
B166ER 双色球 (SSQ) 数据采集 V1.0
从 500.com 抓取历史开奖数据，存储为 CSV
规则: 红球 33选6, 蓝球 16选1
开奖: 每周二/四/日 ~21:15
"""
import urllib.request
import urllib.error
import re
import csv
import os
import json
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = 'https://datachart.500.com/ssq/history/newinc/history.php'
DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(DIR, 'ssq_history.csv')
META_PATH = os.path.join(DIR, 'ssq_meta.json')

RED_POOL = 33
BLUE_POOL = 16
RED_COUNT = 6
BLUE_COUNT = 1


def fetch_range(start: int, end: int, timeout: int = 15) -> str | None:
    url = f'{BASE_URL}?start={start}&end={end}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://datachart.500.com/ssq/',
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.read().decode('gbk', errors='replace')
    except Exception as e:
        print(f'[ERROR] {e}')
        return None


def parse_html(html: str) -> list[dict]:
    """
    SSQ DOM 结构:
    td[0]=行号 | td[1]=期号 | td[2-7]=红球(6个) | td[8]=蓝球(1个) |
    td[9]=&nbsp; | td[10-15]=统计 | td[16]=日期
    """
    results = []
    m = re.search(r'<tbody[^>]*id=.tdata.[^>]*>(.*?)</tbody>', html, re.DOTALL | re.IGNORECASE)
    if not m:
        return results

    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', m.group(1), re.DOTALL)
    for row in rows:
        tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        if len(tds) < 10:
            continue
        tds = [re.sub(r'<[^>]*>', '', t).strip() for t in tds]

        try:
            # 跳过注释行号列
            offset = 1 if (tds[0].isdigit() and len(tds[0]) <= 2) else 0

            issue = tds[offset]
            if not issue.isdigit() or len(issue) < 4:
                continue

            # 红球: offset+1 到 offset+6
            reds = []
            for i in range(offset + 1, offset + 7):
                val = tds[i].replace(',', '')
                if val.isdigit():
                    n = int(val)
                    if 1 <= n <= RED_POOL:
                        reds.append(n)
            if len(reds) != RED_COUNT:
                continue

            # 蓝球: offset+7
            val = tds[offset + 7].replace(',', '')
            if not val.isdigit():
                continue
            blue = int(val)
            if blue < 1 or blue > BLUE_POOL:
                continue

            # 日期: offset+15 (第16列数据)
            date_str = ''
            date_idx = offset + 15
            if len(tds) > date_idx and re.match(r'\d{4}-\d{2}-\d{2}', tds[date_idx]):
                date_str = tds[date_idx]

            results.append({
                'issue': issue,
                'reds': sorted(reds),
                'blue': blue,
                'date': date_str,
            })
        except (ValueError, IndexError):
            continue

    results.sort(key=lambda x: x['issue'])
    return results


def load_csv() -> dict[str, dict]:
    existing = {}
    if os.path.exists(CSV_PATH):
        try:
            with open(CSV_PATH, 'r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    existing[row['issue']] = row
        except Exception:
            pass
    return existing


def merge_and_write(existing: dict, new_data: list[dict]) -> int:
    all_data = {}
    for issue, row in existing.items():
        all_data[issue] = row

    new_count = 0
    for d in new_data:
        is_new = d['issue'] not in existing or not existing[d['issue']].get('date')
        if is_new:
            new_count += 1
        all_data[d['issue']] = {
            'issue': d['issue'],
            'date': d['date'],
            'red': ' '.join(str(n).zfill(2) for n in d['reds']),
            'blue': str(d['blue']).zfill(2),
            **{f'r{i+1}': str(d['reds'][i]).zfill(2) for i in range(6)},
            'b1': str(d['blue']).zfill(2),
        }

    sorted_issues = sorted(all_data.keys(), key=lambda x: int(x))
    fieldnames = ['issue', 'date', 'red', 'blue',
                  'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'b1']

    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for issue in sorted_issues:
            writer.writerow(all_data[issue])

    meta = {
        'last_updated': datetime.now().isoformat(),
        'total_issues': len(sorted_issues),
        'issue_range': f'{sorted_issues[0]}-{sorted_issues[-1]}' if sorted_issues else 'N/A',
        'latest_issue': sorted_issues[-1] if sorted_issues else 'N/A',
        'latest_date': all_data.get(sorted_issues[-1], {}).get('date', '') if sorted_issues else '',
    }
    with open(META_PATH, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    return new_count


def main():
    print('=' * 60)
    print('  B166ER 双色球数据采集 V1.0')
    print(f'  时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('=' * 60)

    existing = load_csv()
    print(f'\n📂 已有: {len(existing)} 期')

    if existing:
        fetch_start = max(int(k) for k in existing.keys()) + 1
    else:
        fetch_start = 26001

    # SSQ始于2003年，2026年期号 ≈ 26001起
    weeks = (datetime.now() - datetime(2026, 1, 1)).days // 7
    fetch_end = 26001 + weeks * 3 + 10

    print(f'🔍 范围: {fetch_start} ~ {fetch_end}')

    BATCH = 50
    all_new = []
    start = fetch_start

    while start <= fetch_end:
        end = min(start + BATCH - 1, fetch_end)
        print(f'  抓取 {start}-{end} ...', end=' ', flush=True)
        html = fetch_range(start, end, timeout=20)
        if html is None:
            print('❌')
            start = end + 1
            continue
        batch = parse_html(html)
        print(f'-> {len(batch)} 条')
        if not batch:
            break
        all_new.extend(batch)
        if len(batch) < BATCH * 0.3:
            break
        start = end + 1

    print(f'\n📥 抓取: {len(all_new)} 条')
    if all_new:
        nc = merge_and_write(existing, all_new)
        print(f'💾 入库: {nc} 期 (新增)')

    final = load_csv()
    print(f'\n📊 最终: {len(final)} 期')
    if final:
        issues = sorted(final.keys(), key=lambda x: int(x))
        print(f'   范围: {issues[0]} - {issues[-1]}')
        latest = final[issues[-1]]
        print(f'   最新: {issues[-1]} ({latest["date"]})')
        print(f'   红球: {latest["red"]}')
        print(f'   蓝球: {latest["blue"]}')
    print(f'\n✅ 完成! CSV: {CSV_PATH}')


if __name__ == '__main__':
    main()
