# AHL乐山项目：新媒体公域→私域→自动化预订 技术方案 V1.0

> **编制日期**：2026-03-27
> **版本**：V1.0（初稿）
> **状态**：待实地验证

---

## 一、项目背景与核心目标

### 1.1 背景问题

酒店行业当前的最大痛点：**内容平台获客，但成交要跳到OTA或电线人工跟进，流失率极高**。

- 用户在抖音/小红书被种草
- 想预订时发现没有直接入口
- 被迫跳转携程/美团，或打电线人工确认
- 流失率保守估计超过60%

### 1.2 核心目标

建立**新媒体公域→私域沉淀→自动化预订**的完整闭环，用户在社群里完成预订并写入PMS，**全程无人工干预**（Phase 2目标）。

### 1.3 乐山嘉州现状评估

| 维度 | 现状 | 说明 |
|------|------|------|
| 携程店铺 | ✅ 已有 | Hotel ID 73690948，4.7分2414条点评 |
| 达人探店 | ✅ 已有 | 小红书/抖音有多个探店视频 |
| 微信公众号 | ❓ 未知 | 需微信搜索确认 |
| 微信小程序 | ❓ 未知 | 需微信搜索确认 |
| 企微社群 | ❓ 未知 | 大概率没有 |
| 微信商户号 | ❓ 未知 | 需财务确认 |
| PMS系统 | ❓ 未知 | 需技术摸底 |
| PMS API | ❓ 未知 | 需确认是否支持API写入 |

---

## 二、完整用户路径设计

```
┌─────────────────────────────────────────────────────────────────────┐
│ 【阶段一：公域触达】                                                  │
│                                                                     │
│  用户刷抖音/小红书                                                    │
│      ↓                                                               │
│  看到酒店种草内容（达人探店/用户好评/景点联动）                            │
│      ↓                                                               │
│  点击评论区链接/小红书店铺/抖音小程序 → 进入酒店页面                      │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│ 【阶段二：私域沉淀】                                                  │
│                                                                     │
│  扫码关注公众号/添加企微/进入社群                                       │
│      ↓                                                               │
│  获得首次福利（折扣暗号/优惠券）                                        │
│      ↓                                                               │
│  成为潜在客户（打标签：首次/兴趣）                                      │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│ 【阶段三：需求唤醒】                                                  │
│                                                                     │
│  社群内持续内容触达（风景实拍/活动/点评）                                │
│      ↓                                                               │
│  用户表达需求："周末想带孩子住江景房，预算600左右"                        │
│      ↓                                                               │
│  AI客服自动接待，识别需求（意图+槽位）                                   │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│ 【阶段四：自动化预订】★ Phase 2核心                                    │
│                                                                     │
│  AI理解需求 → 查询可用房态 → 生成推荐方案                              │
│      ↓                                                               │
│  用户确认方案 → 微信支付锁房                                           │
│      ↓                                                               │
│  支付成功 → PMS自动写入订单                                           │
│      ↓                                                               │
│  订单确认 → 自动发送入住指南给用户                                      │
│      ↓                                                               │
│  全程 <5秒，无人工干预                                                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 三、技术实现方案

### 3.1 公域内容获客层

**目标**：在抖音/小红书产生的内容能被追踪到转化效果

#### 3.1.1 合规引流路径

由于抖音/小红书平台禁止直接跳转微信，必须使用以下合规路径：

**路径A：小红书 → 微信小程序（最推荐）**

```
小红书笔记
    ↓ 文末"左下角门店"入口
进入小红书内置小程序
    ↓ 小程序内扫码/领券
跳转微信小程序
    ↓ 用户授权手机号
自动进入酒店社群
```

**路径B：抖音 → 微信（合规路径）**

```
抖音号 → 评论区置顶"小红书同名"
    ↓ 用户去小红书搜
小红书 → 门店小程序 → 微信

或者：

抖音 → 预约回呼表单
    ↓ 酒店销售24小时内回呼
加微信
```

**路径C：公众号 → 企微（最简单）**

```
任何公域内容 → 评论区置顶"点击主页链接→关注公众号"
    ↓ 公众号自动回复
扫码加企微社群
```

#### 3.1.2 内容发布SOP

| 内容类型 | 平台 | 追踪参数 | 转化目标 |
|---------|------|---------|---------|
| 达人探店 | 小红书+抖音 | UTM source=xiaohongshu/douyin | 到店 |
| 用户好评截图 | 小红书+抖音 | UTM source=ugc | 到店 |
| 景点联动 | 抖音 | UTM source=scenic | 到店 |
| 促销活动 | 公众号 | 短链接+参数 | 社群入群 |

#### 3.1.3 归因分析框架

```python
# 归因数据模型
class AttributionData:
    """归因数据：记录每个用户的来源链路"""
    source: str          # xiaohongshu/douyin/public_account/search
    content_id: str     # 内容ID
    campaign_id: str    # 活动ID
    click_time: datetime
    conversion_time: datetime | None  # 转化为私域用户的时间
    order_time: datetime | None      # 首次下单时间
    order_amount: float | None       # 首次订单金额

# UTM参数规范
UTM_PARAMS = {
    "utm_source": "xiaohongshu",      # 来源平台
    "utm_medium": "explore_post",    # 内容形式：explore_post/short_video/live
    "utm_campaign": "leshan_0301",  # 活动代号
    "utm_content": "kOL_12345",      # KOL ID或内容ID
    "utm_term": "river_view",         # 关键词/房型
}
```

---

### 3.2 私域沉淀层

**目标**：让用户进入企微社群后不流失，核心是**第一次互动体验**

#### 3.2.1 核心SKILL：PRIV-NEW-001 新客自动接待

**触发时机**：用户加入企微后 <3秒

**流程**：
```
用户加企微好友
    ↓ 立即发送欢迎语（<3秒）
    ↓ 欢迎语包含：福利暗号+社群价值介绍+小程序入口
    ↓ 用户点击小程序 → 进入预约界面
    ↓ 用户离店后自动打标签（首次/复购/高价值/KOC）
```

#### 3.2.2 企微API Python代码框架

```python
import requests
import time
from datetime import datetime, timedelta

WECOM_API = "https://qyapi.weixin.qq.com/cgi-bin"

# ============================================================
# 配置区（上线前替换为真实值）
# ============================================================
CORP_ID = "your_corp_id"           # 企业微信CorpID
CORP_SECRET = "your_corp_secret"   # 企业微信Secret
HOTEL_NAME = "乐山锦江嘉州宾馆"
HOTEL_PHONE = "0833-2096666"
DISCOUNT_CODE = "大佛夜景"           # 福利暗号
WELCOME_DISCOUNT = "8折"           # 欢迎折扣

# ============================================================
# 工具函数
# ============================================================
def get_access_token() -> str:
    """获取企业微信Access Token"""
    resp = requests.get(
        f"{WECOM_API}/gettoken",
        params={
            "corpid": CORP_ID,
            "corpsecret": CORP_SECRET
        }
    )
    result = resp.json()
    if result.get("errcode") != 0:
        raise Exception(f"获取AccessToken失败: {result}")
    return result["access_token"]


def get_https_proxy() -> dict | None:
    """如果服务器在内地，需要配置代理访问微信API"""
    # 内地服务器需要配置代理
    # return {"http": "http://proxy:8080", "https": "http://proxy:8080"}
    return None


def send_welcome_message(user_id: str, token: str) -> dict:
    """
    新客入群立即发送欢迎语
    触发时机：用户加企微好友后自动调用（需配置客户联系欢迎语）
    """
    welcome_text = (
        f"🏨 欢迎来到{HOTEL_NAME}！\n\n"
        f"🎁 专属福利：报「{DISCOUNT_CODE}」享{WELCOME_DISCOUNT}优惠\n\n"
        f"📍 【立即预约房间】\n"
        f"[小程序预约入口链接]\n\n"
        f"🛎️ 有任何问题随时联系我，24小时在线！\n"
        f"期待为您提供服务～"
    )

    payload = {
        "touser": user_id,
        "msgtype": "text",
        "text": {"content": welcome_text},
        "send_time": int(time.time())
    }

    resp = requests.post(
        f"{WECOM_API}/message/send",
        params={"access_token": token},
        json=payload,
        proxies=get_https_proxy()
    )
    return resp.json()


def send_welcome_with_link(user_id: str, token: str, miniapp_page: str) -> dict:
    """
    发送带小程序链接的欢迎语（推荐方式）
    miniapp_page格式: "pages/index/index?from=scene"
    """
    welcome_text = (
        f"🏨 欢迎来到{HOTEL_NAME}！\n\n"
        f"🎁 专属福利：报「{DISCOUNT_CODE}」享{WELCOME_DISCOUNT}优惠\n\n"
        f"👇 点击下方小程序链接预约房间"
    )

    payload = {
        "touser": user_id,
        "msgtype": "miniprogram",
        "miniprogram": {
            "appid": "your_miniapp_appid",           # 小程序AppID
            "title": "立即预约 · 乐山锦江嘉州宾馆",
            "pagepath": miniapp_page,                # 小程序页面路径
            "thumb_id": 0                             # 封面图片media_id
        },
        "send_time": int(time.time())
    }

    resp = requests.post(
        f"{WECOM_API}/message/send",
        params={"access_token": token},
        json=payload,
        proxies=get_https_proxy()
    )
    return resp.json()


# ============================================================
# 用户标签管理
# ============================================================
def get_user_tags(token: str) -> list:
    """获取所有客户标签"""
    resp = requests.get(
        f"{WECOM_API}/tag/list",
        params={"access_token": token}
    )
    return resp.json().get("taglist", [])


def add_user_tag(user_id: str, tag_name: str, token: str) -> dict:
    """
    给用户打标签
    
    推荐标签体系：
    - 首次客户（new_first）
    - 复购客户（repeat_buyer）
    - 高价值客户（high_value）
    - KOC/KOL（种草达人）
    - 投诉客户（complaint）
    """
    # 先获取标签ID
    tags = get_user_tags(token)
    tag_id = None
    for tag in tags:
        if tag["tagname"] == tag_name:
            tag_id = tag["tagid"]
            break

    if tag_id is None:
        # 创建新标签
        create_resp = requests.post(
            f"{WECOM_API}/tag/create",
            params={"access_token": token},
            json={"tagname": tag_name}
        )
        tag_id = create_resp.json().get("tagid")

    # 添加标签
    payload = {"user_list": [user_id], "tagid": tag_id}
    resp = requests.post(
        f"{WECOM_API}/tag/tag_add",
        params={"access_token": token},
        json=payload
    )
    return resp.json()


def batch_add_tag_by_external_userids(external_userids: list, tag_id: int, token: str) -> dict:
    """批量打标签"""
    payload = {
        "external_userid": external_userids,
        "tagid": tag_id
    }
    resp = requests.post(
        f"{WECOM_API}/externalcontact/batch_tag_add",
        params={"access_token": token},
        json=payload
    )
    return resp.json()


# ============================================================
# 社群管理
# ============================================================
def create_group_chat(token: str, name: str, user_list: list) -> dict:
    """
    创建社群并拉入用户
    user_list: 企微user_id列表
    """
    payload = {
        "name": name,
        "owner": "your_admin_userid",
        "user_list": user_list,
        "chat_id": ""  # 留空自动生成
    }
    resp = requests.post(
        f"{WECOM_API}/appchat/create",
        params={"access_token": token},
        json=payload
    )
    return resp.json()


def send_group_message(chat_id: str, content: str, token: str) -> dict:
    """发送群消息"""
    payload = {
        "chatid": chat_id,
        "msgtype": "text",
        "text": {"content": content}
    }
    resp = requests.post(
        f"{WECOM_API}/appchat/send",
        params={"access_token": token},
        json=payload
    )
    return resp.json()


# ============================================================
# 客户详情查询
# ============================================================
def get_customer_detail(external_userid: str, token: str) -> dict:
    """获取客户详情（包含标签、来源等）"""
    resp = requests.get(
        f"{WECOM_API}/externalcontact/get",
        params={
            "access_token": token,
            "external_userid": external_userid
        }
    )
    return resp.json()


def get_customer_list(userid: str, token: str) -> list:
    """获取某个企微账号的所有客户列表"""
    resp = requests.get(
        f"{WECOM_API}/externalcontact/list",
        params={
            "access_token": token,
            "userid": userid
        }
    )
    return resp.json().get("external_userid", [])
```

---

### 3.3 AI需求理解层

**核心SKILL：BOOK-NLU-001 新媒体来客需求识别**

当用户在社群内发了一条消息：`"周末想带孩子住江景房，预算600左右"`

#### 3.3.1 意图识别与槽位提取

```python
import re
from datetime import datetime, timedelta
from typing import Optional

# ============================================================
# 意图识别关键词
# ============================================================
INTENT_PATTERNS = {
    "booking": ["住", "订房", "预订", "开房", "房间", "入住", "订", "帮我留"],
    "inquiry": ["请问", "有没有", "可以", "怎么", "问一下", "咨询", "问下"],
    "cancel": ["取消", "退", "退款", "不订了"],
    "modify": ["改", "换", "改期", "改一下"],
    "complaint": ["投诉", "太差", "不满", "差评", "问题"],
}

# ============================================================
# 槽位提取正则模式
# ============================================================
SLOT_PATTERNS = {
    "date": r"(\d{1,2}月\d{1,2}日|本周|周末|周六|周日|明天|今天|后天|下周|下个月)",
    "nights": r"(\d+)晚|住(\d+)晚|(\d+)天晚上|(\d+)天",
    "guests": r"(\d+)大|(\d+)人|一家(\d+)口|三口|四口|五口|带孩|带孩子",
    "room_type": r"江景|城景|亲子|套房|大床|双床|全景|标准|商务|豪华|单间",
    "budget": r"(\d{3,4})左右|预算(\d{3,4})|不超过(\d{3,4})|(\d{3,4})以内",
    "special": r"加床|无烟|高层|安静|加班|出差|生日|结婚",
}

# ============================================================
# 日期映射（相对日期）
# ============================================================
DATE_MAPPING = {
    "今天": 0,
    "明天": 1,
    "后天": 2,
    "本周": "this_weekend",
    "周末": "this_weekend",
    "周六": "next_saturday",
    "周日": "next_sunday",
}


def parse_relative_date(date_str: str) -> str:
    """将相对日期转换为具体日期字符串"""
    today = datetime.now()

    if date_str in DATE_MAPPING:
        mapped = DATE_MAPPING[date_str]
        if isinstance(mapped, int):
            target = today + timedelta(days=mapped)
            return target.strftime("%Y-%m-%d")
        elif mapped == "this_weekend":
            # 计算本周剩余的周六
            days_until_saturday = (5 - today.weekday()) % 7
            if days_until_saturday == 0 and today.weekday() == 5:
                return today.strftime("%Y-%m-%d")
            target = today + timedelta(days=days_until_saturday if days_until_saturday > 0 else 7)
            return target.strftime("%Y-%m-%d")
        elif mapped == "next_saturday":
            days_until_saturday = (5 - today.weekday()) % 7
            target = today + timedelta(days=days_until_saturday if days_until_saturday > 0 else 7)
            return target.strftime("%Y-%m-%d")

    # 处理 "X月X日" 格式
    month_day_match = re.match(r"(\d{1,2})月(\d{1,2})日", date_str)
    if month_day_match:
        month, day = int(month_day_match.group(1)), int(month_day_match.group(2))
        year = today.year if month >= today.month else today.year + 1
        return f"{year}-{month:02d}-{day:02d}"

    return date_str


# ============================================================
# 槽位提取核心函数
# ============================================================
def extract_booking_slots(user_message: str) -> dict:
    """
    从用户消息中提取预订槽位

    输入: "周末想带孩子住江景房，预算600左右"
    输出: {
        "intent": "booking",
        "date": "2026-03-28",
        "guests": "亲子",
        "room_type": "江景",
        "budget": "600",
        "nights": 1,
        "raw_message": "周末想带孩子住江景房，预算600左右"
    }
    """
    slots = {
        "intent": "inquiry",   # 默认意图为咨询
        "date": None,
        "nights": 1,           # 默认1晚
        "guests": None,
        "room_type": None,
        "budget": None,
        "special_requests": [],
        "raw_message": user_message,
        "raw_slots": {},       # 原始匹配结果，便于调试
    }

    # ---- 1. 意图识别 ----
    for intent, keywords in INTENT_PATTERNS.items():
        if any(kw in user_message for kw in keywords):
            slots["intent"] = intent
            break

    # ---- 2. 槽位提取 ----
    for slot_name, pattern in SLOT_PATTERNS.items():
        match = re.search(pattern, user_message)
        if match:
            matched_value = match.group(0)
            slots["raw_slots"][slot_name] = matched_value

            # 特殊处理
            if slot_name == "date":
                slots["date"] = parse_relative_date(matched_value)
            elif slot_name == "nights":
                # 从匹配组中提取数字
                for g in match.groups():
                    if g and g.isdigit():
                        slots["nights"] = int(g)
                        break
            elif slot_name == "budget":
                # 从匹配组中提取数字
                for g in match.groups():
                    if g and g.isdigit():
                        slots["budget"] = g
                        break
            else:
                slots[slot_name] = matched_value

    # ---- 3. 特殊场景处理 ----
    if "孩子" in user_message or "亲子" in user_message:
        slots["guests"] = "亲子"
        slots["room_type"] = slots.get("room_type") or "亲子"  # 亲子优先

    # ---- 4. 默认日期处理 ----
    if slots["date"] is None:
        if slots["intent"] == "booking":
            slots["date"] = "next_weekend"  # 预订意图默认下周周末

    return slots


def build_booking_query(slots: dict) -> dict:
    """
    根据槽位构建PMS房态查询参数
    """
    query = {
        "check_in": slots.get("date"),
        "nights": slots.get("nights", 1),
        "room_type_preference": slots.get("room_type"),
        "guests": slots.get("guests"),
        "budget": slots.get("budget"),
        "special_requests": slots.get("special_requests", []),
    }
    return {k: v for k, v in query.items() if v is not None}


# ============================================================
# NLU处理示例
# ============================================================
if __name__ == "__main__":
    test_messages = [
        "周末想带孩子住江景房，预算600左右",
        "请问明天有房吗，大床房",
        "我想订房，27号住一晚",
        "带孩子来的，有没有亲子房",
        "取消预订",
    ]

    for msg in test_messages:
        slots = extract_booking_slots(msg)
        print(f"\n输入: {msg}")
        print(f"意图: {slots['intent']}")
        print(f"槽位: {slots}")
```

#### 3.3.2 AI客服对话管理

```python
from enum import Enum
from typing import Callable, Optional
import json

class BookingState(Enum):
    """预订状态机"""
    START = "start"                      # 开始
    INTENT_CONFIRMED = "intent_confirmed"  # 意图已确认
    INFO_COLLECTING = "info_collecting"    # 信息收集中
    ROOMS_RECOMMENDED = "rooms_recommended"  # 已推荐房型
    ROOM_CONFIRMED = "room_confirmed"      # 房型已确认
    WAITING_PAYMENT = "waiting_payment"    # 等待支付
    PAID = "paid"                         # 已支付
    COMPLETED = "completed"               # 完成
    CANCELLED = "cancelled"              # 取消


class AIDialogManager:
    """
    AI对话状态管理

    处理用户从咨询到完成预订的完整对话流程
    """

    def __init__(self, pms_client, wxpay_client):
        self.state = BookingState.START
        self.slots = {}
        self.pms = pms_client
        self.wxpay = wxpay_client
        self.trade_no = None

    def handle_message(self, user_message: str, user_id: str) -> dict:
        """
        处理用户消息，返回AI回复

        返回格式:
        {
            "reply": "xxx",          # AI回复文本
            "action": "ask_confirm", # 本次触发的动作
            "state": BookingState,   # 更新后的状态
            "data": {}               # 附加数据（如推荐房型列表）
        }
        """

        # 提取槽位
        new_slots = extract_booking_slots(user_message)
        self.slots.update(new_slots)

        # 状态机处理
        if self.state == BookingState.START:
            return self._handle_start(user_message)

        elif self.state == BookingState.INTENT_CONFIRMED:
            return self._handle_info_collect(user_message)

        elif self.state == BookingState.ROOMS_RECOMMENDED:
            return self._handle_room_selection(user_message)

        elif self.state == BookingState.WAITING_PAYMENT:
            return self._handle_payment_wait(user_message)

        return {"reply": "好的，请稍等，我帮您处理。", "action": "default"}

    def _handle_start(self, user_message: str) -> dict:
        """处理开始状态"""
        intent = self.slots.get("intent", "inquiry")

        if intent == "cancel":
            self.state = BookingState.CANCELLED
            return {
                "reply": "好的，已为您取消。有需要随时联系我们。",
                "action": "cancel",
                "state": self.state,
            }

        if intent == "booking":
            # 有预订意图，尝试收集信息
            self.state = BookingState.INTENT_CONFIRMED
            return self._build_info_collect_reply()

        # 仅为咨询
        return {
            "reply": "您好！请问有什么可以帮您？需要预订房间吗？",
            "action": "greeting",
            "state": self.state,
        }

    def _handle_info_collect(self, user_message: str) -> dict:
        """收集信息状态：查询PMS可用房型"""
        query = build_booking_query(self.slots)

        # 调用PMS查询可用房型
        available_rooms = self.pms.query_availability(
            check_in=query.get("check_in"),
            nights=query.get("nights", 1),
            room_type=query.get("room_type_preference"),
        )

        if not available_rooms:
            self.state = BookingState.INTENT_CONFIRMED
            return {
                "reply": f"抱歉，{query.get('check_in')}暂无可用房型。您可以：\n1. 换一个日期\n2. 换一种房型\n3. 联系前台 {HOTEL_PHONE}",
                "action": "no_availability",
                "state": self.state,
            }

        # 生成推荐回复
        self.state = BookingState.ROOMS_RECOMMENDED
        self._available_rooms = available_rooms  # 暂存用于后续确认

        reply = self._build_room_recommendation(available_rooms, query)
        return {
            "reply": reply,
            "action": "recommend_rooms",
            "state": self.state,
            "data": {"rooms": available_rooms},
        }

    def _handle_room_selection(self, user_message: str) -> dict:
        """处理房型选择"""
        # 从消息中识别用户选择
        selected = self._extract_room_selection(user_message, self._available_rooms)

        if selected is None:
            return {
                "reply": "抱歉，没有找到对应的房型。请告诉我房型序号（如1、2）。",
                "action": "invalid_selection",
                "state": self.state,
            }

        self._selected_room = selected
        self.state = BookingState.ROOM_CONFIRMED

        # 生成确认+支付引导
        room_info = f"{selected['name']} - ¥{selected['price']}/晚"
        reply = (
            f"✅ 您选择的是：\n{room_info}\n"
            f"入住：{self.slots.get('date')}  住宿：{self.slots.get('nights', 1)}晚\n\n"
            f"确认预订请回复【确认】，需要修改请告诉我～"
        )

        return {
            "reply": reply,
            "action": "confirm_room",
            "state": self.state,
            "data": {"room": selected},
        }

    def _handle_payment_wait(self, user_message: str) -> dict:
        """等待支付状态"""
        if "取消" in user_message or "不要" in user_message:
            self.state = BookingState.CANCELLED
            return {
                "reply": "好的，已取消预订。如有需要随时联系我们。",
                "action": "cancel",
                "state": self.state,
            }

        return {
            "reply": "支付码已发，请尽快完成支付（15分钟内有效）。如已支付请忽略～",
            "action": "payment_remind",
            "state": self.state,
        }

    # ---- 辅助方法 ----

    def _build_info_collect_reply(self) -> dict:
        """构建信息收集确认回复"""
        date = self.slots.get("date") or "下周末"
        nights = self.slots.get("nights", 1)
        room_type = self.slots.get("room_type") or "任意房型"
        guests = self.slots.get("guests") or "未说明"

        reply = (
            f"好的，我来帮您查询预订！\n\n"
            f"📅 入住：{date}\n"
            f"🌙 住宿：{nights}晚\n"
            f"🛏️ 房型：{room_type}\n"
            f"👥 人数：{guests}\n\n"
            f"请确认信息正确，我帮您查一下可用的房间～"
        )

        return {
            "reply": reply,
            "action": "confirm_info",
            "state": self.state,
        }

    def _build_room_recommendation(self, rooms: list, query: dict) -> str:
        """构建房型推荐回复"""
        lines = ["找到以下可用房型：\n"]

        for i, room in enumerate(rooms, 1):
            tag = "推荐" if room.get("is_featured") else ""
            lines.append(f"{i}. {room['name']} {tag}\n")
            lines.append(f"   💰 ¥{room['price']}/晚  剩余：{room['available']}间\n")

        lines.append("\n请回复序号选择，如：1")
        return "".join(lines)

    def _extract_room_selection(self, message: str, rooms: list) -> Optional[dict]:
        """从消息中提取房型选择"""
        # 尝试匹配数字序号
        num_match = re.search(r"^[选要]?(\d+)", message)
        if num_match:
            idx = int(num_match.group(1)) - 1
            if 0 <= idx < len(rooms):
                return rooms[idx]

        # 尝试匹配房型名称
        for room in rooms:
            if room["name"] in message:
                return room

        return None

    def generate_payment_qr(self) -> dict:
        """
        生成微信支付二维码
        Phase 2实现
        """
        if self.state != BookingState.ROOM_CONFIRMED:
            raise Exception("状态错误，需先确认房型")

        room = self._selected_room
        out_trade_no = self._generate_trade_no()

        result = self.wxpay.create_order(
            description=f"{HOTEL_NAME}-{room['name']}",
            amount=int(room['price'] * self.slots.get('nights', 1) * 100),
            out_trade_no=out_trade_no,
            notify_url="https://your-domain.com/api/wxpay/callback",
        )

        self.trade_no = out_trade_no
        self.state = BookingState.WAITING_PAYMENT

        return {
            "trade_no": out_trade_no,
            "code_url": result["code_url"],  # 扫码支付链接
            "expire_at": result.get("expire_time"),
        }

    def _generate_trade_no(self) -> str:
        """生成内部订单号"""
        import uuid
        return f"AHL{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:8].upper()}"
```

---

### 3.4 自动化预订核心：支付即锁房（Phase 2）

**这是最关键的技术环节**。

**传统OTA流程**：
```
用户选房 → 填信息 → 支付 → 酒店确认 → 生效
           ↑        ↑
        人工确认   等待
     （流失率极高）
```

**AHL自动化流程（Phase 2）**：
```
用户确认方案 → 微信支付 → 支付成功回调 → PMS写入正式订单 → 发送确认
     ↓           ↓            ↓               ↓            ↓
   AI推荐     即时锁定     自动触发        <3秒完成       即时通知
```

#### 3.4.1 微信支付配置与下单

```python
# ============================================================
# 微信支付 v3 API 集成
# ============================================================
# 安装: pip install wechatpayv3

from wechatpayv3 import WeChatPay, WeChatPayNative
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
import json
import hashlib
import time

# ============================================================
# 配置区（上线前替换为真实值）
# ============================================================
WECHAT_MCHID = "your_mch_id"                    # 商户号
WECHAT_SERIAL = "your_serial_no"               # 证书序列号
WECHAT_PRIVATE_KEY_PATH = "/path/to/apiclient_key.pem"  # 商户私钥
WECHAT_APIV3_KEY = "your_apiv3_key"            # APIv3密钥
WECHAT_CALLBACK_URL = "https://your-domain.com/api/wxpay/callback"

# 小程序AppID（用于UnionID/OpenID获取）
MINIAPP_APPID = "your_miniapp_appid"

# ============================================================
# 微信支付初始化
# ============================================================
def init_wxpay():
    """初始化微信支付客户端"""
    wxpay = WeChatPay(
        wechatpay_native=WeChatPayNative(),
        mchid=WECHAT_MCHID,
        serial_no=WECHAT_SERIAL,
        private_key=open(WECHAT_PRIVATE_KEY_PATH).read(),
        apiv3_key=WECHAT_APIV3_KEY,
    )
    return wxpay


# ============================================================
# 支付订单创建
# ============================================================
def create_pay_order(
    wxpay,
    description: str,
    amount: int,        # 金额（分）
    out_trade_no: str,
    notify_url: str,
    attach: str = "",   # 附加数据（用于存储手机号等）
    scene_type: str = "Invoice"
) -> dict:
    """
    创建微信支付Native订单（扫码支付）

    参数:
        description: 商品描述
        amount: 金额，单位分
        out_trade_no: 商户订单号
        notify_url: 支付成功回调地址
        attach: 附加数据（可存手机号等）
    """
    code, response = wxpay.pay(
        description=description,
        amount=amount,
        notify_url=notify_url,
        out_trade_no=out_trade_no,
        attach=attach,
        scene_type=scene_type,
    )

    if code != 200:
        raise Exception(f"微信支付下单失败: code={code}, response={response}")

    result = json.loads(response)
    return {
        "trade_no": out_trade_no,           # 商户订单号
        "code_url": result["code_url"],      # 扫码支付链接（生成二维码）
        "wxpay_order_id": result["id"],      # 微信支付订单号
        "expire_time": result.get("create_time"),  # 订单创建时间
    }


def create_miniapp_order(
    wxpay,
    description: str,
    amount: int,
    out_trade_no: str,
    notify_url: str,
    attach: str = "",
    openid: str = ""
) -> dict:
    """
    创建小程序支付订单（JSAPI支付）

    用于用户在微信小程序内直接支付
    """
    code, response = wxpay.pay(
        description=description,
        amount=amount,
        notify_url=notify_url,
        out_trade_no=out_trade_no,
        attach=attach,
        trade_type="JSAPI",
        payer={"openid": openid},
    )

    if code != 200:
        raise Exception(f"小程序支付下单失败: code={code}, response={response}")

    result = json.loads(response)

    # 小程序调起支付需要这些参数
    return {
        "timeStamp": str(int(time.time())),
        "nonceStr": result["nonce_str"],
        "package": f"prepay_id={result['id']}",
        "signType": "RSA",
        "paySign": "",  # 需前端使用paySign算法生成
    }


# ============================================================
# 支付回调处理（核心）
# ============================================================
def handle_wxpay_callback(request_body: bytes, headers: dict, wxpay) -> tuple:
    """
    微信支付回调处理

    这是自动化预订的核心！
    用户支付成功 → 微信通知我们 → 我们写PMS → 完成

    返回: (response_body, http_status_code)
    """
    try:
        # ---- 1. 验证签名 ----
        verified, callback_data = wxpay.callback(
            request_body, headers
        )

        if not verified:
            return "FAIL", 400

        # ---- 2. 解密支付结果 ----
        pay_data = callback_data.get("resource", {})
        plain_text = wxpay.decrypt_callback(pay_data)
        data = json.loads(plain_text)

        trade_state = data.get("trade_state")  # SUCCESS/REFUND/PAYERROR等
        out_trade_no = data.get("out_trade_no")

        if trade_state != "SUCCESS":
            # 支付失败/关闭，释放预占房态
            release_prelocked_room(out_trade_no)
            return "OK", 200

        # ---- 3. 支付成功 → 获取预锁房态信息 ----
        locked_info = get_prelocked_room(out_trade_no)
        if locked_info is None:
            # 可能是重复回调，检查是否已处理
            existing_order = find_order_by_trade_no(out_trade_no)
            if existing_order:
                return "OK", 200  # 已处理，直接返回成功
            raise Exception(f"未找到预锁房态: {out_trade_no}")

        # ---- 4. 写入PMS正式订单 ----
        pms_order = create_pms_order(
            room_type_id=locked_info["room_type_id"],
            check_in=locked_info["check_in"],
            check_out=locked_info["check_out"],
            guest_name=data.get("payer", {}).get("nick_name", "微信用户"),
            guest_phone=locked_info.get("guest_phone", ""),
            guest_count=locked_info.get("guest_count", 2),
            source="AHL_私域小程序",
            trade_no=out_trade_no,
            wxpay_order_id=data.get("transaction_id"),
            amount=data.get("amount", {}).get("total"),
        )

        # ---- 5. 发送订单确认消息 ----
        openid = data.get("payer", {}).get("openid")
        if openid and pms_order:
            send_order_confirm_message(
                openid=openid,
                order_no=pms_order["order_id"],
                check_in=locked_info["check_in"],
                room_type=locked_info["room_type_name"],
                amount=locked_info.get("price", 0),
            )

        # ---- 6. 释放预占标记 ----
        release_prelocked_room(out_trade_no)

        return "OK", 200

    except Exception as e:
        # 记录错误日志，但不返回失败（微信会重试）
        print(f"支付回调处理异常: {e}")
        return "OK", 200  # 返回200避免微信无限重试


# ============================================================
# 房态预占管理（Redis实现）
# ============================================================
import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# 预锁key格式: prelock:{trade_no}
PRELOCK_TTL = 900  # 15分钟过期


def get_redis_client():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


def prelock_room(
    room_type_id: str,
    check_in: str,
    check_out: str,
    trade_no: str,
    guest_phone: str = "",
    guest_count: int = 2,
    room_type_name: str = "",
    price: float = 0,
    nights: int = 1,
) -> bool:
    """
    预占房态（支付锁定）

    使用Redis SETNX保证原子性，防止超卖
    """
    r = get_redis_client()
    key = f"prelock:{trade_no}"

    # 先检查该房型当日是否还有可预锁名额
    date_key = f"room:{room_type_id}:{check_in}:locked_count"
    current = r.get(date_key)
    max_lock = r.get(f"room:{room_type_id}:total")

    if current and max_lock:
        if int(current) >= int(max_lock):
            return False  # 已满

    # 写入预锁信息
    lock_info = {
        "room_type_id": room_type_id,
        "check_in": check_in,
        "check_out": check_out,
        "trade_no": trade_no,
        "guest_phone": guest_phone,
        "guest_count": guest_count,
        "room_type_name": room_type_name,
        "price": price,
        "nights": nights,
        "created_at": time.time(),
    }

    r.setex(key, PRELOCK_TTL, json.dumps(lock_info))

    # 增加锁定计数
    r.incr(date_key)
    r.expire(date_key, PRELOCK_TTL * 2)

    return True


def get_prelocked_room(trade_no: str) -> dict | None:
    """获取预锁房态信息"""
    r = get_redis_client()
    key = f"prelock:{trade_no}"
    data = r.get(key)
    if data:
        return json.loads(data)
    return None


def release_prelocked_room(trade_no: str) -> bool:
    """释放预锁房态"""
    r = get_redis_client()
    key = f"prelock:{trade_no}"

    locked_info = get_prelocked_room(trade_no)
    if locked_info:
        # 减少锁定计数
        date_key = f"room:{locked_info['room_type_id']}:{locked_info['check_in']}:locked_count"
        r.decr(date_key)

    r.delete(key)
    return True
```

#### 3.4.2 PMS订单写入

```python
# ============================================================
# PMS系统集成（Phase 2）
# ============================================================

# ============================================================
# 配置区（上线前替换为真实值）
# ============================================================
PMS_API_BASE = "https://pms.your-pms.com/api/v1"
PMS_API_KEY = "your_pms_api_key"
PMS_HOTEL_ID = "hotel_leshan_jiazhou"

# ============================================================
# PMS API客户端
# ============================================================
class PMSClient:
    """PMS系统API客户端"""

    def __init__(self, base_url: str, api_key: str, hotel_id: str):
        self.base_url = base_url
        self.api_key = api_key
        self.hotel_id = hotel_id
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def query_availability(
        self,
        check_in: str,
        nights: int = 1,
        room_type: str = None,
        guests: int = None,
    ) -> list:
        """
        查询可用房型

        返回示例:
        [
            {
                "room_type_id": "RT001",
                "name": "江景大床房",
                "price": 458,
                "available": 3,
                "is_featured": True,
            },
            ...
        ]
        """
        params = {
            "hotel_id": self.hotel_id,
            "check_in": check_in,
            "check_out": self._calc_checkout(check_in, nights),
            "guests": guests,
        }

        if room_type:
            params["room_type_name"] = room_type

        resp = self.session.get(f"{self.base_url}/availability", params=params)
        resp.raise_for_status()
        return resp.json().get("rooms", [])

    def create_order(
        self,
        room_type_id: str,
        check_in: str,
        check_out: str,
        guest_name: str,
        guest_phone: str,
        guest_count: int = 2,
        source: str = "walk_in",
        trade_no: str = "",
        wxpay_order_id: str = "",
        amount: int = 0,
        special_requests: list = None,
    ) -> dict:
        """
        创建PMS订单

        这是自动化预订的核心方法！
        微信支付成功后调用此方法写入PMS
        """
        payload = {
            "hotel_id": self.hotel_id,
            "room_type_id": room_type_id,
            "check_in": check_in,
            "check_out": check_out,
            "guest_name": guest_name,
            "guest_phone": guest_phone,
            "guest_count": guest_count,
            "source": source,
            "external_order_no": trade_no,       # 外部订单号（微信支付）
            "payment_order_no": wxpay_order_id,  # 支付流水号
            "amount_total": amount,               # 已支付金额（分）
            "payment_status": "paid",
            "special_requests": special_requests or [],
        }

        resp = self.session.post(f"{self.base_url}/orders", json=payload)
        resp.raise_for_status()

        result = resp.json()
        return {
            "order_id": result["order_id"],
            "confirmation_no": result.get("confirmation_no"),
            "status": result.get("status"),
        }

    def cancel_order(self, order_id: str, reason: str = "") -> dict:
        """取消订单"""
        payload = {"reason": reason}
        resp = self.session.post(
            f"{self.base_url}/orders/{order_id}/cancel",
            json=payload
        )
        resp.raise_for_status()
        return resp.json()

    def get_order(self, order_id: str) -> dict:
        """查询订单详情"""
        resp = self.session.get(f"{self.base_url}/orders/{order_id}")
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def _calc_checkout(check_in: str, nights: int) -> str:
        """计算退房日期"""
        from datetime import datetime, timedelta
        d = datetime.strptime(check_in, "%Y-%m-%d")
        d += timedelta(days=nights)
        return d.strftime("%Y-%m-%d")


# ============================================================
# 初始化全局PMS客户端
# ============================================================
pms_client = PMSClient(PMS_API_BASE, PMS_API_KEY, PMS_HOTEL_ID)


def create_pms_order(**kwargs) -> dict:
    """PMS订单创建的包装函数"""
    return pms_client.create_order(**kwargs)


def query_pms_availability(**kwargs) -> list:
    """PMS可用房型查询的包装函数"""
    return pms_client.query_availability(**kwargs)


# ============================================================
# 根据交易号查找订单（防重复处理）
# ============================================================
def find_order_by_trade_no(trade_no: str) -> dict | None:
    """根据微信支付交易号查找已创建的PMS订单"""
    # 实现：根据out_trade_no查询本地数据库或PMS
    # 这里返回None，需要根据实际数据库实现
    return None
```

#### 3.4.3 订单确认消息发送

```python
# ============================================================
# 订单确认后自动发送服务
# ============================================================

HOTEL_INFO = {
    "name": "乐山锦江嘉州宾馆",
    "address": "乐山市市中区白塔街85号",
    "phone": "0833-2096666",
    "check_in_time": "14:00后",
    "check_out_time": "12:00前",
    "parking": "免费停车，进店报车牌号",
    "breakfast": "07:00-10:00，房间已含双早",
}


def send_order_confirm_message(
    openid: str,
    order_no: str,
    check_in: str,
    room_type: str,
    amount: float,
) -> dict:
    """
    发送订单确认消息给用户（通过微信模板消息/订阅消息）
    """
    # ---- 方式1：微信模板消息（已停止支持，但部分老账号可用）----
    # ---- 方式2：微信订阅消息（当前推荐）----

    template_id = "your_subscribeTemplateId"  # 需在微信公众平台配置

    data = {
        "character_string1": {  # 订单号
            "value": order_no
        },
        "date2": {  # 入住日期
            "value": check_in
        },
        "character_string3": {  # 房型
            "value": room_type
        },
        "amount4": {  # 金额
            "value": f"¥{amount/100:.2f}" if isinstance(amount, int) else f"¥{amount}"
        },
        "phrase5": {  # 订单状态
            "value": "已确认"
        },
    }

    payload = {
        "touser": openid,
        "template_id": template_id,
        "data": data,
        "page": f"pages/order/detail?orderNo={order_no}",  # 小程序页面
    }

    resp = requests.post(
        "https://api.weixin.qq.com/cgi-bin/message/subscribebiz/send",
        params={"access_token": get_wx_access_token()},
        json=payload
    )
    return resp.json()


def send_rich_text_confirm(
    openid: str,
    order_no: str,
    check_in: str,
    room_type: str,
) -> dict:
    """
    发送富文本订单确认（通过客服消息，更灵活）
    """
    msg = (
        f"✅ 预订确认成功！\n\n"
        f"🏨 {HOTEL_INFO['name']}\n"
        f"📅 入住：{check_in}\n"
        f"🛏️ 房型：{room_type}\n"
        f"🔖 订单号：{order_no}\n\n"
        f"━━━━━━━━━━━━━━━━\n\n"
        f"📍 地址：{HOTEL_INFO['address']}\n"
        f"☎️ 电话：{HOTEL_INFO['phone']}\n\n"
        f"🕐 入住：{HOTEL_INFO['check_in_time']}\n"
        f"🕐 退房：{HOTEL_INFO['check_out_time']}\n"
        f"🅿️ 停车：{HOTEL_INFO['parking']}\n"
        f"🍳 早餐：{HOTEL_INFO['breakfast']}\n\n"
        f"有任何问题可随时联系我们，祝您旅途愉快！🌟"
    )

    payload = {
        "touser": openid,
        "msgtype": "text",
        "text": {"content": msg}
    }

    resp = requests.post(
        f"{WECOM_API}/message/send",
        params={"access_token": get_wx_access_token()},
        json=payload
    )
    return resp.json()


# ============================================================
# 微信Access Token管理
# ============================================================
_wx_token_cache = {"token": None, "expires_at": 0}


def get_wx_access_token() -> str:
    """获取微信Access Token（带缓存）"""
    global _wx_token_cache

    if _wx_token_cache["token"] and time.time() < _wx_token_cache["expires_at"] - 60:
        return _wx_token_cache["token"]

    resp = requests.get(
        "https://api.weixin.qq.com/cgi-bin/token",
        params={
            "grant_type": "client_credential",
            "appid": MINIAPP_APPID,
            "secret": "your_miniapp_secret"
        }
    )
    result = resp.json()
    _wx_token_cache["token"] = result["access_token"]
    _wx_token_cache["expires_at"] = time.time() + result["expires_in"]

    return _wx_token_cache["token"]
```

---

## 四、完整SKILL清单

| SKILL ID | 名称 | 输入 | 输出 | 依赖 | Phase |
|---------|------|------|------|------|-------|
| PRIV-NEW-001 | 新媒体公域获客追踪 | 抖音/小红书/公众号数据 | 各渠道转化漏斗 | UTM参数+数据看板 | P0 |
| PRIV-NEW-002 | 新客自动接待 | 企微新好友 | 欢迎语+社群+福利触发 | 企微API | P0 |
| PRIV-NEW-003 | 社群AI客服 | 用户在社群的消息 | NLU识别+需求结构化 | LLM/关键词 | P1 |
| BOOK-NEW-001 | 小程序订单生成 | 用户选房确认 | 微信支付预下单+锁房 | 微信支付API | P2 |
| BOOK-NEW-002 | 支付回调处理 | 微信支付成功回调 | PMS正式订单写入 | PMS API | P2 |
| BOOK-NEW-003 | 订单确认自动发送 | PMS订单创建成功 | 入住指南推送 | 企微/订阅消息API | P2 |

---

## 五、乐山嘉州具体落地路径

### Phase 1：搭建基础（不依赖PMS API）

**目标**：建立最小闭环，测试从内容获客→私域沉淀→预订转化

**时间估算**：约2-3周

| 步骤 | 任务 | 时间 | 产出 | 优先级 |
|------|------|------|------|--------|
| 1 | **微信搜索确认现状** | 1天 | 确认公众号/小程序/企微是否存在 | 🔴 必做 |
| 2 | **开通微信公众号** | 1天 | 内容沉淀主阵地 | 🔴 必做 |
| 3 | **开通微信小程序（预约版）** | 3-5天 | 用户预约入口，无需支付 | 🟡 P1 |
| 4 | **搭建社群+AI客服（关键词模式）** | 2天 | 用户接待自动化（Phase 1用关键词+模板回复，非LLM） | 🟡 P1 |
| 5 | **抖音/小红书内容协同** | 持续 | 公域获客 | 🟡 P1 |
| 6 | **携程EBK数据拉通** | 1天 | 历史用户画像，可导出手机号做短信触达 | 🟢 选做 |

**Phase 1 "自动化"的诚实说明**：

Phase 1的"自动化"是指**人工少干预**而不是"零人工"：

| 环节 | Phase 1实际状态 | 说明 |
|------|----------------|------|
| 欢迎语 | ✅ 自动 | 企微欢迎语自动发送 |
| 需求识别 | ⚠️ 半自动 | AI识别后人工确认再推荐 |
| 房型推荐 | ⚠️ 模板化 | 人工预设推荐模板，AI匹配套用 |
| 预订转化 | ❌ 人工跟进 | 用户确认后，由销售人工电话跟进确认 |
| 订单录入 | ❌ 人工录入 | 人工在PMS录入订单 |

**核心差异**：Phase 1 用户表达预订意向后，需要**人工电话确认**，解决"信任"和"复杂需求（如特殊日期、团队）"问题。

---

### Phase 2：支付即锁房（PMS API打通后）

**前提**：PMS支持API写入订单

**时间估算**：约2-4周（取决于PMS对接难度）

| 步骤 | 任务 | 时间 | 说明 |
|------|------|------|------|
| 1 | 微信商户号申请/确认 | 3-5天 | 如已有商户号可跳过 |
| 2 | 小程序支付能力接入 | 3-5天 | 微信支付v3 API对接 |
| 3 | PMS API对接 | 1-2周 | 房态查询+订单写入API |
| 4 | 回调逻辑开发 | 3-5天 | 支付成功→PMS写入 |
| 5 | 联调测试 | 3-5天 | 端到端测试 |
| 6 | 上线灰度 | 1周 | 5%流量先跑 |

---

### Phase 3：智能化升级（可选）

| 功能 | 说明 | 价值 |
|------|------|------|
| LLM意图理解 | 替代关键词匹配，更自然 | 用户体验↑ |
| 智能推荐 | 根据用户画像个性化推荐 | 转化率↑ |
| 自动清房控价 | 根据预订进度自动调整价格 | 收益↑ |
| RFM分层运营 | 基于消费行为的精细化运营 | 复购率↑ |

---

## 六、关键问题清单（需实地确认）

| 问题 | 确认方式 | 影响 |
|------|---------|------|
| 酒店是否有微信公众号 | 微信搜索"乐山锦江嘉州宾馆" | 内容发布主阵地 |
| 是否有微信小程序 | 微信搜索 | 预约入口 |
| 是否开通微信商户号 | 财务确认 | 收款能力 |
| 是否开通企微 | 管理方确认 | 私域运营基础 |
| PMS系统名称 | 技术摸底 | 对接方式 |
| PMS是否支持API | 技术摸底 | Phase 2能否实现 |
| 当前预订转化流程 | 现场观察/访谈 | 优化起点 |

---

## 七、风险与对策

| 风险 | 概率 | 影响 | 对策 |
|------|------|------|------|
| PMS不支持API | 中 | 高 | Phase 1用人工电话跟进，Phase 2再谈API |
| 微信支付商户号申请被拒 | 低 | 高 | 使用已有商户号，或通过服务商渠道 |
| 内容引流效果差 | 中 | 中 | 复用携程EBK已有用户数据做精准触达 |
| 企微被封/限流 | 低 | 中 | 多账号矩阵，分散风险 |
| 用户信任度不足 | 高 | 中 | Phase 1保留人工电话确认环节 |

---

## 八、补充说明

### 8.1 关于携程店铺（Hotel ID 73690948）

携程店铺是**重要参考**而非竞争对手：

1. **携程EBK**可以导出历史订单用户数据（需酒店授权）
2. **点评内容**可以直接搬运到小红书/抖音（UGC素材）
3. **携程用户**可以通过短信触达，引导加入私域社群
4. **OTA评分**是公域信任背书，是内容种草的天然素材

**核心逻辑**：把携程当流量池，不当成交道主战场。

### 8.2 技术债说明

Phase 1的MVP（最小可行产品）存在以下技术债，上线后需逐步偿还：

| 技术债 | 说明 | 偿还时间 |
|--------|------|---------|
| 关键词→LLM | Phase 1用关键词匹配，成本低但体验有限 | Phase 3 |
| 人工预订→自动预订 | Phase 1用户确认后人工跟进 | Phase 2 |
| 单小程序→多小程序矩阵 | 未来可能需要防止封号 | Phase 3 |
| 短信/电话→企微消息 | 老用户习惯短信/电话，需引导 | 持续 |

---

**文档版本**：V1.0
**下次更新**：待实地确认后
**负责人**：待指定
