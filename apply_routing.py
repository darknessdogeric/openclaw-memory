# -*- coding: utf-8 -*-
"""
apply_routing.py — 【已废弃·薄壳委托】路由登记入口

变更记录（2026-10-25 心跳收敛）：
  旧行为：把 routing_update_needed.json 的新增路由按【文件名】写进
          skills/knowledge-base/SKILL.md 的 AUTO-ROUTING 追加区。
  问题  ：① SKILL.md 每次会话都加载，承载增长型索引会让它从 5.3KB 涨到 13.9KB；
          ② 与 kb_routing_table.py --apply 形成两套并行写入机制（文件名 vs 全路径），
             同一批 148 个文件两套格式并存，路由匹配时互相干扰。
  现状  ：SKILL.md 的 AUTO-ROUTING 区已剥离（该区 77 条已被 routing-index.md 100% 覆盖，
          缺失 0 条，剥离无损）；文件级路由登记的唯一事实源改为
          skills/knowledge-base/routing-index.md。
  本文件 ：保留为兼容入口，直接委托 kb_routing_table.py --apply（幂等）。

用法: python apply_routing.py   # 等价于 python kb_routing_table.py --apply
"""
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WS = Path(__file__).resolve().parent
TARGET = WS / 'kb_routing_table.py'

if not TARGET.exists():
    print('❌ 找不到 {}'.format(TARGET))
    sys.exit(2)

print('[apply_routing] 已废弃：路由登记的唯一事实源是 skills/knowledge-base/routing-index.md')
print('[apply_routing] 委托执行: python kb_routing_table.py --apply')
print()

rc = subprocess.run([sys.executable, str(TARGET), '--apply'], cwd=str(WS)).returncode
sys.exit(rc)
