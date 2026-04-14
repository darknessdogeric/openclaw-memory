# -*- coding: utf-8 -*-
# 26038期 and 26039期 复盘

# 26038期 (2026-04-11 周六)
actual_38 = {'front': [8, 17, 21, 33, 35], 'back': [6, 7]}
preds_38 = [
    {'front': [7, 15, 20, 25, 32], 'back': [4, 6]},
    {'front': [7, 18, 24, 27, 32], 'back': [4, 11]},
    {'front': [7, 15, 20, 26, 34], 'back': [9, 3]},
    {'front': [3, 7, 24, 27, 34], 'back': [9, 3]},
    {'front': [9, 20, 24, 27, 33], 'back': [9, 8]},
]

print('=== 26038期复盘 (2026-04-11 周六) ===')
print(f'实际: 前区{actual_38["front"]} 后区{actual_38["back"]}')
for i, p in enumerate(preds_38):
    fh = len(set(p['front']) & set(actual_38['front']))
    bh = len(set(p['back']) & set(actual_38['back']))
    score = fh * 10 + bh * 5
    front_hit = list(set(p["front"]) & set(actual_38["front"]))
    back_hit = list(set(p["back"]) & set(actual_38["back"]))
    print(f'方案{i+1}: 前区{fh}个{front_hit} 后区{bh}个{back_hit} → {score}分')

best_38 = max(preds_38, key=lambda p: len(set(p['front'])&set(actual_38['front']))*10 + len(set(p['back'])&set(actual_38['back']))*5)
print(f'最佳方案: 前区{best_38["front"]} + 后区{best_38["back"]}')

# 26039期 (2026-04-13 周一)
actual_39 = {'front': [9, 11, 20, 26, 27], 'back': [6, 9]}
preds_39 = [
    {'front': [6, 14, 22, 33, 35], 'back': [7, 12]},
    {'front': [5, 13, 21, 31, 34], 'back': [6, 8]},
    {'front': [4, 12, 20, 30, 35], 'back': [3, 7]},
    {'front': [8, 15, 23, 32, 34], 'back': [6, 12]},
    {'front': [3, 18, 25, 33, 35], 'back': [8, 10]},
]

print()
print('=== 26039期复盘 (2026-04-13 周一) ===')
print(f'实际: 前区{actual_39["front"]} 后区{actual_39["back"]}')
for i, p in enumerate(preds_39):
    fh = len(set(p['front']) & set(actual_39['front']))
    bh = len(set(p['back']) & set(actual_39['back']))
    score = fh * 10 + bh * 5
    front_hit = list(set(p["front"]) & set(actual_39["front"]))
    back_hit = list(set(p["back"]) & set(actual_39["back"]))
    print(f'方案{i+1}: 前区{fh}个{front_hit} 后区{bh}个{back_hit} → {score}分')

best_39 = max(preds_39, key=lambda p: len(set(p['front'])&set(actual_39['front']))*10 + len(set(p['back'])&set(actual_39['back']))*5)
print(f'最佳方案: 前区{best_39["front"]} + 后区{best_39["back"]}')
