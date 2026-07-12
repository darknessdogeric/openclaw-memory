# AHL-乐山-私域运营技术方案-V1.0

> **版本**: V1.0  
> **日期**: 2026-03-27  
> **状态**: 起草  
> **负责人**: AHL技术组

---

## 模块1：私域运营SKILL体系

### 乐山落地现状评估

#### 能不能做？—— 可行性分析

**现状基础（乐山嘉州宾馆）**：

| 维度 | 现状 | 可用性 |
|------|------|--------|
| 客源基础 | 携程2414条点评，年接待量估算5000+人次 | ✅ 有存量 |
| 特色定位 | 宠物友好/270度江景 | ✅ 适合做垂直社群 |
| 会员系统 | 锦江会员体系（推测） | ⚠️ 待确认打通方式 |
| 联系方式 | 客人手机号（携程订单有） | ✅ 可通过EBK导出 |
| 企微使用 | 推测为个人微信管理 | ❌ 需要升级为企微 |
| 社群工具 | 未知 | ❌ 需要全新搭建 |

**核心问题与答案**：

| 问题 | 答案 | 行动项 |
|------|------|--------|
| 企微是否是酒店现有工具？ | **推测：否**，乐山中小酒店多用个人微信 | 推动酒店开通企微（免费） |
| 锦江会员系统是否绑定了手机号？ | **推测：是**，锦江体系支持 | 确认从锦江PMS导出会员数据的方式 |
| 携程订单手机号能否获取？ | **可以**，通过EBK后台导出 | 确认EBK导出权限和格式 |

#### 需要什么前提？

1. **最小可落地前提（Phase 1）**：
   - 酒店开通企业微信（免费，10分钟搞定）
   - 拉微信群（酒店现有客户群或新建立）
   - 获取携程EBK订单导出权限（联系携程BD）
   - 安装OpenClaw Agent（已完成）

2. **进阶前提（Phase 2）**：
   - 企微SCRM API权限（需企业认证）
   - PMS API对接（房态实时同步）
   - 锦江会员系统API对接

3. **完整前提（Phase 3）**：
   - 微信公众号/小程序（模板消息推送）
   - CRM系统（客户数据中台）

---

### SKILL清单

#### PRIV-001：OTA引流SOP

**规格卡**：

```
┌─────────────────────────────────────────────────────────┐
│ SKILL编号    │ PRIV-001                                │
├─────────────────────────────────────────────────────────┤
│ SKILL名称    │ OTA引流SOP                              │
├─────────────────────────────────────────────────────────┤
│ 目标         │ 客人离店后自动拉入社群，沉淀为私域会员   │
├─────────────────────────────────────────────────────────┤
│ 输入         │ 离店客人数据（手机号/姓名/入住日期）    │
│             │ - 来源1：携程EBK导出（手动）              │
│             │ - 来源2：PMS系统API（自动，Phase 2）      │
├─────────────────────────────────────────────────────────┤
│ 处理逻辑     │ Step1: 数据清洗（去重/手机号格式校验）  │
│             │ Step2: 生成企微添加请求                  │
│             │ Step3: 发送欢迎语+优惠券                 │
│             │ Step4: 标记入群状态                      │
├─────────────────────────────────────────────────────────┤
│ 输出         │ 私域会员档案（JSON）                    │
│             │ {phone, wechat_id, add_time, source,     │
│             │  member_level, tags[]}                    │
├─────────────────────────────────────────────────────────┤
│ 数据依赖     │ - SQLite: guest_private.db               │
│             │ - 企微API: 联系人添加接口                 │
│             │ - 优惠券系统: 锦江/酒店自营              │
├─────────────────────────────────────────────────────────┤
│ 边界/限制    │ - 单次最多处理500条                      │
│             │ - 频率限制：每分钟不超过60次添加请求      │
│             │ - 需客人同意接收消息（Opt-in）           │
└─────────────────────────────────────────────────────────┘
```

**技术原理**：

```
为什么这样做？
├── OTA订单 → 客人已在携程留过手机号 → 离店后触达转化率最高
├── 离店当天是黄金时间：体验刚完成，印象最深
└── 进社群 = 降低未来OTA佣金（私域复购无需给携程扣点）

为什么不是入住时就拉群？
└── 客人刚到店最关心的是入住体验，不是被营销
└── 离店时拉群阻力最小（刚满意离开，正向情绪）
```

#### PRIV-002：社群自动运营

**规格卡**：

```
┌─────────────────────────────────────────────────────────┐
│ SKILL编号    │ PRIV-002                                │
├─────────────────────────────────────────────────────────┤
│ SKILL名称    │ 社群自动运营                            │
├─────────────────────────────────────────────────────────┤
│ 目标         │ 保持社群活跃，提升复购率                │
├─────────────────────────────────────────────────────────┤
│ 输入         │ 客人行为事件（入住/离店/点评/收藏）     │
│             │ 触发时间规则（基于事件的时间点）         │
├─────────────────────────────────────────────────────────┤
│ 触发规则     │ T+0（入住当天）: 欢迎语+设施介绍         │
│             │ T+0（离店当天）: 感谢+好评请求            │
│             │ T+7（入住后7天）: 二次触达优惠            │
│             │ T+N（点评后当天）: 自动感谢+积分发放      │
├─────────────────────────────────────────────────────────┤
│ 处理逻辑     │ 事件识别 → 模板匹配 → 内容生成 → 发送  │
│             │ （使用LLM优化话术，避免机械感）           │
├─────────────────────────────────────────────────────────┤
│ 输出         │ 发送记录（成功/失败/未送达）            │
│             │ 客人响应数据（点击/回复/转化）            │
├─────────────────────────────────────────────────────────┤
│ 数据依赖     │ - 企微群发API                           │
│             │ - 微信模板消息（需公众号授权）            │
│             │ - 酒店知识库（设施介绍/优惠券信息）       │
├─────────────────────────────────────────────────────────┤
│ 边界/限制    │ - 每周每客不超过3条主动消息              │
│             │ - 晚上22:00-次日09:00不发送              │
│             │ - 客人回复"退订"则停止触达              │
└─────────────────────────────────────────────────────────┘
```

**技术原理**：

```
为什么设计这些时间节点？
├── 入住当天（T+0）：建立情感连接，此时最适合介绍特色设施
│   └── 心理学依据：峰终定律，印象最深刻时刻
├── 离店当天（T+0）：请求好评，效果比事后好3倍
│   └── 携程规则：客人离店后14天内可追评
├── 入住后7天（T+7）：记忆犹新，优惠触发复购决策
│   └── 数据依据：酒店复购窗口期通常在30天内
└── 点评后当天（T+N）：正向反馈强化，转化为忠实会员

为什么限制发送频率？
└── 过度营销 = 被拉黑 = 永久失去这个客户
└── 行业经验：每周超过3条推送，取关率上升40%
```

#### PRIV-003：会员LTV分层管理

**规格卡**：

```
┌─────────────────────────────────────────────────────────┐
│ SKILL编号    │ PRIV-003                                │
├─────────────────────────────────────────────────────────┤
│ SKILL名称    │ 会员LTV分层管理                         │
├─────────────────────────────────────────────────────────┤
│ 目标         │ 识别高价值会员，做差异化运营             │
├─────────────────────────────────────────────────────────┤
│ 输入         │ 全量入住记录+消费数据                   │
│             │ {guest_id, phone, check_in, check_out,    │
│             │  room_type, avg_rate, total_spend,       │
│             │  source, tags[], behaviors[]}             │
├─────────────────────────────────────────────────────────┤
│ 分层模型     │ RFM模型                                 │
│             │ R（Recency）：最近一次入住距今天数        │
│             │ F（Frequency）：过去365天入住次数        │
│             │ M（Monetary）：过去365天消费总额          │
│             │                                          │
│             │ 综合分 = w1×R + w2×F + w3×M              │
│             │ 权重初值：w1=0.4, w2=0.3, w3=0.3          │
│             │ （可按酒店数据调优）                      │
├─────────────────────────────────────────────────────────┤
│ 分层结果     │ A类（Top 5%）: VIP，1V1专属管家          │
│             │ B类（Top 6-20%）: 高级会员，专属优惠     │
│             │ C类（Top 21-50%）: 活跃会员，常规触达     │
│             │ D类（Bottom 50%）: 沉睡会员，低频唤醒     │
├─────────────────────────────────────────────────────────┤
│ 输出         │ 分层结果表guest_ltv.csv                  │
│             │ 每种类型的营销策略建议                    │
├─────────────────────────────────────────────────────────┤
│ 数据依赖     │ - SQLite: guest_private.db               │
│             │ - PMS入住记录（历史数据导入）            │
│             │ - 携程订单数据（补充消费字段）           │
├─────────────────────────────────────────────────────────┤
│ 边界/限制    │ - 每月重新计算一次（全量）              │
│             │ - 新客人（<3次入住）使用规则判断         │
│             │ - 数据不足时默认归入C类                  │
└─────────────────────────────────────────────────────────┘
```

**技术原理**：

```
为什么用RFM而不是其他模型？
├── 酒店行业特性：低频消费，高客单价
├── RFM能捕捉：最近是否来/来的勤不勤/花了多少钱
├── 这三个维度组合能识别出：
│   ├── 高价值会员（R低F高M高）：忠诚度最高的金矿
│   ├── 流失风险会员（R高F高M高）：以前很优质，最近没来
│   ├── 潜力会员（R低F低M高）：花得多但不常来，激活F
│   └── 低价值会员（R高F低M低）：投入产出比差

为什么Top20%作为VIP阈值？
└── 二八定律：20%客户贡献80%利润
└── 酒店行业经验：重点维护Top20%会员，性价比最高
└── A类（Top5%）做1V1管家服务，B类（6-20%）做自动化VIP权益
```

---

### 技术实现路径

#### Phase 1：手动半自动（现在就能做，1-2周落地）

```
目标：不依赖API，用现有工具搭最小闭环

工具栈：
├── 数据获取：携程EBK手动导出Excel
├── 客户管理：企业微信（免费）
├── 社群运营：微信群+群发功能
├── 内容生成：LLM（Kimi/DeepSeek）辅助写文案
└── 数据存储：SQLite本地数据库

工作流：
[携程EBK导出] → [Excel转CSV] → [LLM生成个性化话术]
    → [企微手动添加] → [社群沉淀] → [群发触达]

人工介入点：
├── 携程订单导出：每周手动操作
├── 企微添加：AI辅助生成请求语，人工确认发送
└── 差评/投诉：人工处理

预计完成时间：1-2周
预计成本：0元（使用免费工具）
```

#### Phase 2：API半自动（1-2个月后）

```
目标：减少人工操作，提高实时性

工具栈：
├── PMS API对接：房态/订单自动同步
├── 企微SCRM API：自动添加/标签/群发
├── 携程EBK API：订单自动抓取（需申请）
└── CRM雏形：SQLite升级为正式数据库

工作流：
[PMS订单完成] → [自动触发企微添加请求]
    → [欢迎语+优惠券自动发送] → [自动打标签入群]

新增SKILL：
├── PRIV-002升级：基于实时事件触发（不再依赖定时）
└── PRIV-003升级：实时RFM计算（不再是每月批处理）

预计完成时间：1-2个月
预计成本：API对接开发（约2-3万元）
```

#### Phase 3：全自动智能（3-6个月后）

```
目标：全流程自动化，AI驱动的私域运营

工具栈：
├── 微信公众号/小程序：模板消息推送
├── CDP（客户数据平台）：统一客户画像
├── 自动化营销平台：流程画布
└── AI决策引擎：个性化推荐+动态定价

工作流：
[全渠道数据整合] → [AI客户生命周期管理]
    → [个性化内容生成] → [智能触达优化]

最终形态：
├── 新客：AI自动分配销售跟进
├── 在店：AI推荐体验项目，提升客单价
├── 离店：AI自动评价管理
├── 复购：AI预测+个性化优惠
└── 沉睡：AI自动唤醒策略

预计完成时间：3-6个月
预计成本：系统建设+维护（约10-20万元/年）
```

---

### 关键代码框架

#### PRIV-001：OTA引流SOP

```python
# -*- coding: utf-8 -*-
"""
PRIV-001: OTA引流SOP
功能：客人离店后自动拉入社群
Phase: 1（手动半自动）
"""

import sqlite3
import csv
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

# ============================================================
# 配置区
# ============================================================
DB_PATH = "data/guest_private.db"
GUEST_TABLE = "guests_from_ota"
QUEUE_TABLE = "wechat_add_queue"
LOG_TABLE = "operation_log"

# 企微API配置（Phase 2启用）
WECOM_API_URL = "https://qyapi.weixin.qq.com/cgi-bin/"
WECOM_CORP_ID = "YOUR_CORP_ID"
WECOM_SECRET = "YOUR_SECRET"

# ============================================================
# 工具函数
# ============================================================

def phone_format(phone: str) -> Optional[str]:
    """手机号格式校验和标准化"""
    # 去除非数字字符
    digits = re.sub(r'\D', '', phone)
    # 中国手机号：11位，以1开头
    if len(digits) == 11 and digits.startswith('1'):
        return digits
    return None

def init_database():
    """初始化SQLite数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 客人档案表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guests_from_ota (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE NOT NULL,
            name TEXT,
            source TEXT,  -- ctrip/meituan/jinjiang/direct
            first_check_in DATE,
            last_check_in DATE,
            total_stays INTEGER DEFAULT 0,
            total_spend REAL DEFAULT 0,
            member_level TEXT DEFAULT 'D',
            tags TEXT,  -- JSON array
            wechat_id TEXT,
            add_wechat_time DATETIME,
            in_group BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 企微添加队列表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wechat_add_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            name TEXT,
            status TEXT DEFAULT 'pending',  -- pending/success/failed
            priority INTEGER DEFAULT 0,
            scheduled_at DATETIME,
            attempted_at DATETIME,
            result TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 操作日志表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS operation_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_id TEXT,
            action TEXT,
            target_phone TEXT,
            result TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    return conn


class OTAImport:
    """从OTA导入客人数据"""
    
    def __init__(self, conn):
        self.conn = conn
    
    def import_from_ebk_csv(self, csv_path: str) -> Dict:
        """
        从携程EBK导出的CSV导入客人数据
        CSV格式（需确认实际字段）：
        订单号,客人姓名,手机号,入住日期,离店日期,房型,房价,来源
        """
        imported = 0
        duplicates = 0
        errors = 0
        
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    phone = phone_format(row.get('手机号', ''))
                    if not phone:
                        errors += 1
                        continue
                    
                    check_in = row.get('入住日期', '')
                    check_out = row.get('离店日期', '')
                    source = row.get('来源', 'ctrip')
                    name = row.get('客人姓名', '')
                    
                    # 检查是否已存在
                    cursor = self.conn.cursor()
                    cursor.execute(
                        'SELECT id FROM guests_from_ota WHERE phone = ?',
                        (phone,)
                    )
                    if cursor.fetchone():
                        duplicates += 1
                        continue
                    
                    # 插入新记录
                    cursor.execute('''
                        INSERT INTO guests_from_ota 
                        (phone, name, source, first_check_in, last_check_in)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (phone, name, source, check_in, check_out))
                    
                    imported += 1
                    
                except Exception as e:
                    errors += 1
                    print(f"导入行出错: {e}")
        
        self.conn.commit()
        return {
            'imported': imported,
            'duplicates': duplicates,
            'errors': errors
        }


class WeChatAddWorkflow:
    """企微添加工作流（Phase 1手动版）"""
    
    def __init__(self, conn):
        self.conn = conn
    
    def generate_welcome_message(self, guest_name: str, check_out_date: str) -> str:
        """
        生成欢迎语（Phase 1用模板，Phase 2用LLM）
        """
        template = """您好{name}！

感谢您入住锦江嘉州宾馆，希望您在乐山度过美好时光 🌟

现已邀请您加入【嘉州宾馆会员福利群】：
👉 加入后可享受：
• 专属会员折扣
• 优先预订江景房
• 不定期优惠券发放
• 乐山本地旅游攻略

回复"加入"即可入群，期待再次相遇！"""
        
        name = guest_name if guest_name else "贵宾"
        return template.format(name=name, check_out_date=check_out_date)
    
    def generate_coupon_payload(self) -> Dict:
        """生成优惠券信息"""
        return {
            "type": "discount",
            "value": "50元",
            "condition": "满300元可用",
            "valid_days": 30,
            "code": "WELCOME2026"
        }
    
    def prepare_add_queue(self, days_before: int = 0) -> List[Dict]:
        """
        准备添加队列：找出今天（或N天前）离店的客人
        days_before: 0=今天离店, 1=昨天离店, 依此类推
        """
        cursor = self.conn.cursor()
        target_date = datetime.now() - timedelta(days=days_before)
        target_str = target_date.strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT phone, name, last_check_in, source
            FROM guests_from_ota
            WHERE last_check_in = ?
            AND (wechat_id IS NULL OR wechat_id = '')
            AND add_wechat_time IS NULL
        ''', (target_str,))
        
        results = cursor.fetchall()
        queue_items = []
        
        for row in results:
            phone, name, last_check_in, source = row
            queue_items.append({
                'phone': phone,
                'name': name or '',
                'check_out': last_check_in,
                'source': source,
                'welcome_msg': self.generate_welcome_message(name, last_check_in),
                'coupon': self.generate_coupon_payload()
            })
        
        return queue_items
    
    def export_queue_for_manual(self, output_path: str, days_before: int = 0) -> int:
        """
        导出添加队列为Excel，用于人工操作
        Phase 1核心功能
        """
        queue = self.prepare_add_queue(days_before)
        
        if not queue:
            print(f"没有需要添加的客人（{days_before}天前离店）")
            return 0
        
        # 写入CSV（含完整信息，人工操作时一目了然）
        with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'phone', 'name', 'check_out', 'source', 
                'welcome_msg', 'coupon', 'status'
            ])
            writer.writeheader()
            
            for item in queue:
                writer.writerow({
                    **item,
                    'status': '待添加'
                })
        
        # 更新队列状态
        cursor = self.conn.cursor()
        for item in queue:
            cursor.execute('''
                INSERT INTO wechat_add_queue (phone, name, status, scheduled_at)
                VALUES (?, ?, 'pending', ?)
            ''', (item['phone'], item['name'], datetime.now()))
        
        self.conn.commit()
        return len(queue)
    
    def log_operation(self, skill_id: str, action: str, phone: str, result: str):
        """记录操作日志"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO operation_log (skill_id, action, target_phone, result)
            VALUES (?, ?, ?, ?)
        ''', (skill_id, action, phone, result))
        self.conn.commit()


# ============================================================
# Phase 2: 企微API自动版（预留接口）
# ============================================================

class WeComAutoAdd:
    """企微API自动添加（Phase 2）"""
    
    def __init__(self, corp_id: str, secret: str):
        self.corp_id = corp_id
        self.secret = secret
        self.access_token = None
    
    def get_access_token(self) -> str:
        """获取access_token"""
        import requests
        
        url = f"{WECOM_API_URL}gettoken"
        params = {
            'corpid': self.corp_id,
            'corpsecret': self.secret
        }
        
        resp = requests.get(url, params=params)
        data = resp.json()
        
        if data.get('errcode') == 0:
            self.access_token = data['access_token']
            return self.access_token
        else:
            raise Exception(f"获取access_token失败: {data}")
    
    def add_external_contact(self, phone: str, name: str, welcome_msg: str) -> Dict:
        """
        添加外部联系人
        实际需要：
        1. 通过手机号获取userid
        2. 创建外部联系人
        3. 发送欢迎语
        """
        import requests
        
        if not self.access_token:
            self.get_access_token()
        
        url = f"{WECOM_API_URL}externalcontact/add"
        params = {'access_token': self.access_token}
        
        payload = {
            'external_userid': phone,  # 实际应该是外部联系人userid
            'name': name,
            'phone': phone
        }
        
        resp = requests.post(url, params=params, json=payload)
        return resp.json()


# ============================================================
# 主程序（Phase 1手动模式）
# ============================================================

def main():
    """主程序入口"""
    print("=" * 50)
    print("PRIV-001: OTA引流SOP")
    print("=" * 50)
    
    # 初始化数据库
    conn = init_database()
    print("✅ 数据库初始化完成")
    
    # 导入携程数据
    import_tool = OTAImport(conn)
    
    # 示例：导入EBK导出的CSV
    # result = import_tool.import_from_ebk_csv("携程订单导出_2026-03.csv")
    # print(f"导入结果: {result}")
    
    # 生成今日添加队列
    workflow = WeChatAddWorkflow(conn)
    
    # 导出昨天离店的客人（今天拉群）
    output_path = "output/wechat_add_queue_today.csv"
    count = workflow.export_queue_for_manual(output_path, days_before=1)
    
    print(f"✅ 已生成添加队列，共{count}人")
    print(f"📁 文件位置: {output_path}")
    print("\n📋 下一步操作：")
    print("1. 打开CSV文件")
    print("2. 使用企微工作台-客户联系-添加客户")
    print("3. 逐个添加并发送欢迎语")
    print("4. 添加完成后在表格中标注'已添加'")
    print("5. 同步更新数据库状态")


if __name__ == "__main__":
    main()
```

#### PRIV-002：社群自动运营

```python
# -*- coding: utf-8 -*-
"""
PRIV-002: 社群自动运营
功能：基于客人行为事件自动触发消息
Phase: 1（定时轮询+模板消息）
"""

import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import time

# ============================================================
# 配置区
# ============================================================

DB_PATH = "data/guest_private.db"

# 消息发送时间窗口
SEND_WINDOW_START = 9  # 早上9点
SEND_WINDOW_END = 22   # 晚上10点

# 频率限制
MAX_MESSAGES_PER_WEEK = 3

# 事件定义
EVENT_TYPES = {
    'check_in': '入住当天',
    'check_out': '离店当天',
    'review_posted': '点评后',
    'days_7_post_stay': '入住后7天',
    'days_30_post_stay': '入住后30天'
}

# ============================================================
# 消息模板
# ============================================================

MESSAGE_TEMPLATES = {
    'check_in': {
        'title': '🏨 入住欢迎',
        'template': """尊敬的{name}您好，欢迎回家！

您在嘉州宾馆的房间已准备就绪，以下信息助您开启美好旅程：

📍 特色推荐：
• 270度江景房——清晨可观三江汇流
• 宠物友好——毛孩子免费入住
• 附近景点——步行5分钟到乐山大佛

🍳 早餐时间：07:00-10:00（带房卡到1楼餐厅）
📞 紧急联系：0833-2096666

祝您住店愉快！""",
        'media': 'checkin_guide.jpg'
    },
    
    'check_out': {
        'title': '🙏 期待再会',
        'template': """{name}您好，时间过得真快！

感谢您选择嘉州宾馆，希望您在乐山留下了美好回忆 🌟

🧳 退房提示：
• 退房时间：14:00前
• 如需延迟退房可联系前台
• 行李寄存服务免费

⭐ 您已完成入住，如果满意，恳请您在携程/美团给我们一个5星好评
   您的肯定是给我们最大的鼓励！

💝 专属福利：
回复"下次入住"可领取50元优惠券（限30天内使用）

期待与您再次相遇！""",
        'coupon': True
    },
    
    'review_posted': {
        'title': '❤️ 感谢您的肯定',
        'template': """{name}您好，感谢您在百忙之中留下点评！

您的认可让我们更有动力做好每一处细节 💪

🎁 积分发放：
已为您发放100会员积分，可用于：
• 兑换房型升级
• 抵扣餐饮消费
• 换取精美礼品

感谢一路有您，期待下次相遇！""",
        'points': 100
    },
    
    'days_7_post_stay': {
        'title': '🎁 专属优惠',
        'template': """{name}您好，距离您的上次入住已有一周啦！

我们想念您了，也为您准备了一份小小的心意 🎁

✨ 7天专属优惠：
• 订房可享受9折优惠
• 优先安排江景房
• 免费升级（视房态）

📅 有效期：7天
使用方法：预订时出示此消息即可

👉 回复"我要订房"快速预订""",
        'discount': '9折',
        'valid_days': 7
    },
    
    'days_30_post_stay': {
        'title': '🌸 乐山依然在等您',
        'template': """{name}您好，好久不见！

嘉州宾馆的江景依旧美丽，乐山的美食依然诱人 🍜

🌺 30天回馈：
• 复购可享8.5折
• 会员日双倍积分
• 专属管家服务

📞 快速预订：0833-2096666
或者直接回复"订房"告诉我们您的需求

期待您回来！""",
        'discount': '8.5折',
        'valid_days': 30
    }
}

# ============================================================
# 工具函数
# ============================================================

def is_within_send_window() -> bool:
    """检查当前是否在发送时间窗口内"""
    now = datetime.now()
    current_hour = now.hour
    return SEND_WINDOW_START <= current_hour <= SEND_WINDOW_END

def should_send_message(phone: str, event_type: str, conn: sqlite3.Connection) -> bool:
    """
    检查是否应该发送消息（频率控制）
    """
    cursor = conn.cursor()
    one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    
    # 统计过去7天发送的消息数
    cursor.execute('''
        SELECT COUNT(*) FROM message_send_log
        WHERE phone = ?
        AND created_at > ?
    ''', (phone, one_week_ago))
    
    count = cursor.fetchone()[0]
    
    # 如果已达到上限，不发送
    if count >= MAX_MESSAGES_PER_WEEK:
        return False
    
    # 检查是否今天已发送该类型消息（避免重复）
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT COUNT(*) FROM message_send_log
        WHERE phone = ?
        AND event_type = ?
        AND created_at LIKE ?
    ''', (phone, event_type, f'{today}%'))
    
    if cursor.fetchone()[0] > 0:
        return False
    
    return True

def record_message_sent(phone: str, event_type: str, message_id: str, conn: sqlite3.Connection):
    """记录消息发送日志"""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS message_send_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT,
            event_type TEXT,
            message_id TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        INSERT INTO message_send_log (phone, event_type, message_id)
        VALUES (?, ?, ?)
    ''', (phone, event_type, message_id))
    conn.commit()

# ============================================================
# 消息发送引擎
# ============================================================

class CommunityMessageEngine:
    """社群消息发送引擎"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.init_tables()
    
    def init_tables(self):
        """初始化表结构"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS message_send_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT,
                event_type TEXT,
                message_id TEXT,
                status TEXT DEFAULT 'sent',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS message_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT,
                event_type TEXT,
                scheduled_at DATETIME,
                status TEXT DEFAULT 'pending',
                payload TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def generate_message(self, phone: str, event_type: str, guest_name: str = '') -> Dict:
        """
        生成消息内容
        Phase 1: 模板填充
        Phase 2: LLM个性化生成
        """
        template_data = MESSAGE_TEMPLATES.get(event_type)
        if not template_data:
            return None
        
        # 获取客人姓名（如果有）
        if not guest_name:
            cursor = self.conn.cursor()
            cursor.execute('SELECT name FROM guests_from_ota WHERE phone = ?', (phone,))
            row = cursor.fetchone()
            guest_name = row[0] if row else '贵宾'
        
        # 填充模板
        message_body = template_data['template'].format(name=guest_name)
        
        return {
            'title': template_data['title'],
            'body': message_body,
            'event_type': event_type,
            'template_id': event_type
        }
    
    def queue_message(self, phone: str, event_type: str, scheduled_at: datetime = None):
        """将消息加入发送队列"""
        if scheduled_at is None:
            scheduled_at = datetime.now()
        
        message = self.generate_message(phone, event_type)
        if not message:
            return False
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO message_queue (phone, event_type, scheduled_at, payload)
            VALUES (?, ?, ?, ?)
        ''', (phone, event_type, scheduled_at, json.dumps(message)))
        self.conn.commit()
        
        return True
    
    def process_queue(self) -> Dict:
        """
        处理消息队列
        Phase 1: 模拟处理（打印到文件）
        Phase 2: 调用企微API实际发送
        """
        if not is_within_send_window():
            return {'status': 'skipped', 'reason': 'outside send window'}
        
        cursor = self.conn.cursor()
        
        # 获取待发送消息
        cursor.execute('''
            SELECT id, phone, event_type, payload
            FROM message_queue
            WHERE status = 'pending'
            AND scheduled_at <= ?
            ORDER BY scheduled_at ASC
            LIMIT 100
        ''', (datetime.now(),))
        
        rows = cursor.fetchall()
        results = {'sent': 0, 'failed': 0, 'skipped': 0}
        
        for row in rows:
            queue_id, phone, event_type, payload_str = row
            payload = json.loads(payload_str)
            
            # 频率检查
            if not should_send_message(phone, event_type, self.conn):
                cursor.execute(
                    'UPDATE message_queue SET status = ? WHERE id = ?',
                    ('skipped_freq', queue_id)
                )
                results['skipped'] += 1
                continue
            
            try:
                # Phase 1: 输出到文件（模拟发送）
                self._simulate_send(phone, payload)
                
                # 记录发送日志
                record_message_sent(phone, event_type, str(queue_id), self.conn)
                
                # 更新队列状态
                cursor.execute(
                    'UPDATE message_queue SET status = ? WHERE id = ?',
                    ('sent', queue_id)
                )
                results['sent'] += 1
                
                # 添加延时避免频率限制
                time.sleep(0.5)
                
            except Exception as e:
                cursor.execute(
                    'UPDATE message_queue SET status = ? WHERE id = ?',
                    (f'failed:{str(e)}', queue_id)
                )
                results['failed'] += 1
        
        self.conn.commit()
        return results
    
    def _simulate_send(self, phone: str, payload: Dict):
        """
        模拟发送（Phase 1）
        实际部署时替换为企微API调用
        """
        # 输出到文件
        output_file = f"output/messages_{datetime.now().strftime('%Y%m%d')}.txt"
        
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"时间: {datetime.now()}\n")
            f.write(f"收件人: {phone}\n")
            f.write(f"类型: {payload.get('event_type')}\n")
            f.write(f"标题: {payload.get('title')}\n")
            f.write(f"内容:\n{payload.get('body')}\n")
    
    def trigger_event(self, phone: str, event_type: str, delay_hours: int = 0):
        """
        触发事件（由外部系统调用）
        event_type: check_in/check_out/review_posted/days_7_post_stay/days_30_post_stay
        """
        if event_type not in MESSAGE_TEMPLATES:
            raise ValueError(f"不支持的事件类型: {event_type}")
        
        scheduled_at = datetime.now() + timedelta(hours=delay_hours)
        self.queue_message(phone, event_type, scheduled_at)


# ============================================================
# 定时任务（每日运行）
# ============================================================

def daily_trigger():
    """每日定时任务：自动触发需要发送的消息"""
    conn = sqlite3.connect(DB_PATH)
    engine = CommunityMessageEngine(DB_PATH)
    
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    cursor = conn.cursor()
    
    # 1. 触发离店消息（昨天离店的客人，今天发送）
    cursor.execute('''
        SELECT phone, name, last_check_in
        FROM guests_from_ota
        WHERE last_check_in = ?
    ''', (yesterday,))
    
    for row in cursor.fetchall():
        phone, name, _ = row
        engine.trigger_event(phone, 'check_out', delay_hours=10)  # 早上10点发送
    
    # 2. 触发7天复购消息（7天前入住的客人）
    days_7_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT phone, name
        FROM guests_from_ota
        WHERE last_check_in = ?
    ''', (days_7_ago,))
    
    for row in cursor.fetchall():
        phone, name = row
        engine.trigger_event(phone, 'days_7_post_stay', delay_hours=11)  # 早上11点发送
    
    conn.close()
    
    return {'status': 'triggered'}


# ============================================================
# 主程序
# ============================================================

def main():
    """主程序入口"""
    print("=" * 50)
    print("PRIV-002: 社群自动运营")
    print("=" * 50)
    
    engine = CommunityMessageEngine(DB_PATH)
    
    # 演示：触发一条测试消息
    print("\n📤 模拟发送测试消息...")
    engine.trigger_event('13800138000', 'check_in', delay_hours=0)
    
    # 处理队列
    print("\n⚙️ 处理发送队列...")
    result = engine.process_queue()
    print(f"发送结果: {result}")
    
    print("\n✅ 演示完成！")
    print("实际部署时：")
    print("1. 部署为每日定时任务（凌晨跑daily_trigger）")
    print("2. 替换_simulate_send为企微API实际发送")


if __name__ == "__main__":
    main()
```

#### PRIV-003：会员LTV分层管理

```python
# -*- coding: utf-8 -*-
"""
PRIV-003: 会员LTV分层管理
功能：基于RFM模型对会员进行分层
Phase: 1（批量计算）
"""

import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import json
import csv

# ============================================================
# 配置区
# ============================================================

DB_PATH = "data/guest_private.db"
OUTPUT_DIR = "output/ltv_analysis"

# RFM权重
RFM_WEIGHTS = {
    'R': 0.4,  # 最近入住
    'F': 0.3,  # 入住频次
    'M': 0.3   # 消费金额
}

# 分层阈值
TIER_THRESHOLDS = {
    'A': 80,  # Top 5%
    'B': 60,  # Top 6-20%
    'C': 40,  # Top 21-50%
    'D': 0    # Bottom 50%
}

# 分析周期（天）
ANALYSIS_PERIOD_DAYS = 365

# ============================================================
# 工具函数
# ============================================================

def calculate_days_since(date_str: str) -> int:
    """计算距离今天的天数"""
    if not date_str:
        return 999
    try:
        check_date = datetime.strptime(date_str, '%Y-%m-%d')
        return (datetime.now() - check_date).days
    except:
        return 999

def normalize_score(value: float, min_val: float, max_val: float) -> float:
    """
    将值标准化到0-100分
    使用Min-Max归一化
    """
    if max_val == min_val:
        return 50  # 如果所有值相同，返回中间值
    return ((value - min_val) / (max_val - min_val)) * 100

def calculate_rfm_score(r: int, f: int, m: float, 
                        r_max: int, f_max: int, m_max: float,
                        weights: Dict) -> float:
    """
    计算RFM综合得分
    
    参数:
    - r: 最近入住天数（越小越好，所以用100-r标准化）
    - f: 入住频次（越大越好）
    - m: 消费金额（越大越好）
    - r_max, f_max, m_max: 各维度最大值（用于归一化）
    """
    # R分数：最近入住天数越少分数越高
    # 注意：999天没来的，R分数应该是0
    if r >= 365:
        r_score = 0
    else:
        r_score = 100 - normalize_score(r, 0, 365)
    
    # F分数：入住次数越多分数越高
    f_score = normalize_score(f, 0, max(f_max, 1))
    
    # M分数：消费金额越高分数越高
    m_score = normalize_score(m, 0, max(m_max, 1))
    
    # 加权求和
    total_score = (
        weights['R'] * r_score +
        weights['F'] * f_score +
        weights['M'] * m_score
    )
    
    return round(total_score, 2)

def assign_tier(score: float, percentile: float) -> str:
    """
    根据得分和百分位分配会员等级
    
    逻辑：
    - Top 5% → A类（VIP）
    - Top 6-20% → B类（高级会员）
    - Top 21-50% → C类（活跃会员）
    - Bottom 50% → D类（沉睡会员）
    """
    if percentile <= 5:
        return 'A'
    elif percentile <= 20:
        return 'B'
    elif percentile <= 50:
        return 'C'
    else:
        return 'D'

# ============================================================
# LTV分析引擎
# ============================================================

class LTVAnalyzer:
    """会员LTV分析引擎"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
    
    def calculate_guest_rfm(self) -> List[Dict]:
        """
        计算每个客人的RFM指标
        
        返回：
        [{
            'phone': str,
            'name': str,
            'R': int,  # 最近入住天数
            'F': int,  # 入住次数
            'M': float,  # 总消费
            'avg_rate': float,  # 平均房价
            'total_days': int,  # 累计入住天数
            'first_stay': str,  # 首次入住
            'last_stay': str   # 最近入住
        }]
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT 
                phone,
                name,
                first_check_in,
                last_check_in,
                total_stays,
                total_spend,
                source
            FROM guests_from_ota
            WHERE total_stays > 0
            ORDER BY phone
        ''')
        
        results = []
        for row in cursor.fetchall():
            phone, name, first_check_in, last_check_in, total_stays, total_spend, source = row
            
            R = calculate_days_since(last_check_in)
            F = total_stays or 0
            M = total_spend or 0.0
            avg_rate = M / F if F > 0 else 0
            
            results.append({
                'phone': phone,
                'name': name or '',
                'R': R,
                'F': F,
                'M': M,
                'avg_rate': avg_rate,
                'total_days': 0,  # 需要从入住明细计算
                'first_stay': first_check_in,
                'last_stay': last_check_in,
                'source': source
            })
        
        return results
    
    def calculate_ltv_scores(self, guest_data: List[Dict]) -> List[Dict]:
        """
        计算RFM得分并分层
        
        步骤：
        1. 找出各维度的最大值
        2. 对每个客人计算RFM得分
        3. 按得分排序，确定百分位
        4. 分配会员等级
        """
        if not guest_data:
            return []
        
        # Step 1: 找最大值
        r_max = max(g['R'] for g in guest_data)
        f_max = max(g['F'] for g in guest_data)
        m_max = max(g['M'] for g in guest_data)
        
        # Step 2: 计算每个客人的RFM得分
        for guest in guest_data:
            guest['rfm_score'] = calculate_rfm_score(
                guest['R'], guest['F'], guest['M'],
                r_max, f_max, m_max,
                RFM_WEIGHTS
            )
        
        # Step 3: 按得分排序
        sorted_guests = sorted(guest_data, key=lambda x: x['rfm_score'], reverse=True)
        
        # Step 4: 确定百分位并分配等级
        total = len(sorted_guests)
        for idx, guest in enumerate(sorted_guests):
            percentile = ((total - idx) / total) * 100
            guest['percentile'] = percentile
            guest['tier'] = assign_tier(guest['rfm_score'], percentile)
            guest['rank'] = idx + 1
        
        return sorted_guests
    
    def generate_tier_summary(self, scored_guests: List[Dict]) -> Dict:
        """生成各层级汇总统计"""
        tier_stats = {
            'A': {'count': 0, 'total_spend': 0, 'avg_spend': 0, 'avg_stays': 0},
            'B': {'count': 0, 'total_spend': 0, 'avg_spend': 0, 'avg_stays': 0},
            'C': {'count': 0, 'total_spend': 0, 'avg_spend': 0, 'avg_stays': 0},
            'D': {'count': 0, 'total_spend': 0, 'avg_spend': 0, 'avg_stays': 0}
        }
        
        for guest in scored_guests:
            tier = guest['tier']
            tier_stats[tier]['count'] += 1
            tier_stats[tier]['total_spend'] += guest['M']
        
        # 计算平均值
        for tier in tier_stats:
            stats = tier_stats[tier]
            if stats['count'] > 0:
                stats['avg_spend'] = stats['total_spend'] / stats['count']
                
                # 计算平均入住次数
                tier_guests = [g for g in scored_guests if g['tier'] == tier]
                stats['avg_stays'] = sum(g['F'] for g in tier_guests) / stats['count']
        
        return tier_stats
    
    def export_results(self, scored_guests: List[Dict], output_dir: str):
        """导出分析结果"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d')
        
        # 1. 导出全量数据CSV
        csv_path = f"{output_dir}/guests_ltv_{timestamp}.csv"
        
        with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
            fieldnames = [
                'rank', 'phone', 'name', 'tier', 'rfm_score',
                'R', 'F', 'M', 'avg_rate',
                'percentile', 'first_stay', 'last_stay', 'source'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for guest in scored_guests:
                writer.writerow({
                    'rank': guest['rank'],
                    'phone': guest['phone'],
                    'name': guest['name'],
                    'tier': guest['tier'],
                    'rfm_score': guest['rfm_score'],
                    'R': guest['R'],
                    'F': guest['F'],
                    'M': round(guest['M'], 2),
                    'avg_rate': round(guest['avg_rate'], 2),
                    'percentile': round(guest['percentile'], 1),
                    'first_stay': guest['first_stay'],
                    'last_stay': guest['last_stay'],
                    'source': guest['source']
                })
        
        # 2. 导出分层汇总
        tier_stats = self.generate_tier_summary(scored_guests)
        summary_path = f"{output_dir}/tier_summary_{timestamp}.json"
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'total_guests': len(scored_guests),
                'tier_stats': tier_stats,
                'rfm_weights': RFM_WEIGHTS
            }, f, ensure_ascii=False, indent=2)
        
        # 3. 导出VIP名单（A类和B类）
        vip_path = f"{output_dir}/vip_guests_{timestamp}.csv"
        
        with open(vip_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['rank', 'phone', 'name', 'tier', 'rfm_score', 'M', 'F'])
            writer.writeheader()
            
            for guest in scored_guests:
                if guest['tier'] in ['A', 'B']:
                    writer.writerow({
                        'rank': guest['rank'],
                        'phone': guest['phone'],
                        'name': guest['name'],
                        'tier': guest['tier'],
                        'rfm_score': guest['rfm_score'],
                        'M': round(guest['M'], 2),
                        'F': guest['F']
                    })
        
        return {
            'csv_path': csv_path,
            'summary_path': summary_path,
            'vip_path': vip_path
        }
    
    def update_member_levels(self, scored_guests: List[Dict]):
        """更新数据库中的会员等级"""
        cursor = self.conn.cursor()
        
        for guest in scored_guests:
            cursor.execute('''
                UPDATE guests_from_ota
                SET member_level = ?
                WHERE phone = ?
            ''', (guest['tier'], guest['phone']))
        
        self.conn.commit()
    
    def run_full_analysis(self, output_dir: str = OUTPUT_DIR) -> Dict:
        """
        运行完整的LTV分析
        """
        print("=" * 50)
        print("PRIV-003: 会员LTV分层分析")
        print("=" * 50)
        
        # Step 1: 获取数据
        print("\n📊 Step 1: 获取会员数据...")
        guest_data = self.calculate_guest_rfm()
        print(f"   共获取 {len(guest_data)} 位有效会员")
        
        if not guest_data:
            print("   ⚠️ 没有足够的入住数据进行分析")
            return {'status': 'no_data'}
        
        # Step 2: 计算RFM得分并分层
        print("\n📈 Step 2: 计算RFM得分...")
        scored_guests = self.calculate_ltv_scores(guest_data)
        
        # 显示各层级分布
        tier_counts = {}
        for g in scored_guests:
            tier = g['tier']
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        
        for tier in ['A', 'B', 'C', 'D']:
            count = tier_counts.get(tier, 0)
            pct = count / len(scored_guests) * 100 if scored_guests else 0
            print(f"   {tier}类: {count}人 ({pct:.1f}%)")
        
        # Step 3: 更新数据库
        print("\n💾 Step 3: 更新会员等级...")
        self.update_member_levels(scored_guests)
        print("   ✅ 等级已更新")
        
        # Step 4: 导出结果
        print("\n📁 Step 4: 导出分析结果...")
        paths = self.export_results(scored_guests, output_dir)
        
        for key, path in paths.items():
            print(f"   {key}: {path}")
        
        # Step 5: 生成策略建议
        print("\n💡 Step 5: 营销策略建议:")
        self.print_strategy_recommendations(scored_guests)
        
        self.conn.close()
        
        return {
            'status': 'completed',
            'total_guests': len(scored_guests),
            'tier_counts': tier_counts,
            'output_files': paths
        }
    
    def print_strategy_recommendations(self, scored_guests: List[Dict]):
        """打印各层级的营销策略建议"""
        recommendations = {
            'A': [
                "🎯 1V1专属管家服务",
                "🎁 生日专属礼包/免费升房",
                "📞 总经理直接跟进投诉",
                "💎 每年一次免费体验入住"
            ],
            'B': [
                "⭐ 专属VIP折扣（9折）",
                "🎂 生日月双倍积分",
                "📬 优先预订江景房/套房",
                "🏷️ 专属会员日活动邀请"
            ],
            'C': [
                "🎫 定期优惠券推送（每月1次）",
                "🌟 新菜品/新设施优先体验邀请",
                "📱 社群专属活动参与资格"
            ],
            'D': [
                "📧 低频唤醒邮件（每季度1次）",
                "💰 大额唤醒优惠（5折起）",
                "📞 问卷调研收集流失原因"
            ]
        }
        
        tier_stats = self.generate_tier_summary(scored_guests)
        
        for tier in ['A', 'B', 'C', 'D']:
            count = tier_stats[tier]['count']
            avg_spend = tier_stats[tier]['avg_spend']
            
            print(f"\n【{tier}类会员】（{count}人，平均消费¥{avg_spend:.0f}）")
            for rec in recommendations[tier]:
                print(f"  {rec}")


# ============================================================
# 主程序
# ============================================================

def main():
    """主程序入口"""
    analyzer = LTVAnalyzer(DB_PATH)
    result = analyzer.run_full_analysis()
    
    print("\n" + "=" * 50)
    print("分析完成！")
    print("=" * 50)
    
    return result


if __name__ == "__main__":
    main()
```

---

### 乐山落地行动清单

#### 第一周：基础设施准备

| 序号 | 行动项 | 负责方 | 完成标准 | 优先级 |
|------|--------|--------|----------|--------|
| 1 | 酒店开通企业微信 | 酒店方 | 企微后台可登录 | P0 |
| 2 | 创建【嘉州宾馆会员福利群】 | 酒店方 | 群已建立，1期目标200人 | P0 |
| 3 | 申请携程EBK数据导出权限 | 酒店方+ Eric | 联系携程BD获取导出功能 | P0 |
| 4 | 导出历史订单（过去6个月） | 酒店方 | 获取Excel文件 | P0 |
| 5 | 安装Python环境（如未安装） | 技术方 | python3可运行 | P0 |
| 6 | 初始化SQLite数据库 | 技术方 | guest_private.db已创建 | P0 |

#### 第二周：数据导入+手动流程跑通

| 序号 | 行动项 | 负责方 | 完成标准 | 优先级 |
|------|--------|--------|----------|--------|
| 7 | 导入携程历史订单到SQLite | 技术方 | 数据显示正常 | P1 |
| 8 | 运行PRIV-001导出添加队列 | 技术方 | CSV文件生成 | P1 |
| 9 | 酒店人员执行企微添加 | 酒店方 | 添加率>60% | P1 |
| 10 | 确认社群活跃度（进群率） | 酒店方 | 进群率>50% | P1 |

#### 第三周：社群运营启动

| 序号 | 行动项 | 负责方 | 完成标准 | 优先级 |
|------|--------|--------|----------|--------|
| 11 | 准备欢迎语+优惠券 | 酒店方 | 话术确认，优惠券到位 | P1 |
| 12 | 首次社群消息发送（欢迎） | 酒店方 | 发送成功，无投诉 | P1 |
| 13 | 设置每日添加队列导出 | 技术方 | 定时任务跑通 | P2 |
| 14 | 运行PRIV-003首次LTV分析 | 技术方 | 分层结果产出 | P2 |

#### 第四周及以后：持续优化

| 序号 | 行动项 | 负责方 | 完成标准 | 优先级 |
|------|--------|--------|----------|--------|
| 15 | 分析添加转化率，优化话术 | 双方 | 转化率提升至70% | P2 |
| 16 | 根据LTV分层制定VIP权益 | 酒店方 | A/B类会员权益确定 | P2 |
| 17 | 启动离店自动触达 | 技术方 | 流程自动化 | P2 |
| 18 | Phase 2规划：PMS API对接 | 技术方 | 方案确定，启动开发 | P3 |

---

### 关键成功指标（KPI）

| 阶段 | 指标 | 目标值 | 测量方式 |
|------|------|--------|----------|
| Phase 1 | 私域沉淀量 | 6个月内沉淀1000+会员 | SQLite记录数 |
| Phase 1 | 添加通过率 | >60% | 成功添加/尝试添加 |
| Phase 1 | 进群转化率 | >50% | 进群人数/添加成功数 |
| Phase 2 | 月活跃率 | >30%（每月有互动） | 消息打开率 |
| Phase 2 | 复购率 | 私域会员复购率>15% | 二次订单数/总会员数 |
| Phase 3 | LTV提升 | A类会员LTV提升20% | 年度消费对比 |

---

### 风险与应对

| 风险 | 可能性 | 影响 | 应对措施 |
|------|--------|------|----------|
| 酒店不愿意用企微 | 中 | 高 | 强调免费+降低工作量；先从个人微信过渡 |
| 客人不愿意加企微 | 中 | 中 | 提供明确价值（优惠券）；话术优化 |
| 携程限制数据导出 | 低 | 高 | 尝试API对接；人工手动导出备选 |
| 过度营销导致取关 | 高 | 中 | 严格遵守频率限制；内容优先于推销 |
| 员工执行力不足 | 中 | 中 | 简化流程；设置提醒机制 |

---

**文档状态**: ✅ V1.0完成
**下一步**: 与酒店方确认企微开通和数据导出权限后启动Phase 1
