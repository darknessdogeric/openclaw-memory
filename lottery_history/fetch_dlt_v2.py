"""
B166ER 大乐透数据采集 V2.1
从 500.com 抓取历史开奖数据，解析并存储为 CSV
修复: V2.0 正则失效 → V2.1 基于实际 DOM 结构解析
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

BASE_URL = 'https://datachart.500.com/dlt/history/newinc/history.php'
CSV_PATH = os.path.join(os.path.dirname(__file__), 'dlt_history.csv')
META_PATH = os.path.join(os.path.dirname(__file__), 'dlt_meta.json')

FRONT_POOL = 35
BACK_POOL = 12
FRONT_COUNT = 5
BACK_COUNT = 2


def fetch_range(start: int, end: int, timeout: int = 15) -> str | None:
    url = f'{BASE_URL}?start={start}&end={end}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://datachart.500.com/dlt/',
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.read().decode('gbk', errors='replace')
    except Exception as e:
        print(f'[ERROR] {e}')
        return None


def parse_html_v2(html: str) -> list[dict]:
    """
    V2.1 解析逻辑 - 基于实际 DOM 结构:
    <tbody id="tdata">
      <tr class="t_tr1">
        <td class="t_tr1">26076</td>     ← 期号
        <td class="cfont2">15</td>       ← 前区1
        <td class="cfont2">20</td>       ← 前区2
        <td class="cfont2">27</td>       ← 前区3
        <td class="cfont2">28</td>       ← 前区4
        <td class="cfont2">35</td>       ← 前区5
        <td class="cfont4">02</td>       ← 后区1
        <td class="cfont4">11</td>       ← 后区2
        <td class="t_tr1">804,904,837</td> ← 奖池
        ...
        <td class="t_tr1">2026-07-08</td> ← 开奖日期
      </tr>
    </tbody>
    """
    results = []

    # 1. 提取 <tbody id="tdata"> 内的所有内容
    tbody_match = re.search(r'<tbody\s+id="tdata">(.*?)</tbody>', html, re.DOTALL)
    if not tbody_match:
        print('  ⚠️ 未找到 tbody#tdata')
        return results

    tbody_html = tbody_match.group(1)

    # 2. 按 <tr 分割每一行
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', tbody_html, re.DOTALL)

    for row in rows:
        # 提取所有 <td> 内的纯文本
        # 注意: 有一行注释 <!--<td>2</td>--> 会被匹配为第0列，需跳过
        tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        if len(tds) < 10:
            continue

        # 清理HTML标签残留（如 <!-- 注释 -->）
        tds = [re.sub(r'<[^>]*>', '', t).strip() for t in tds]

        try:
            # 跳过注释引入的假列: td[0] 如果是单数字则是行号，真正期号在 td[1]
            # 结构: td[0]=行号 | td[1]=期号 | td[2-6]=前区 | td[7-8]=后区 | td[9-14]=统计 | td[15]=日期
            if tds[0].isdigit() and len(tds[0]) <= 2:
                # 有行号列，偏移 +1
                offset = 1
            else:
                offset = 0

            issue = tds[offset]
            if not issue.isdigit() or len(issue) < 4:
                continue

            # 前区: offset+1 到 offset+5
            front = []
            for i in range(offset + 1, offset + 6):
                val = tds[i].replace(',', '')
                if val.isdigit():
                    n = int(val)
                    if 1 <= n <= FRONT_POOL:
                        front.append(n)

            if len(front) != FRONT_COUNT:
                continue

            # 后区: offset+6, offset+7
            back = []
            for i in range(offset + 6, offset + 8):
                val = tds[i].replace(',', '')
                if val.isdigit():
                    n = int(val)
                    if 1 <= n <= BACK_POOL:
                        back.append(n)

            if len(back) != BACK_COUNT:
                continue

            # 日期: td[offset+14] (0-indexed, 即第15列数据)
            date_str = ''
            date_idx = offset + 14
            if len(tds) > date_idx and re.match(r'\d{4}-\d{2}-\d{2}', tds[date_idx]):
                date_str = tds[date_idx]

            results.append({
                'issue': issue,
                'front': sorted(front),
                'back': sorted(back),
                'date': date_str,
            })

        except (ValueError, IndexError):
            continue

    results.sort(key=lambda x: x['issue'])
    return results


def load_existing_csv() -> dict[str, dict]:
    existing = {}
    if os.path.exists(CSV_PATH):
        try:
            with open(CSV_PATH, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing[row['issue']] = row
        except Exception:
            pass
    return existing


def merge_and_write(existing: dict[str, dict], new_data: list[dict]) -> int:
    all_data = {}
    for issue, row in existing.items():
        all_data[issue] = row

    new_count = 0
    for d in new_data:
        front_str = ' '.join(str(n).zfill(2) for n in d['front'])
        back_str = ' '.join(str(n).zfill(2) for n in d['back'])
        row = {
            'issue': d['issue'],
            'date': d['date'],
            'front': front_str,
            'back': back_str,
            'front_1': str(d['front'][0]),
            'front_2': str(d['front'][1]),
            'front_3': str(d['front'][2]),
            'front_4': str(d['front'][3]),
            'front_5': str(d['front'][4]),
            'back_1': str(d['back'][0]),
            'back_2': str(d['back'][1]),
        }
        is_new = d['issue'] not in existing or not existing[d['issue']].get('date')
        if is_new:
            new_count += 1
        all_data[d['issue']] = row

    sorted_issues = sorted(all_data.keys())
    fieldnames = ['issue', 'date', 'front', 'back',
                  'front_1', 'front_2', 'front_3', 'front_4', 'front_5',
                  'back_1', 'back_2']

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
    print('  B166ER 大乐透数据采集 V2.1')
    print(f'  时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('=' * 60)

    existing = load_existing_csv()
    print(f'\n📂 已有: {len(existing)} 期')

    # 决定抓取范围
    if existing:
        max_existing = max(int(k) for k in existing.keys())
        fetch_start = max_existing + 1
    else:
        fetch_start = 26001  # 从最早开始

    weeks_since_start = (datetime.now() - datetime(2026, 1, 3)).days // 7
    estimated_current = 26001 + weeks_since_start * 3
    fetch_end = estimated_current + 10

    print(f'🔍 范围: {fetch_start} ~ {fetch_end}')

    BATCH_SIZE = 50
    all_new = []
    start = fetch_start

    while start <= fetch_end:
        end = min(start + BATCH_SIZE - 1, fetch_end)
        print(f'  抓取 {start}-{end} ...', end=' ', flush=True)
        html = fetch_range(start, end, timeout=20)

        if html is None:
            print('❌ 网络错误')
            start = end + 1
            continue

        batch = parse_html_v2(html)
        print(f'→ {len(batch)} 条')

        if not batch:
            break

        all_new.extend(batch)

        # 如果返回远少于请求，已经到最新
        if len(batch) < BATCH_SIZE * 0.3:
            break

        start = end + 1

    print(f'\n📥 抓取: {len(all_new)} 条')

    if all_new:
        new_count = merge_and_write(existing, all_new)
        print(f'💾 入库: {new_count} 期 (新增)')

    final = load_existing_csv()
    print(f'\n📊 最终:')
    print(f'   总期数: {len(final)}')
    if final:
        issues = sorted(final.keys())
        print(f'   范围: {issues[0]} - {issues[-1]}')
        latest = final[issues[-1]]
        print(f'   最新: {issues[-1]} 期 ({latest["date"]})')
        print(f'   前区: {latest["front"]}')
        print(f'   后区: {latest["back"]}')
    print(f'\n✅ 完成!')
    print(f'   CSV: {CSV_PATH}')


if __name__ == '__main__':
    main()
