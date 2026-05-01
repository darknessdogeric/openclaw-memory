path = 'scripts/gen_mayday_ppt.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: add more cities for erxian
old1 = "'二线', '昆明\u00b7三亚\u00b7厦门\u00b7大连\u00b7贵阳\\n南宁\u00b7南昌\u00b7福州\u00b7合肥\u00b7太原', '+8~15%', 'Color Walk+\u5ea6\u5047\u5347\u7ea7'"
new1 = "'二线', '昆明\u00b7三亚\u00b7厦门\u00b7大连\u00b7贵阳\\n南宁\u00b7南昌\u00b7福州\u00b7合肥\u00b7太原\\n哈尔滨\u00b7长春\u00b7呼和浩特\u00b7乌鲁木齐\\n兰州\u00b7银川\u00b7西宁\u00b7拉萨\u00b7海口', '+8~15%', 'Color Walk+\u5ea6\u5047\u5347\u7ea7\\n\u957f\u7ebf\u95e8\u6237\u00b7\u907f\u6691'"
if old1 in content:
    content = content.replace(old1, new1)
    print('Fix 1 OK')
else:
    print('Fix 1 NOT FOUND, searching...')
    for line in content.split('\n'):
        if '二线' in line and 'Color Walk' in line:
            print(f'  Found: {line.strip()[:120]}')

# Fix 2: add DPI note
old2 = "18\u6570\u636e\u6e90\uff1a\u4ea4\u901a\u8fd0\u8f93\u90e8\u00b7\u9152\u5e97\u4e4b\u5bb6\u00b7\u6d69\u534e\u00b7\u4e2d\u4fe1\u00b7\u540c\u7a0b\u00b7\u643a\u7a0b\u00b7\u8fc8\u70b9\u00b7\u73af\u7403\u65c5\u8baf\u00b7STR\u00b7\u6234\u5fb7\u6881\u884c\u7b49"
new2 = "\u5efa\u8bae\u5bfc\u51faDPI\u2265300 \u00b7 18\u6570\u636e\u6e90\uff1a\u4ea4\u901a\u8fd0\u8f93\u90e8\u00b7\u9152\u5e97\u4e4b\u5bb6\u00b7\u6d69\u534e\u00b7\u4e2d\u4fe1\u00b7\u540c\u7a0b\u00b7\u643a\u7a0b\u00b7\u8fc8\u70b9\u00b7\u73af\u7403\u65c5\u8baf\u00b7STR\u00b7\u6234\u5fb7\u6881\u884c\u7b49"
if old2 in content:
    content = content.replace(old2, new2)
    print('Fix 2 OK')
else:
    print('Fix 2 NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
