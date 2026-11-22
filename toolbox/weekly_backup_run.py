# -*- coding: utf-8 -*-
"""Wrapper to run weekly_backup.py with UTF-8 console."""
import sys
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\toolbox')
# Force stdout utf-8 on Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

# Import and run main
import weekly_backup
weekly_backup.backup()
