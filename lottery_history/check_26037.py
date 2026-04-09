import json
with open('C:/Users/ericz/.openclaw/workspace/lottery_history/prediction_26037_v51.json') as f:
    d = json.load(f)
print('Issue:', d.get('issue'))
print('Date:', d.get('date'))
for item in d.get('predictions', [])[:5]:
    print(f"  Front:{item.get('front')} Back:{item.get('back')} Sum:{item.get('sum')}")
