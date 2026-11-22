"""修复 v3 脚本中 4 处 B() 字符串缺少结尾单引号"""
p = r'D:\B166ER-OpenClaw\workspace\toolbox\gen_tea_plan_v3.py'
with open(p, encoding='utf-8') as f:
    s = f.read()

# 模式：B('xxx) 缺结尾 '  →  B('xxx')
# 用正则匹配：B\('(.*?)\)  -> 把结尾的 ) 替换为 ')
import re
# 只匹配 B( 函数调用，且缺少结尾 '
# 找到 B(' ... ) 但后面不是 '
# 简化的方式：B('xxx) 其中 xxx 不含 '

# 直接列出这 4 行并修复
lines = s.split('\n')
fixed_lines = []
fixes_applied = 0
for line in lines:
    new_line = line
    if "B('" in line and not "B('')" in line:
        # 检查这一行是否以 ')\n 或 ')\r 结尾（即缺 '）
        if new_line.rstrip().endswith(')'):
            # 找到 B(' 开始
            idx = new_line.find("B('")
            if idx >= 0:
                # 看 B('...' 的尾巴是不是缺 '
                # 模式：B('xxxx)  →  B('xxxx')
                # 找到最后一个 )
                stripped = new_line.rstrip()
                if stripped.endswith(')'):
                    # 倒数第 2 个字符应该是 ' 才是完整的
                    # 当前最后一个字符是 ')'，倒数第二是 'g'（业务）或者 ')'？
                    # 修复：B('xxx) → B('xxx')
                    if not stripped.endswith("')"):
                        new_line = stripped + "'" + new_line[len(stripped):]
                        fixes_applied += 1
    fixed_lines.append(new_line)

new_s = '\n'.join(fixed_lines)
with open(p, 'w', encoding='utf-8') as f:
    f.write(new_s)
print(f'共修复 {fixes_applied} 处')
