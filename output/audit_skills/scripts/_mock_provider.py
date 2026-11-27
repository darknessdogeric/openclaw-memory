#!/usr/bin/env python3
"""Mock 图像 provider — 满足 provider_command 契约, 生成占位 PNG, 无需任何 API
契约: 接收 --request-file <path>, 读 JSON, 打印 {status:SUCCESS, image_path:...}
"""
import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ap = argparse.ArgumentParser()
ap.add_argument("--request-file", required=True)
args = ap.parse_args()

req = json.loads(Path(args.request_file).read_text(encoding="utf-8"))
n = int(req.get("slide_number", 0) or 0)
slide = req.get("slide") or {}
goal = str(slide.get("page_goal") or slide.get("content") or "")

try:
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (1600, 900), "#0f1420")
    d = ImageDraw.Draw(im)
    d.rectangle([40, 40, 1560, 860], outline="#3d7ef0", width=4)
    d.text((690, 400), f"SLIDE {n:02d}", fill="#e6e8ec")
    d.text((560, 445), goal[:46], fill="#8a93a5")
    out_dir = os.environ.get("MOCK_OUT_DIR") or tempfile.gettempdir()
    out = Path(out_dir) / f"mock-slide-{n:02d}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out)
    result = {"status": "SUCCESS", "provider": "mock", "image_path": str(out.resolve())}
except Exception as e:
    result = {"status": "FAILED", "provider": "mock", "reason": f"{type(e).__name__}: {e}"}

json.dump(result, sys.stdout, ensure_ascii=False)
sys.exit(0 if result["status"] == "SUCCESS" else 1)
