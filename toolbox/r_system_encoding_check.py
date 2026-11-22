#!/usr/bin/env python3
"""检查 rules.md 的编码损坏位置和可恢复性"""
import os

path = os.path.expanduser("~/self-improving/rules.md")
raw = open(path, "rb").read()

print("=== 原始字节概览 ===")
print(f"文件字节数: {len(raw)}")
print(f"前 3 字节 (BOM检测): {raw[:3].hex()}  ({raw[:3]})")

# 检测 UTF-8 BOM
if raw[:3] == b'\xef\xbb\xbf':
    print("  -> 有 UTF-8 BOM")
else:
    print("  -> 无 UTF-8 BOM")

# 尝试按 UTF-8 解码，找错误位置
print("\n=== UTF-8 解码错误位置（前 20 处）===")
errors = []
i = 0
n = len(raw)
while i < n:
    b = raw[i]
    if b < 0x80:
        i += 1
    elif b < 0xC0:
        errors.append((i, 'continuation-without-start', raw[i:i+4].hex()))
        i += 1
    elif b < 0xE0:
        if i+1 < n and (raw[i+1] & 0xC0) == 0x80:
            i += 2
        else:
            errors.append((i, 'bad-2byte', raw[i:i+3].hex()))
            i += 1
    elif b < 0xF0:
        if i+2 < n and (raw[i+1] & 0xC0) == 0x80 and (raw[i+2] & 0xC0) == 0x80:
            i += 3
        else:
            errors.append((i, 'bad-3byte', raw[i:i+4].hex()))
            i += 1
    elif b < 0xF8:
        if i+3 < n and (raw[i+1] & 0xC0) == 0x80 and (raw[i+2] & 0xC0) == 0x80 and (raw[i+3] & 0xC0) == 0x80:
            i += 4
        else:
            errors.append((i, 'bad-4byte', raw[i:i+5].hex()))
            i += 1
    else:
        errors.append((i, 'invalid-start', raw[i:i+2].hex()))
        i += 1

print(f"  解码错误总数: {len(errors)}")
for pos, typ, hexv in errors[:20]:
    # 定位行号
    lineno = raw[:pos].count(b'\n') + 1
    print(f"  字节偏移 {pos} (行 {lineno}): {typ} {hexv}")

# 用 GBK 尝试解码看看是不是 GBK 文件
print("\n=== GBK 解码测试 ===")
try:
    gbk_text = raw.decode('gbk')
    print(f"  GBK 解码成功！字符数: {len(gbk_text)}")
    # 检查是否包含乱码特征
    print(f"  前 200 字: {gbk_text[:200]}")
except Exception as e:
    print(f"  GBK 解码失败: {e}")
