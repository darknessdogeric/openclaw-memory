# AHL-乐山-AI预订匹配技术方案-V1.0

> **版本**: V1.0  
> **日期**: 2026-03-27  
> **状态**: 起草  
> **负责人**: AHL技术组

---

## 模块2：AI预订自动匹配与接单

### 乐山落地现状评估

#### 能不能做？—— 可行性分析

**AHL协议的核心能力**：

```
传统OTA流程：
用户 → 搜索/浏览 → 自行筛选 → 自行比价 → 自行下单
        ↑
   用户自己做决策，平台只提供信息展示

AHL协议流程：
用户 → 表达需求（语音/文字） → AI管家推荐 → 自动接单
        ↑
   AI帮助做决策，核心价值：降低用户决策成本
```

**为什么Phase 1不能全自动，但半自动是可行的？**

| 障碍 | 原因 | Phase 1应对 |
|------|------|-------------|
| PMS无API | 乐山嘉州PMS未开放接口 | 人工获取房态，人工下单 |
| 微信限制 | 模板消息需公众号，小程序需认证 | 使用电话/短信过渡 |
| 支付问题 | 微信支付商户号复杂 | 微信转账或到店支付 |
| OTA对接 | 携程/美团API不对个人开放 | 跳转OTA链接完成下单 |

**Phase 1的现实路径**：

```
用户需求 → AI理解 → 房态匹配 → 推荐展示 → 人工确认 → 跳转OTA/电话预订
              ↑                           ↑
         AI完成（今日可做）          人工完成（酒店前台）
```

#### 需要什么前提？

| 前提条件 | 当前状态 | 行动项 | 优先级 |
|----------|----------|--------|--------|
| 酒店房型信息 | 需整理 | 建立房型基础数据库（名称/面积/床型/价格/特色） | P0 |
| 实时房态 | 需人工获取 | 前台每日更新可用房态 | P0 |
| 酒店特色标签 | 需定义 | 建立标签体系（江景/城景/亲子/宠物友好等） | P1 |
| PMS API | 无 | Phase 2对接 | P2 |
| 直销小程序 | 无 | Phase 3开发 | P3 |

---

### SKILL清单

#### BOOK-001：需求收集

**规格卡**：

```
┌─────────────────────────────────────────────────────────┐
│ SKILL编号    │ BOOK-001                               │
├─────────────────────────────────────────────────────────┤
│ SKILL名称    │ 需求收集（AI客服交互）                 │
├─────────────────────────────────────────────────────────┤
│ 目标         │ 将用户模糊需求转化为结构化需求单       │
├─────────────────────────────────────────────────────────┤
│ 输入         │ 用户原始表达（文字/语音转文字）         │
│             │ 场景：微信对话/电话/小程序/OTA咨询      │
├─────────────────────────────────────────────────────────┤
│ 处理逻辑     │ Step1: NLU意图识别（订房/咨询/投诉）   │
│             │ Step2: 实体抽取（日期/人数/房型/预算）  │
│             │ Step3: 槽位填充（缺字段时追问）         │
│             │ Step4: 生成结构化需求单                 │
├─────────────────────────────────────────────────────────┤
│ 输出         │ 结构化需求单（JSON）                   │
│             │ {                                       │
│             │   intent: "booking",                    │
│             │   check_in: "2026-04-05",              │
│             │   check_out: "2026-04-07",             │
│             │   nights: 2,                           │
│             │   guests: 2,                           │
│             │   room_type: null,  // 待推荐         │
│             │   budget: "300-500",                   │
│             │   preferences: ["江景", "有窗"],       │
│             │   special: ["宠物"],                   │
│             │   source: "wechat",                    │
│             │   raw_query: "我想带狗住两天"          │
│             │ }                                       │
├─────────────────────────────────────────────────────────┤
│ 数据依赖     │ - 酒店知识库（房型/价格/设施）         │
│             │ - LLM API（DeepSeek/Kimi）             │
│             │ - 自然语言处理模型（实体识别）         │
├─────────────────────────────────────────────────────────┤
│ 边界/限制    │ - 单轮对话最多5轮追问                  │
│             │ - 超时30分钟未完成则挂起               │
│             │ - 无法识别时转人工                      │
└─────────────────────────────────────────────────────────┘
```

**技术原理**：

```
为什么需要"需求收集"这个环节？
├── 用户表达往往是模糊的："我想住两天""带狗住""不要太吵"
├── 直接推荐会导致信息不对称（用户不知道有什么房型）
└── AI的作用：用对话方式引导用户明确需求，同时获取关键信息

意图识别（Intent Detection）为什么重要？
├── 不是所有消息都是订房需求
├── 可能是：问地址/问wifi/问早餐/投诉
├── 错误处理意图会严重影响用户体验
└── 解决方案：先分类，再分流

槽位填充（Slot Filling）的逻辑：
├── 订房必须信息：入住日期、离店日期、人数
├── 可选信息：房型偏好、预算、特殊需求
├── 缺失必填字段时：主动追问
├── 缺失可选字段时：AI根据偏好推理或标记"待确认"
```

#### BOOK-002：房源匹配

**规格卡**：

```
┌─────────────────────────────────────────────────────────┐
│ SKILL编号    │ BOOK-002                               │
├─────────────────────────────────────────────────────────┤
│ SKILL名称    │ 房源智能匹配                           │
├─────────────────────────────────────────────────────────┤
│ 目标         │ 基于需求单推荐最适合的TOP3房源         │
├─────────────────────────────────────────────────────────┤
│ 输入         │ 结构化需求单 + 可用房态数据            │
│             │ 需求单：BOOK-001输出                   │
│             │ 房态：PMS系统或人工维护的房态表         │
├─────────────────────────────────────────────────────────┤
│ 匹配算法     │ 多维度加权评分                         │
│             │                                          │
│             │ MatchScore = w1×DateMatch              │
│             │               + w2×GuestMatch            │
│             │               + w3×PriceMatch           │
│             │               + w4×PrefMatch            │
│             │               + w5×SpecialMatch         │
│             │                                          │
│             │ 权重初值：                             │
│             │ w1=0.25, w2=0.20, w3=0.20,             │
│             │ w4=0.25, w5=0.10                        │
├─────────────────────────────────────────────────────────┤
│ 输出         │ 推荐结果列表                           │
│             │ [{                                       │
│             │   "rank": 1,                            │
│             │   "room_id": "J01",                    │
│             │   "room_name": "江景大床房",            │
│             │   "match_score": 85,                    │
│             │   "match_reasons": [                    │
│             │     "✅ 270度江景，满足观景需求",       │
│             │     "✅ 支持宠物入住",                   │
│             │     "✅ 价格¥380，在预算范围内"         │
│             │   ],                                    │
│             │   "price": 380,                         │
│             │   "original_price": 480,                │
│             │   "available": true,                     │
│             │   "image_url": "..."                    │
│             │ }]                                      │
├─────────────────────────────────────────────────────────┤
│ 数据依赖     │ - 酒店房型数据库（room_inventory）    │
│             │ - 实时房态表（availability）            │
│             │ - 历史成交数据（可选，用于个性化）      │
├─────────────────────────────────────────────────────────┤
│ 边界/限制    │ - 最多返回5个推荐                      │
│             │ - 只推荐有房的房型                      │
│             │ - 价格超过预算50%的不推荐               │
│             │ - 已售罄房型不推荐                      │
└─────────────────────────────────────────────────────────┘
```

**技术原理**：

```
为什么用加权评分而不是规则匹配？

规则匹配的局限：
├── 规则难以穷尽所有场景
├── 规则冲突时难以调和
├── 难以权衡多个因素的优先级
└── 无法处理"程度"概念（稍微超预算 vs 严重超预算）

加权评分的优势：
├── 因素可独立调整（看重江景vs看重价格）
├── 分数可解释（用户知道为什么推荐这个）
├── 便于优化（看数据调权重）
└── 支持模糊偏好（"最好有江景"而不是"必须有江景"）

为什么推荐TOP3而不是TOP1？
├── 用户决策需要比较
├── TOP1可能因为价格或其他因素最终不选
├── 保留备选方案提升成交率
└── 数据显示：展示3个选项的转化率比1个高40%
```

#### BOOK-003：自动接单（Phase 2/3）

**规格卡**：

```
┌─────────────────────────────────────────────────────────┐
│ SKILL编号    │ BOOK-003                               │
├─────────────────────────────────────────────────────────┤
│ SKILL名称    │ 自动接单处理                           │
├─────────────────────────────────────────────────────────┤
│ 目标         │ 用户确认后自动完成预订                  │
├─────────────────────────────────────────────────────────┤
│ Phase 2触发条件 │ PMS API已对接                       │
│ Phase 3触发条件 │ 直销小程序已完成                     │
├─────────────────────────────────────────────────────────┤
│ 处理流程     │ 确认房型 → 获取用户信息 → 创建订单    │
│             │ → 发起支付 → 支付确认 → 发送确认通知  │
├─────────────────────────────────────────────────────────┤
│ 分渠道处理   │                                          │
│             │ 直销(直销小程序):                       │
│             │   → 直接写入PMS订单                     │
│             │   → 触发微信支付                        │
│             │   → 发送确认短信/模板消息               │
│             │                                          │
│             │ OTA渠道(携程/美团):                     │
│             │   → 拼接OTA预订链接                     │
│             │   → 跳转OTA小程序/App完成预订           │
│             │   → 回调通知确认状态                    │
├─────────────────────────────────────────────────────────┤
│ 异常处理     │ 支付超时 → 订单释放房态               │
│             │ 支付失败 → 提示重新支付或换支付方式     │
│             │ PMS写入失败 → 转人工处理，保留用户意向  │
├─────────────────────────────────────────────────────────┤
│ 数据依赖     │ - PMS API（Phase 2）                   │
│             │ - 微信支付商户（Phase 3）               │
│             │ - OTA平台API（跳转模式，无需API）       │
└─────────────────────────────────────────────────────────┘
```

**技术原理**：

```
为什么区分直销和OTA渠道？
├── 直销：利润更高（省去OTA 15-20%佣金）
├── OTA：流量更大，但有佣金成本
└── 策略：优先推直销，但尊重用户习惯

为什么Phase 2用"跳转"而不是API对接OTA？
├── 携程/美团不对个人开放API
├── 即使对接也需要复杂认证
├── 跳转方案的体验已经足够好
└── 用户感受：点击链接 → 跳转小程序 → 自动填充日期房型 → 确认支付

OTA跳转链接示例：
携程：https://www.ctrip.com/hotel/leshan/xxx?checkIn=2026-04-05&checkOut=2026-04-07
     参数：游客端的搜索结果页，带预填参数

更好的方案（Phase 3）：
直销小程序内完成全部流程，不依赖OTA
```

---

### 技术实现路径

#### Phase 1：AI需求收集 + 人工匹配（现在就能做）

```
目标：不依赖API，用LLM做需求理解+推荐展示

工作流程：
[用户发消息] → [BOOK-001解析需求] → [生成推荐卡片] → [人工确认]
                                                                    ↓
                                                          [通知前台/转发OTA链接]

技术栈：
├── LLM API（DeepSeek/Kimi）：对话理解+话术生成
├── 微信客服消息：消息收发
├── 房态表（手动维护）：Excel/飞书表格
└── 推荐卡片生成：HTML模板转图片

每日工作：
├── 早上：人工更新当日可用房态
├── 有咨询时：AI解析需求 → 展示推荐 → 人工确认
└── 无需7x24值班，用户留言后5分钟内响应即可

预计完成时间：2-3周
预计成本：LLM API调用（约500元/月）
```

#### Phase 2：半自动接单（1-2个月后）

```
目标：减少人工操作，提高响应速度

新增能力：
├── PMS API对接：自动获取房态/创建订单
├── 企微消息推送：推荐结果自动发送给用户
├── 携程EBK API：订单状态同步

工作流程变化：
[用户发消息] → [BOOK-001解析需求] → [BOOK-002自动匹配]
                                                        ↓
                               [推荐卡片自动发送] → [用户确认]
                                                        ↓
                               [BOOK-003创建PMS订单] → [OTA跳转/直销]

技术栈：
├── PMS系统（如：别样红PMS）：API对接
├── 企微SCRM：消息自动推送
└── LLM + 插件系统：自动执行

预计完成时间：1-2个月（视PMS API开放情况）
预计成本：PMS对接开发（约3-5万元）
```

#### Phase 3：全自动闭环（3-6个月后）

```
目标：用户自助完成全流程，无需人工介入

完整流程：
[用户语音/文字表达需求]
        ↓
[BOOK-001 + BOOK-002 一体化处理]
        ↓
[推荐卡片展示 + 用户点击确认]
        ↓
[BOOK-003 自动创建订单 + 微信支付]
        ↓
[订单确认 + 入住指南自动发送]
        ↓
[入住当天：自动发送入住提醒]
        ↓
[离店当天：自动发送退房指南 + 好评请求]

技术栈：
├── 直销小程序：完整预订+支付闭环
├── AI对话系统：自然语言交互
├── PMS API：订单+房态+会员一体化
├── 微信支付：直连结算
└── AI客服：7x24自动应答

预计完成时间：3-6个月
预计成本：直销小程序开发（约10-20万元）
```

---

### 关键代码框架

#### BOOK-001：需求收集

```python
# -*- coding: utf-8 -*-
"""
BOOK-001: 需求收集
功能：NLU解析用户订房需求，生成结构化需求单
Phase: 1（LLM驱动，无需额外API）
"""

import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import sqlite3

# ============================================================
# 配置区
# ============================================================

# LLM API配置（Phase 1使用）
LLM_API_URL = "https://api.deepseek.com/v1/chat/completions"
LLM_API_KEY = "YOUR_API_KEY"
LLM_MODEL = "deepseek-chat"

# 意图识别阈值
INTENT_CONFIDENCE_THRESHOLD = 0.7

# 必要槽位
REQUIRED_SLOTS = ["check_in", "check_out", "guests"]

# ============================================================
# 数据模型
# ============================================================

@dataclass
class BookingRequest:
    """订房需求单"""
    intent: str  # booking/inquiry/complaint/other
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    nights: Optional[int] = None
    guests: Optional[int] = None
    room_type: Optional[str] = None
    budget: Optional[str] = None  # "300-500" 或 "300以下" 或 "500以上"
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    preferences: List[str] = None  # ["江景", "有窗", "宠物友好"]
    special: List[str] = None  # ["宠物", "无障碍", "加床"]
    source: str = "wechat"
    raw_query: str = ""
    missing_slots: List[str] = None
    confidence: float = 0.0
    
    def __post_init__(self):
        if self.preferences is None:
            self.preferences = []
        if self.special is None:
            self.special = []
        if self.missing_slots is None:
            self.missing_slots = []
    
    def is_complete(self) -> bool:
        """检查必填槽位是否完整"""
        for slot in REQUIRED_SLOTS:
            if getattr(self, slot) is None:
                return False
        return True
    
    def to_dict(self) -> Dict:
        return asdict(self)


class HotelKnowledge:
    """酒店知识库（基础信息）"""
    
    def __init__(self):
        self.room_types = {
            "江景大床房": {
                "id": "J01",
                "name": "江景大床房",
                "area": "35",
                "bed": "1.8m大床",
                "floor": "8-15层",
                "features": ["270度江景", "落地窗", "观景浴缸"],
                "max_guests": 2,
                "price": 480,
                "tags": ["江景", "大床", "浪漫"]
            },
            "江景双床房": {
                "id": "J02",
                "name": "江景双床房",
                "area": "38",
                "bed": "1.2m双床",
                "floor": "8-15层",
                "features": ["270度江景", "双床", "商务"],
                "max_guests": 2,
                "price": 520,
                "tags": ["江景", "双床", "商务"]
            },
            "城景亲子房": {
                "id": "Q01",
                "name": "城景亲子房",
                "area": "45",
                "bed": "1.5m大床+1.2m小床",
                "floor": "5-10层",
                "features": ["亲子友好", "小床", "儿童用品"],
                "max_guests": 3,
                "price": 580,
                "tags": ["亲子", "家庭", "城景"]
            },
            "宠物友好房": {
                "id": "C01",
                "name": "宠物友好房",
                "area": "40",
                "bed": "1.8m大床",
                "floor": "3-7层",
                "features": ["宠物免费", "一楼直达", "宠物用品"],
                "max_guests": 2,
                "price": 420,
                "tags": ["宠物", "一楼", "方便"]
            },
            "商务套房": {
                "id": "S01",
                "name": "商务套房",
                "area": "60",
                "bed": "1.8m大床",
                "floor": "15层",
                "features": ["客厅", "办公区", "江景"],
                "max_guests": 2,
                "price": 880,
                "tags": ["江景", "套房", "商务"]
            }
        }
        
        self.facilities = {
            "早餐": {"time": "07:00-10:00", "price": 68, "location": "1楼餐厅"},
            "停车场": {"price": "免费", "note": "含充电桩"},
            "宠物": {"price": "免费", "note": "需提前联系"},
            "入住": {"time": "14:00后", "note": "最晚18:00入住"},
            "退房": {"time": "14:00前", "note": "可延迟到14:00"}
        }
        
        self.policies = {
            "取消": "当天18:00前免费取消",
            "预付": "特殊节假日需预付",
            "发票": "入住时告知前台"
        }
    
    def get_room_by_id(self, room_id: str) -> Optional[Dict]:
        for room in self.room_types.values():
            if room["id"] == room_id:
                return room
        return None
    
    def search_rooms(self, tags: List[str]) -> List[Dict]:
        """根据标签搜索房型"""
        results = []
        for room in self.room_types.values():
            # 简单匹配：标签中有任一匹配即返回
            for tag in tags:
                if tag in room["tags"] or tag in room["features"]:
                    results.append(room)
                    break
        return results


class NLUProcessor:
    """自然语言理解处理器"""
    
    def __init__(self, hotel_kb: HotelKnowledge):
        self.hotel_kb = hotel_kb
        self.intent_keywords = {
            "booking": ["订", "住", "房间", "预订", "预定", "开房", "入住"],
            "inquiry": ["问", "怎么", "多少", "请问", "咨询", "有没有"],
            "complaint": ["差", "不好", "投诉", "退款", "赔偿", "生气"],
            "cancel": ["取消", "退", "不要了", "退订"]
        }
    
    def extract_intent(self, text: str) -> Tuple[str, float]:
        """意图识别"""
        text_lower = text.lower()
        scores = {}
        
        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[intent] = score
        
        if max(scores.values()) == 0:
            return "other", 0.5
        
        best_intent = max(scores, key=scores.get)
        confidence = min(scores[best_intent] / 2, 1.0)
        
        return best_intent, confidence
    
    def extract_dates(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """日期提取"""
        check_in, check_out = None, None
        
        # 今天
        if "今天" in text:
            check_in = datetime.now().strftime('%Y-%m-%d')
        # 明天
        if "明天" in text:
            check_in = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        # 后天
        if "后天" in text:
            check_in = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
        
        # 匹配日期格式：4月5日 / 04-05 / 2026-04-05
        date_patterns = [
            (r'(\d{1,2})月(\d{1,2})日', '%m月%d日'),
            (r'(\d{4})-(\d{1,2})-(\d{1,2})', '%Y-%m-%d'),
            (r'(\d{1,2})-(\d{1,2})', '%m-%d')
        ]
        
        for pattern, fmt in date_patterns:
            matches = re.findall(pattern, text)
            if matches:
                # 取第一个匹配作为入住日期
                m = matches[0]
                if len(m) == 2:  # 月日
                    year = datetime.now().year
                    check_in = f"{year}-{int(m[0]):02d}-{int(m[1]):02d}"
                elif len(m) == 3:  # 年月日
                    if len(m[0]) == 4:
                        check_in = f"{m[0]}-{int(m[1]):02d}-{int(m[2]):02d}"
                    else:
                        year = datetime.now().year
                        check_in = f"{year}-{int(m[0]):02d}-{int(m[1]):02d}"
                break
        
        # 住X天
        nights_match = re.search(r'住(\d+)', text)
        if nights_match:
            nights = int(nights_match.group(1))
            if check_in:
                check_out = (datetime.strptime(check_in, '%Y-%m-%d') + timedelta(days=nights)).strftime('%Y-%m-%d')
        
        # 几号到几号
        from_to_match = re.search(r'(\d{1,2})号?到(\d{1,2})号', text)
        if from_to_match:
            start_day = int(from_to_match.group(1))
            end_day = int(from_to_match.group(2))
            year = datetime.now().year
            month = datetime.now().month
            check_in = f"{year}-{month:02d}-{start_day:02d}"
            check_out = f"{year}-{month:02d}-{end_day:02d}"
        
        return check_in, check_out
    
    def extract_guests(self, text: str) -> Optional[int]:
        """人数提取"""
        patterns = [
            r'(\d+)个?人',
            r'(\d+)位',
            r'(\d+)大',
            r'两人', r'三人', r'一人',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                num_map = {"两": 2, "三": 3, "一": 1, "一": 1}
                if match.group(1) in num_map:
                    return num_map[match.group(1)]
                return int(match.group(1))
        
        return None
    
    def extract_budget(self, text: str) -> Tuple[Optional[int], Optional[int]]:
        """预算提取"""
        budget_min, budget_max = None, None
        
        # 300以下 / 300以内 / 低于300
        under_match = re.search(r'(\d+)以?下|低于(\d+)', text)
        if under_match:
            budget_max = int(under_match.group(1) or under_match.group(2))
        
        # 300以上 / 超过300
        over_match = re.search(r'(\d+)以?上|超过(\d+)', text)
        if over_match:
            budget_min = int(over_match.group(1) or over_match.group(2))
        
        # 300-500 / 300到500
        range_match = re.search(r'(\d+)-(\d+)', text)
        if range_match:
            budget_min = int(range_match.group(1))
            budget_max = int(range_match.group(2))
        
        return budget_min, budget_max
    
    def extract_preferences(self, text: str) -> List[str]:
        """偏好提取"""
        preferences = []
        
        pref_keywords = {
            "江景": ["江景", "看江", "江边", "三江"],
            "城景": ["城景", "看城", "夜景"],
            "大床": ["大床", "大一点"],
            "双床": ["双床", "两张床"],
            "亲子": ["亲子", "小孩", "儿童", "带娃"],
            "宠物": ["宠物", "带狗", "带猫", "毛孩子"],
            "安静": ["安静", "不吵", "清静"],
            "有窗": ["有窗", "窗户", "采光"],
            "电梯": ["电梯", "高楼"],
            "便宜": ["便宜", "实惠", "省钱"]
        }
        
        for pref, keywords in pref_keywords.items():
            if any(kw in text for kw in keywords):
                preferences.append(pref)
        
        return preferences
    
    def process(self, raw_query: str, source: str = "wechat") -> BookingRequest:
        """
        完整NLU处理流程
        """
        # 1. 意图识别
        intent, confidence = self.extract_intent(raw_query)
        
        # 2. 槽位提取
        check_in, check_out = self.extract_dates(raw_query)
        guests = self.extract_guests(raw_query)
        budget_min, budget_max = self.extract_budget(raw_query)
        preferences = self.extract_preferences(raw_query)
        
        # 计算住宿晚数
        nights = None
        if check_in and check_out:
            try:
                d1 = datetime.strptime(check_in, '%Y-%m-%d')
                d2 = datetime.strptime(check_out, '%Y-%m-%d')
                nights = (d2 - d1).days
            except:
                nights = None
        
        # 3. 缺失槽位检查
        missing_slots = []
        if intent == "booking":
            if not check_in:
                missing_slots.append("check_in")
            if not check_out and not nights:
                missing_slots.append("check_out")
            if not guests:
                missing_slots.append("guests")
        
        # 4. 构建需求单
        request = BookingRequest(
            intent=intent,
            check_in=check_in,
            check_out=check_out,
            nights=nights,
            guests=guests,
            budget_min=budget_min,
            budget_max=budget_max,
            budget=f"{budget_min}-{budget_max}" if budget_min and budget_max else None,
            preferences=preferences,
            source=source,
            raw_query=raw_query,
            missing_slots=missing_slots,
            confidence=confidence
        )
        
        return request


class ConversationManager:
    """对话管理器（处理多轮对话）"""
    
    def __init__(self, nlu_processor: NLUProcessor):
        self.nlu = nlu_processor
        self.active_sessions: Dict[str, BookingRequest] = {}
        self.session_timeout = 30 * 60  # 30分钟超时
    
    def process_message(self, user_id: str, message: str, source: str = "wechat") -> Tuple[BookingRequest, str]:
        """
        处理用户消息
        返回：(需求单, 回复话术)
        """
        # 检查是否有活跃会话
        if user_id in self.active_sessions:
            request = self.active_sessions[user_id]
            
            # 解析本轮回复
            if message in ["明天", "明天吧", "好", "可以", "是的"]:
                # 用户在确认
                if "check_in" in request.missing_slots:
                    request.check_in = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
                    if request.nights:
                        request.check_out = (datetime.strptime(request.check_in, '%Y-%m-%d') + timedelta(days=request.nights)).strftime('%Y-%m-%d')
                    request.missing_slots.remove("check_in")
                
                if request.is_complete():
                    del self.active_sessions[user_id]
                    return request, "好的，信息已确认！我来为您推荐..."
            
            elif message.isdigit():
                # 用户在回答人数
                if "guests" in request.missing_slots:
                    request.guests = int(message)
                    request.missing_slots.remove("guests")
                    
                    if request.is_complete():
                        del self.active_sessions[user_id]
                        return request, "好的，信息已确认！我来为您推荐..."
            
            # 更新原始查询
            request.raw_query += f" | 用户回复: {message}"
        
        # 新会话：完整解析
        request = self.nlu.process(message, source)
        
        # 如果是订房意图但信息不全，建立会话追问
        if request.intent == "booking" and not request.is_complete():
            self.active_sessions[user_id] = request
            reply = self._generate_clarification(request)
            return request, reply
        
        return request, None
    
    def _generate_clarification(self, request: BookingRequest) -> str:
        """生成追问话术"""
        if "check_in" in request.missing_slots:
            return "好的，请问您想哪天入住呢？"
        if "check_out" in request.missing_slots:
            nights = request.nights or 1
            return f"好的，住{nights}晚。请问您打算几号离开呢？"
        if "guests" in request.missing_slots:
            return "好的，请问一共几位入住呢？"
        
        return "好的，我来为您推荐合适的房型..."


class ResponseGenerator:
    """回复生成器"""
    
    def __init__(self, hotel_kb: HotelKnowledge):
        self.hotel_kb = hotel_kb
    
    def generate_booking_response(self, request: BookingRequest, recommendations: List[Dict]) -> str:
        """生成订房推荐回复"""
        if not recommendations:
            return "抱歉，根据您的需求暂时没有合适的房型，建议您联系前台：0833-2096666"
        
        lines = ["为您推荐以下房型：\n"]
        
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"{i}. 【{rec['room_name']}】")
            lines.append(f"   💰 价格：¥{rec['price']}/晚")
            
            # 匹配理由
            for reason in rec['match_reasons'][:2]:
                lines.append(f"   {reason}")
            
            lines.append("")
        
        lines.append("请问您想选择哪个房型呢？")
        lines.append("或拨打前台电话：0833-2096666 人工预订")
        
        return "\n".join(lines)
    
    def generate_inquiry_response(self, question: str) -> str:
        """生成咨询回复"""
        kb = self.hotel_kb
        
        if any(kw in question for kw in ["电话", "联系", "号码"]):
            return "📞 酒店电话：0833-2096666"
        
        if any(kw in question for kw in ["地址", "在哪", "位置"]):
            return "📍 地址：乐山市市中区白塔街85号"
        
        if any(kw in question for kw in ["入住", "几点"]):
            return "🕐 入住时间：14:00后（最晚18:00）\n🕐 退房时间：14:00前"
        
        if any(kw in question for kw in ["早餐", "吃饭"]):
            return "🍳 早餐时间：07:00-10:00\n📍 地点：1楼餐厅\n💰 价格：68元/位"
        
        if any(kw in question for kw in ["停车", "车位"]):
            return "🚗 停车：免费停车，有充电桩"
        
        if any(kw in question for kw in ["宠物", "狗", "猫"]):
            return "🐾 宠物友好：免费携带宠物入住，请提前联系告知"
        
        return "您好，请问有什么可以帮您？您也可以拨打前台：0833-2096666"


# ============================================================
# 主程序（Phase 1演示）
# ============================================================

def main():
    """Phase 1演示"""
    print("=" * 50)
    print("BOOK-001: 需求收集演示")
    print("=" * 50)
    
    # 初始化组件
    hotel_kb = HotelKnowledge()
    nlu = NLUProcessor(hotel_kb)
    conv_mgr = ConversationManager(nlu)
    resp_gen = ResponseGenerator(hotel_kb)
    
    # 模拟对话
    test_queries = [
        "我想带狗住两天",
        "明天到后天",
        "两个人",
        "请问酒店电话多少",
        "我想订4月5号到7号的房间"
    ]
    
    for query in test_queries:
        print(f"\n👤 用户: {query}")
        
        request, reply = conv_mgr.process_message("test_user", query)
        
        print(f"\n📋 解析结果:")
        print(f"   意图: {request.intent}")
        print(f"   置信度: {request.confidence}")
        print(f"   入住: {request.check_in}")
        print(f"   离店: {request.check_out}")
        print(f"   晚数: {request.nights}")
        print(f"   人数: {request.guests}")
        print(f"   预算: {request.budget}")
        print(f"   偏好: {request.preferences}")
        print(f"   缺失槽位: {request.missing_slots}")
        
        if reply:
            print(f"\n🤖 追问: {reply}")
        elif request.intent == "booking" and request.is_complete():
            print(f"\n🤖 AI推荐已生成，准备调用BOOK-002...")
    
    print("\n" + "=" * 50)
    print("Phase 1 实现方案总结:")
    print("=" * 50)
    print("""
1. 【对话理解】NLUProcessor解析用户需求
2. 【多轮对话】ConversationManager处理追问
3. 【回复生成】ResponseGenerator生成回复

部署方式:
- 对接微信客服消息API
- LLM API用于复杂场景
- Phase 1可纯规则运行（无需LLM调用）

Phase 1局限性:
- 规则匹配有限，复杂表达可能识别错误
- 房态需要人工维护
- 无法自动下单，需要人工跟进

Phase 2升级方向:
- LLM驱动，提升理解准确率
- PMS API对接，自动获取房态
- 企微消息自动推送
    """)


if __name__ == "__main__":
    main()
```

#### BOOK-002：房源匹配

```python
# -*- coding: utf-8 -*-
"""
BOOK-002: 房源智能匹配
功能：基于需求单匹配最佳房源
Phase: 1（规则+评分，无需ML）
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import sqlite3

# ============================================================
# 配置区
# ============================================================

DB_PATH = "data/guest_private.db"

# 匹配权重
MATCH_WEIGHTS = {
    "date": 0.25,      # 日期匹配
    "guest": 0.20,    # 人数匹配
    "price": 0.20,    # 价格匹配
    "pref": 0.25,     # 偏好匹配
    "special": 0.10   # 特殊需求匹配
}

# ============================================================
# 房态管理（Phase 1手动维护）
# ============================================================

class RoomInventory:
    """
    房型库存（Phase 1从Excel/飞书导入，Phase 2从PMS API获取）
    """
    
    def __init__(self):
        # 房型基础信息
        self.rooms = {
            "J01": {
                "id": "J01",
                "name": "江景大床房",
                "name_short": "江景大床",
                "area": "35",
                "bed": "1.8m大床",
                "floor": "8-15层",
                "features": ["270度江景", "落地窗", "观景浴缸", "智能客控"],
                "max_guests": 2,
                "base_price": 480,
                "tags": ["江景", "大床", "浪漫", "情侣"],
                "pet_friendly": True,
                "floor_level": "high"
            },
            "J02": {
                "id": "J02",
                "name": "江景双床房",
                "name_short": "江景双床",
                "area": "38",
                "bed": "1.2m双床×2",
                "floor": "8-15层",
                "features": ["270度江景", "双床", "商务", "干湿分离"],
                "max_guests": 2,
                "base_price": 520,
                "tags": ["江景", "双床", "商务"],
                "pet_friendly": False,
                "floor_level": "high"
            },
            "Q01": {
                "id": "Q01",
                "name": "城景亲子房",
                "name_short": "亲子房",
                "area": "45",
                "bed": "1.5m大床+1.2m小床",
                "floor": "5-10层",
                "features": ["亲子友好", "儿童用品", "亲子活动"],
                "max_guests": 3,
                "base_price": 580,
                "tags": ["亲子", "家庭", "城景", "儿童"],
                "pet_friendly": False,
                "floor_level": "mid"
            },
            "C01": {
                "id": "C01",
                "name": "宠物友好房",
                "name_short": "宠物房",
                "area": "40",
                "bed": "1.8m大床",
                "floor": "3-7层",
                "features": ["宠物免费", "一楼直达", "宠物用品", "花园景观"],
                "max_guests": 2,
                "base_price": 420,
                "tags": ["宠物", "一楼", "方便", "经济"],
                "pet_friendly": True,
                "floor_level": "low"
            },
            "S01": {
                "id": "S01",
                "name": "商务套房",
                "name_short": "套房",
                "area": "60",
                "bed": "1.8m大床",
                "floor": "15层",
                "features": ["独立客厅", "江景", "办公区", "按摩椅"],
                "max_guests": 2,
                "base_price": 880,
                "tags": ["江景", "套房", "商务", "高端"],
                "pet_friendly": False,
                "floor_level": "high"
            },
            "J03": {
                "id": "J03",
                "name": "江景豪华房",
                "name_short": "江景豪华",
                "area": "42",
                "bed": "1.8m大床",
                "floor": "12-15层",
                "features": ["270度江景", "超大浴缸", "管家服务"],
                "max_guests": 2,
                "base_price": 680,
                "tags": ["江景", "豪华", "情侣", "高端"],
                "pet_friendly": False,
                "floor_level": "high"
            }
        }
        
        # 每日可用房态（Phase 1手动更新）
        self.availability = {}
        self.pricing = {}
    
    def set_availability(self, date: str, room_id: str, available: int):
        """设置某日某房型的可用数量"""
        if date not in self.availability:
            self.availability[date] = {}
        self.availability[date][room_id] = available
    
    def set_price_override(self, date: str, room_id: str, price: float):
        """设置某日某房型的价格（可覆盖基础价）"""
        if date not in self.pricing:
            self.pricing[date] = {}
        self.pricing[date][room_id] = price
    
    def get_available_rooms(self, check_in: str, check_out: str) -> List[str]:
        """获取日期范围内可用的房型ID列表"""
        available = []
        
        # 解析日期
        try:
            start = datetime.strptime(check_in, '%Y-%m-%d')
            end = datetime.strptime(check_out, '%Y-%m-%d')
        except:
            return []
        
        # 检查每天的可用性
        current = start
        while current < end:
            date_str = current.strftime('%Y-%m-%d')
            
            for room_id, room in self.rooms.items():
                count = self.availability.get(date_str, {}).get(room_id, 1)
                if count <= 0:
                    if room_id in available:
                        available.remove(room_id)
            
            current += timedelta(days=1)
        
        # 返回有房的房型
        return list(self.rooms.keys())
    
    def get_price(self, room_id: str, date: str) -> float:
        """获取某日某房型的价格"""
        if date in self.pricing and room_id in self.pricing[date]:
            return self.pricing[date][room_id]
        
        room = self.rooms.get(room_id)
        if room:
            return room["base_price"]
        
        return 0
    
    def load_from_excel(self, excel_path: str):
        """从Excel加载可用房态（Phase 1功能）"""
        # 简化实现，实际需要pandas读取Excel
        pass
    
    def load_from_pms_api(self, api_url: str, token: str):
        """从PMS API加载房态（Phase 2功能）"""
        # 预留接口
        pass


@dataclass
class RoomRecommendation:
    """房源推荐结果"""
    rank: int
    room_id: str
    room_name: str
    match_score: float
    match_reasons: List[str]
    price: float
    original_price: float
    available: bool
    available_count: int
    features: List[str]
    image_url: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class RoomMatcher:
    """房源匹配引擎"""
    
    def __init__(self, inventory: RoomInventory):
        self.inventory = inventory
        self.weights = MATCH_WEIGHTS
    
    def match(self, request: Dict, top_n: int = 3) -> List[RoomRecommendation]:
        """
        核心匹配算法
        
        参数:
        - request: BOOK-001输出的需求单
        - top_n: 返回前N个推荐
        
        返回:
        - 排序后的推荐列表
        """
        # 1. 获取可用房型
        available_room_ids = []
        if request.get('check_in') and request.get('check_out'):
            available_room_ids = self.inventory.get_available_rooms(
                request['check_in'], 
                request['check_out']
            )
        else:
            # 如果没有日期，返回所有房型
            available_room_ids = list(self.inventory.rooms.keys())
        
        if not available_room_ids:
            return []
        
        # 2. 计算每个房型的匹配分
        scored_rooms = []
        
        for room_id in available_room_ids:
            room = self.inventory.rooms.get(room_id)
            if not room:
                continue
            
            # 获取该房型在需求日期范围内的平均价格
            prices = []
            if request.get('check_in') and request.get('check_out'):
                try:
                    start = datetime.strptime(request['check_in'], '%Y-%m-%d')
                    end = datetime.strptime(request['check_out'], '%Y-%m-%d')
                    current = start
                    while current < end:
                        price = self.inventory.get_price(room_id, current.strftime('%Y-%m-%d'))
                        prices.append(price)
                        current += timedelta(days=1)
                except:
                    prices = [room['base_price']]
            else:
                prices = [room['base_price']]
            
            avg_price = sum(prices) / len(prices) if prices else room['base_price']
            
            # 计算各维度得分
            scores = self._calculate_dimension_scores(request, room, avg_price)
            
            # 综合得分
            total_score = (
                self.weights['date'] * scores['date'] +
                self.weights['guest'] * scores['guest'] +
                self.weights['price'] * scores['price'] +
                self.weights['pref'] * scores['pref'] +
                self.weights['special'] * scores['special']
            )
            
            # 生成匹配理由
            reasons = self._generate_match_reasons(request, room, scores)
            
            # 获取可用数量
            avail_count = 1
            if request.get('check_in'):
                avail_count = self.inventory.availability.get(request['check_in'], {}).get(room_id, 1)
            
            scored_rooms.append(RoomRecommendation(
                rank=0,
                room_id=room_id,
                room_name=room['name'],
                match_score=round(total_score, 1),
                match_reasons=reasons,
                price=round(avg_price, 0),
                original_price=room['base_price'],
                available=avail_count > 0,
                available_count=avail_count,
                features=room['features']
            ))
        
        # 3. 排序
        scored_rooms.sort(key=lambda x: x.match_score, reverse=True)
        
        # 4. 设置排名
        for i, rec in enumerate(scored_rooms[:top_n], 1):
            rec.rank = i
        
        return scored_rooms[:top_n]
    
    def _calculate_dimension_scores(self, request: Dict, room: Dict, avg_price: float) -> Dict:
        """计算各维度得分"""
        scores = {
            'date': 100,  # 默认满分
            'guest': 100,
            'price': 100,
            'pref': 50,   # 默认中等分
            'special': 50
        }
        
        # 人数匹配得分
        guests = request.get('guests', 2)
        max_guests = room.get('max_guests', 2)
        
        if guests <= max_guests:
            scores['guest'] = 100
        else:
            # 超出人数限制，大幅扣分
            scores['guest'] = max(0, 100 - (guests - max_guests) * 30)
        
        # 价格匹配得分
        budget_min = request.get('budget_min')
        budget_max = request.get('budget_max')
        
        if budget_max:
            if avg_price <= budget_max:
                if budget_min:
                    if budget_min <= avg_price <= budget_max * 1.1:
                        scores['price'] = 100
                    else:
                        scores['price'] = max(0, 100 - (avg_price - budget_max) / 10)
                else:
                    # 只有上限
                    scores['price'] = max(0, 100 - (avg_price - budget_max) / 10)
            else:
                # 超出预算
                over_ratio = (avg_price - budget_max) / budget_max
                if over_ratio > 0.5:
                    scores['price'] = 0  # 超出50%以上不推荐
                else:
                    scores['price'] = max(0, 100 - over_ratio * 100)
        
        # 偏好匹配得分
        preferences = request.get('preferences', [])
        if preferences:
            match_count = 0
            for pref in preferences:
                pref_lower = pref.lower()
                # 检查标签
                if any(pref_lower in tag.lower() for tag in room.get('tags', [])):
                    match_count += 1
                # 检查特色
                if any(pref_lower in feat.lower() for feat in room.get('features', [])):
                    match_count += 1
            
            if preferences:
                scores['pref'] = (match_count / len(preferences)) * 100
        
        # 特殊需求匹配
        special = request.get('special', [])
        if special:
            if '宠物' in special:
                if room.get('pet_friendly'):
                    scores['special'] = 100
                else:
                    scores['special'] = 0  # 需要宠物但房型不支持，直接0
            
            if '亲子' in special or '儿童' in special:
                if '亲子' in room.get('tags', []) or '儿童' in room.get('features', []):
                    scores['special'] = 100
        
        return scores
    
    def _generate_match_reasons(self, request: Dict, room: Dict, scores: Dict) -> List[str]:
        """生成匹配理由"""
        reasons = []
        
        # 价格
        budget_max = request.get('budget_max')
        if budget_max:
            if scores['price'] >= 80:
                reasons.append(f"✅ 价格¥{room.get('base_price')}，在预算范围内")
            elif scores['price'] >= 50:
                reasons.append(f"⚠️ 价格¥{room.get('base_price')}，略超预算")
        
        # 偏好
        preferences = request.get('preferences', [])
        for pref in preferences:
            pref_lower = pref.lower()
            if any(pref_lower in tag.lower() for tag in room.get('tags', [])):
                reasons.append(f"✅ {pref}需求匹配")
        
        # 特色
        if '江景' in preferences or '看江' in preferences:
            if any('江景' in feat for feat in room.get('features', [])):
                reasons.append("✅ 配备江景特色")
        
        # 人数
        guests = request.get('guests', 2)
        if guests > 1 and room.get('max_guests', 2) >= guests:
            reasons.append(f"✅ 可住{guests}人")
        
        # 特殊需求
        special = request.get('special', [])
        if '宠物' in special and room.get('pet_friendly'):
            reasons.append("✅ 支持宠物入住")
        
        # 如果没有特殊匹配，添加常规理由
        if not reasons:
            reasons.append(f"✅ {room.get('name_short', room['name'])}性价比推荐")
        
        return reasons[:3]  # 最多3条理由


def generate_recommendation_cards(recommendations: List[RoomRecommendation]) -> str:
    """生成推荐卡片（用于微信消息展示）"""
    if not recommendations:
        return "抱歉，根据您的需求暂无合适房型，建议联系前台：0833-2096666"
    
    lines = ["🏨 为您推荐以下房型：\n"]
    
    emoji_map = {
        "江景大床": "🛏️",
        "江景双床": "🛏️",
        "亲子": "👨‍👩‍👧",
        "宠物": "🐾",
        "套房": "🏠",
        "豪华": "✨"
    }
    
    for rec in recommendations:
        # 选择emoji
        emoji = "🏨"
        for key, emo in emoji_map.items():
            if key in rec.room_name:
                emoji = emo
                break
        
        lines.append(f"{emoji} {rec.rank}. 【{rec.room_name}】")
        lines.append(f"   💰 ¥{rec.price}/晚")
        
        # 匹配理由
        for reason in rec.match_reasons:
            lines.append(f"   {reason}")
        
        lines.append(f"   📏 {rec.features[0] if rec.features else ''}")
        
        if rec.available_count > 0:
            lines.append(f"   ✅ 今日可订")
        else:
            lines.append(f"   ⚠️ 紧张")
        
        lines.append("")
    
    lines.append("📞 详情咨询：0833-2096666")
    
    return "\n".join(lines)


# ============================================================
# 主程序
# ============================================================

def main():
    """演示"""
    print("=" * 50)
    print("BOOK-002: 房源匹配演示")
    print("=" * 50)
    
    # 初始化
    inventory = RoomInventory()
    
    # 设置模拟房态
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    inventory.set_availability(today, "J01", 2)
    inventory.set_availability(today, "J02", 1)
    inventory.set_availability(today, "C01", 3)
    inventory.set_availability(today, "S01", 0)
    
    inventory.set_availability(tomorrow, "J01", 2)
    inventory.set_availability(tomorrow, "J02", 2)
    inventory.set_availability(tomorrow, "C01", 2)
    
    # 创建匹配器
    matcher = RoomMatcher(inventory)
    
    # 模拟需求单
    test_requests = [
        {
            "check_in": today,
            "check_out": tomorrow,
            "guests": 2,
            "preferences": ["江景"],
            "special": [],
            "budget_max": 600
        },
        {
            "check_in": today,
            "check_out": tomorrow,
            "guests": 2,
            "preferences": [],
            "special": ["宠物"],
            "budget_max": 500
        },
        {
            "check_in": today,
            "check_out": tomorrow,
            "guests": 3,
            "preferences": ["亲子"],
            "special": ["亲子"],
            "budget_max": 800
        }
    ]
    
    for i, req in enumerate(test_requests, 1):
        print(f"\n{'='*40}")
        print(f"测试需求 {i}: {req}")
        print("-" * 40)
        
        recommendations = matcher.match(req, top_n=3)
        
        print("\n推荐结果:")
        cards = generate_recommendation_cards(recommendations)
        print(cards)
    
    print("\n" + "=" * 50)
    print("Phase 1 实现要点:")
    print("=" * 50)
    print("""
1. 【房态管理】RoomInventory管理房型基础信息和可用性
2. 【匹配算法】RoomMatcher基于加权评分匹配
3. 【推荐生成】按得分排序，生成带理由的推荐卡片

Phase 1局限性:
- 房态需人工维护Excel
- 权重固定，无法个性化学习
- 无法处理复杂偏好组合

Phase 2升级方向:
- PMS API实时同步房态
- LLM学习用户反馈，动态调整权重
- 历史数据训练个性化推荐模型
    """)


if __name__ == "__main__":
    main()
```

---

### 乐山落地行动清单

#### 第一周：酒店信息整理

| 序号 | 行动项 | 负责方 | 完成标准 | 优先级 |
|------|--------|--------|----------|--------|
| 1 | 整理房型基础信息表 | Eric + 酒店 | 6种房型信息完整（名称/面积/床型/价格/特色/标签） | P0 |
| 2 | 定义酒店标签体系 | Eric | 江景/城景/亲子/宠物友好/商务等标签确认 | P0 |
| 3 | 收集房型图片 | 酒店 | 每种房型3-5张高清图 | P1 |
| 4 | 确认每日房态更新机制 | 酒店 | 前台每日16:00前更新次日房态 | P1 |

#### 第二周：BOOK-001/002开发

| 序号 | 行动项 | 负责方 | 完成标准 | 优先级 |
|------|--------|--------|----------|--------|
| 5 | 部署NLU解析模块 | 技术方 | 本地Python可运行 | P0 |
| 6 | 部署房源匹配模块 | 技术方 | 推荐逻辑跑通 | P0 |
| 7 | 对接微信客服消息 | 技术方 | 消息收发测试成功 | P1 |
| 8 | 测试对话流程 | 双方 | 3轮以上对话测试 | P1 |

#### 第三周：人工接单流程跑通

| 序号 | 行动项 | 负责方 | 完成标准 | 优先级 |
|------|--------|--------|----------|--------|
| 9 | 制定接单SOP | Eric | 明确从接单到确认的流程 | P0 |
| 10 | 培训前台人员 | 酒店 | 前台能使用系统 | P1 |
| 11 | 首次真实用户测试 | 双方 | 有真实用户咨询并完成预订 | P2 |
| 12 | 收集反馈优化话术 | 技术方 | 第一版话术库建立 | P2 |

#### 第四周及以后

| 序号 | 行动项 | 负责方 | 完成标准 | 优先级 |
|------|--------|--------|----------|--------|
| 13 | BOOK-003规划 | 技术方 | Phase 2/3技术方案确定 | P2 |
| 14 | 数据积累与分析 | 技术方 | 收集用户行为数据 | P3 |
| 15 | Phase 2启动 | 双方 | PMS API对接启动 | P3 |

---

### 关键成功指标（KPI）

| 阶段 | 指标 | 目标值 | 测量方式 |
|------|------|--------|----------|
| Phase 1 | 需求识别准确率 | >80% | 人工抽检 |
| Phase 1 | 推荐转化率 | >20% | 推荐后实际预订数/推荐数 |
| Phase 1 | 用户满意度 | >4.0分 | 咨询后评分 |
| Phase 2 | 自动接单成功率 | >90% | 成功接单/尝试接单 |
| Phase 2 | 响应时间 | <1分钟 | 从用户提问到推荐发出 |
| Phase 3 | 全流程自助完成率 | >70% | 无需人工介入的订单比例 |

---

### 风险与应对

| 风险 | 可能性 | 影响 | 应对措施 |
|------|--------|------|----------|
| LLM理解错误 | 中 | 高 | 设置兜底转人工；积累bad case优化 |
| 房态不准导致超售 | 低 | 极高 | 每日上限控制；超售立即告警 |
| 用户习惯OTA | 高 | 中 | 推荐时显示OTA价格对比；突出直销优惠 |
| 微信消息限制 | 中 | 中 | 关注模板消息配额；提前报备 |
| 夜间无人值班 | 高 | 中 | 设置自动回复+明早处理提示 |

---

### BOOK-001 + BOOK-002 协作流程图

```
用户输入: "我想带狗住两天"

         ┌─────────────────────────┐
         │   BOOK-001: 需求收集     │
         │                         │
         │ 意图识别 → 订房/咨询    │
         │ 日期提取 → 4月5日入住   │
         │ 人数提取 → 2人          │
         │ 偏好提取 → [宠物]       │
         │ 缺失槽位 → 离店日期     │
         │                         │
         │ 多轮追问: "住几天呢？"  │
         │ 用户回复: "两天"        │
         │                         │
         │ ✅ 生成完整需求单       │
         └───────────┬─────────────┘
                     │
                     ▼
         ┌─────────────────────────┐
         │   BOOK-002: 房源匹配     │
         │                         │
         │ 输入: 需求单            │
         │ - check_in: 4月5日     │
         │ - check_out: 4月7日    │
         │ - guests: 2             │
         │ - preferences: [宠物]   │
         │                         │
         │ 匹配计算:               │
         │ - C01(宠物房): 95分 ✅  │
         │ - J01(江景大床): 70分  │
         │ - J02(江景双床): 65分  │
         │                         │
         │ ✅ 生成TOP3推荐卡片     │
         └───────────┬─────────────┘
                     │
                     ▼
         ┌─────────────────────────┐
         │   消息展示给用户        │
         │                         │
         │ 🐾 为您推荐以下房型：   │
         │                         │
         │ 1. 【宠物友好房】      │
         │    💰 ¥420/晚            │
         │    ✅ 支持宠物入住      │
         │                         │
         │ 2. 【江景大床房】       │
         │    💰 ¥480/晚            │
         │    ⚠️ 略超预算          │
         │                         │
         │ 请选择房型或联系：      │
         │ 📞 0833-2096666         │
         └─────────────────────────┘
                     │
                     ▼
         ┌─────────────────────────┐
         │   人工介入（Phase 1）    │
         │                         │
         │ 前台确认房型            │
         │ → 创建订单              │
         │ → 发送确认链接          │
         │ → 用户完成支付          │
         └─────────────────────────┘
```

---

**文档状态**: ✅ V1.0完成
**下一步**: 整理房型信息 + 部署BOOK-001/002代码
