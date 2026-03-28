# AHL 乐山锦江嘉州宾馆 技术架构方案 V1.0

> **版本**: V1.0
> **日期**: 2026-03-27
> **试点酒店**: 四川乐山锦江嘉州宾馆
> **模块**: 模块4（技术深化任务）
> **状态**: 技术架构设计，待部署验证

---

## 文档目的

本方案定义AHL数字员工在锦江嘉州宾馆部署的技术架构，回答一个核心问题：**这套系统怎么跑起来？**

核心原则：**简单、可靠、可维护。不追求高大上，用最小复杂度解决实际问题。**

---

## 一、技术选型原理

### 1.1 为什么用Python而不是其他语言

| 语言 | 优势 | 劣势 | 适用场景 |
|------|------|------|---------|
| **Python** | 数据处理强、爬虫生态好、学习成本低 | 性能一般 | **首选，数据处理+爬虫** |
| Node.js | 前后端统一、异步IO强 | 数据处理库弱 | 实时推送场景 |
| Java | 稳定、成熟、企业级 | 笨重、学习曲线 | 大型企业系统 |
| Go | 性能高、并发好 | 生态较新 | 高并发爬虫 |

**选择Python的理由**：
- 数据处理：pandas/numpy生态无可替代
- 爬虫：requests/beautifulsoup/scrapy最成熟
- 学习曲线低：酒店IT人员可维护
- 社区活跃：遇到问题容易找到解决方案

### 1.2 为什么用SQLite而不是MySQL/PostgreSQL

| 数据库 | 优势 | 劣势 | 适用场景 |
|--------|------|------|---------|
| **SQLite** | 零配置、文件级、备份简单、无需服务 | 并发写入弱、单文件上限2TB | **Phase 1首选** |
| MySQL | 成熟、并发强、可网络访问 | 需要安装、配置复杂 | 团队协作/多用户 |
| PostgreSQL | 功能强、扩展性好 | 学习曲线、配置复杂 | 高级场景 |

**选择SQLite的理由**：
- Phase 1场景是单机运行，无需网络访问
- 零配置：安装Python后直接使用
- 备份简单：复制文件即可
- 数据量可控：每日几百到几千条记录，SQLite完全够用
- 如果未来数据量增大，可以平滑迁移到PostgreSQL

### 1.3 为什么用requests而不是Selenium/Playwright

| 工具 | 优势 | 劣势 | 适用场景 |
|------|------|------|---------|
| **requests** | 轻量、快速、可控、反爬易实现 | 不能处理JS渲染 | **首选，携程/美团页面可抓** |
| Selenium | 处理JS渲染、支持交互 | 资源重、速度慢、维护复杂 | JS必需场景 |
| Playwright | 现代、速度快、跨浏览器 | 资源重、学习成本 | JS必需场景 |

**选择requests的理由**：
- 携程/美团的房价数据在HTML中已渲染（服务端渲染）
- requests速度比Selenium快10-50倍
- requests资源消耗低，可在树莓派上运行
- requests反爬策略可控（自定义Header/代理/延迟）
- Selenium/Playwright仅在JS渲染页面无法抓取时作为降级方案

### 1.4 为什么用schedule而不是Airflow

| 调度器 | 优势 | 劣势 | 适用场景 |
|--------|------|------|---------|
| **schedule** | 轻量、代码内嵌、无需服务 | 无UI、单机 | **Phase 1首选** |
| APScheduler | 功能丰富、持久化 | 有一定复杂度 | 需要持久化任务 |
| Airflow | 企业级、UI强大、可视化 | 重量级、部署复杂 | 多任务依赖编排 |
| Windows Task Scheduler | 系统自带、无需安装 | 跨平台差、配置繁琐 | Windows服务器 |

**选择schedule的理由**：
- Phase 1任务简单（每日定时执行几个脚本）
- 无需额外部署服务（和主程序一起运行）
- 轻量：schedule库只有几百行代码
- 如果未来任务复杂化，可平滑迁移到APScheduler或Airflow

---

## 二、系统架构图

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        AHL数字员工 - 乐山部署                       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                      数据输入层                            │   │
│  │                                                           │   │
│  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │   │
│  │   │ PMS Excel   │  │ 携程EBK     │  │ 竞品爬虫    │      │   │
│  │   │ 手工导入    │  │ 数据导出    │  │ (携程+美团) │      │   │
│  │   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘      │   │
│  │          │                │                │              │   │
│  └──────────│────────────────│────────────────│──────────────┘   │
│             │                │                │                  │
│             ▼                ▼                ▼                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                      数据存储层                            │   │
│  │                                                           │   │
│  │   ┌─────────────────────────────────────────────────┐    │   │
│  │   │                    SQLite                        │    │   │
│  │   │                                                  │    │   │
│  │   │  Tables:                                        │    │   │
│  │   │  - orders (订单数据)                            │    │   │
│  │   │  - daily_metrics (每日指标)                     │    │   │
│  │   │  - competitor_prices (竞品价格)                 │    │   │
│  │   │  - str_index (STR指数)                          │    │   │
│  │   │  - alerts (预警记录)                            │    │   │
│  │   │  - reviews (差评记录)                           │    │   │
│  │   └─────────────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                      SKILL计算层                           │   │
│  │                                                           │   │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │   │
│  │   │ RM-001  │  │ RM-002  │  │ RM-003  │  │ RM-004  │    │   │
│  │   │ ADR/    │  │ STR     │  │ 竞品    │  │ 价格    │    │   │
│  │   │ OCC/    │  │ 指数    │  │ 爬虫    │  │ 预警    │    │   │
│  │   │ RevPAR  │  │         │  │         │  │         │    │   │
│  │   └─────────┘  └─────────┘  └─────────┘  └─────────┘    │   │
│  │                                                           │   │
│  │   ┌─────────┐  ┌─────────┐                              │   │
│  │   │ RM-005  │  │ OTA-001 │  ┌─────────┐                │   │
│  │   │ 收益    │  │ OTA排名 │  │ OTA-002 │                │   │
│  │   │ 日报    │  │ 诊断    │  │ 差评    │                │   │
│  │   │         │  │         │  │ 预警    │                │   │
│  │   └─────────┘  └─────────┘  └─────────┘                │   │
│  │                                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                      推送输出层                             │   │
│  │                                                           │   │
│  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │   │
│  │   │ 企业微信    │  │ 邮件        │  │ 本地文件    │      │   │
│  │   │ Webhook     │  │ 推送        │  │ 存档        │      │   │
│  │   └─────────────┘  └─────────────┘  └─────────────┘      │   │
│  │                                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 数据流详解

```
数据生命周期

1. 数据采集（输入）
   PMS Excel → 手工导入 → SQLite orders表
   携程EBK → 手工导出 → SQLite daily_metrics表
   竞品爬虫 → 自动抓取 → SQLite competitor_prices表

2. 数据处理（计算）
   orders表 → RM-001 → daily_metrics表
   daily_metrics + competitor_prices → RM-002 → str_index表
   competitor_prices → RM-004 → alerts表
   daily_metrics + str_index + alerts → RM-005 → reports表

3. 数据输出（推送）
   reports表 → 日报推送 → 企业微信
   alerts表 → 预警推送 → 企业微信（实时）
   daily_metrics → 存档 → JSON/CSV文件
```

---

## 三、数据库设计

### 3.1 SQLite数据库结构

```sql
-- 数据库文件：./data/ahl_leshan.db
-- 创建时间：首次运行自动创建

-- 表1：订单数据
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id VARCHAR(64) NOT NULL UNIQUE,
    hotel_id VARCHAR(32) NOT NULL,
    hotel_name VARCHAR(128),
    
    guest_name VARCHAR(64),
    guest_phone VARCHAR(32),
    checkin_date DATE NOT NULL,
    checkout_date DATE NOT NULL,
    room_type VARCHAR(32),
    room_no VARCHAR(16),
    rate_code VARCHAR(32),
    
    room_revenue DECIMAL(12,2) DEFAULT 0,
    total_revenue DECIMAL(12,2) DEFAULT 0,
    
    channel VARCHAR(32),
    channel_order_id VARCHAR(64),
    status VARCHAR(32),
    payment_status VARCHAR(32),
    
    data_source VARCHAR(32),
    import_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 表2：每日指标
CREATE TABLE IF NOT EXISTS daily_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id VARCHAR(32) NOT NULL,
    date DATE NOT NULL UNIQUE,
    
    total_rooms INTEGER,
    occupied INTEGER,
    vacant INTEGER,
    ooo INTEGER,
    complimentary INTEGER,
    house_use INTEGER,
    
    room_revenue DECIMAL(12,2) DEFAULT 0,
    total_revenue DECIMAL(12,2) DEFAULT 0,
    
    occupancy_pct DECIMAL(6,2),
    adr DECIMAL(8,2),
    revpar DECIMAL(8,2),
    
    arrivals INTEGER DEFAULT 0,
    departures INTEGER DEFAULT 0,
    inhouse_guests INTEGER DEFAULT 0,
    order_count INTEGER DEFAULT 0,
    
    data_source VARCHAR(32),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 表3：竞品价格
CREATE TABLE IF NOT EXISTS competitor_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id VARCHAR(32) NOT NULL,
    hotel_name VARCHAR(128),
    date DATE NOT NULL,
    price DECIMAL(8,2),
    room_type VARCHAR(64),
    source VARCHAR(16),
    star_level INTEGER,
    chain VARCHAR(32),
    
    crawl_time DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 表4：STR指数
CREATE TABLE IF NOT EXISTS str_index (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id VARCHAR(32) NOT NULL,
    date DATE NOT NULL,
    period VARCHAR(32),
    
    self_occupancy DECIMAL(6,2),
    self_adr DECIMAL(8,2),
    self_revpar DECIMAL(8,2),
    
    market_occupancy DECIMAL(6,2),
    market_adr DECIMAL(8,2),
    market_revpar DECIMAL(8,2),
    
    mpi DECIMAL(6,2),
    ari DECIMAL(6,2),
    rgi DECIMAL(6,2),
    
    mpi_interpretation TEXT,
    ari_interpretation TEXT,
    rgi_interpretation TEXT,
    
    data_source VARCHAR(32),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 表5：预警记录
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id VARCHAR(32) NOT NULL,
    alert_type VARCHAR(32) NOT NULL,
    severity VARCHAR(16),
    
    competitor_id VARCHAR(32),
    competitor_name VARCHAR(128),
    
    current_value DECIMAL(10,2),
    previous_value DECIMAL(10,2),
    threshold DECIMAL(10,2),
    
    message TEXT,
    is_read BOOLEAN DEFAULT 0,
    is_sent BOOLEAN DEFAULT 0,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 表6：差评记录
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id VARCHAR(32) NOT NULL,
    platform VARCHAR(16) NOT NULL,
    
    guest_name VARCHAR(64),
    checkin_date DATE,
    review_date DATE NOT NULL,
    score DECIMAL(3,1) NOT NULL,
    content TEXT,
    
    categories VARCHAR(256),
    is_replied BOOLEAN DEFAULT 0,
    reply_content TEXT,
    reply_time DATETIME,
    
    is_handled BOOLEAN DEFAULT 0,
    handler VARCHAR(64),
    handle_time DATETIME,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(checkin_date);
CREATE INDEX IF NOT EXISTS idx_daily_metrics_date ON daily_metrics(date);
CREATE INDEX IF NOT EXISTS idx_competitor_date ON competitor_prices(date);
CREATE INDEX IF NOT EXISTS idx_str_date ON str_index(date);
CREATE INDEX IF NOT EXISTS idx_alerts_type ON alerts(alert_type);
CREATE INDEX IF NOT EXISTS idx_alerts_read ON alerts(is_read);
CREATE INDEX IF NOT EXISTS idx_reviews_date ON reviews(review_date);
```

### 3.2 数据库管理脚本

```python
#!/usr/bin/env python3
"""
数据库初始化与管理
AHL乐山锦江嘉州宾馆专用

功能：
1. 初始化数据库和表结构
2. 数据查询
3. 数据备份
4. 数据清理
"""

import sqlite3
import logging
import shutil
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    SQLite数据库管理器
    
    职责：
    1. 初始化数据库连接
    2. 创建表结构
    3. 提供CRUD操作封装
    4. 数据备份与清理
    """
    
    def __init__(self, db_path: str = "./data/ahl_leshan.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库连接"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # 支持字典访问
        self._create_tables()
        logger.info(f"数据库已连接: {self.db_path}")
    
    def _create_tables(self):
        """创建表结构"""
        schema = """
        -- 订单数据
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id VARCHAR(64) NOT NULL UNIQUE,
            hotel_id VARCHAR(32) NOT NULL,
            hotel_name VARCHAR(128),
            guest_name VARCHAR(64),
            guest_phone VARCHAR(32),
            checkin_date DATE NOT NULL,
            checkout_date DATE NOT NULL,
            room_type VARCHAR(32),
            room_no VARCHAR(16),
            rate_code VARCHAR(32),
            room_revenue DECIMAL(12,2) DEFAULT 0,
            total_revenue DECIMAL(12,2) DEFAULT 0,
            channel VARCHAR(32),
            channel_order_id VARCHAR(64),
            status VARCHAR(32),
            payment_status VARCHAR(32),
            data_source VARCHAR(32),
            import_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        -- 每日指标
        CREATE TABLE IF NOT EXISTS daily_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id VARCHAR(32) NOT NULL,
            date DATE NOT NULL UNIQUE,
            total_rooms INTEGER,
            occupied INTEGER,
            vacant INTEGER,
            ooo INTEGER,
            complimentary INTEGER,
            house_use INTEGER,
            room_revenue DECIMAL(12,2) DEFAULT 0,
            total_revenue DECIMAL(12,2) DEFAULT 0,
            occupancy_pct DECIMAL(6,2),
            adr DECIMAL(8,2),
            revpar DECIMAL(8,2),
            arrivals INTEGER DEFAULT 0,
            departures INTEGER DEFAULT 0,
            inhouse_guests INTEGER DEFAULT 0,
            order_count INTEGER DEFAULT 0,
            data_source VARCHAR(32),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        -- 竞品价格
        CREATE TABLE IF NOT EXISTS competitor_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id VARCHAR(32) NOT NULL,
            hotel_name VARCHAR(128),
            date DATE NOT NULL,
            price DECIMAL(8,2),
            room_type VARCHAR(64),
            source VARCHAR(16),
            star_level INTEGER,
            chain VARCHAR(32),
            crawl_time DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        -- STR指数
        CREATE TABLE IF NOT EXISTS str_index (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id VARCHAR(32) NOT NULL,
            date DATE NOT NULL,
            period VARCHAR(32),
            self_occupancy DECIMAL(6,2),
            self_adr DECIMAL(8,2),
            self_revpar DECIMAL(8,2),
            market_occupancy DECIMAL(6,2),
            market_adr DECIMAL(8,2),
            market_revpar DECIMAL(8,2),
            mpi DECIMAL(6,2),
            ari DECIMAL(6,2),
            rgi DECIMAL(6,2),
            mpi_interpretation TEXT,
            ari_interpretation TEXT,
            rgi_interpretation TEXT,
            data_source VARCHAR(32),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        -- 预警记录
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id VARCHAR(32) NOT NULL,
            alert_type VARCHAR(32) NOT NULL,
            severity VARCHAR(16),
            competitor_id VARCHAR(32),
            competitor_name VARCHAR(128),
            current_value DECIMAL(10,2),
            previous_value DECIMAL(10,2),
            threshold DECIMAL(10,2),
            message TEXT,
            is_read BOOLEAN DEFAULT 0,
            is_sent BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        -- 差评记录
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id VARCHAR(32) NOT NULL,
            platform VARCHAR(16) NOT NULL,
            guest_name VARCHAR(64),
            checkin_date DATE,
            review_date DATE NOT NULL,
            score DECIMAL(3,1) NOT NULL,
            content TEXT,
            categories VARCHAR(256),
            is_replied BOOLEAN DEFAULT 0,
            reply_content TEXT,
            reply_time DATETIME,
            is_handled BOOLEAN DEFAULT 0,
            handler VARCHAR(64),
            handle_time DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        -- 索引
        CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(checkin_date);
        CREATE INDEX IF NOT EXISTS idx_daily_metrics_date ON daily_metrics(date);
        CREATE INDEX IF NOT EXISTS idx_competitor_date ON competitor_prices(date);
        CREATE INDEX IF NOT EXISTS idx_str_date ON str_index(date);
        CREATE INDEX IF NOT EXISTS idx_alerts_type ON alerts(alert_type);
        CREATE INDEX IF NOT EXISTS idx_reviews_date ON reviews(review_date);
        """
        
        self.conn.executescript(schema)
        self.conn.commit()
        logger.info("数据库表结构已初始化")
    
    def backup(self, backup_dir: str = "./data/backups"):
        """
        备份数据库
        
        原理：复制db文件，文件名加上时间戳
        """
        Path(backup_dir).mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = Path(backup_dir) / f"ahl_leshan_{timestamp}.db"
        
        shutil.copy2(self.db_path, backup_path)
        
        # 只保留最近10个备份
        backups = sorted(Path(backup_dir).glob("ahl_leshan_*.db"), 
                        key=lambda x: x.stat().st_mtime)
        while len(backups) > 10:
            old = backups.pop(0)
            old.unlink()
            logger.info(f"删除旧备份: {old}")
        
        logger.info(f"数据库已备份: {backup_path}")
        return str(backup_path)
    
    def query(self, sql: str, params: tuple = ()) -> List[Dict]:
        """查询数据"""
        cursor = self.conn.execute(sql, params)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]
    
    def execute(self, sql: str, params: tuple = ()):
        """执行SQL"""
        self.conn.execute(sql, params)
        self.conn.commit()
    
    def close(self):
        """关闭连接"""
        self.conn.close()
        logger.info("数据库连接已关闭")


if __name__ == "__main__":
    db = DatabaseManager()
    
    # 示例：备份数据库
    backup_path = db.backup()
    print(f"备份成功: {backup_path}")
    
    # 示例：查询最近7天的每日指标
    results = db.query("""
        SELECT * FROM daily_metrics 
        WHERE date >= date('now', '-7 days')
        ORDER BY date DESC
    """)
    print(f"查询到{len(results)}条每日指标")
    
    db.close()
```

---

## 四、部署步骤

### 4.1 步骤1：环境搭建

```bash
# 1.1 检查Python版本（需要3.10+）
python --version
# 输出应为 Python 3.10.x 或更高

# 如果没有Python，下载安装：https://www.python.org/downloads/windows/

# 1.2 创建项目目录
mkdir -p AHL-Leshan
cd AHL-Leshan

# 1.3 创建虚拟环境（推荐，避免依赖冲突）
python -m venv venv

# Windows激活虚拟环境
venv\Scripts\activate

# macOS/Linux激活
# source venv/bin/activate

# 1.4 安装依赖
pip install --upgrade pip
pip install pandas requests beautifulsoup4 lxml python-dateutil schedule

# 或一键安装
pip install -r requirements.txt
```

**requirements.txt内容**：
```
pandas>=2.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
python-dateutil>=2.8.0
schedule>=1.2.0
```

### 4.2 步骤2：数据库初始化

```python
# 运行数据库初始化脚本
python db_manager.py
```

预期输出：
```
INFO - 数据库已连接: ./data/ahl_leshan.db
INFO - 数据库表结构已初始化
INFO - 数据库连接已关闭
```

### 4.3 步骤3：配置竞品URL

编辑`config/competitors.yaml`：

```yaml
# config/competitors.yaml
hotel:
  id: "JZZS001"
  name: "锦江嘉州宾馆"
  city: "leshan"
  total_rooms: 180  # 待确认

competitors:
  - hotel_id: "leshan_001"
    name: "全季酒店(乐山大佛店)"
    star_level: 4
    chain: "华住会"
    ctrip_url: ""  # 待实地确认
    meituan_url: ""  # 待实地确认
    primary_room: "商务大床房"
    monitor_interval_hours: 12
    alert_threshold:
      high_price: 500
      low_price: 200

  # ... 其他竞品
```

### 4.4 步骤4：手动数据导入测试

```python
# 4.1 导入PMS订单数据（Excel）
python main_import.py --type orders --file "./exports/orders_20260327.xlsx"

# 4.2 导入携程EBK数据（Excel）
python main_import.py --type ebk --file "./exports/ctrip_ebk_20260327.xlsx"

# 4.3 验证导入结果
python -c "
from db_manager import DatabaseManager
db = DatabaseManager()
orders = db.query('SELECT COUNT(*) as cnt FROM orders')
metrics = db.query('SELECT COUNT(*) as cnt FROM daily_metrics')
print(f'订单数: {orders[0][\"cnt\"]}')
print(f'每日指标: {metrics[0][\"cnt\"]}')
db.close()
"
```

### 4.5 步骤5：日报推送测试

```python
# 5.1 配置企业微信Webhook（可选）
# 在企业微信中创建群机器人，复制Webhook URL
# 编辑 config/notification.yaml
echo "webhook_url: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY" > config/notification.yaml

# 5.2 手动触发日报生成和推送
python main_daily.py --date 2026-03-27 --push

# 预期：收到微信推送的收益日报
```

### 4.6 步骤6：配置定时任务

**Windows方案（推荐）**：

```batch
# 创建定时任务：每日早上9点执行
schtasks /create ^
  /tn "AHL_每日收益日报" ^
  /tr "C:\AHL-Leshan\venv\Scripts\python.exe C:\AHL-Leshan\main_daily.py" ^
  /sc daily ^
  /st 09:00 ^
  /ru SYSTEM ^
  /f

# 创建定时任务：每12小时执行竞品爬虫
schtasks /create ^
  /tn "AHL_竞品价格抓取" ^
  /tr "C:\AHL-Leshan\venv\Scripts\python.exe C:\AHL-Leshan\main_crawler.py" ^
  /sc daily ^
  /st 08:00 ^
  /mo 2 ^  /sc daily /st 08:00 和 /sc daily /st 20:00
```

**Python schedule方案（代码内嵌）**：

```python
#!/usr/bin/env python3
"""
定时任务调度器
AHL乐山锦江嘉州宾馆专用

功能：
1. 每日早上9点：生成并推送收益日报
2. 每日早上8点/晚上8点：抓取竞品价格
3. 实时监控：差评预警（每小时检查一次）
"""

import schedule
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def job_daily_report():
    """每日收益日报"""
    logger.info("执行：生成收益日报")
    # 调用 main_daily.py
    import subprocess
    subprocess.run(["python", "main_daily.py"])


def job_competitor_crawl():
    """竞品价格抓取"""
    logger.info("执行：抓取竞品价格")
    import subprocess
    subprocess.run(["python", "main_crawler.py"])


def job_review_alert():
    """差评预警检查"""
    logger.info("执行：差评预警检查")
    import subprocess
    subprocess.run(["python", "main_review_alert.py"])


def main():
    # 定时任务配置
    # 每日早上9点：日报
    schedule.every().day.at("09:00").do(job_daily_report)
    
    # 每12小时：竞品爬虫
    schedule.every().day.at("08:00").do(job_competitor_crawl)
    schedule.every().day.at("20:00").do(job_competitor_crawl)
    
    # 每小时：差评检查（仅工作时间）
    for hour in range(9, 22):
        schedule.every().day.at(f"{hour:02d}:05").do(job_review_alert)
    
    logger.info("定时任务已启动")
    logger.info("- 每日09:00：收益日报")
    logger.info("- 每日08:00/20:00：竞品价格抓取")
    logger.info("- 每小时(9-21点)：差评预警检查")
    
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
```

---

## 五、第三方Key清单

### 5.1 免费Key（必配）

| 服务 | 用途 | 获取方式 | 成本 |
|------|------|---------|------|
| 和风天气API | 天气预报（影响出行决策） | https://id.cityforge.org/console | 免费（开发版） |

```python
# 和风天气API使用示例
import requests

API_KEY = "YOUR_HEFENG_KEY"  # 注册后获取
CITY_CODE = "1012714"  # 乐山城市代码

def get_weather():
    url = f"https://devapi.qweather.com/v7/weather/3d"
    params = {
        "key": API_KEY,
        "location": CITY_CODE,
    }
    response = requests.get(url, params=params)
    return response.json()
```

### 5.2 免费但需申请（建议申请）

| 服务 | 用途 | 申请方式 | 周期 |
|------|------|---------|------|
| 携程Trip.com API | PMS数据自动拉取 | 通过锦江集团IT申请 | 2-4周 |
| 美团开放平台 | 美团数据自动拉取 | 登录美团开放平台申请 | 2-4周 |

### 5.3 付费服务（可选）

| 服务 | 用途 | 成本 | 必要性 |
|------|------|------|--------|
| 斥候（云创信息） | 实时竞品数据 | 按酒店数收费 | 低（爬虫可替代） |
| STR数据 | 权威市场基准 | 年费数万至数十万 | 低（Phase 1用竞品估算即可） |

### 5.4 无需Key（当前方案）

| 数据源 | 获取方式 | 难度 |
|--------|---------|------|
| 携程EBK导出 | 酒店后台手工导出 | 无门槛 |
| 美团商家后台导出 | 酒店后台手工导出 | 无门槛 |
| 竞品价格爬虫 | requests直接抓取 | 中（有反爬风险） |

---

## 六、OpenClaw Skill触发机制

### 6.1 什么是OpenClaw Skill

OpenClaw Skill是一种可被AI助手调用的技能模块。在AHL乐山项目中，SKILL对应RM-001~RM-005、OTA-001~OTA-002等分析模块。

### 6.2 SKILL触发方式

**方式1：定时自动触发（推荐用于日报）**

```python
# 在OpenClaw中配置定时任务
# 触发条件：每日09:00
# 触发动作：执行AHL-SKILL-RM005脚本
```

**方式2：事件触发（推荐用于预警）**

```python
# 当新数据导入时触发
# 触发条件：SQLite数据变更
# 触发动作：执行对应SKILL
```

**方式3：对话触发（用户主动查询）**

```
用户：帮我看看昨天的收益日报
AI助手 → 调用RM-005 → 返回日报
```

### 6.3 SKILL注册到OpenClaw

```yaml
# .openclaw/skills/ahl-rm-skills/SKILL.md
name: AHL收益管理SKILL集
description: 锦江嘉州宾馆专用收益管理分析SKILL
scripts:
  rm001: python skills/RM-001_adr_occ_revpar.py
  rm002: python skills/RM-002_str_index.py
  rm003: python skills/RM-003_competitor_crawler.py
  rm004: python skills/RM-004_price_alert.py
  rm005: python skills/RM-005_daily_report.py
```

---

## 七、目录结构与文件清单

### 7.1 完整目录结构

```
AHL-Leshan/
│
├── 📂 skills/                    # SKILL模块
│   ├── __init__.py
│   ├── RM-001_adr_occ_revpar.py  # ADR/OCC/RevPAR计算
│   ├── RM-002_str_index.py       # STR指数计算
│   ├── RM-003_competitor_crawler.py  # 竞品价格爬虫
│   ├── RM-004_price_alert.py     # 价格预警
│   ├── RM-005_daily_report.py     # 收益日报生成
│   ├── OTA-001_ranking_diagnosis.py  # OTA排名诊断
│   └── OTA-002_review_alert.py   # 差评预警
│
├── 📂 data/                      # 数据目录
│   ├── 📂 backups/               # 数据库备份
│   ├── 📂 exports/               # 导入文件（Excel/CSV）
│   ├── 📂 revenue/               # 收益指标JSON
│   ├── 📂 competitor/            # 竞品价格CSV
│   └── 📂 reports/               # 日报存档
│
├── 📂 logs/                      # 日志目录
│   ├── 📂 crawler/               # 爬虫日志
│   ├── 📂 skill/                 # SKILL日志
│   └── 📂 daily/                 # 每日任务日志
│
├── 📂 config/                    # 配置文件
│   ├── competitors.yaml          # 竞品配置
│   ├── notification.yaml          # 推送配置
│   └── database.yaml             # 数据库配置
│
├── 📂 database/                  # 数据库目录
│   └── ahl_leshan.db             # SQLite数据库
│
├── 📂 scripts/                   # 工具脚本
│   ├── db_manager.py             # 数据库管理
│   ├── data_importer.py          # 数据导入
│   └── backup.py                 # 备份脚本
│
├── 📄 main_daily.py              # 每日任务入口
├── 📄 main_crawler.py            # 爬虫任务入口
├── 📄 main_schedule.py           # 定时调度入口
├── 📄 requirements.txt            # Python依赖
├── 📄 README.md                   # 项目说明
└── 📄 .gitignore                  # Git忽略配置
```

### 7.2 关键文件说明

| 文件 | 用途 | 运行时 |
|------|------|--------|
| `main_daily.py` | 每日日报生成+推送 | 每日09:00 |
| `main_crawler.py` | 竞品价格爬虫 | 每日08:00/20:00 |
| `main_schedule.py` | 定时任务调度器 | 常驻运行 |
| `db_manager.py` | 数据库初始化+管理 | 一次性 |
| `data_importer.py` | Excel数据导入 | 手动触发 |

---

## 八、技术风险与应对

| 风险 | 级别 | 应对方案 | 回退方案 |
|------|------|---------|---------|
| **竞品爬虫被封** | 🟡 中 | UA轮换+延迟+代理池 | 降级到EBK导入手动录入 |
| **携程页面改版** | 🟡 中 | 维护解析脚本 | 临时降级 |
| **数据库损坏** | 🔴 高 | 每日自动备份 | 从备份恢复 |
| **服务器断电** | 🟡 中 | 任务重启后自动续跑 | 缺失数据手动补录 |
| **API申请失败** | 🟡 中 | 保持Excel手工导入 | 继续手工+爬虫补充 |
| **数据质量差** | 🟡 中 | 数据校验+人工抽查 | 标记异常数据 |

---

## 九、运维清单

### 9.1 每日检查

- [ ] 日报是否按时推送
- [ ] 爬虫是否有失败记录
- [ ] 数据库备份是否成功

### 9.2 每周检查

- [ ] 竞品数据完整性（10家竞品都有数据）
- [ ] STR指数是否正常计算
- [ ] 差评预警是否正常

### 9.3 每月检查

- [ ] 数据库大小（超过1GB需清理历史数据）
- [ ] 日志文件大小（清理过期日志）
- [ ] 备份保留数量（保持10个以上）

### 9.4 季度检查

- [ ] 竞品列表是否需要更新
- [ ] 预警阈值是否需要调整
- [ ] 爬虫频率是否需要调整

---

**文档状态**: V1.0（技术架构版）
**下次更新**: 部署后更新实际配置
**负责人**: AHL技术组
