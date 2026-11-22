#!/usr/bin/env python3
"""R-NEW-V5: Append state.json data loss event to corrections.md."""
import os

entry = """
| 2026-08-14 | **state.json 被 PowerShell ConvertTo-Json 静默失败 + 0 字节覆盖（数据丢失事件 #3）**:HB #3208 写 state.json 时写 `$state | ConvertTo-Json -Depth 10 -Encoding UTF8`,但 **PowerShell 的 ConvertTo-Json 不支持 -Encoding 参数**(仅 Get/Set-Content 等文件命令支持)。错误信息"找不到与参数名称 Encoding 匹配的参数" -> $stateJson 变量为 $null(赋值语句失败但 PowerShell 不抛终止错误) -> 后面的 `[System.IO.File]::WriteAllText($tmpPath, $null, ...)` 接受 $null 为空字符串 -> tmp 文件 0 字节 -> Move-Item 把 0 字节文件覆盖原 state.json -> state.json 从 1181 字节变为 0 字节。**与 R-NEW-V3 同源 bug 模式**:HEARTBEAT.md/HEARTBEAT/state.json 任何"看似原子"的写操作都有"参数错误导致静默 0 字节"风险。**3 个根因**:① PowerShell 7+ ConvertTo-Json 不支持 -Encoding(与 Set/Get-Content 不同) ② 变量赋值失败时 PowerShell 不抛终止错误 ③ `Move-Item -Force` 覆盖文件无大小校验。**修复路径**:写 toolbox/restore_state_json.py 用 Python json.dump + os.replace 原子写入,写盘前 assert size > 0。**与 R-NEW-V3/V4 升级关系**:R-NEW-V3 = HEARTBEAT.md append-only;R-NEW-V4 = state.json atomic-tmp-move;R-NEW-V5 = **写盘前必须 assert size > 0 + PowerShell 嵌套参数失败模式化识别**。**未污染交付**:state.json 已用 Python atomic restore 成功恢复(1181 字节),HB #3208 已正确 append 到 HEARTBEAT.md,Eric 那边无感知。**R-NEW-V5 待 Eric 批准后入 rules.md**。 | **R-NEW-V5 候选**(待 Eric 同意后写 rules.md):① PowerShell 任何 `ConvertTo-Json / ConvertFrom-Json` 调用不传 -Encoding(仅 Cmdlet 文件命令支持)② 写盘前必须 assert size > 0 再 Move-Item/Replace③ 任何变量赋值失败要 echo + exit 1,不能 silent-fail-然后-0-字节覆盖。**关联**:R-NEW-V3/V4 兄弟规则,统一"看似原子但实际可丢数据"的 bug 类。 | 已记录,R-NEW-V5 待批 |
"""

path = r'C:\Users\ericz\self-improving\corrections.md'
size_before = os.path.getsize(path)
with open(path, 'a', encoding='utf-8') as f:
    f.write(entry)
size_after = os.path.getsize(path)
print(f'APPEND OK: {size_before} -> {size_after} bytes (+{size_after - size_before})')