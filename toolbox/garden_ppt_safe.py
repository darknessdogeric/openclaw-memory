content = open(r'D:\B166ER-OpenClaw\workspace\toolbox\garden_ppt.txt', 'r', encoding='utf-8').read()
with open(r'D:\B166ER-OpenClaw\workspace\toolbox\garden_ppt_safe.txt', 'w', encoding='utf-8') as f:
    f.write(content)