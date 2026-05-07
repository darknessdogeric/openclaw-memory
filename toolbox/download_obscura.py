# -*- coding: utf-8 -*-
"""断点续传下载Obscura"""
import os, sys, urllib.request, urllib.error

DEST = r"D:\B166ER-OpenClaw\workspace\toolbox\obscura\obscura_new.zip"
URL = "https://github.com/h4ckf0r0day/obscura/releases/download/v0.1.2/obscura-x86_64-windows.zip"
EXPECTED_SIZE = 35_322_430  # bytes

def download_with_resume():
    headers = {"User-Agent": "Mozilla/5.0"}

    # 检查已有大小
    existing = os.path.getsize(DEST) if os.path.exists(DEST) else 0
    print(f"已有: {existing/1024/1024:.1f} MB / {EXPECTED_SIZE/1024/1024:.1f} MB")

    req = urllib.request.Request(URL, headers=headers)
    req.get_method = lambda: "GET"

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            total = int(resp.headers.get("Content-Length", EXPECTED_SIZE))
            print(f"服务端文件大小: {total/1024/1024:.1f} MB")

            if existing >= total * 0.98:
                print("文件已下载完成!")
                return True

            # 断点续传
            mode = "ab" if existing > 0 else "wb"
            print(f"模式: {'续传' if mode == 'ab' else '全新下载'}")
            with open(DEST, mode) as f:
                downloaded = existing
                f.seek(0, 2)  # 确保在末尾
                chunk_size = 64 * 1024
                while True:
                    buf = resp.read(chunk_size)
                    if not buf:
                        break
                    f.write(buf)
                    downloaded += len(buf)
                    pct = downloaded / total * 100
                    sys.stdout.write(f"\r进度: {downloaded/1024/1024:.1f}/{total/1024/1024:.1f} MB ({pct:.1f}%)")
                    sys.stdout.flush()
            print("\n完成!")
            return True
    except urllib.error.HTTPError as e:
        print(f"HTTP错误: {e.code} {e.reason}")
        return False
    except Exception as e:
        print(f"错误: {e}")
        return False

if __name__ == "__main__":
    download_with_resume()
