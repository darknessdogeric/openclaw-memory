import re
content = open(r'D:\B166ER-OpenClaw\workspace\toolbox\_hb_append_291.py', encoding='utf-8').read()
m = re.search(r'ENTRY = """(.*?)"""', content, re.DOTALL)
ENTRY = m.group(1)
print('ENTRY length (chars):', len(ENTRY))
print('ENTRY bytes (utf-8):', len(ENTRY.encode('utf-8')))
print('First 80 chars:', repr(ENTRY[:80]))
print('Last 80 chars:', repr(ENTRY[-80:]))