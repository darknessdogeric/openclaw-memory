# AHL 乐山锦江嘉州宾馆 OTA数据采集技术方案 V1.0

> **版本**: V1.0
> **日期**: 2026-03-27
> **试点酒店**: 四川乐山锦江嘉州宾馆
> **模块**: 模块2（技术深化任务）
> **状态**: 基于行业知识的技术方案，待实地调研验证

---

## 文档目的

本方案解决核心问题：**AHL数字员工如何获取OTA平台的运营数据（产量/价格/点评），作为收益管理的数据基础？**

核心原则：**现实主义——不依赖"等API批下来"，必须给保底方案。最快5分钟的EBK导入手工方案优先。**

---

## 一、OTA数据获取原理

### 1.1 为什么OTA数据是收益管理的基础

收益管理的本质是**"在对的时机，把对的产品，用对的价格，卖给对的人"**。

要做到这一点，必须回答三个问题：
1. **自己卖得怎么样？** → PMS数据（ADR/OCC/RevPAR）
2. **对手卖得怎么样？** → 竞品价格监控
3. **客人怎么看我们？** → OTA点评数据

OTA平台（携程/美团/飞猪）是酒店最大的流量入口，也是数据最丰富的来源。但OTA平台的数据，酒店**本来就有权获取**，只是大多数酒店不知道在哪里。

---

### 1.2 携程数据生态解析

携程对酒店提供的数据工具分为三层：

| 层级 | 工具 | 数据内容 | 获取难度 | 推荐度 |
|------|------|---------|---------|-------|
| **L1** | EBK后台（酒店自主操作） | ADR/OCC/RevPAR/点评/产量 | ⭐ 无门槛 | **⭐⭐⭐⭐⭐** |
| **L2** | 携程开放平台（Trip.com API） | 全量业务数据+实时房态 | ⭐⭐⭐⭐（需申请） | ⭐⭐⭐ |
| **L3** | 爬虫技术 | 竞品价格/房价日历 | ⭐⭐⭐（反爬风险） | ⭐⭐ |

**为什么EBK是第一选择？**
- 酒店开通EBK数据权限，**不需要AHL介入申请**
- 酒店前台或销售自己在携程后台操作，**5分钟搞定**
- 数据包括：自己酒店的ADR/OCC/RevPAR、竞品产量、点评分数
- 携程EBK数据**比爬虫更权威**，因为是平台官方统计

---

### 1.3 美团数据生态解析

美团对酒店的数据工具分两层：

| 层级 | 工具 | 数据内容 | 获取难度 |
|------|------|---------|---------|
| **L1** | 美团酒店商家后台 | 产量/ADR/OCC/排名/点评 | ⭐ 无门槛 |
| **L2** | 美团开放平台 | 全量数据+实时房态 | ⭐⭐⭐（需申请） |

**美团EBK类似工具**：`美团旅行商家版` APP或`美团酒店商家后台`网页版

---

## 二、携程EBK数据导出SOP（酒店方操作，5分钟搞定）

### 2.1 什么是EBK

EBK = **E-Booking Key**，携程酒店后台数据导出工具。酒店开通后，可自主导出：
- 每日产量数据（ADR/OCC/RevPAR）
- 竞品对比数据（周边同档次酒店产量）
- 点评数据（分数/内容/回复）
- 流量数据（曝光/浏览/转化）

### 2.2 开通EBK操作步骤（酒店方自行操作）

```
预计耗时：5分钟
操作人：酒店前台经理或销售经理
权限要求：携程后台管理员账号
```

**Step 1：登录携程酒店后台**

浏览器打开：`https://hotels.ctrip.com/hotel/${hotelId}`

或直接搜索"携程酒店后台登录"

**Step 2：找到数据导出入口**

路径：`数据中心 → 产量数据 → 导出`

不同酒店后台版本路径略有差异，常见路径：
- `收益管理 → 数据报表 → 产量导出`
- `我的携程 → 数据中心 → EBK数据`

**Step 3：选择日期范围导出**

- 导出台北向：选择"自定义日期"（通常导出近30天）
- 文件格式：`Excel` 或 `CSV`（推荐Excel，避免编码问题）
- 字段选择：建议全选，确保包含ADR/OCC/RevPAR

**Step 4：确认导出的字段**

标准EBK导出应包含以下字段：

| 字段 | 说明 | 对应AHL字段 |
|------|------|------------|
| 日期 | 统计日期 | `date` |
| 酒店名称 | 酒店名称 | `hotel_name` |
| 在住房数 | 当日在住房量 | `occupied` |
| 离店房数 | 当日离店房量 | `departures` |
| 入住房数 | 当日新入住 | `arrivals` |
| 总房量 | 可售房总量 | `total_rooms` |
| 入住率 | OCC% | `occupancy_pct` |
| ADR | 平均房价 | `adr` |
| RevPAR | 每房收益 | `revpar` |
| 客房收入 | 当日客房收入 | `room_revenue` |
| 订单量 | 订单数 | `order_count` |
| 净房间数 | 净间夜 | `room_nights` |

**Step 5：保存文件**

文件名格式：`携程产量数据_YYYYMMDD_YYYYMMDD.xlsx`

保存路径：固定共享文件夹（如`D:\酒店数据\OTA\`）

### 2.3 EBK导出操作截图示意

> ⚠️ 具体界面以携程实际后台为准，以下为示意

```
┌─────────────────────────────────────────────────────────┐
│  携程酒店后台 - 数据中心                                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  📊 产量数据                                              │
│    ├── 今日实时 ▸                                        │
│    ├── 每日明细 ▸  ← 【在这里导出】                        │
│    ├── 竞品对比 ▸                                        │
│    └── 历史数据 ▸                                        │
│                                                          │
│  选择日期范围：[2026-03-01] ~ [2026-03-26]               │
│  数据粒度：☐ 按日  ☑ 按月                                │
│  导出格式：☑ Excel  ☐ CSV                               │
│                                                          │
│  [立即导出]  [定时任务]                                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 2.4 竞品对比数据导出

在携程EBK中，竞品对比数据是**最有价值的数据之一**：

- 位置：`数据中心 → 竞品对比`
- 数据：周边竞品的ADR/OCC/RevPAR（携程根据OTA产量估算）
- 用途：计算STR指数（MPI/ARI/RGI）

**导出步骤**：
1. 进入`竞品对比`
2. 选择对比维度：`产量/价格/点评`
3. 选择竞品酒店（可多选）
4. 选择日期范围
5. 导出Excel

---

## 三、竞品价格爬虫技术方案

### 3.1 爬虫原理与酒店行业适配

**为什么竞品价格需要爬虫？**

EBK提供的是**自己酒店的数据**，但竞品的价格实时变化，携程EBK的竞品数据有1-2天延迟。要做到**实时价格监控**，必须依赖爬虫。

**技术原理**：

爬虫模拟真人访问携程/美团的竞品酒店页面，抓取房价日历数据。流程：
```
1. 伪装User-Agent（让网站以为是真实浏览器）
2. 访问竞品酒店页面
3. 解析页面HTML，提取房价信息
4. 清洗数据，存储到数据库
5. 间隔一段时间后重复（定时任务）
```

**法律与合规边界**：
- 爬取**公开显示的价格信息**是合法的（不是个人隐私）
- 禁止绕过网站的反爬措施（如验证码破解、IP封禁规避）
- 竞品价格是公开信息，酒店行业常用
- **建议**：仅用于自家收益分析，不对外传播

---

### 3.2 携程竞品价格爬虫（requests版）

```python
#!/usr/bin/env python3
"""
携程竞品价格爬虫
AHL乐山锦江嘉州宾馆专用

功能：定时抓取携程上竞品酒店的房价日历数据
原理：requests + BeautifulSoup，轻量可控
依赖：requests, beautifulsoup4, lxml

作者：AHL技术组
版本：v1.0
"""

import requests
import pandas as pd
import time
import random
import logging
import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path
from bs4 import BeautifulSoup

# ============================================================
# 配置区
# ============================================================

CONFIG = {
    # 爬虫基础配置
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    ],
    
    # 请求配置
    "request_timeout": 15,           # 请求超时（秒）
    "min_interval": 8,                # 最小请求间隔（秒）
    "max_interval": 20,               # 最大请求间隔（秒）
    "max_retries": 3,                 # 最大重试次数
    
    # 反爬降级配置
    "auto_downgrade": True,           # 被封后自动降级
    "ban_threshold": 5,               # 连续失败次数阈值
    
    # 数据配置
    "data_dir": "./data/competitor/ctrip",
    "log_dir": "./logs/competitor",
    
    # 竞品配置（乐山主要竞品酒店）
    # ⚠️ 以下URL需实地确认，以下为示例格式
    "competitors": [
        {
            "hotel_id": "hotel_leshan_001",
            "name": "全季酒店(乐山大佛店)",
            "ctrip_url": "https://hotels.ctrip.com/hotel/leshan lvyouqu_taizhanlu/",
            "room_type": "商务大床房",
            "star_level": 4,
        },
        {
            "hotel_id": "hotel_leshan_002",
            "name": "麗枫酒店(乐山高铁站店)",
            "ctrip_url": "https://hotels.ctrip.com/hotel/leshan gaotie/",
            "room_type": "舒适大床房",
            "star_level": 3,
        },
        {
            "hotel_id": "hotel_leshan_003",
            "name": "和颐酒店(乐山店)",
            "ctrip_url": "https://hotels.ctrip.com/hotel/leshan/",
            "room_type": "商务大床房",
            "star_level": 4,
        },
        {
            "hotel_id": "hotel_leshan_004",
            "name": "亚朵酒店(乐山大佛店)",
            "ctrip_url": "https://hotels.ctrip.com/hotel/leshan/",
            "room_type": "高级大床房",
            "star_level": 4,
        },
        {
            "hotel_id": "hotel_leshan_005",
            "name": "禅驿酒店(乐山大佛店)",
            "ctrip_url": "https://hotels.ctrip.com/hotel/leshan/",
            "room_type": "禅意大床房",
            "star_level": 4,
        },
    ],
}

# ============================================================
# 日志配置
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(
            f"{CONFIG['log_dir']}/ctrip_crawl_{datetime.now().strftime('%Y%m%d')}.log",
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# 工具函数
# ============================================================

def get_random_ua() -> str:
    """随机获取User-Agent"""
    return random.choice(CONFIG["user_agents"])


def get_random_delay():
    """随机延迟，模拟真人操作"""
    delay = random.uniform(CONFIG["min_interval"], CONFIG["max_interval"])
    logger.debug(f"延迟 {delay:.1f} 秒")
    time.sleep(delay)


def get_page_headers() -> Dict:
    """生成请求头"""
    return {
        "User-Agent": get_random_ua(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
    }


def request_with_retry(url: str, method: str = "GET") -> Optional[str]:
    """
    带重试的HTTP请求
    
    原理：被封后自动降级，使用代理或增加延迟
    """
    for attempt in range(CONFIG["max_retries"]):
        try:
            get_random_delay()  # 每次请求前随机延迟
            
            response = requests.get(
                url,
                headers=get_page_headers(),
                timeout=CONFIG["request_timeout"],
                allow_redirects=True,
            )
            
            # 检查响应状态
            if response.status_code == 200:
                # 验证页面内容（携程被封时常返回验证码页）
                content = response.text
                if "验证" in content or "访问异常" in content or "captcha" in content.lower():
                    logger.warning(f"检测到验证码页面（第{attempt+1}次）")
                    if attempt < CONFIG["max_retries"] - 1:
                        time.sleep(30)  # 等待30秒后再试
                        continue
                    else:
                        logger.error("验证码无法绕过，降级到备选方案")
                        return None
                return content
                
            elif response.status_code == 403:
                logger.warning(f"请求被拒绝（403），IP可能被封（第{attempt+1}次）")
                if attempt < CONFIG["max_retries"] - 1:
                    time.sleep(60)  # 等待1分钟后再试
                    continue
                else:
                    logger.error("IP被封，停止当前批次")
                    return None
                    
            else:
                logger.warning(f"HTTP {response.status_code}（第{attempt+1}次）")
                if attempt < CONFIG["max_retries"] - 1:
                    time.sleep(10)
                    continue
                    
        except requests.exceptions.RequestException as e:
            logger.warning(f"请求异常（第{attempt+1}次）: {e}")
            if attempt < CONFIG["max_retries"] - 1:
                time.sleep(10)
                continue
    
    return None


# ============================================================
# 携程页面解析函数
# ============================================================

def parse_ctrip_price_page(html: str, hotel_id: str, check_date: str) -> List[Dict]:
    """
    解析携程酒店房价日历页面
    
    原理：携程房价日历通常在页面JavaScript中以JSON格式存储
    解析策略：正则匹配 + BeautifulSoup备用
    
    参数:
        html: 页面HTML内容
        hotel_id: 酒店ID
        check_date: 查询日期（YYYY-MM-DD）
    
    返回:
        List[Dict]: 价格数据列表
    """
    results = []
    soup = BeautifulSoup(html, "lxml")
    
    # 策略1：查找JSON数据（携程常将房价数据内嵌在script标签中）
    import re
    
    # 查找 window.__BIZ_DATA__ 或类似全局变量
    biz_data_pattern = r'window\.__.*?=\s*(\{.*?\});'
    biz_matches = re.findall(biz_data_pattern, html, re.DOTALL)
    
    for match in biz_matches:
        try:
            data = json.loads(match)
            # 在数据中查找房价信息
            prices = extract_prices_from_json(data, hotel_id, check_date)
            if prices:
                results.extend(prices)
        except (json.JSONDecodeError, Exception) as e:
            logger.debug(f"JSON解析失败: {e}")
    
    # 策略2：直接查找房价元素（携程新版页面）
    price_elements = soup.select(".hotel_item_price, .price_item, [data-price]")
    
    for elem in price_elements:
        try:
            price_text = elem.get_text(strip=True)
            # 提取数字
            price_match = re.search(r'(\d+)', price_text)
            if price_match:
                price = float(price_match.group(1))
                
                # 查找日期信息
                date_elem = elem.select_one(".date, .price_date, [data-date]")
                date_str = date_elem.get("data-date", check_date) if date_elem else check_date
                
                results.append({
                    "hotel_id": hotel_id,
                    "date": date_str,
                    "price": price,
                    "room_type": elem.get("data-room-type", ""),
                    "source": "ctrip",
                    "crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })
        except Exception as e:
            logger.debug(f"房价元素解析失败: {e}")
    
    # 策略3（降级）：如果以上都失败，尝试页面文本匹配
    if not results:
        logger.info(f"尝试降级解析策略...")
        price_pattern = r'(\d{3,5})元'
        price_matches = re.findall(price_pattern, html)
        
        for idx, price_str in enumerate(price_matches[:7]):  # 限制取前7个价格
            results.append({
                "hotel_id": hotel_id,
                "date": check_date,
                "price": float(price_str),
                "room_type": f"房型{idx+1}",
                "source": "ctrip_fallback",
                "crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })
    
    return results


def extract_prices_from_json(data: Dict, hotel_id: str, check_date: str) -> List[Dict]:
    """从JSON数据中提取房价"""
    results = []
    
    def recursive_search(obj):
        if isinstance(obj, dict):
            # 查找价格相关字段
            for key in ["price", "priceInfo", "roomPrice", "ratePlan"]:
                if key in obj and isinstance(obj[key], (int, float)):
                    results.append({
                        "hotel_id": hotel_id,
                        "date": check_date,
                        "price": float(obj[key]),
                        "room_type": obj.get("roomType", ""),
                        "source": "ctrip_json",
                        "crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })
            # 递归查找
            for value in obj.values():
                recursive_search(value)
        elif isinstance(obj, list):
            for item in obj:
                recursive_search(item)
    
    recursive_search(data)
    return results


# ============================================================
# 携程酒店搜索（用于发现竞品酒店URL）
# ============================================================

def search_ctrip_hotel(hotel_name: str) -> Optional[str]:
    """
    搜索携程酒店并返回酒店页面URL
    
    参数:
        hotel_name: 酒店名称
    
    返回:
        str: 酒店页面URL，或None
    """
    search_url = f"https://hotels.ctrip.com/hotel/leshan/"
    params = {"kw": hotel_name}
    
    try:
        response = requests.get(
            search_url,
            params=params,
            headers=get_page_headers(),
            timeout=CONFIG["request_timeout"],
        )
        
        if response.status_code == 200:
            # 解析搜索结果，提取第一个酒店链接
            soup = BeautifulSoup(response.text, "lxml")
            first_result = soup.select_one(".hotel_item a, .result a, a[href*='/hotel/']")
            
            if first_result:
                href = first_result.get("href", "")
                if href.startswith("/"):
                    return f"https://hotels.ctrip.com{href}"
                return href
                
    except Exception as e:
        logger.warning(f"搜索失败: {e}")
    
    return None


# ============================================================
# 房价日历抓取（针对特定日期范围）
# ============================================================

def crawl_hotel_price_calendar(hotel_id: str, hotel_url: str, 
                                start_date: str, end_date: str,
                                room_type: str = "") -> pd.DataFrame:
    """
    抓取酒店房价日历（多日）
    
    参数:
        hotel_id: 酒店ID
        hotel_url: 携程酒店页面URL
        start_date: 开始日期（YYYY-MM-DD）
        end_date: 结束日期（YYYY-MM-DD）
        room_type: 房型名称（可选）
    
    返回:
        DataFrame: 每日房价数据
    """
    logger.info(f"开始抓取 {hotel_id} 房价日历: {start_date} ~ {end_date}")
    
    all_prices = []
    
    # 解析日期范围
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    current = start
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        
        # 携程房价日历URL格式（通常带日期参数）
        # 实际URL格式需通过浏览器开发者工具查看
        calendar_url = f"{hotel_url}?checkIn={date_str}&checkOut={(current + timedelta(days=1)).strftime('%Y-%m-%d')}"
        
        html = request_with_retry(calendar_url)
        
        if html:
            prices = parse_ctrip_price_page(html, hotel_id, date_str)
            all_prices.extend(prices)
            logger.info(f"  {date_str}: 获取到{len(prices)}条价格数据")
        else:
            logger.warning(f"  {date_str}: 获取失败")
        
        current += timedelta(days=1)
    
    if all_prices:
        df = pd.DataFrame(all_prices)
        df["hotel_url"] = hotel_url
        return df
    
    return pd.DataFrame()


# ============================================================
# 数据存储
# ============================================================

def save_prices_to_csv(df: pd.DataFrame, hotel_id: str):
    """保存价格数据到CSV"""
    if df.empty:
        return
    
    Path(CONFIG["data_dir"]).mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y%m%d")
    filepath = Path(CONFIG["data_dir"]) / f"{hotel_id}_{today}.csv"
    
    # 追加模式（如果文件存在则合并）
    if filepath.exists():
        existing = pd.read_csv(filepath)
        df = pd.concat([existing, df], ignore_index=True)
        # 去重（同一酒店+同一日期+同一价格）
        df = df.drop_duplicates(subset=["hotel_id", "date", "price", "room_type"])
    
    df.to_csv(filepath, index=False, encoding="utf-8-sig")
    logger.info(f"数据已保存: {filepath} ({len(df)}条)")


def save_prices_to_sqlite(df: pd.DataFrame, db_path: str = "./data/competitor.db"):
    """
    保存价格数据到SQLite数据库
    
    SQLite优势：
    - 无需安装，文件级数据库
    - 支持SQL查询
    - 备份简单（复制文件即可）
    """
    import sqlite3
    
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    
    df.to_sql(
        name="competitor_prices",
        con=conn,
        if_exists="append",
        index=False,
    )
    
    conn.close()
    logger.info(f"数据已保存到SQLite: {db_path}")


# ============================================================
# 主执行函数
# ============================================================

def main():
    """
    主执行函数：抓取所有竞品酒店价格
    
    建议执行频率：
    - 工作日：每日2次（早9点、晚6点）
    - 周末/节假日：每日4次（早8点、11点、14点、18点）
    """
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    logger.info(f"========== 携程竞品价格抓取开始 ==========")
    logger.info(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 统计
    success_count = 0
    fail_count = 0
    
    for competitor in CONFIG["competitors"]:
        hotel_id = competitor["hotel_id"]
        hotel_name = competitor["name"]
        hotel_url = competitor["ctrip_url"]
        
        logger.info(f"抓取中: {hotel_name}")
        
        try:
            # 抓取未来7天的房价
            df = crawl_hotel_price_calendar(
                hotel_id=hotel_id,
                hotel_url=hotel_url,
                start_date=today,
                end_date=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                room_type=competitor.get("room_type", ""),
            )
            
            if not df.empty:
                # 同时保存CSV和SQLite
                save_prices_to_csv(df, hotel_id)
                save_prices_to_sqlite(df)
                success_count += 1
            else:
                logger.warning(f"未获取到 {hotel_name} 的价格数据")
                fail_count += 1
                
        except Exception as e:
            logger.error(f"抓取失败 {hotel_name}: {e}")
            fail_count += 1
    
    logger.info(f"========== 携程竞品价格抓取完成 ==========")
    logger.info(f"成功: {success_count}/{len(CONFIG['competitors'])}")
    logger.info(f"失败: {fail_count}/{len(CONFIG['competitors'])}")


if __name__ == "__main__":
    main()
```

**使用说明**：

```bash
# 安装依赖
pip install requests beautifulsoup4 lxml pandas

# 执行抓取
python ctrip_competitor_crawler.py

# 配置定时任务（建议早9点、晚6点各执行一次）
# Windows
schtasks /create /tn "AHL_CtripCrawler" /tr "python ctrip_competitor_crawler.py" /sc daily /st 09:00

# Linux
# 0 9,18 * * * /usr/bin/python3 /path/to/ctrip_competitor_crawler.py
```

---

### 3.3 美团竞品价格爬虫（requests版）

```python
#!/usr/bin/env python3
"""
美团竞品价格爬虫
AHL乐山锦江嘉州宾馆专用

功能：定时抓取美团上竞品酒店的房价日历数据
原理：requests + BeautifulSoup
依赖：requests, beautifulsoup4, lxml

作者：AHL技术组
版本：v1.0
"""

import requests
import pandas as pd
import time
import random
import logging
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path
from bs4 import BeautifulSoup

# ============================================================
# 配置区
# ============================================================

CONFIG = {
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    ],
    
    "request_timeout": 15,
    "min_interval": 10,
    "max_interval": 25,
    "max_retries": 3,
    
    "data_dir": "./data/competitor/meituan",
    "log_dir": "./logs/competitor",
    
    # 竞品配置
    "competitors": [
        {
            "hotel_id": "mt_leshan_001",
            "name": "全季酒店(乐山大佛店)",
            "meituan_url": "https://ihotel.meituan.com/hotel/detail/?hotelId=12345678",
            "room_type": "商务大床房",
        },
        {
            "hotel_id": "mt_leshan_002",
            "name": "麗枫酒店(乐山高铁站店)",
            "meituan_url": "https://ihotel.meituan.com/hotel/detail/?hotelId=87654321",
            "room_type": "舒适大床房",
        },
    ],
}

# ============================================================
# 日志配置
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(
            f"{CONFIG['log_dir']}/meituan_crawl_{datetime.now().strftime('%Y%m%d')}.log",
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def get_random_ua() -> str:
    return random.choice(CONFIG["user_agents"])


def get_random_delay():
    delay = random.uniform(CONFIG["min_interval"], CONFIG["max_interval"])
    time.sleep(delay)


def get_page_headers() -> Dict:
    return {
        "User-Agent": get_random_ua(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://www.meituan.com/",
    }


def request_with_retry(url: str) -> Optional[str]:
    """带重试的HTTP请求"""
    for attempt in range(CONFIG["max_retries"]):
        try:
            get_random_delay()
            
            response = requests.get(
                url,
                headers=get_page_headers(),
                timeout=CONFIG["request_timeout"],
            )
            
            if response.status_code == 200:
                content = response.text
                if "验证" in content or "访问异常" in content:
                    logger.warning(f"检测到风控（第{attempt+1}次）")
                    time.sleep(30)
                    continue
                return content
            else:
                logger.warning(f"HTTP {response.status_code}（第{attempt+1}次）")
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"请求异常（第{attempt+1}次）: {e}")
    
    return None


def parse_meituan_price_page(html: str, hotel_id: str, check_date: str) -> List[Dict]:
    """
    解析美团酒店房价日历页面
    
    美团页面结构与携程不同，价格数据通常在React/Vue组件中
    降级策略：直接匹配页面中的价格数字
    """
    results = []
    soup = BeautifulSoup(html, "lxml")
    
    # 策略1：查找美团价格元素
    price_elements = soup.select(
        ".price-wrapper, .room-price, .price-info, [data-price], .J_price"
    )
    
    for elem in price_elements:
        try:
            price_text = elem.get_text(strip=True)
            price_match = re.search(r'(\d+)', price_text)
            if price_match:
                results.append({
                    "hotel_id": hotel_id,
                    "date": check_date,
                    "price": float(price_match.group(1)),
                    "room_type": elem.get("data-roomtype", ""),
                    "source": "meituan",
                    "crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })
        except Exception as e:
            logger.debug(f"解析失败: {e}")
    
    # 策略2（降级）：正则全文匹配价格
    if not results:
        price_pattern = r'"price"\s*:\s*(\d+)'
        price_matches = re.findall(price_pattern, html)
        
        for idx, price_str in enumerate(price_matches[:7]):
            results.append({
                "hotel_id": hotel_id,
                "date": check_date,
                "price": float(price_str),
                "room_type": f"房型{idx+1}",
                "source": "meituan_regex",
                "crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })
    
    return results


def crawl_meituan_hotel_price(hotel_id: str, hotel_url: str,
                               start_date: str, end_date: str) -> pd.DataFrame:
    """抓取美团酒店价格日历"""
    logger.info(f"抓取美团 {hotel_id}: {start_date} ~ {end_date}")
    
    all_prices = []
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    current = start
    
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        
        # 美团酒店详情URL
        # 实际URL需通过浏览器开发者工具查看
        detail_url = f"{hotel_url}&ci={date_str}&co={(current + timedelta(days=1)).strftime('%Y%m-%d')}"
        
        html = request_with_retry(detail_url)
        
        if html:
            prices = parse_meituan_price_page(html, hotel_id, date_str)
            all_prices.extend(prices)
        
        current += timedelta(days=1)
    
    return pd.DataFrame(all_prices) if all_prices else pd.DataFrame()


def save_to_csv(df: pd.DataFrame, hotel_id: str):
    """保存到CSV"""
    if df.empty:
        return
    
    Path(CONFIG["data_dir"]).mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    filepath = Path(CONFIG["data_dir"]) / f"{hotel_id}_{today}.csv"
    
    if filepath.exists():
        existing = pd.read_csv(filepath)
        df = pd.concat([existing, df], ignore_index=True)
        df.drop_duplicates(subset=["hotel_id", "date", "price"], keep="last")
    
    df.to_csv(filepath, index=False, encoding="utf-8-sig")


def main():
    """主执行函数"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    logger.info(f"========== 美团竞品价格抓取开始 ==========")
    
    for competitor in CONFIG["competitors"]:
        try:
            df = crawl_meituan_hotel_price(
                hotel_id=competitor["hotel_id"],
                hotel_url=competitor["meituan_url"],
                start_date=today,
                end_date=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            )
            
            if not df.empty:
                save_to_csv(df, competitor["hotel_id"])
                logger.info(f"成功: {competitor['name']} ({len(df)}条)")
                
        except Exception as e:
            logger.error(f"失败: {competitor['name']}: {e}")
    
    logger.info("========== 美团竞品价格抓取完成 ==========")


if __name__ == "__main__":
    main()
```

---

### 3.4 数据清洗与存储

```python
#!/usr/bin/env python3
"""
竞品价格数据清洗与存储
AHL乐山锦江嘉州宾馆专用

功能：
1. 合并携程/美团爬虫数据
2. 清洗异常值（如0元、99999元）
3. 计算日均价格/最低价格
4. 存储到SQLite
"""

import pandas as pd
import sqlite3
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CompetitorPriceCleaner:
    """
    竞品价格数据清洗器
    
    清洗规则：
    1. 去除异常价格（<50元或>5000元）
    2. 去除重复数据
    3. 统一日期格式
    4. 计算统计指标
    """
    
    def __init__(self, db_path: str = "./data/competitor.db"):
        self.db_path = db_path
        self.price_min = 50      # 最低合理价格
        self.price_max = 5000    # 最高合理价格
    
    def clean_price(self, price: float) -> float:
        """清洗单个价格"""
        if pd.isna(price):
            return None
        if price < self.price_min or price > self.price_max:
            return None
        return price
    
    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """清洗DataFrame"""
        if df.empty:
            return df
        
        # 清洗价格
        df["price_cleaned"] = df["price"].apply(self.clean_price)
        
        # 去除清洗后的空值
        df = df.dropna(subset=["price_cleaned"])
        
        # 统一日期格式
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        
        # 添加清洗时间戳
        df["clean_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return df
    
    def calculate_daily_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算竞品每日统计指标
        
        输出字段：
        - avg_price: 日均价格
        - min_price: 最低价格
        - max_price: 最高价格
        - sample_count: 价格样本数
        """
        if df.empty:
            return pd.DataFrame()
        
        stats = df.groupby(["hotel_id", "date"]).agg(
            avg_price=("price_cleaned", "mean"),
            min_price=("price_cleaned", "min"),
            max_price=("price_cleaned", "max"),
            sample_count=("price_cleaned", "count"),
        ).reset_index()
        
        # 保留2位小数
        stats["avg_price"] = stats["avg_price"].round(2)
        
        return stats
    
    def save_to_db(self, df: pd.DataFrame, table_name: str = "competitor_prices"):
        """保存到SQLite"""
        if df.empty:
            return
        
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        
        df.to_sql(
            name=table_name,
            con=conn,
            if_exists="append",
            index=False,
        )
        
        conn.close()
        logger.info(f"已保存{len(df)}条数据到 {self.db_path}")
    
    def get_latest_prices(self, hotel_id: str, days: int = 7) -> pd.DataFrame:
        """获取最新价格数据"""
        conn = sqlite3.connect(self.db_path)
        
        query = f"""
            SELECT * FROM competitor_prices
            WHERE hotel_id = '{hotel_id}'
            AND date >= date('now', '-{days} days')
            ORDER BY date DESC
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df


def main():
    """主执行：清洗所有数据并存储"""
    cleaner = CompetitorPriceCleaner()
    
    data_dir = Path("./data/competitor")
    
    # 遍历所有CSV文件
    for csv_file in data_dir.rglob("*.csv"):
        try:
            df = pd.read_csv(csv_file)
            df_cleaned = cleaner.clean_dataframe(df)
            
            if not df_cleaned.empty:
                cleaner.save_to_db(df_cleaned)
                logger.info(f"已清洗: {csv_file.name}")
                
        except Exception as e:
            logger.error(f"清洗失败 {csv_file}: {e}")
    
    logger.info("========== 数据清洗完成 ==========")


if __name__ == "__main__":
    main()
```

---

## 四、三种数据获取方案对比

### 4.1 携程数据获取方案对比

| 维度 | 方案A：EBK手工导出 | 方案B：Trip.com API | 方案C：爬虫 |
|------|------------------|---------------------|-----------|
| **获取难度** | ⭐ 无门槛 | ⭐⭐⭐⭐ 需申请 | ⭐⭐⭐ 有风险 |
| **所需时间** | 5分钟（酒店方操作） | 2-4周（API申请） | 即刻（但不稳定） |
| **数据完整性** | ⭐⭐⭐⭐ 官方统计 | ⭐⭐⭐⭐⭐ 全量+实时 | ⭐⭐⭐ 可能有缺失 |
| **数据类型** | ADR/OCC/RevPAR/点评/竞品产量 | 全量业务数据+实时 | 竞品实时价格 |
| **成本** | 免费 | 免费（需签约） | 运维成本 |
| **稳定性** | ⭐⭐⭐⭐⭐ 极稳定 | ⭐⭐⭐⭐⭐ 稳定 | ⭐⭐ 容易被封 |
| **频率** | 手动/日频率 | 自动/实时 | 自动/定时 |
| **推荐度** | **⭐⭐⭐⭐⭐ 首选** | ⭐⭐⭐⭐ 进阶 | ⭐⭐⭐ 补充 |

### 4.2 美团数据获取方案对比

| 维度 | 方案A：商家后台导出 | 方案B：美团开放平台 | 方案C：爬虫 |
|------|-------------------|-------------------|-----------|
| **获取难度** | ⭐ 无门槛 | ⭐⭐⭐⭐ 需签约 | ⭐⭐⭐ 有风险 |
| **所需时间** | 5分钟 | 2-4周 | 即刻 |
| **数据完整性** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **成本** | 免费 | 免费 | 运维成本 |
| **稳定性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **推荐度** | **⭐⭐⭐⭐⭐ 首选** | ⭐⭐⭐⭐ 进阶 | ⭐⭐ 补充 |

### 4.3 推荐的数据获取策略

```
Phase 1（立即可执行）：
1. 酒店开通EBK/商家后台导出权限（5分钟）
2. 每日由酒店人员手动导出 → AHL数字员工自动处理
3. 配置竞品爬虫作为补充数据源

Phase 2（API申请通过后）：
1. 切换到Trip.com API自动拉取
2. 爬虫降级为竞品实时价格监控（仅补充）

Phase 3（长期）：
1. 如有预算，引入STR月度数据（权威基准）
2. 考虑斥候（云创信息）实时竞品数据服务
```

---

## 五、竞品监控配置清单

### 5.1 乐山嘉州宾馆竞品列表

> ⚠️ 以下竞品基于行业知识推断，**必须实地确认调整**

| 序号 | 竞品名称 | 档次 | 携程链接 | 美团链接 | 房型 | 建议监控频次 |
|------|---------|------|---------|---------|------|------------|
| 1 | 全季酒店(乐山大佛店) | 中高端 | 待确认 | 待确认 | 商务大床房 | 每日2次 |
| 2 | 麗枫酒店(乐山高铁站店) | 中端 | 待确认 | 待确认 | 舒适大床房 | 每日2次 |
| 3 | 和颐酒店(乐山店) | 中高端 | 待确认 | 待确认 | 商务大床房 | 每日2次 |
| 4 | 亚朵酒店(乐山大佛店) | 中高端 | 待确认 | 待确认 | 高级大床房 | 每日2次 |
| 5 | 禅驿酒店(乐山大佛店) | 文旅特色 | 待确认 | 待确认 | 禅意大床房 | 每日2次 |
| 6 | 锦江之星(乐山店) | 经济型 | 待确认 | 待确认 | 标准房 | 每日1次 |
| 7 | 7天酒店(乐山大佛店) | 经济型 | 待确认 | 待确认 | 自主大床房 | 每日1次 |
| 8 | 如家酒店(乐山店) | 经济型 | 待确认 | 待确认 | 标准房 | 每日1次 |
| 9 | 沃莱顿酒店(乐山店) | 中端 | 待确认 | 待确认 | 豪华房 | 每日2次 |
| 10 | 嘉好悦居酒店(乐山店) | 中端 | 待确认 | 待确认 | 精品大床房 | 每日2次 |

### 5.2 竞品配置数据结构

```yaml
# config/competitors.yaml
competitors:
  - hotel_id: "leshan_001"
    name: "全季酒店(乐山大佛店)"
    star_level: 4
    chain: "华住会"
    ctrip_url: ""  # 待实地确认
    meituan_url: ""  # 待实地确认
    primary_room: "商务大床房"
    monitor_interval_hours: 12  # 每12小时抓一次
    alert_threshold:  # 价格预警阈值
      high_price: 500  # 高于500元触发关注
      low_price: 200   # 低于200元触发关注
  
  - hotel_id: "leshan_002"
    name: "麗枫酒店(乐山高铁站店)"
    star_level: 3
    chain: "锦江"
    # ... 同上格式
```

### 5.3 实地确认清单

> 到达酒店后，必须确认以下信息

| 确认项 | 问题 | 确认方法 |
|-------|------|---------|
| 竞品列表是否准确 | 这10家是不是我们的主要竞争对手？ | 和前台/销售聊 |
| 竞品携程URL | 能否打开这几家酒店的携程页面？ | 实地打开浏览器 |
| 竞品档次是否匹配 | 哪些是直接竞争对手？ | 对比房价/位置/设施 |
| 是否需要增删 | 有没有遗漏的竞品？ | 询问酒店销售 |
| 价格波动规律 | 周末/节假日价格有什么规律？ | 询问酒店人员 |

---

## 六、数据字段字典

### 6.1 竞品价格数据字段

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| `id` | INT | ✅ | 自增ID | 1 |
| `hotel_id` | VARCHAR(32) | ✅ | 竞品酒店ID | leshan_001 |
| `hotel_name` | VARCHAR(64) | ✅ | 竞品酒店名称 | 全季酒店(乐山大佛店) |
| `date` | DATE | ✅ | 价格日期 | 2026-03-27 |
| `price` | DECIMAL(8,2) | ✅ | 价格（元） | 328.00 |
| `room_type` | VARCHAR(32) | ❌ | 房型 | 商务大床房 |
| `source` | VARCHAR(16) | ✅ | 数据来源 | ctrip/meituan |
| `crawl_time` | DATETIME | ✅ | 抓取时间 | 2026-03-27 09:00:00 |
| `star_level` | INT | ❌ | 星级 | 4 |
| `chain` | VARCHAR(32) | ❌ | 连锁品牌 | 华住会 |
| `city` | VARCHAR(16) | ✅ | 城市 | 乐山 |
| `district` | VARCHAR(32) | ❌ | 行政区 | 市中區 |
| `remark` | VARCHAR(256) | ❌ | 备注 | 周末价格 |

### 6.2 OTA产量数据字段（EBK导出）

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| `date` | DATE | ✅ | 统计日期 | 2026-03-26 |
| `hotel_id` | VARCHAR(32) | ✅ | 酒店ID | JZZS001 |
| `hotel_name` | VARCHAR(64) | ✅ | 酒店名称 | 锦江嘉州宾馆 |
| `occupied` | INT | ✅ | 在住房数 | 142 |
| `departures` | INT | ❌ | 离店房数 | 38 |
| `arrivals` | INT | ❌ | 入住房数 | 45 |
| `total_rooms` | INT | ✅ | 总房量 | 180 |
| `occupancy_pct` | DECIMAL(5,2) | ✅ | 入住率 | 78.89 |
| `adr` | DECIMAL(8,2) | ✅ | 平均房价 | 312.50 |
| `revpar` | DECIMAL(8,2) | ✅ | 每房收益 | 246.53 |
| `room_revenue` | DECIMAL(12,2) | ✅ | 客房收入 | 44375.00 |
| `order_count` | INT | ❌ | 订单量 | 128 |
| `room_nights` | DECIMAL(8,2) | ❌ | 净房间夜 | 165.5 |
| `data_source` | VARCHAR(16) | ✅ | 数据来源 | EBK/manual |
| `export_time` | DATETIME | ✅ | 导出时间 | 2026-03-27 09:00:00 |

---

## 七、第三方备用数据服务

### 7.1 斥候（云创信息）

**官网**：https://www.yunchuangtech.com/

**数据内容**：
- 实时竞品房价数据（携程+美团）
- 竞品产量估算
- 市场热度指数

**价格**：按监控酒店数量收费

**适合场景**：Phase 2/3，不想自己运维爬虫

### 7.2 STR (Smith Travel Research)

**官网**：https://str.com/

**数据内容**：
- 中国酒店行业月度数据
- 市场基准（全国/区域/城市）
- 细分市场对比

**价格**：昂贵（年费制，通常数万至数十万/年）

**适合场景**：大型酒店集团，需要权威基准

### 7.3 飞猪数据通

**官网**：阿里巴巴旗下飞猪

**数据内容**：
- 飞猪平台酒店数据
- 产量/流量/转化

**获取方式**：飞猪商家后台

---

## 八、风险与应对

| 风险 | 级别 | 应对方案 |
|------|------|---------|
| **竞品爬虫被封** | 🟡 中 | 立即降级到EBK导出手动录入；增加请求间隔 |
| **携程页面改版** | 🟡 中 | 维护爬虫适配脚本；定期检查数据完整性 |
| **酒店不开通EBK** | 🔴 高 | 强调"数据不出酒店"；展示收益日报demo |
| **竞品列表不准确** | 🟡 中 | 实地和酒店前台/销售确认 |
| **数据质量差** | 🟡 中 | 设置数据校验规则；人工抽查核对 |
| **爬虫IP被封** | 🟡 中 | 使用代理池；降低请求频率 |

---

## 九、下一步动作

### 立即可执行（不依赖审批）
- [ ] **编写竞品价格爬虫**（已提供代码框架）
- [ ] **编写数据清洗脚本**（已提供代码框架）
- [ ] **配置竞品列表**（实地确认URL）
- [ ] **测试携程EBK导出**（酒店方操作，5分钟）

### 需实地确认
- [ ] 确认携程EBK账号有效性
- [ ] 确认竞品酒店URL
- [ ] 确认美团商家后台账号
- [ ] 和酒店前台确认竞品列表

### API申请后执行
- [ ] 申请Trip.com API（Phase 2）
- [ ] 申请美团开放平台（Phase 2）
- [ ] 评估斥候数据服务（Phase 2/3）

---

**文档状态**: V1.0（技术深化版）
**下次更新**: 实地调研后更新竞品列表和URL
**负责人**: AHL技术组
