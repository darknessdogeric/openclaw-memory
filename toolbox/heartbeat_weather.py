import urllib.request, json

try:
    with urllib.request.urlopen('https://wttr.in/Xiangyang?format=j1', timeout=8) as r:
        d = json.loads(r.read())
    w = d['current_condition'][0]
    print(f"襄阳天气: {w['weatherDesc'][0]['value']}, {w['temp_C']}°C, 湿度{w['humidity']}%, 风速{w['windspeedKmph']}km/h")
except Exception as e:
    print(f"天气查询失败: {e}")
