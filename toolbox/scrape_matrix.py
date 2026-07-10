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
        "douyin.com", "fliggy.com",
        ".jd.com", ".taobao.com",
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
                          encoding="utf-8", errors="replace")
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


_SKYVERN_VENV_PY = os.path.join(_ROOT, "workspace", "skyvern_env", "Scripts", "python.exe")
_SKYVERN_SCRIPTS = os.path.join(_ROOT, "toolbox", "skyvern_scripts")
_SKYVERN_LLM_KEY = os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY") or ""

def _run_skyvern_script(script_content: str, timeout: int = 300) -> str:
    """在 Skyvern 3.12 虚拟环境中执行脚本，返回 stdout"""
    import tempfile, pathlib
    os.makedirs(_SKYVERN_SCRIPTS, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", suffix="_skyvern.py",
                                      dir=_SKYVERN_SCRIPTS, delete=False,
                                      encoding="utf-8") as f:
        f.write(script_content)
        script_path = f.name
    env = os.environ.copy()
    if _SKYVERN_LLM_KEY:
        env["OPENAI_API_KEY"] = _SKYVERN_LLM_KEY
    try:
        r = subprocess.run([_SKYVERN_VENV_PY, script_path],
                          capture_output=True, timeout=timeout,
                          env=env, cwd=_ROOT, errors="replace")
        return (r.stdout or "").strip()
    except subprocess.TimeoutExpired:
        return "{\"success\":false,\"error\":\"timeout\"}"
    finally:
        try:
            os.unlink(script_path)
        except:
            pass


def _skyvern_extract(url: str, prompt: str, schema: dict = None,
                     max_steps: int = 8) -> dict:
    """用 Skyvern Vision LLM 从页面提取结构化数据"""
    schema_str = json.dumps(schema) if schema else "null"
    script = f'''
import asyncio, json, os
from skyvern import Skyvern
async def main():
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY","")
    if not api_key:
        print(json.dumps({{"success":False,"error":"no_api_key"}})); return
    sv = Skyvern(api_key=api_key)
    task = await sv.run_task(
        prompt="Navigate to {url} and {prompt}",
        max_steps={max_steps},
        data_extraction_schema={schema_str},
        headless=True
    )
    print(json.dumps({{
        "success": task.get("completed",False),
        "data": task.get("extracted_data") or task.get("status",""),
        "error": None,
        "steps": task.get("steps",0)
    }}, ensure_ascii=False))
asyncio.run(main())
'''
    try:
        out = _run_skyvern_script(script)
        return json.loads(out)
    except:
        return {"success": False, "error": out[:200], "data": None}


# ──────────────────────────────────────────────
# 8. Skyvern 适配器（智能兜底层，Priority 1）
# ──────────────────────────────────────────────
class SkyvernAdapter(BaseScraperAdapter):
    """
    Skyvern Vision LLM 适配器
    兜底方案：当 scrap_tools/Obscura/Playwright/Tavily 都失败时使用
    核心优势：无需XPath，用自然语言理解任何页面，换网站不坏
    """
    name = "Skyvern"
    priority = 1  # 最高优先级（数字小），在所有工具都失败后作为智能兜底
    
    SKYVERN_TRIGGERS = ["extract", "结构化", "复杂页面", "登录", "需要理解"]

    def is_available(self) -> bool:
        return (
            os.path.exists(_SKYVERN_VENV_PY)
            and bool(_SKYVERN_LLM_KEY)
        )

    def can_handle(self, url: str, task_type: str = "auto") -> bool:
        # 仅在以下情况触发 Skyvern：
        # 1. task_type == "vision" 或 "smart"（显式要求智能理解）
        # 2. 之前所有工具都失败了（由编排器判断）
        # 3. url 包含需要复杂交互的关键词
        if task_type in ("vision", "smart"):
            return True
        if any(t in url.lower() for t in self.SKYVERN_TRIGGERS):
            return True
        return False

    def scrape(self, url: str, **kwargs) -> ScrapeResult:
        prompt = kwargs.get("prompt", f"Extract the main content from this page")
        schema = kwargs.get("schema")
        max_steps = kwargs.get("max_steps", 8)

        result = _skyvern_extract(url, prompt, schema, max_steps)

        if result.get("success"):
            data = result.get("data", {})
            content = json.dumps(data, ensure_ascii=False) if isinstance(data, dict) else str(data)
            return ScrapeResult(
                status=ScrapeStatus.SUCCESS,
                content=content,
                tool_used=self.name,
                attempts=result.get("steps", 1),
                url=url
            )
        return ScrapeResult(
            status=ScrapeStatus.FAILED,
            content="",
            tool_used=self.name,
            attempts=1,
            errors=[result.get("error", "unknown")],
            url=url
        )


# ──────────────────────────────────────────────
# 9. Vision 适配器（智能兜底）
# ──────────────────────────────────────────────
# ─────────────────────────────────────────────
# 9.5 InvisiblePlaywright 适配器（跨境 OTA + Firefox 引擎 2026-06-12）
# ─────────────────────────────────────────────
class InvisiblePlaywrightAdapter(BaseScraperAdapter):
    """
    InvisiblePlaywright 适配器 - Firefox 150 + C++ 源 patch
    专属场景：跨境 OTA / 强反爬平台（Booking/Agoda/Airbnb/Expedia）
    核心优势：reCAPTCHA v3 0.90 vs Chromium 0.3-0.5（断层领先）
    验证：2026-06-12 A/B 对比，Obscura 被 consent 页拦截，本工具成功
    """
    name = "InvisiblePlaywright"
    priority = 4  # 介于 Playwright(3) 和 Tavily(4) 之间

    CROSS_BORDER_DOMAINS = [
        # OTA 跨境平台
        "booking.com", "agoda.com", "tripadvisor.com",
        "expedia.com", "hotels.com", "trivago.com",
        "airbnb.com", "kayak.com", "priceline.com",
        # 跨境社交 / 媒体
        "twitter.com", "x.com", "linkedin.com",
        "instagram.com", "facebook.com", "pinterest.com",
        "reddit.com", "yelp.com", "glassdoor.com",
        # 跨境电商
        "amazon.com", "ebay.com", "aliexpress.com",
    ]

    def is_available(self) -> bool:
        try:
            from invisible_playwright import InvisiblePlaywright
            return True
        except ImportError:
            return False

    def can_handle(self, url: str, task_type: str = "auto") -> bool:
        url_lower = url.lower()
        # 跨境场景：默认走 invisible_playwright
        if any(d in url_lower for d in self.CROSS_BORDER_DOMAINS):
            return True
        # task_type=cross-border 显式指定
        if task_type == "cross-border":
            return True
        return False

    def scrape(self, url: str, **kwargs) -> ScrapeResult:
        try:
            from invisible_playwright import InvisiblePlaywright
            wait_ms = kwargs.get("wait_ms", 8000)
            timeout_ms = kwargs.get("timeout_ms", 45000)
            extract = kwargs.get("extract", "title")
            proxy = kwargs.get("proxy", None)
            timezone = kwargs.get("timezone", None)

            ctx_args = {}
            if proxy:
                ctx_args["proxy"] = proxy
            if timezone:
                ctx_args["timezone"] = timezone

            with InvisiblePlaywright(**ctx_args) as browser:
                page = browser.new_page()
                try:
                    page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
                    page.wait_for_timeout(wait_ms)
                    if extract == "title":
                        content = page.title()
                    elif extract == "html":
                        content = page.content()
                    elif extract == "text":
                        content = page.evaluate("() => document.body.innerText")
                    else:
                        content = page.evaluate(extract)
                    return ScrapeResult(
                        status=ScrapeStatus.SUCCESS if content else ScrapeStatus.PARTIAL,
                        content=content or "",
                        tool_used=self.name,
                        attempts=1,
                        url=url,
                    )
                except Exception as e:
                    return ScrapeResult(
                        status=ScrapeStatus.FAILED, content="",
                        tool_used=self.name, attempts=1,
                        errors=[str(e)], url=url,
                    )
                finally:
                    page.close()
        except ImportError:
            return ScrapeResult(status=ScrapeStatus.FAILED, content="",
                              tool_used=self.name, attempts=1,
                              errors=["invisible_playwright not installed"], url=url)
        except Exception as e:
            return ScrapeResult(status=ScrapeStatus.FAILED, content="",
                              tool_used=self.name, attempts=1,
                              errors=[str(e)], url=url)


class VisionAdapter(BaseScraperAdapter):
    """
    Vision LLM 适配器
    用 MiniMax-M2 Vision 直接理解页面截图——彻底告别XPath
    作为所有工具都失败后的智能兜底
    """
    name = "Vision"
    priority = 5

    def is_available(self) -> bool:
        try:
            sys.path.insert(0, os.path.join(_ROOT, "toolbox"))
            from vision_extractor import is_vision_available
            return is_vision_available()
        except ImportError:
            return False

    def can_handle(self, url: str, task_type: str = "auto") -> bool:
        # Vision 作为兜底：任何 url 都可以处理，但优先级最低
        return task_type in ("vision", "smart")

    def scrape(self, url: str, **kwargs) -> ScrapeResult:
        prompt = kwargs.get("prompt", "Extract all useful text from this page")
        try:
            sys.path.insert(0, os.path.join(_ROOT, "toolbox"))
            from vision_extractor import extract_with_vision

            result = extract_with_vision(url, prompt)

            if result.success:
                return ScrapeResult(
                    status=ScrapeStatus.SUCCESS,
                    content=result.content,
                    tool_used=self.name,
                    attempts=1,
                    url=url
                )
            return ScrapeResult(
                status=ScrapeStatus.PARTIAL,
                content=result.content or "",
                tool_used=self.name,
                attempts=1,
                errors=[result.error] if result.error else [],
                url=url
            )
        except ImportError:
            return ScrapeResult(status=ScrapeStatus.FAILED, content="",
                              tool_used=self.name, attempts=1,
                              errors=["vision_extractor not found"], url=url)
        except Exception as e:
            return ScrapeResult(status=ScrapeStatus.FAILED, content="",
                              tool_used=self.name, attempts=1,
                              errors=[str(e)], url=url)


# ──────────────────────────────────────────────
# 10. 编排器（含 Vision 兜底）
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
            InvisiblePlaywrightAdapter(),  # 跨境 OTA / Firefox 引擎 备选
            TavilyAdapter(),
            VisionAdapter(),  # Vision LLM 兜底（scrap失败时调用）
        ]:
            if adapter.is_available():
                self.adapters.append(adapter)
        self.adapters.sort(key=lambda x: x.priority)

    def scrape(self, url: str, task_type: str = "auto",
               max_attempts: int = 4, **kwargs) -> ScrapeResult:
        errors = []
        attempts = 0

        # Skyvern 作为最后兜底（当所有其他工具都失败时）
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

        # ── 所有工具都失败了？尝试 Skyvern 智能兜底 ──
        if skyvern_available := SkyvernAdapter().is_available():
            try:
                skyvern = SkyvernAdapter()
                prompt = kwargs.get("prompt", "Extract all useful information from this page")
                result = skyvern.scrape(url, prompt=prompt,
                                        schema=kwargs.get("schema"),
                                        max_steps=kwargs.get("max_steps", 8))
                if result.status == ScrapeStatus.SUCCESS:
                    return result
                errors.append(f"Skyvern兜底失败: {result.errors}")
            except Exception as e:
                errors.append(f"Skyvern兜底异常: {str(e)}")

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
    """
    统一爬取接口（含 Skyvern 智能兜底）
    
    额外参数（Skyvern）：
        prompt: 自然语言提取指令
        schema: JSON Schema 输出格式
        max_steps: 最大步数（控制任务复杂度）
    """
    return get_orchestrator().scrape(url, task_type, **kwargs)

def scrape_smart(url: str, prompt: str = "Extract all useful content",
                 schema: dict = None, max_steps: int = 8) -> ScrapeResult:
    """
    Skyvern 智能提取 - 强制使用 Vision LLM 理解页面
    适用于：复杂页面/无API/需要语义理解的场景
    """
    return get_orchestrator().scrape(url, task_type="vision",
                                    prompt=prompt, schema=schema,
                                    max_steps=max_steps)

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
