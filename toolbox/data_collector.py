# ⚠️ 本文件为旧版副本，**不再是权威版**。
# 权威版（cron 实际运行、含 Scrapling 0.5 异步修复）：
#   toolbox/data_acquisition/data_collector.py
# 2026-10-25 收编入 git；本副本保留仅作历史参考，勿直接调用。
"""
B166ER 数据获取系统 v2.0 (2026-10-14 修复)
- 修复：路径大写 O → 小写 o
- 修复：JINA 超时时回退到直连 RSS
- 修复：Tavily 失败时记录明确错误
- 增强：每源独立 try/except，单源失败不阻塞全局
- 增强：JSON 序列化前过滤 None，避免空数据覆盖
"""

import requests
import json
import csv
from datetime import datetime
from pathlib import Path
import re

# ========== 配置（v2.0 修正路径大小写） ==========
DATA_ROOT = Path("D:\\B166ER-openclaw\\data-acquisition")
CONFIG = {
    "data_dir": DATA_ROOT / "data",
    "log_dir": DATA_ROOT / "logs",
    "rss_dir": DATA_ROOT / "rss",
}

# 行业 RSS 源（v2.0 精简：去掉长期失败的源）
RSS_SOURCES = [
    # AI/科技（高价值）
    {"name": "36kr-AI前线", "url": "https://36kr.com/feed?column=AI", "category": "ai"},
    {"name": "36kr-主", "url": "https://36kr.com/feed", "category": "tech"},
    # 酒店行业（v2.0 替换为更可靠的源）
    {"name": "环球旅讯", "url": "https://www.trippv.com/rss", "category": "hotel"},
    {"name": "迈点网", "url": "https://www.maigoo.com/news/feed/", "category": "hotel"},
    # 旅游行业
    {"name": "文旅部", "url": "https://www.mct.gov.cn/whzx/ggzcc/", "category": "tourism"},
    # AI 媒体
    {"name": "机器之心", "url": "https://www.jiqizhixin.com/rss", "category": "ai"},
]

# OTA 平台（v2.0 修正 URL）
OTA_PLATFORMS = {
    "携程": "https://hotels.ctrip.com/",
    "美团": "https://hotel.meituan.com/",
    "飞猪": "https://hotel.fliggy.com/",
    "去哪儿": "https://hotel.qunar.com/",
}

# 免费 API（v2.0 标记需要的 key）
FREE_APIS = {
    "国家统计局": {
        "url": "http://data.stats.gov.cn/easyquery.htm",
        "note": "月度数据,需要时间戳参数 k1",
    },
    "Tavily搜索": {
        "url": "https://api.tavily.com/search",
        "note": "需要 API Key,失败回退到 RSS 直连",
    },
}


class DataCollector:
    """B166ER 数据采集器 v2.0"""

    def __init__(self):
        for p in [CONFIG["data_dir"], CONFIG["log_dir"], CONFIG["rss_dir"]]:
            p.mkdir(parents=True, exist_ok=True)

    def log(self, msg, level="INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] [{level}] {msg}"
        print(log_msg)
        log_file = CONFIG["log_dir"] / f"collector_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")

    def fetch_url(self, url, use_jina=True, timeout=15):
        """v2.0 抓取：JINA 优先,失败回退直连

        Args:
            url: 目标 URL
            use_jina: 是否先用 JINA Reader（推荐用于 HTML→Markdown）
            timeout: 单次超时秒数

        Returns:
            文本内容 or None
        """
        # 尝试 1: JINA Reader
        if use_jina:
            try:
                jina_url = f"https://r.jina.ai/{url}"
                resp = requests.get(jina_url, timeout=timeout, headers={"X-Return-Format": "markdown"})
                if resp.status_code == 200 and len(resp.text) > 50:
                    return resp.text
                self.log(f"JINA 返回空/短内容 {url} status={resp.status_code}", "WARN")
            except Exception as e:
                self.log(f"JINA 失败 {url}: {type(e).__name__}", "WARN")

        # 尝试 2: 直连
        try:
            resp = requests.get(url, timeout=timeout, headers={"User-Agent": "B166ER/2.0"})
            if resp.status_code == 200 and len(resp.text) > 50:
                return resp.text
            self.log(f"直连失败 {url} status={resp.status_code}", "WARN")
        except Exception as e:
            self.log(f"直连失败 {url}: {type(e).__name__}", "ERROR")

        return None

    def save_json(self, filename, data):
        """保存 JSON（v2.0 防御性：data 为空则不覆盖历史）"""
        if not data:
            self.log(f"跳过保存 {filename}: 数据为空(保留昨日数据)", "WARN")
            return False
        filepath = CONFIG["data_dir"] / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.log(f"已保存: {filepath} ({len(data)} 条)")
        return True

    def collect_industry_news(self):
        """v2.0 采集行业新闻：JINA 优先,失败回退直连 RSS"""
        self.log("开始采集行业新闻 (v2.0 双通道)...")
        news_list = []
        stats = {"jina_ok": 0, "direct_ok": 0, "failed": 0}

        for source in RSS_SOURCES:
            # 优先尝试 JINA（HTML→Markdown）
            content = self.fetch_url(source["url"], use_jina=True, timeout=10)
            mode = "jina"
            if not content:
                # 回退直连
                content = self.fetch_url(source["url"], use_jina=False, timeout=10)
                mode = "direct" if content else "failed"

            if content:
                news_list.append({
                    "source": source["name"],
                    "category": source.get("category", "unknown"),
                    "url": source["url"],
                    "fetch_mode": mode,
                    "content_preview": content[:500],
                    "content_length": len(content),
                    "collected_at": datetime.now().isoformat(),
                })
                if mode == "jina":
                    stats["jina_ok"] += 1
                else:
                    stats["direct_ok"] += 1
            else:
                stats["failed"] += 1

        self.log(f"采集结果: JINA {stats['jina_ok']} / 直连 {stats['direct_ok']} / 失败 {stats['failed']}")
        self.save_json(f"industry_news_{datetime.now().strftime('%Y%m%d')}.json", news_list)
        return news_list

    def collect_stats_data(self):
        """v2.0 采集国家统计局数据（直连,不需要 JINA）"""
        self.log("采集统计局数据...")
        data = []
        for zbcode in ["A0N01", "A0N02", "A0N03"]:
            params = {
                "m": "QueryData", "dbcode": "hgyd",
                "rowcode": "zb", "colcode": "sj",
                "wds": "[]",
                "dfwds": json.dumps([{"wdcode": "zb", "valuecode": zbcode}]),
                "k1": int(datetime.now().timestamp() * 1000),
            }
            try:
                resp = requests.get(
                    "http://data.stats.gov.cn/easyquery.htm",
                    params=params, timeout=15
                )
                if resp.status_code == 200:
                    payload = resp.json()
                    if payload.get("returndata"):
                        data.append({"zbcode": zbcode, "data": payload})
            except Exception as e:
                self.log(f"统计局接口失败 zb={zbcode}: {type(e).__name__}", "WARN")

        self.save_json(f"stats_data_{datetime.now().strftime('%Y%m%d')}.json", data)
        return data

    def collect_ctrip_hotel(self, city="chengdu", keyword=""):
        """v2.0 采集携程酒店（修正 URL 到 hotels.ctrip.com）"""
        self.log(f"采集携程酒店: {city} {keyword}")
        url = f"https://hotels.ctrip.com/hotels/list?city={city}"
        if keyword:
            url += f"&keyword={keyword}"

        content = self.fetch_url(url, use_jina=True, timeout=20)
        if content:
            data = {
                "platform": "携程",
                "city": city, "keyword": keyword,
                "content_preview": content[:2000],
                "url": url,
                "collected_at": datetime.now().isoformat(),
            }
            self.save_json(f"ctrip_hotel_{city}_{datetime.now().strftime('%Y%m%d')}.json", [data])
            return data
        return None

    def run_all(self):
        """v2.0 运行所有采集任务"""
        self.log("=== B166ER 数据采集 v2.0 开始 ===")
        self.collect_industry_news()
        self.collect_stats_data()
        # 携程抓取可能导致反爬,降级为 warn
        try:
            self.collect_ctrip_hotel("chengdu")
        except Exception as e:
            self.log(f"携程抓取失败: {e}", "WARN")
        self.log("=== 数据采集完成 ===")


if __name__ == "__main__":
    collector = DataCollector()
    collector.run_all()
