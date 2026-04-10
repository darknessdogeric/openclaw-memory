#!/usr/bin/env python3
"""
NanoBrowser 安装脚本
直接下载GitHub最新release并加载到Edge/Chrome
"""
import urllib.request, zipfile, os, shutil, subprocess

RELEASE_URL = "https://github.com/nanobrowser/nanobrowser/releases/download/v0.0.9/nanobrowser.zip"
# 注意：版本号可能需要更新，请访问 https://github.com/nanobrowser/nanobrowser/releases 检查最新版本
INSTALL_DIR = r"C:\Users\ericz\NanoBrowser"
ZIP_PATH = os.path.join(INSTALL_DIR, "nanobrowser.zip")

def download(url, dest):
    print(f"下载中: {url}")
    urllib.request.urlretrieve(url, dest)
    print(f"已保存: {dest}")

def install():
    # 1. 创建目录
    os.makedirs(INSTALL_DIR, exist_ok=True)
    
    # 2. 下载
    try:
        download(RELEASE_URL, ZIP_PATH)
    except Exception as e:
        print(f"下载失败: {e}")
        print("\n请手动访问以下链接下载:")
        print("https://github.com/nanobrowser/nanobrowser/releases")
        return
    
    # 3. 解压
    print("解压中...")
    with zipfile.ZipFile(ZIP_PATH, 'r') as z:
        z.extractall(INSTALL_DIR)
    print(f"解压完成: {INSTALL_DIR}")
    
    # 4. 打开扩展管理页面
    print("\n现在请手动加载扩展:")
    print("1. 打开 edge://extensions/ 或 chrome://extensions/")
    print("2. 开启【开发者模式】(右上角)")
    print("3. 点击【加载解包的扩展】")
    print(f"4. 选择文件夹: {INSTALL_DIR}")
    
    # 5. 用Edge打开扩展页面
    try:
        subprocess.Popen(["msedge", "edge://extensions/"])
    except:
        pass

if __name__ == "__main__":
    install()
