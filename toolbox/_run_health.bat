@echo off
cd /d "D:\B166ER-OpenClaw\workspace\toolbox"
python -X utf8 vault_sync.py health > "D:\B166ER-OpenClaw\workspace\toolbox\.vault_health.txt" 2>&1
echo DONE > "D:\B166ER-OpenClaw\workspace\toolbox\.vault_health_done.txt"