# -*- coding: utf-8 -*-
"""
AHL爬虫技能矩阵 - 统一爬虫接口
四工具编排: scrap_tools / Obscura / Playwright / Tavily
"""
from __future__ import annotations
import os, sys, json, subprocess, time
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from abc import ABC, abstractmethod

# ──────────────────────────────────────────────
# 0. 路径常量
# ──────────────────────────────────────────────
_ROOT = r"D:\B166ER-OpenClaw\workspace"
_SCRAPE_TOOLS = os.path.join(_ROOT, "scrap_tools.py")
_OBSCURA_BIN = os.path.join(_ROOT, "toolbox", "obscura", "obscura.exe")
_TAVILY_KEY = os.environ.get(
    "TAVILY_API_KEY",
    "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"
)

# ──────────────────────────────────────────────
# 1. 结果标准化
# ──────────────────────────────────────────────
class ScrapeStatus(Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"

@dataclass
class ScrapeResult:
    status: ScrapeStatus
    content: str
    tool_used: str
    attempts: int = 1
    errors: list = field(default_factory=list)
    url: str = ""

# ──────────────────────────────────────────────
# 2. 抽象基类
# ──────────────────────────────────────────────
class BaseScraperAdapter(ABC):
    name: str = "Base"
    priority: int = 99

    @abstractmethod
    def can_handle(self, url: str, task_type: str = "auto") -> bool: ...

    @abstractmethod
    def scrape(self, url: str, **kwargs) -> ScrapeResult: ...

    def is_available(self) -> bool:
        return True

# ──────────────────────────────────────────────
# 3. scrap_tools 适配器
# ──────────────────────────────────────────────
class ScrapToolsAdapter(BaseScraperAdapter):
    """
    适配 scrap_tools.py
    速度最快，零依赖，适合静态页面
    """

    name = "scrap_tools"
    priority = 1

    STATIC_PATTERNS = [
        ".gov.cn", ".baidu.com", ".wikipedia.org",
        "news.sina.com", "news.163.com", ".sina.com",
        ".qq.com/news", ".ifeng.com", ".chinanews.com",
        "journal.cn", ".cctv.com", ".xinhuanet.com",
        "*.cn/info/", "*.gov/", ".org.cn", ".edu.cn",
    ]

    ANTI_PATTERNS = [
        "ctrip.com", "meituan.com", "xiaohongshu.com",
        "douyin.com", "fliggy.com", "hotels.com",
        "booking.com", "airbnb.com", "expedia.com",
        "agoda.com", "marriott.com", "hilton.com",
        "ihg.com", "wyndham.com",
    ]

    def is_available(self) -> bool:
        return os.path.exists(_SCRAPE_TOOLS)

    def can_handle(self, url: str, task_type: str = "auto") -> bool:
        url_lower = url.lower()
        # 强制dynamic不用scrap_tools
        if task_type == "dynamic":
            return False
        # 强反爬，不用scrap_tools
        if any(p in url_lower for p in self.ANTI_PATTERNS):
            return False
        # research类型应该用Tavily
        if task_type == "research":
            return False
        # 已知静态站点优先
        if any(p.replace("*", "") in url_lower for p in self.STATIC_PATTERNS):
            return True
        # 默认可以试（scrap_tools有dynamic fallback）
        return True

    def scrape(self, url: str, **kwargs) -> ScrapeResult:
        try:
            mode = kwargs.get("mode", "auto")
            if mode == "auto":
                result = self._fetch(url)
                if not result.strip() or "error" in result.lower()[:50]:
                    result = self._dynamic(url)
            elif mode == "static":
                result = self._fetch(url)
            else:
                result = self._dynamic(url)

            if result.strip() and "error" not in result.lower()[:50]:
                return ScrapeResult(status=ScrapeStatus.SUCCESS, content=result,
                                  tool_used=self.name, attempts=1, url=url)
            return ScrapeResult(status=ScrapeStatus.PARTIAL, content=result,
                              tool_used=self.name, attempts=1,
                              errors=["empty or error"], url=url)
        except FileNotFoundError:
            return ScrapeResult(status=ScrapeStatus.FAILED, content="",
                              tool_used=self.name, attempts=1,
                              errors=["scrap_tools.py not found"], url=url)
        except Exception as e:
            return ScrapeResult(status=ScrapeStatus.FAILED, content="",
                              tool_used=self.name, attempts=1,
                              errors=[str(e)], url=url)

    def _fetch(self, url: str) -> str:
        cmd = [sys.executable, _SCRAPE_TOOLS, "fetch", url]
        r = subprocess.run(cmd, capture_output=True, timeout=120,
                          errors="replace")
        return (r.stdout or "") + (r.stderr or "")


    def _dynamic(self, url: str) -> str:
        cmd = [sys.executable, _SCRAPE_TOOLS, "dynamic", url]
        r = subprocess.run(cmd, capture_output=True, timeout=120,
                          errors="replace")
        return (r.stdout or "") + (r.stderr or "")


# ──────────────────────────────────────────────
# 4. Obscura 适配器
# ──────────────────────────────────────────────
class ObscuraAdapter(BaseScraperAdapter):
    """
    适配 Obscura (Rust无头浏览器)
    内置反检测，极低内存，JS渲染
    """

    name = "Obscura"
    priority = 2

    OBSCURA_PATTERNS = [
        "ctrip.com", "meituan.com", "xiaohongshu.com",
        "douyin.com", "fliggy.com", "hotels.com",
        "booking.com", "airbnb.com", "expedia.com",
        "agoda.com", ".jd.com", ".taobao.com",
    ]

    def is_available(self) -> bool:
        return os.path.exists(_OBSCURA_BIN)

    def can_handle(self, url: str, task_type: str = "auto") -> bool:
        url_lower = url.lower()
        if any(p in url_lower for p in self.OBSCURA_PATTERNS):
            return True
        if task_type == "dynamic":
            return True
        return False

    def scrape(self, url: str, **kwargs) -> ScrapeResult:
        stealth = kwargs.get("stealth", True)
        eval_js = kwargs.get("eval", "document.body.innerText")
        timeout = kwargs.get("timeout", 30)

        try:
            result = self._cli_fetch(url, eval_js, stealth, timeout)
            if result.strip():
                return ScrapeResult(status=ScrapeStatus.SUCCESS, content=result,
                                  tool_used=self.name, attempts=1, url=url)
            return ScrapeResult(status=ScrapeStatus.PARTIAL, content=result,
                              tool_used=self.name, attempts=1,
                              errors=["empty content"], url=url)
        except FileNotFoundError:
            return ScrapeResult(status=ScrapeStatus.FAILED, content="",
                              tool_used=self.name, attempts=1,
                              errors=["Obscura not installed"], url=url)
        except subprocess.TimeoutExpired:
            return ScrapeResult(status=ScrapeStatus.FAILED, content="",
                              tool_used=self.name, attempts=1,
                              errors=["timeout"], url=url)
        except Exception as e:
            return ScrapeResult(status=ScrapeStatus.FAILED, content="",
                              tool_used=self.name, attempts=1,
                              errors=[str(e)], url=url)

    def _cli_fetch(self, url: str, eval_js: str, stealth: bool, timeout: int) -> str:
        cmd = [_OBSCURA_BIN, "fetch", url]
        if stealth:
            cmd.append("--stealth")
        cmd.extend(["--eval", eval_js, "--timeout", str(timeout), "--quiet"])
        r = subprocess.run(cmd, capture_output=True, timeout=timeout + 10,
                          errors="replace")
        return r.stdout.strip() if r.stdout else ""


# ──────────────────────────────────────────────
# 5. Playwright 适配器
# ──────────────────────────────────────────────
class PlaywrightAdapter(BaseScraperAdapter):
    """Playwright: 复杂交互/登录态"""

    name = "Playwright"
    priority = 3

    PW_PATTERNS = ["/login", "/signin", "/auth", "form"]

    def is_available(self) -> bool:
        try:
            import playwright
            return True
        except ImportError:
            return False

    def can_handle(self, url: str, task_type: str = "auto") -> bool:
        url_lower = url.lower()
        if any(p in url_lower for p in self.PW_PATTERNS):
            return True
        if task_type in ("interactive", "form", "login"):
            return True
        return False

    def scrape(self, url: str, **kwargs) -> ScrapeResult:
        try:
            from playwright.sync_api import sync_playwright
            wait_time = kwargs.get("wait_time", 3)
            timeout = kwargs.get("timeout", 30) * 1000

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=timeout)
                page.wait_for_timeout(wait_time * 1000)
                content = page.inner_text("body")
                browser.close()

            return ScrapeResult(status=ScrapeStatus.SUCCESS, content=content or "",
                              tool_used=self.name, attempts=1, url=url)
        except ImportError:
            return ScrapeResult(status=ScrapeStatus.FAILED, content="",
                              tool_used=self.name, attempts=1,
                              errors=["Playwright not installed"], url=url)
        except Exception as e:
            return ScrapeResult(status=ScrapeStatus.FAILED, content="",
                              tool_used=self.name, attempts=1,
                              errors=[str(e)], url=url)


# ──────────────────────────────────────────────
# 6. Tavily API 适配器
# ──────────────────────────────────────────────
class TavilyAdapter(BaseScraperAdapter):
    """Tavily API: 研究型搜索"""

    name = "Tavily"
    priority = 4

    def is_available(self) -> bool:
        return bool(_TAVILY_KEY)

    def can_handle(self, url: str, task_type: str = "auto") -> bool:
        return task_type == "research" or url == "__search__"

    def scrape(self, url: str, **kwargs) -> ScrapeResult:
        query = url if url != "__search__" else kwargs.get("query", "")
        try:
            import urllib.request
            payload = json.dumps({
                "api_key": _TAVILY_KEY,
                "query": query,
                "max_results": kwargs.get("max_results", 5),
                "include_answer": True,
                "include_raw_content": False,
            }).encode("utf-8")
            req = urllib.request.Request(
                "https://api.tavily.com/search",
                data=payload,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            parts = []
            if data.get("answer"):
                parts.append(f"[答案] {data['answer']}")
            for item in data.get("results", [])[:5]:
                parts.append(f"## {item['title']}\n{item['url']}\n{item.get('content', '')[:200]}")
            content = "\n\n".join(parts)

            return ScrapeResult(status=ScrapeStatus.SUCCESS, content=content,
                              tool_used=self.name, attempts=1, url=query)
        except Exception as e:
            return ScrapeResult(status=ScrapeStatus.FAILED, content="",
                              tool_used=self.name, attempts=1,
                              errors=[str(e)], url=query)


# ──────────────────────────────────────────────
# 7. 编排器
# ──────────────────────────────────────────────
class ScrapeSkillOrchestrator:
    """
    爬虫技能矩阵编排器
    自动路由 + 失败自动降级
    """

    def __init__(self):
        self.adapters: list[BaseScraperAdapter] = []
        for adapter in [
            ScrapToolsAdapter(),
            ObscuraAdapter(),
            PlaywrightAdapter(),
            TavilyAdapter(),
        ]:
            if adapter.is_available():
                self.adapters.append(adapter)
        self.adapters.sort(key=lambda x: x.priority)

    def scrape(self, url: str, task_type: str = "auto",
               max_attempts: int = 4, **kwargs) -> ScrapeResult:
        errors = []
        attempts = 0

        for adapter in self.adapters:
            if not adapter.can_handle(url, task_type):
                continue
            attempts += 1
            try:
                result = adapter.scrape(url, **kwargs)
                result.attempts = attempts
                if result.status != ScrapeStatus.FAILED:
                    return result
                errors.append(f"{adapter.name}: {result.errors}")
            except Exception as e:
                errors.append(f"{adapter.name} Exception: {str(e)}")

        return ScrapeResult(
            status=ScrapeStatus.FAILED,
            content="",
            tool_used="none",
            attempts=attempts,
            errors=errors,
            url=url
        )

    def report(self) -> dict:
        return {
            "adapters": [
                {"name": a.name, "priority": a.priority,
                 "available": a.is_available()}
                for a in self.adapters
            ],
            "total_tools": len(self.adapters),
        }


# ──────────────────────────────────────────────
# 8. 快捷函数
# ──────────────────────────────────────────────
_orch: Optional[ScrapeSkillOrchestrator] = None

def get_orchestrator() -> ScrapeSkillOrchestrator:
    global _orch
    if _orch is None:
        _orch = ScrapeSkillOrchestrator()
    return _orch

def scrape(url: str, task_type: str = "auto", **kwargs) -> ScrapeResult:
    return get_orchestrator().scrape(url, task_type, **kwargs)

def scrape_search(query: str, max_results: int = 5) -> ScrapeResult:
    return get_orchestrator().scrape("__search__", task_type="research",
                                    query=query, max_results=max_results)

def matrix_report() -> dict:
    return get_orchestrator().report()


# ──────────────────────────────────────────────
# 9. CLI入口
# ──────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AHL爬虫技能矩阵")
    parser.add_argument("url", help="目标URL")
    parser.add_argument("--type", "-t", default="auto",
                        choices=["auto", "static", "dynamic", "research", "interactive"])
    parser.add_argument("--report", "-r", action="store_true")
    args = parser.parse_args()

    if args.report:
        print(json.dumps(matrix_report(), indent=2, ensure_ascii=False))
        sys.exit(0)

    result = scrape(args.url, task_type=args.type)
    print(f"[{result.status.value}] tool={result.tool_used} attempts={result.attempts}")
    print(f"URL: {result.url}")
    if result.errors:
        print(f"Errors: {result.errors}")
    print("---Content---")
    print(result.content[:1000] if result.content else "(empty)")
