#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
obsidian_link_suite.py — Obsidian 链接工具集 (今晚所有 ROI 整合)

命令:
  scan         - 扫 vault,生成 link density 报告
  diagnose     - 找孤岛 (用 loose 比较)
  inject       - 给孤岛加正向 link (related 区块)
  mirror       - 给 hub MOC 加反向 link (桌面项目素材)
  daylinks     - 给 daily note 加 mini-MOC
  dataview     - 准备 Dataview 视图页面
  full         - 一键跑 inject + mirror (Eric 习惯动作)

典型调用:
  python toolbox/obsidian_link_suite.py scan            # 看现状
  python toolbox/obsidian_link_suite.py diagnose        # 找孤岛
  python toolbox/obsidian_link_suite.py full            # 全打
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

CMDS = ['scan', 'diagnose', 'inject', 'mirror', 'daylinks', 'dataview', 'full']

USAGE = f"""
obsidian_link_suite.py — Obsidian 链接工具集

命令:
  scan         扫 vault, 生成 link density 报告
  diagnose     找孤岛 (用 loose .md 比较)
  inject       给孤岛加正向 link (related 区块) - ROI 1
  mirror       给 hub MOC 加反向 link (桌面项目素材) - ROI 2
  daylinks     给 daily note 加 mini-MOC
  dataview     准备 Dataview 视图页面
  full         一键跑 inject + mirror

可用命令: {CMDS}
"""

if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
    print(USAGE)
    sys.exit(1)

cmd = sys.argv[1]
print(f"即将运行: {cmd}")
print("提示: 今晚的 ROI 1+2+2.5+3 已经做完, 这个 CLI 是工具沉淀")
print(f"明天 Eric 跑 `python toolbox/obsidian_link_suite.py {cmd}` 即可复用")
print()

# 实际执行: 转发到对应脚本
import subprocess
from pathlib import Path
TOOLBOX = Path(__file__).parent

SCRIPT_MAP = {
    'scan': 'obsidian_link_diag.py',
    'diagnose': 'obsidian_link_diag.py',
    'inject': 'obsidian_link_injector.py',
    'mirror': 'obsidian_roi25_mirror.py',
    'daylinks': 'obsidian_daylinks.py',  # 待做
    'dataview': 'dataview_views.py',
    'full': 'obsidian_link_full.py',     # 待做
}

script = SCRIPT_MAP.get(cmd)
if script and (TOOLBOX / script).exists():
    print(f"转发到: {script}")
    result = subprocess.run(
        [sys.executable, str(TOOLBOX / script)] + sys.argv[2:],
        capture_output=False
    )
    sys.exit(result.returncode)
else:
    print(f"[TODO] {cmd} 还没绑定到脚本, 明天补")
    print(f"或手动跑: python toolbox/{script}")
    sys.exit(0)