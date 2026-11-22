# -*- coding: utf-8 -*-
"""合并 7 个版本国堰营销培训手册为 1 个文件"""
import os
from pathlib import Path
import re

DIR = Path(r'D:\B166ER-openclaw\workspace\anyi-ops-kb\08_培训手册')

files = [
    DIR / '国堰宾馆深度营销进阶培训手册_v1.0_2026-10-02.md',
    DIR / '国堰宾馆深度营销进阶培训手册_v2.0_2026-10-03.md',
    DIR / '国堰宾馆深度营销进阶培训手册_v3.0_重点深化版_2026-10-10.md',
    DIR / '国堰宾馆深度营销进阶培训手册_v3.1_RFP专项深化_2026-10-10.md',
    DIR / '国堰宾馆深度营销进阶培训手册_v3.2_三板块强化版_2026-10-17.md',
    DIR / '国堰宾馆深度营销进阶培训手册_v3.3_三板块强化版+执行物_2026-10-17.md',
    DIR / '国堰宾馆深度营销进阶培训手册_v3.4_限功能性本地社区化_2026-10-17.md',
]

for f in files:
    print(f'{"OK" if f.exists() else "MISSING":4} {f.name} ({f.stat().st_size//1024} KB)' if f.exists() else f'MISSING {f.name}')

print('---')
print(f'Total: {sum(f.stat().st_size for f in files if f.exists())//1024} KB')
