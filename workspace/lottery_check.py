import urllib.request, json
url = 'https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&historyPageSize=5&pageNo=1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
        for item in data['value']['list'][:5]:
            print(f"Issue:{item['issueCode']} Front:{item['frontWinNumber']} Back:{item['backWinNumber']}")
except Exception as e:
    print(f'Error: {e}')
