import json, sys
sys.stdout.reconfigure(encoding='utf-8')
result_front = {7, 12, 13, 28, 32}
result_back = {6, 8}
with open('C:/Users/ericz/.openclaw/workspace/lottery_history/prediction_26037_v51.json', encoding='utf-8') as f:
    pred = json.load(f)
print('26037期 V5.1 预测复盘')
print('Result: Front=07,12,13,28,32 | Back=06,08 | Sum=92')
print()
for p in pred['predictions']:
    front_set = set(p['front'])
    back_set = set(p['back'])
    front_hit = len(front_set & result_front)
    back_hit = len(back_set & result_back)
    print(f"Bet {p['no']}: Front={p['front']} Back={p['back']}")
    print(f"  Front hit: {front_hit}/5 -> {front_set & result_front}")
    print(f"  Back hit:  {back_hit}/2 -> {back_set & result_back}")
    score = front_hit * 10 + back_hit * 5
    print(f"  Score: {score}")
    print()
