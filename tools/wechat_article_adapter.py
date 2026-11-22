"""
WeChat Article Adapter — B166ER 公众号信号层
=============================================

封装 wechat-article-exporter 项目的 API 调用。
提供：
  - 公众号搜索 (search_biz)
  - 文章列表 (appmsgpublish)
  - 文章内容获取
  - 信号摘要生成

两种部署模式：
  1. 在线模式：使用 down.mptext.top 公共服务
  2. 自部署模式：使用本地 Docker / 自托管实例

依赖：requests, beautifulsoup4
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

try:
    import requests
except ImportError:
    requests = None  # type: ignore


# ============================================================
# 配置
# ============================================================

WORKSPACE = Path(__file__).resolve().parent.parent
CONFIG_DIR = WORKSPACE / "config"
SIGNAL_CACHE = CONFIG_DIR / "wechat_signal_cache"
SIGNAL_CACHE.mkdir(parents=True, exist_ok=True)

DEFAULT_BASE_URLS = {
    "public": "https://down.mptext.top",     # 在线公共服务
    "self_hosted": "http://127.0.0.1:3000",  # 本地自部署
}


@dataclass
class WeChatArticle:
    """公众号文章"""
    aid: str
    title: str
    author: str
    publish_time: int  # unix timestamp
    digest: str = ""
    content_url: str = ""
    cover_url: str = ""
    # 元数据（仅当 wxdown-service 配置后可用）
    read_num: Optional[int] = None
    like_num: Optional[int] = None
    comment_num: Optional[int] = None
    # 抓取时的时间
    fetched_at: int = field(default_factory=lambda: int(time.time()))

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def publish_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.publish_time)

    @property
    def signal_age_hours(self) -> float:
        return (time.time() - self.publish_time) / 3600


@dataclass
class WeChatAccount:
    """公众号"""
    fakeid: str
    nickname: str
    alias: str = ""
    signature: str = ""
    avatar_url: str = ""
    category: str = ""
    last_fetch: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


# ============================================================
# 适配器
# ============================================================


class WeChatArticleAdapter:
    """微信公众号文章适配器"""

    def __init__(self, base_url: str = "public", session_cookie: Optional[str] = None):
        if requests is None:
            raise ImportError("需要安装 requests: pip install requests")

        if base_url in DEFAULT_BASE_URLS:
            self.base_url = DEFAULT_BASE_URLS[base_url]
        else:
            self.base_url = base_url.rstrip("/")

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })
        if session_cookie:
            self.session.headers["Cookie"] = session_cookie

    # ----- 健康检查 -----
    def health(self) -> dict:
        """检查服务状态"""
        try:
            r = self.session.get(f"{self.base_url}/", timeout=10)
            return {
                "ok": r.status_code == 200,
                "status_code": r.status_code,
                "base_url": self.base_url,
                "title_contains_login": "登录" in r.text or "扫码" in r.text,
            }
        except Exception as e:
            return {"ok": False, "error": str(e), "base_url": self.base_url}

    # ----- 公众号搜索 -----
    def search_account(self, keyword: str, begin: int = 0, size: int = 10) -> list[WeChatAccount]:
        """搜索公众号"""
        try:
            r = self.session.get(
                f"{self.base_url}/api/public/v1/account",
                params={"keyword": keyword, "begin": begin, "size": size},
                timeout=30,
            )
            data = r.json()
        except Exception as e:
            print(f"[search_account] 请求失败: {e}")
            return []

        if data.get("base_resp", {}).get("ret") != 0:
            err = data.get("base_resp", {}).get("err_msg", "未知错误")
            print(f"[search_account] 服务端错误: {err}")
            return []

        # list 字段可能为字符串（需 JSON parse）
        biz_list_raw = data.get("list", "[]")
        if isinstance(biz_list_raw, str):
            try:
                biz_list = json.loads(biz_list_raw)
            except json.JSONDecodeError:
                biz_list = []
        else:
            biz_list = biz_list_raw

        results = []
        for item in biz_list:
            results.append(WeChatAccount(
                fakeid=item.get("fakeid", ""),
                nickname=item.get("nickname", ""),
                alias=item.get("alias", ""),
                signature=item.get("signature", ""),
                avatar_url=item.get("round_head_img", "") or item.get("头像", ""),
                category=item.get("category", ""),
            ))
        return results

    # ----- 文章列表 -----
    def list_articles(
        self,
        fakeid: str,
        begin: int = 0,
        size: int = 10,
        keyword: str = "",
    ) -> list[WeChatArticle]:
        """获取公众号文章列表"""
        try:
            r = self.session.get(
                f"{self.base_url}/api/public/v1/article",
                params={
                    "fakeid": fakeid,
                    "begin": begin,
                    "size": size,
                    "keyword": keyword,
                },
                timeout=30,
            )
            data = r.json()
        except Exception as e:
            print(f"[list_articles] 请求失败: {e}")
            return []

        if data.get("base_resp", {}).get("ret") != 0:
            err = data.get("base_resp", {}).get("err_msg", "未知错误")
            print(f"[list_articles] 服务端错误: {err}")
            return []

        articles = []
        for item in data.get("articles", []):
            try:
                articles.append(WeChatArticle(
                    aid=str(item.get("aid", "")),
                    title=item.get("title", ""),
                    author=item.get("author", "") or item.get("nickname", ""),
                    publish_time=int(item.get("create_time", 0) or item.get("update_time", 0)),
                    digest=item.get("digest", ""),
                    content_url=item.get("link", ""),
                    cover_url=item.get("cover", "") or item.get("cdn_url", ""),
                ))
            except Exception as e:
                print(f"[list_articles] 解析文章失败: {e}")
                continue
        return articles

    # ----- 复合：拉取一个公众号的最新文章 -----
    def fetch_recent(
        self,
        account: WeChatAccount | str,
        size: int = 20,
        days: int = 7,
    ) -> list[WeChatArticle]:
        """拉取一个公众号最近 N 天的文章"""
        if isinstance(account, str):
            # 只给了 fakeid，先查
            acc = WeChatAccount(fakeid=account, nickname=account)
        else:
            acc = account

        articles = self.list_articles(acc.fakeid, begin=0, size=size)
        # 过滤最近 N 天
        cutoff = time.time() - days * 86400
        return [a for a in articles if a.publish_time >= cutoff]

    # ----- 信号摘要生成 -----
    def generate_signal_report(
        self,
        articles_by_account: dict[str, list[WeChatArticle]],
        output_path: Optional[Path] = None,
    ) -> str:
        """生成每日信号摘要报告 (Markdown)"""
        today = datetime.now().strftime("%Y-%m-%d")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        lines = [
            f"# 公众号信号摘要 — {today}",
            f"_生成时间：{now_str} | 来源：wechat-article-exporter_",
            "",
            f"> **覆盖公众号数**：{len(articles_by_account)}",
            f"> **总文章数**：{sum(len(v) for v in articles_by_account.values())}",
            "",
            "---",
            "",
        ]

        # 按公众号分类
        for account_name, articles in articles_by_account.items():
            if not articles:
                continue
            lines.append(f"## {account_name}（{len(articles)} 篇）")
            lines.append("")
            for art in articles:
                age = f"{art.signal_age_hours:.1f}h 前" if art.signal_age_hours < 48 \
                    else f"{art.signal_age_hours/24:.1f}d 前"
                lines.append(f"### [{art.title}]({art.content_url})")
                lines.append(f"- **作者**：{art.author}")
                lines.append(f"- **时间**：{art.publish_datetime.strftime('%Y-%m-%d %H:%M')} ({age})")
                if art.digest:
                    lines.append(f"- **摘要**：{art.digest[:150]}")
                if art.read_num is not None:
                    lines.append(f"- **阅读**：{art.read_num} | 点赞：{art.like_num} | 评论：{art.comment_num}")
                lines.append("")

        report = "\n".join(lines)

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(report, encoding="utf-8")
            print(f"报告已写入: {output_path}")

        return report


# ============================================================
# CLI
# ============================================================


def cli_search(keyword: str, base_url: str = "public"):
    """CLI: 搜索公众号"""
    print(f"[SEARCH] 搜索公众号: {keyword}")
    adapter = WeChatArticleAdapter(base_url=base_url)
    health = adapter.health()
    print(f"[HEALTH] 服务状态: {health}")

    accounts = adapter.search_account(keyword, size=10)
    if not accounts:
        print("[FAIL] 未找到公众号或需要登录")
        return

    print(f"[OK] 找到 {len(accounts)} 个公众号:")
    for i, acc in enumerate(accounts, 1):
        print(f"  {i}. {acc.nickname} (fakeid: {acc.fakeid})")
        if acc.signature:
            print(f"     简介: {acc.signature[:80]}")


def cli_articles(fakeid: str, size: int = 10, base_url: str = "public"):
    """CLI: 获取公众号文章列表"""
    print(f"[LIST] 获取公众号文章: {fakeid}")
    adapter = WeChatArticleAdapter(base_url=base_url)
    articles = adapter.list_articles(fakeid, size=size)
    if not articles:
        print("[FAIL] 未获取到文章或需要登录")
        return

    print(f"[OK] 获取 {len(articles)} 篇文章:")
    for i, art in enumerate(articles, 1):
        age_h = art.signal_age_hours
        age_str = f"{age_h:.1f}h 前" if age_h < 48 else f"{age_h/24:.1f}d 前"
        print(f"  {i}. [{age_str}] {art.title}")
        if art.digest:
            print(f"     {art.digest[:100]}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法:")
        print("  python wechat_article_adapter.py search <关键词>")
        print("  python wechat_article_adapter.py articles <fakeid> [size]")
        print("  python wechat_article_adapter.py health")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "search" and len(sys.argv) >= 3:
        cli_search(sys.argv[2])
    elif cmd == "articles" and len(sys.argv) >= 3:
        size = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        cli_articles(sys.argv[2], size=size)
    elif cmd == "health":
        adapter = WeChatArticleAdapter()
        print(adapter.health())
    else:
        print(f"❌ 未知命令: {cmd}")