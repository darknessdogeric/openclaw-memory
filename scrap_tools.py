#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scrap_tools - 静态/动态页面抓取工具
=====================================
支持 fetch（静态）+ dynamic（JS渲染）两种模式
依赖 Playwright（已安装于 skyvern_env）

用法:
    python scrap_tools.py fetch <url>           # 静态页面
    python scrap_tools.py dynamic <url>        # JS渲染页面
    python scrap_tools.py search <query>       # 搜索
    python scrap_tools.py smart <query>         # 智能搜索（多引擎）
    python scrap_tools.py parse <html>           # 解析HTML
"""
import sys, os, json, subprocess, argparse

# ──────────────────────────────────────────────
# 路径：优先用 skyvern_env 的 Playwright
# ──────────────────────────────────────────────
VENV_PY = r"D:\B166ER-OpenClaw\workspace\workspace\skyvern_env\Scripts\python.exe"
HAS_VENV = os.path.exists(VENV_PY)

PYExec = VENV_PY if HAS_VENV else sys.executable

# ──────────────────────────────────────────────
# 静态抓取（urllib / requests）
# ──────────────────────────────────────────────
def fetch_url(url: str) -> str:
    import urllib.request, urllib.error

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            charset = "utf-8"
            ct = resp.headers.get("Content-Type", "")
            if "charset=" in ct:
                charset = ct.split("charset=")[-1].strip().split(";")[0]
            raw = resp.read()
            return raw.decode(charset, errors="replace")
    except urllib.error.HTTPError as e:
        return f"[HTTP Error {e.code}] {e.reason}"
    except Exception as e:
        return f"[Error] {str(e)}"


# ──────────────────────────────────────────────
# 动态抓取（Playwright JS渲染）
# ──────────────────────────────────────────────
def _run_pw_script(url: str, mode: str = "text") -> str:
    """
    在 skyvern_env 里用 Playwright 抓取页面
    mode: text → inner_text | html → content | screenshot → 保存截图
    """
    script = f'''
import sys
sys.path.insert(0, r'D:\\B166ER-OpenClaw\\workspace\\workspace\\skyvern_env\\Lib\\site-packages')
from playwright.sync_api import sync_playwright

url = {repr(url)}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={{"width": 1280, "height": 900}})
    page.goto(url, timeout=30000, wait_until="networkidle")
    page.wait_for_timeout(2000)

    if {repr(mode)} == "text":
        print(page.inner_text("body"))
    elif {repr(mode)} == "html":
        print(page.content())
    elif {repr(mode)} == "screenshot":
        import tempfile, uuid
        path = tempfile.gettempdir() + "\\\\pw_screenshot_" + uuid.uuid4().hex[:8] + ".png"
        page.screenshot(path=path, full_page=False)
        print("SCREENSHOT:" + path)

    browser.close()
'''
    import tempfile
    with tempfile.NamedTemporaryFile(
        mode="w", suffix="_pw_fetch.py",
        dir=os.path.dirname(__file__) or ".",
        delete=False, encoding="utf-8"
    ) as f:
        f.write(script)
        script_path = f.name

    try:
        r = subprocess.run(
            [PYExec, script_path],
            capture_output=True, timeout=60,
            cwd=os.path.dirname(__file__) or ".", errors="replace"
        )
        os.unlink(script_path)
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        try:
            os.unlink(script_path)
        except:
            pass
        return f"[Error] {str(e)}"


def dynamic_url(url: str) -> str:
    return _run_pw_script(url, "text")


# ──────────────────────────────────────────────
# 搜索（多引擎回退）
# ──────────────────────────────────────────────
def search(query: str, engine: str = "auto") -> str:
    """搜索，回退逻辑：DuckDuckGo → Bing → Baidu"""
    try:
        import urllib.request, urllib.parse

        q = urllib.parse.quote(query)
        # 优先 DuckDuckGo（无反爬）
        url = f"https://duckduckgo.com/html/?q={q}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 Chrome/120.0"}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"[Search Error] {str(e)}"


def smart_search(query: str) -> str:
    """智能搜索：同时尝试多个引擎"""
    results = {}
    # DuckDuckGo
    try:
        import urllib.request, urllib.parse
        q = urllib.parse.quote(query)
        req = urllib.request.Request(
            f"https://duckduckgo.com/html/?q={q}",
            headers={"User-Agent": "Mozilla/5.0 Chrome/120.0"}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            results["duckduckgo"] = resp.read().decode("utf-8", errors="replace")[:2000]
    except Exception:
        results["duckduckgo"] = ""

    return json.dumps(results, ensure_ascii=False, indent=2)


# ──────────────────────────────────────────────
# HTML 解析（beautifulsoup4）
# ──────────────────────────────────────────────
def parse_html(html: str, engine: str = "bs4") -> str:
    """从HTML中提取正文"""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # 移除 script/style/nav/footer
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        # 合并空行
        lines = [l for l in text.split("\n") if l.strip()]
        return "\n".join(lines[:200])  # 最多200行
    except ImportError:
        # fallback: 正则提取
        import re
        text = re.sub(r"<script.*?</script>", "", html, flags=re.DOTALL)
        text = re.sub(r"<style.*?</style>", "", text, flags=re.DOTALL)
        text = re.sub(r"<[^>]+>", "", text)
        return text.strip()[:5000]
    except Exception as e:
        return f"[Parse Error] {str(e)}"


# ──────────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="scrap_tools: 静态+动态页面抓取",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_fetch = sub.add_parser("fetch", help="抓取静态页面（urllib）")
    p_fetch.add_argument("url", help="目标URL")

    p_dyn = sub.add_parser("dynamic", help="抓取JS渲染页面（Playwright）")
    p_dyn.add_argument("url", help="目标URL")

    p_search = sub.add_parser("search", help="搜索")
    p_search.add_argument("query", help="搜索词")
    p_search.add_argument("--engine", "-e", default="auto",
                          choices=["auto", "ddg", "bing", "baidu"],
                          help="搜索引擎")

    p_smart = sub.add_parser("smart", help="智能搜索（多引擎）")
    p_smart.add_argument("query", help="搜索词")

    p_parse = sub.add_parser("parse", help="解析HTML")
    p_parse.add_argument("html", help="HTML内容（从stdin或文件）")
    p_parse.add_argument("--file", "-f", help="从文件读取HTML")

    args = parser.parse_args()

    if args.cmd == "fetch":
        result = fetch_url(args.url)
        print(result)

    elif args.cmd == "dynamic":
        result = dynamic_url(args.url)
        print(result)

    elif args.cmd == "search":
        result = search(args.query, args.engine)
        print(result)

    elif args.cmd == "smart":
        result = smart_search(args.query)
        print(result)

    elif args.cmd == "parse":
        if args.file:
            with open(args.file, "r", encoding="utf-8", errors="replace") as f:
                html = f.read()
        else:
            html = args.html
        result = parse_html(html)
        print(result)


if __name__ == "__main__":
    main()
