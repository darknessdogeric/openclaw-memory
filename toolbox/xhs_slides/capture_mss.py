import os
import time
import mss
import ctypes

HTML_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_slides"
OUTPUT_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_slides\output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

files = [
    ("slide_01_cover.html",   "01_封面.png"),
    ("slide_02_el1.html",      "02_要素1_产能识别.png"),
    ("slide_03_el2.html",      "03_要素2_客群区隔.png"),
    ("slide_04_el3.html",      "04_要素3_解耦定价.png"),
    ("slide_05_el4.html",      "05_要素4_消耗加速器.png"),
    ("slide_06_el5.html",      "06_要素5_边界条件.png"),
    ("slide_07_results.html",   "07_成果与方法论.png"),
]

# Find Chrome window
user32 = ctypes.windll.user32

def find_chrome_window():
    import win32gui, win32con
    result = []
    def enum_cb(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                result.append((hwnd, title))
    win32gui.EnumWindows(enum_cb, None)
    return result

try:
    import win32gui
    windows = find_chrome_window()
    print("Visible windows:")
    for hwnd, title in windows[:20]:
        print(f"  {hwnd}: {title[:60]}")
except ImportError:
    print("win32gui not available")
    windows = []

print("\nUsing mss fullscreen capture...")
with mss.mss() as sct:
    mon = sct.monitors[1]  # primary monitor
    print(f"Monitor: {mon}")
    screenshot = sct.shot(mon=1)
    print(f"Screenshot saved: {screenshot}")
