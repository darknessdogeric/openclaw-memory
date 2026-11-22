#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 Scrapling 隐身栈抓取单个研报页面正文并打印。

Usage: python fetch_stealth_text.py <url> [limit_chars]

与 data_collector.py 共用 AsyncStealthySession，因此能绕过 data_collector
裸 urllib 抓不到正文的 Cloudflare/JS 渲染问题。
"""
import asyncio
import re
import sys

from scrapling.fetchers import AsyncStealthySession

_NOISE_RE = re.compile(r"^(首页|登录|注册|更多|详情|下载|返回|English|中文|分享|收藏|打印)$")


async def grab(url: str, limit: int, network_idle: bool) -> str:
    kwargs = {"timeout": 60000}
    if network_idle:
        kwargs["network_idle"] = True
    async with AsyncStealthySession(max_pages=1) as session:
        page = await session.fetch(url, **kwargs)

    title = ""
    try:
        t = page.css("title::text")
        title = re.sub(r"\s+", " ", t[0]).strip() if t else ""
    except Exception:
        pass

    body = ""
    for sel in ("article", ".article-content", ".content", ".report-content",
                "#content", "body"):
        try:
            nodes = page.css(sel)
        except Exception:
            continue
        for el in nodes:
            try:
                txt = el.text_content()
            except Exception:
                continue
            if txt and len(re.sub(r"\s+", "", txt)) > 400:
                body = txt
                break
        if body:
            break
    if not body:
        try:
            body = page.get_all_text(ignore_tags=("script", "style", "noscript"))
        except Exception:
            body = str(getattr(page, "html_content", b""))

    # 逐行清洗，去导航噪声与重复
    seen, lines = set(), []
    for ln in (body or "").split("\n"):
        ln = re.sub(r"[ \t\u00a0]+", " ", ln).strip()
        if len(ln) < 2 or _NOISE_RE.match(ln) or ln in seen:
            continue
        seen.add(ln)
        lines.append(ln)
    text = "\n".join(lines)
    return f"URL: {url}\nTITLE: {title}\nHTTP: {getattr(page, 'status', '?')}\n" \
           f"{'=' * 60}\n{text[:limit]}\n--- [chars={len(text)} shown={min(limit, len(text))}] ---"


def main() -> int:
    url = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
    idle = "--idle" in sys.argv
    out_path = None
    for i, a in enumerate(sys.argv):
        if a == "--out" and i + 1 < len(sys.argv):
            out_path = sys.argv[i + 1]
    text = asyncio.run(grab(url, limit, idle))
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"saved -> {out_path} ({len(text)} chars)")
    else:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())