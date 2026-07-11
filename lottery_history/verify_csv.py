import csv
path = r'C:\Users\Administrator\.openclaw\workspace\lottery_history\dlt_history.csv'
with open(path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
print(f'Total: {len(rows)} issues')
with_date = sum(1 for r in rows if r['date'])
print(f'With date: {with_date}/{len(rows)}')
print(f'\nFirst 3:')
for r in rows[:3]:
    print(f'  {r["issue"]} | {r["date"]} | {r["front"]} | {r["back"]}')
print(f'\nLast 5:')
for r in rows[-5:]:
    print(f'  {r["issue"]} | {r["date"]} | {r["front"]} | {r["back"]}')
