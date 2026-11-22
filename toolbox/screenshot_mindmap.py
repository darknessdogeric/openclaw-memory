"""
Edge headless screenshot with virtual-time-budget for JS rendering
"""
import os
import subprocess

OUT_DIR = r"D:\B166ER-OpenClaw\workspace\outputs\酒管公司供应链工程-交付包-v1.0\04-思维导图"
HTML_PATH = os.path.join(OUT_DIR, "酒管公司供应链工程-思维导图.html")
PNG_1X = os.path.join(OUT_DIR, "酒管公司供应链工程-思维导图.png")
PNG_2X = os.path.join(OUT_DIR, "酒管公司供应链工程-思维导图-2x.png")

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def screenshot(html_path, png_path, width, height, virtual_time_ms=8000):
    file_url = "file:///" + html_path.replace("\\", "/")
    args = [
        EDGE,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        f"--window-size={width},{height}",
        f"--virtual-time-budget={virtual_time_ms}",
        f"--screenshot={png_path}",
        file_url,
    ]
    proc = subprocess.run(args, capture_output=True, text=True, timeout=120,
                          encoding="utf-8", errors="ignore")
    if proc.returncode != 0:
        print(f"  Return code: {proc.returncode}")
        if proc.stderr:
            print(f"  STDERR (first 200 chars): {proc.stderr[:200]}")
    return os.path.exists(png_path)


def main():
    print("Generating 1x screenshot...")
    if screenshot(HTML_PATH, PNG_1X, 1080, 1440, virtual_time_ms=10000):
        print(f"  1x: {os.path.getsize(PNG_1X):,} bytes")
    else:
        print("  1x FAILED")

    print("Generating 2x screenshot...")
    if screenshot(HTML_PATH, PNG_2X, 2160, 2880, virtual_time_ms=10000):
        print(f"  2x: {os.path.getsize(PNG_2X):,} bytes")
    else:
        print("  2x FAILED")


if __name__ == "__main__":
    main()