"""推送月报预测-T5 到 Obsidian"""
import sys
import shutil
from pathlib import Path

# 准备临时文件
src = Path(r"D:\B166ER-OpenClaw\workspace\docs\产业发展部\02-产业研究方法论\月报专题\2026-09月酒店市场预测报告.md")
tmp = Path(r"D:\B166ER-OpenClaw\workspace\toolbox\monthly-pred-2026-08-25.md")
shutil.copy2(src, tmp)
print(f"Copied to {tmp}")

# 调用 cron_to_obsidian.py
import subprocess
script = Path(r"D:\B166ER-OpenClaw\workspace\toolbox\cron_to_obsidian.py")

summary_text = (
    "9月预测三大要点："
    "①双节驱动型弱复苏（OCC微涨/ADR微跌/RevPAR仍降3%）；"
    "②K型分化加剧（豪华+1~3% vs 经济-7~-4%）；"
    "③县域长线领涨（布尔津/九寨沟/婺源TOP10+连住7天+30%）"
)

cmd = [
    sys.executable,
    str(script),
    "--task", "月报预测-T5",
    "--content-file", str(tmp),
    "--importance", "high",
    "--summary", summary_text,
    "--append-daily",
]
print("Running:", " ".join(cmd[:6]), "...")
result = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return:", result.returncode)
