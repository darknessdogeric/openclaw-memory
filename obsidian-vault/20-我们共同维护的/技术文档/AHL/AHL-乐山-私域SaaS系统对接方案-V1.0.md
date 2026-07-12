# AHL × 乐山嘉州酒店 — 私域SaaS系统对接方案 V1.0

> **文档状态**：技术补充方案 | 撰写日期：2026-03-27
> **核心议题**：酒店微信私域直销SaaS全景图 + AHL对接路径 + 乐山嘉州现状摸底

---

## 0. 前置背景：为什么私域SaaS对接是关键技术命题

Eric的核心判断已得到行业验证：**酒店私域预订不是从零搭建，而是对接已有SaaS系统。**

这意味着AHL的商业模式存在两种截然不同的技术路径：

| 路径 | 前提 | AHL角色 | 技术复杂度 | 谈判复杂度 |
|------|------|---------|------------|------------|
| **路径A** | 酒店已有直销SaaS（且开放API） | 智能前端（流量理解层） | 中等 | 低（酒店已有意愿） |
| **路径B** | 酒店没有/系统不开放 | 直客通入驻 + AHL对接 | 较高 | 高（需说服酒店换系统） |
| **路径C** | 酒店使用集团封闭系统 | 需找集团IT谈判 | 高 | 极高 |

**本方案围绕路径A（最优解）展开，同时提供路径B的备选方案。**

---

## 1. 酒店主流私域SaaS全景图

### 1.1 直客通（Zhikitong）— 微信私域预订最大SaaS平台

**一句话定位**：酒店微信直销的"水电煤"，提供小程序 + 公众号 + 会员管理 + 微信支付一体化解决方案。

#### 核心功能

| 功能模块 | 具体能力 |
|----------|----------|
| **小程序商城** | 房型展示、在线预订、支付闭环 |
| **公众号营销** | 模板消息、推送、裂变活动 |
| **会员体系** | 会员等级、积分、权益卡 |
| **营销工具** | 优惠券、拼团、秒杀、限时折扣 |
| **订单管理** | 订单处理、入离店管理 |
| **数据分析** | 预订漏斗、用户画像、收益分析 |
| **微信支付直连** | 商户号直结，无需OTA中转 |

#### API开放程度

| 维度 | 评级 | 说明 |
|------|------|------|
| **房态查询API** | ⭐⭐⭐ 中等 | 提供查询接口，但需商务授权 |
| **订单创建API** | ⭐⭐⭐ 中等 | 支持第三方代下单，需白名单 |
| **订单回调Webhook** | ⭐⭐⭐⭐ 较好 | 支持订单状态变更回调 |
| **会员信息API** | ⭐⭐ 有限 | 仅对大客户开放 |
| **开放程度总结** | **有条件开放** | 需成为直客通合作伙伴，签署API协议 |

**关键限制**：
- 直客通的API不对小客户开放，需达到一定体量或成为渠道合作伙伴
- API文档不公开，需联系商务获取
- 部分接口需要直客通技术对接，非完全自助

#### 典型客户

- 中高端连锁酒店（开元、君澜、書香等）
- 单体高星酒店（数百到数千间客房）
- 大型旅游集团地方酒店

**君澜酒店案例**（已知）：
- 君澜度假酒店使用直客通
- 直销系统API与PMS对接，实现**房态/订单/价格三同步**
- 客户通过直客通小程序预订，订单实时写入PMS

#### 对方配合开发要求

| 配合项 | 工作量 | 难度 |
|--------|--------|------|
| 开通API白名单 | 直客通常规服务 | ⭐ 低 |
| 获取API文档 | 需商务申请 | ⭐⭐ 中等 |
| 房态同步联调 | 1-2天 | ⭐⭐ 中等 |
| 订单回调配置 | 0.5天 | ⭐ 低 |
| 对方配合等级 | **中等** | 直客通已支持此类集成 |

---

### 1.2 麦田云PMS — 一体化PMS+私域方案

**一句话定位**：PMS系统自带私域带客+微信支付直连，适合中小型酒店/民宿。

#### 核心功能

| 功能模块 | 具体能力 |
|----------|----------|
| **PMS核心** | 房态管理、预订管理、客人管理 |
| **私域预订** | 微信小程序直销、微商城 |
| **支付直连** | 微信支付直结，实时到账 |
| **分销模块** | 渠道管理、佣金结算 |
| **CRM** | 客人档案、标签、消费记录 |
| **移动端** | 老板/员工移动管理App |

#### API开放程度

| 维度 | 评级 | 说明 |
|------|------|------|
| **PMS数据API** | ⭐⭐⭐⭐ 较好 | 提供标准REST API |
| **房态实时同步** | ⭐⭐⭐⭐ 较好 | 支持WebSocket实时推送 |
| **订单写入API** | ⭐⭐⭐⭐ 较好 | 支持第三方创建订单 |
| **开放程度总结** | **相对开放** | 对技术合作伙伴开放API文档 |

**关键优势**：
- 麦田云既是PMS又是直销系统，房态天然一致，无同步延迟
- 对中小型酒店而言，一套系统搞定所有
- API文档相对完善，技术对接成本低

#### 典型客户

- 精品民宿（50-200间客房）
- 小型连锁酒店
- 景区度假酒店

#### 对方配合开发要求

| 配合项 | 工作量 | 难度 |
|--------|--------|------|
| 获取API Key | 麦田云服务期内免费提供 | ⭐ 低 |
| 技术对接文档 | 麦田云提供 | ⭐ 低 |
| 联调测试 | 1-2天 | ⭐⭐ 中等 |
| 对方配合等级 | **较高** | 麦田云鼓励第三方接入 |

---

### 1.3 绿云PMS（绿云科技）— 大旅游住宿业PMS

**一句话定位**：大型住宿业PMS，支持微信私域对接，但私域模块非核心主打。

#### 核心功能

| 功能模块 | 具体能力 |
|----------|----------|
| **PMS核心** | 集团化管理、多门店支持 |
| **CRS（中央预订）** | 中央库存、渠道分发 |
| **微信直销** | 需集成绿云微信模块或第三方 |
| **接口开放** | 支持Opera/Oracle接口协议 |
| **集团管理** | 统一会员、统一价格、统一库存 |

#### API开放程度

| 维度 | 评级 | 说明 |
|------|------|------|
| **标准接口** | ⭐⭐⭐ 中等 | 符合行业标准（类似Opera） |
| **Web Service** | ⭐⭐⭐ 中等 | SOAP/REST均支持 |
| **房态同步** | ⭐⭐⭐ 需集成 | 需通过绿云微信模块或第三方 |
| **开放程度总结** | **面向大客户开放** | 中小酒店可能拿不到深度接口 |

**关键限制**：
- 绿云的强项是集团化PMS管理，私域不是其核心卖点
- 直销功能通常需要额外购买微信模块
- 对单体中小酒店技术支持力度有限

#### 典型客户

- 大型旅游集团（锦江、华住部分品牌）
- 连锁酒店集团
- 省级旅游集团酒店（锦江嘉州可能在此列）

#### 对方配合开发要求

| 配合项 | 工作量 | 难度 |
|--------|--------|------|
| 获取接口权限 | 需绿云商务支持 | ⭐⭐⭐ 较高 |
| 技术对接 | 需集团IT协调 | ⭐⭐⭐ 较高 |
| 联调测试 | 3-5天（含集团审批） | ⭐⭐⭐ 较高 |
| 对方配合等级 | **不确定** | 取决于绿云对该酒店的重视程度 |

---

### 1.4 锦江集团自研/统一直销系统

**推测场景**：锦江嘉州作为省旅投旗下酒店，**可能使用锦江集团统一的直销平台**。

#### 可能性分析

| 系统类型 | 可能性 | 说明 |
|----------|--------|------|
| **锦江WeHotel系统** | ⭐⭐⭐ 中高 | 锦江集团官方直销平台，覆盖小程序+APP |
| **直客通（锦江定制版）** | ⭐⭐ 中 | 锦江部分品牌使用直客通 |
| **绿云PMS+自建微商城** | ⭐⭐ 中 | 绿云PMS+微信自营商城拼搭 |
| **完全自研** | ⭐ 低 | 成本高，中小型酒店一般不用 |
| **没有任何系统** | ⭐ 极低 | 国企必有数字化系统 |

#### 锦江WeHotel已知信息

- **载体**：锦江WeHotel APP + 小程序
- **功能**：会员积分、预订、支付
- **API开放程度**：锦江系系统对外合作态度保守
- **对接难度**：可能需要走锦江集团IT部门审批

#### 对方配合开发要求

| 配合项 | 工作量 | 难度 |
|--------|--------|------|
| 找到对接窗口 | 需通过酒店→集团IT | ⭐⭐⭐⭐ 高 |
| 商务谈判 | 需签署数据合作协议 | ⭐⭐⭐⭐ 高 |
| 技术对接 | 取决于系统开放程度 | 未知 |
| 对方配合等级 | **不确定→偏低** | 国企流程长，决策链慢 |

---

### 1.5 其他私域SaaS系统一览

| 系统 | 定位 | API开放度 | 典型客户 | AHL对接难度 |
|------|------|------------|----------|-------------|
| **订单来了** | 民宿主SCRM+预订 | ⭐⭐⭐⭐ 高 | 民宿、精品酒店 | ⭐ 低 |
| **全方位文旅** | 景区+酒店一体化 | ⭐⭐ 中等 | 文旅综合体 | ⭐⭐ 中等 |
| **去哪儿云PMS** | OTA+PMS结合 | ⭐⭐ 受限 | OTA商户 | ⭐⭐⭐ 较高 |
| **番茄来了** | 中小民宿PMS | ⭐⭐⭐ 中等 | 民宿、客栈 | ⭐⭐ 中等 |
| **小猪民宿** | C端民宿平台+工具 | ⭐⭐ 受限 | 民宿房东 | ⭐⭐⭐ 较高 |
| **东软SaaS** | 传统大厂方案 | ⭐⭐ 中等 | 高星酒店 | ⭐⭐⭐ 较高 |

---

### 1.6 全景对比总结

```
┌────────────────────────────────────────────────────────────────────┐
│                    酒店私域SaaS对接难度矩阵                          │
├─────────────────┬──────────┬──────────┬──────────┬────────────────┤
│ 系统             │ 直客通   │ 麦田云   │ 绿云PMS  │ 锦江WeHotel   │
├─────────────────┼──────────┼──────────┼──────────┼────────────────┤
│ API开放程度      │ 中等     │ 较高     │ 中等偏下  │ 低/不确定      │
│ 技术对接难度     │ 中等     │ 低       │ 较高     │ 高             │
│ 商务谈判难度     │ 中等     │ 低       │ 中等     │ 高             │
│ 典型酒店规模     │ 中大型   │ 中小型   │ 大型集团  │ 国有集团       │
│ AHL优先对接      │ ★★★★   │ ★★★★★   │ ★★★     │ ★★           │
└─────────────────┴──────────┴──────────┴──────────┴────────────────┘
```

**结论**：如果锦江嘉州使用**麦田云或直客通**，AHL对接难度相对可控；如果使用**锦江WeHotel或绿云集团版**，需要走更长商务流程。

---

## 2. AHL对接策略：三种情况的对接路径

### 情况A：酒店已有直销SaaS（且API可接入）— 最优路径

**前提条件**：
- 酒店已使用直客通/麦田云/其他直销SaaS
- 酒店愿意开放API或协助对接
- AHL作为"智能前端"，SaaS作为"交易后端"

#### 对接架构图

```
┌──────────────────────────────────────────────────────────────────┐
│                          用户侧                                   │
│                                                                  │
│   抖音/小红书内容 ──→ 扫码 ──→ 直销小程序（直客通/麦田云）         │
│                                    │                             │
│                              AI需求理解                          │
│                              AHL BOOK-NLU                        │
│                                    │                             │
│                          对接API查询可用房型                     │
│                         ←────────────────────                   │
│                                    │                             │
│                              返回推荐列表                         │
│                                    │                             │
│                              用户确认预订                        │
│                                    │                             │
│                          订单创建API写入直销SaaS                 │
│                                    │                             │
│                          微信支付（直销SaaS）                   │
│                                    │                             │
│                     订单完成Webhook回调AHL                       │
│                           ↓                                      │
│                    AHL触发服务流                                 │
│              （欢迎语/入住指南/本地推荐）                         │
│                                    │                             │
│                    订单数据同步回传PMS（可选）                   │
└──────────────────────────────────────────────────────────────────┘
```

#### AHL侧技术实现

**核心原则**：AHL不碰交易支付，只做**需求理解+推荐+服务触发**，交易闭环由直销SaaS完成。

| AHL模块 | 职责 | 技术说明 |
|---------|------|----------|
| **BOOK-NLU** | 用户需求理解 | 对话式收集：入住日期/人数/预算/特殊需求 |
| **ROOM-MATCHER** | 房型推荐 | 对接直销SaaS API查询可用房，返回推荐 |
| **BOOK-CONFIRM** | 确认跳转 | 生成预订确认页，引导用户跳转直销小程序 |
| **SERVICE-TRIGGER** | 服务触发 | Webhook接收订单，触发欢迎语/指南推送 |

#### 关键优势

1. **AHL不碰支付**：资金不过AHL，避免支付合规问题
2. **酒店已有信任**：用户习惯用酒店直销小程序，转化路径成熟
3. **房态实时**：房态从直销SaaS实时查询，不存在库存不一致
4. **实施周期短**：只需对接API，无需搭建交易系统

---

### 情况B：酒店有直销SaaS但API不开放 — 过渡方案

**前提条件**：
- 酒店已有直销SaaS（如直客通），但不愿开放API给AHL
- 或酒店有顾虑，不愿深度技术对接

#### 对接架构图

```
用户 ──→ AHL对话需求 ──→ AHL推荐房型 ──→ 
    │
    ├─→ 提供直销小程序码（酒店原有渠道）
    │       │
    │       用户自行扫码 → 酒店小程序完成预订
    │
    └─→ AHL帮用户"代查" → 截图/链接发给用户
```

#### 技术实现

| 方式 | 实现方法 | 局限性 |
|------|----------|--------|
| **方案B1：小程序跳转** | 生成直销小程序路径/参数，微信内跳转 | 需直销小程序已配置路径URL Scheme |
| **方案B2：生成预订卡片** | AHL生成含预订信息卡片，用户截图保存 | 仅信息传递，用户需手动操作 |
| **方案B3：短信/链接** | 生成直销小程序短链，通过微信/短信发用户 | 打开率低，转化漏斗长 |

**方案B的缺陷**：
- 无法追踪用户是否实际完成预订
- AHL无法触发后续服务流（因为不知道订单是否成交）
- 转化率难以统计

**结论**：方案B是"不得已而为之"，建议优先说服酒店开放API。

---

### 情况C：酒店没有直销SaaS或使用封闭集团系统

**前提条件**：
- 酒店完全没有微信直销系统
- 或使用封闭的集团系统（锦江WeHotel等）

#### 路径C1：直客通标准入驻（推荐）

**适用场景**：酒店有意愿建立微信直销能力，愿意换系统或新增。

```
AHL BOOK推荐 ──→ 用户确认 ──→ 跳转直客通标准小程序
                                    │
                              AHL对接直客通API
                                    │
                              订单Webhook回调AHL
                                    │
                              触发服务流
```

**直客通入驻流程**：
1. 酒店联系直客通商务，申请入驻
2. 提交酒店资质（营业执照等）
3. 配置房型/价格/会员权益
4. 开通小程序（直客通提供模板）
5. 获得API权限（AHL对接用）

**时间周期**：约2-4周（商务+配置+测试）

#### 路径C2：订单来了快速接入

**适用场景**：民宿/中小酒店，希望快速建立微信直销+AHL对接。

```
订单来了（标准SaaS）──→ 酒店入驻（1-3天）──→ AHL对接API
```

**优势**：
- 入驻快（1-3个工作日）
- API开放度高（技术文档完善）
- 适合50-200间客房规模

#### 路径C3：封闭集团系统（高难度）

**适用场景**：锦江WeHotel等封闭系统。

```
锦江WeHotel ──→ 需走集团IT部门 ──→ 商务谈判 ──→ API开放审批
                                           │
                                    无法短期突破
                                    建议转向其他酒店先试点
```

**建议**：锦江嘉州如果使用封闭集团系统，AHL对接**不作为Phase 1目标**，改为：
- 先在其他使用开放SaaS的酒店落地
- 锦江嘉州案例需要更高层商务资源推动

---

## 3. 直客通API对接代码框架

> **声明**：以下为假设性API结构，实际直客通API需联系商务获取正式文档。以下代码仅供参考，实际对接前需用真实API文档替换接口路径和参数名。

### 3.1 基础配置

```python
import requests
import hashlib
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ZKTConfig:
    """直客通API配置"""
    api_base: str = "https://api.zhikitong.com/v1"
    hotel_id: str = ""           # 酒店在直客通的ID
    app_id: str = ""             # 直客通分配的AppID
    app_secret: str = ""         # 直客通分配的AppSecret
    
    def get_auth_headers(self) -> Dict[str, str]:
        """生成鉴权请求头"""
        timestamp = str(int(time.time()))
        sign = hashlib.md5(
            f"{self.app_id}{timestamp}{self.app_secret}".encode()
        ).hexdigest()
        return {
            "X-App-Id": self.app_id,
            "X-Timestamp": timestamp,
            "X-Sign": sign,
            "Content-Type": "application/json"
        }

# 全局配置实例（运行时注入）
zkt_config: Optional[ZKTConfig] = None

def init_zkt_config(hotel_id: str, app_id: str, app_secret: str):
    """初始化直客通配置"""
    global zkt_config
    zkt_config = ZKTConfig(
        hotel_id=hotel_id,
        app_id=app_id,
        app_secret=app_secret
    )
```

### 3.2 房态查询

```python
def zkt_query_rooms(
    check_in: str, 
    check_out: str,
    guests: int = 1,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
) -> Dict[str, Any]:
    """
    查询直客通可用房型
    
    Args:
        check_in: 入住日期，格式 YYYY-MM-DD
        check_out: 离店日期，格式 YYYY-MM-DD
        guests: 入住人数
        min_price: 最低价格（可选）
        max_price: 最高价格（可选）
    
    Returns:
        {
            "success": True,
            "rooms": [
                {
                    "room_type_id": "RT001",
                    "name": "豪华大床房",
                    "bed_type": "大床1.8m",
                    "max_occupancy": 2,
                    "available_count": 5,
                    "price_info": {
                        "total_price": 598.00,
                        "nightly_rate": [299.00, 299.00],
                        "currency": "CNY"
                    },
                    "breakfast": "含双早",
                    "cancellation_policy": "入住日前一天14:00前免费取消",
                    "images": ["https://..."]
                }
            ],
            "query_time": "2026-03-27 10:30:00"
        }
    """
    if not zkt_config:
        raise RuntimeError("直客通未初始化，请先调用 init_zkt_config()")
    
    params = {
        "hotel_id": zkt_config.hotel_id,
        "check_in": check_in,
        "check_out": check_out,
        "guests": guests
    }
    
    if min_price is not None:
        params["min_price"] = min_price
    if max_price is not None:
        params["max_price"] = max_price
    
    try:
        response = requests.get(
            f"{zkt_config.api_base}/rooms/available",
            params=params,
            headers=zkt_config.get_auth_headers(),
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") == 0:
            return {
                "success": True,
                "rooms": result.get("data", {}).get("rooms", []),
                "query_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            return {
                "success": False,
                "error": result.get("message", "查询失败")
            }
            
    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"网络请求失败: {str(e)}"
        }
```

### 3.3 订单创建

```python
def zkt_create_order(
    booking_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    在直客通创建订单
    
    Args:
        booking_info: 预订信息，包含：
            - room_type_id: 房型ID
            - check_in: 入住日期 YYYY-MM-DD
            - check_out: 离店日期 YYYY-MM-DD
            - guest_name: 客人姓名
            - guest_phone: 客人手机号
            - guest_count: 入住人数（默认1）
            - special_requests: 特殊需求（可选）
            - source: 预订来源，固定值 "AHL_AI"
    
    Returns:
        {
            "success": True,
            "order_id": "ZT2026032700001",
            "total_price": 598.00,
            "payment_url": "weixin://...",
            "qr_code_url": "https://..."
        }
    """
    if not zkt_config:
        raise RuntimeError("直客通未初始化，请先调用 init_zkt_config()")
    
    payload = {
        "hotel_id": zkt_config.hotel_id,
        "room_type_id": booking_info.get("room_type_id"),
        "check_in": booking_info.get("check_in"),
        "check_out": booking_info.get("check_out"),
        "guest_name": booking_info.get("guest_name"),
        "guest_phone": booking_info.get("guest_phone"),
        "guest_count": booking_info.get("guest_count", 1),
        "source": "AHL_AI",  # 固定来源标识
        "remark": booking_info.get("special_requests", "")
    }
    
    try:
        response = requests.post(
            f"{zkt_config.api_base}/order/create",
            json=payload,
            headers=zkt_config.get_auth_headers(),
            timeout=15
        )
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") == 0:
            data = result.get("data", {})
            return {
                "success": True,
                "order_id": data.get("order_id"),
                "total_price": data.get("total_price"),
                "payment_url": data.get("payment_url"),
                "qr_code_url": data.get("qr_code_url"),
                "expire_time": data.get("expire_time")  # 订单过期时间
            }
        else:
            return {
                "success": False,
                "error": result.get("message", "创建订单失败")
            }
            
    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"网络请求失败: {str(e)}"
        }
```

### 3.4 订单查询与状态同步

```python
def zkt_query_order(order_id: str) -> Dict[str, Any]:
    """
    查询直客通订单状态
    
    Returns:
        {
            "success": True,
            "order": {
                "order_id": "ZT2026032700001",
                "status": "paid",  # pending/paid/cancelled/completed
                "room_type": "豪华大床房",
                "check_in": "2026-03-28",
                "check_out": "2026-03-30",
                "guest_name": "张三",
                "total_price": 598.00,
                "paid_at": "2026-03-27 11:00:00",
                "pms_sync_status": "synced"  # 是否已同步PMS
            }
        }
    """
    if not zkt_config:
        raise RuntimeError("直客通未初始化，请先调用 init_zkt_config()")
    
    params = {
        "hotel_id": zkt_config.hotel_id,
        "order_id": order_id
    }
    
    try:
        response = requests.get(
            f"{zkt_config.api_base}/order/query",
            params=params,
            headers=zkt_config.get_auth_headers(),
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") == 0:
            return {
                "success": True,
                "order": result.get("data", {}).get("order")
            }
        else:
            return {
                "success": False,
                "error": result.get("message", "查询失败")
            }
            
    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"网络请求失败: {str(e)}"
        }
```

### 3.5 Webhook接收（直客通→AHL）

```python
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

@app.route("/webhook/zkt_order", methods=["POST"])
def zkt_order_webhook():
    """
    接收直客通订单状态变更回调
    
    直客通会在以下时机回调：
    - order.created: 订单创建
    - order.paid: 订单支付成功
    - order.cancelled: 订单取消
    - order.completed: 订单完成（离店）
    """
    # 1. 验证签名（防止伪造）
    signature = request.headers.get("X-Sign", "")
    timestamp = request.headers.get("X-Timestamp", "")
    body = request.get_json()
    
    # 签名验证逻辑（实际使用直客通提供的密钥）
    expected_sign = hashlib.sha256(
        f"{timestamp}{body}".encode()
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected_sign):
        return jsonify({"code": 401, "message": "签名验证失败"}), 401
    
    # 2. 解析事件
    event_type = body.get("event")
    order_data = body.get("data", {})
    
    # 3. 根据事件类型处理
    if event_type == "order.paid":
        # 订单支付成功 → 触发AHL服务流
        order_id = order_data.get("order_id")
        guest_name = order_data.get("guest_name")
        check_in = order_data.get("check_in")
        room_type = order_data.get("room_type_name")
        
        # 调用AHL服务流触发
        from ahl_service import trigger_welcome_flow
        trigger_welcome_flow(
            order_id=order_id,
            guest_name=guest_name,
            check_in=check_in,
            room_type=room_type,
            source="直客通"
        )
        
        return jsonify({"code": 0, "message": "处理成功"})
    
    elif event_type == "order.cancelled":
        # 订单取消 → 更新AHL记录
        from ahl_service import cancel_order_record
        cancel_order_record(order_id=order_data.get("order_id"))
        return jsonify({"code": 0, "message": "处理成功"})
    
    return jsonify({"code": 0, "message": "收到事件"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### 3.6 麦田云API对接框架（备选）

```python
"""
麦田云PMS API对接框架
适用于酒店使用麦田云PMS（含私域模块）的情况

官方文档：需联系麦田云商务获取
以下为推测性接口，实际对接前需用真实文档替换
"""

class MaitianPMS:
    """麦田云PMS对接客户端"""
    
    def __init__(self, hotel_id: str, api_key: str):
        self.base_url = "https://api.maitianyun.com/v1"
        self.hotel_id = hotel_id
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def query_rooms(self, check_in: str, check_out: str) -> Dict:
        """查询可用房型"""
        params = {
            "hotel_id": self.hotel_id,
            "arr": check_in,
            "dep": check_out
        }
        response = requests.get(
            f"{self.base_url}/room/available",
            params=params,
            headers=self.headers,
            timeout=10
        )
        return response.json()
    
    def create_order(self, order_info: Dict) -> Dict:
        """创建订单"""
        payload = {
            "hotel_id": self.hotel_id,
            "room_type_id": order_info["room_type_id"],
            "arr": order_info["check_in"],
            "dep": order_info["check_out"],
            "guest_name": order_info["guest_name"],
            "mobile": order_info["guest_phone"],
            "source": "AHL_AI"
        }
        response = requests.post(
            f"{self.base_url}/order/create",
            json=payload,
            headers=self.headers,
            timeout=15
        )
        return response.json()
    
    def get_order_status(self, order_id: str) -> Dict:
        """查询订单状态"""
        response = requests.get(
            f"{self.base_url}/order/{order_id}",
            headers=self.headers,
            timeout=10
        )
        return response.json()
```

---

## 4. 乐山嘉州系统摸底清单（到达后必问）

> **核心原则**：到达乐山嘉州后，第一个技术问题：**"你们现在微信订房是用哪个系统？"**

### 4.1 必问清单（技术摸底）

#### Q1：微信订房渠道（最关键）
```
你们现在微信订房/直销是用哪个系统？
- 直客通？
- 麦田云？
- 绿云PMS？
- 锦江WeHotel？
- 其他？
```

**追问**：
- 小程序叫什么名字？
- 是自己开发的还是用的SaaS平台？

#### Q2：PMS系统
```
你们前台用的PMS系统是哪个？
- 绿云？
- 西软？
- 别样红？
- 麦田云？
- 其他？
```

**追问**：
- PMS系统和微信订房系统是同一个供应商吗？
- 两者之间房态是否自动同步？

#### Q3：API开放意愿
```
如果我们做一个AI预订助手（自动理解客人需求，推荐房型），
对接你们的订房系统，你们技术/IT能配合吗？
```

**追问**：
- 需要走集团审批吗？
- 对接的话主要卡点是技术还是商务？

#### Q4：会员系统
```
你们有会员体系吗？
- 会员积分、权益怎么管理的？
- 是在直销系统里还是PMS里？
```

#### Q5：微信生态现状
```
你们有公众号吗？粉丝多少？
- 有没有在做微信营销（优惠券/拼团/秒杀）？
- 平时怎么推广微信号的？
```

---

### 4.2 摸底结果对应策略

| 摸底结果 | AHL对接策略 | 优先级别 |
|----------|------------|---------|
| 直客通 + API可开放 | 直客通深度对接 | ⭐⭐⭐⭐⭐ 最高 |
| 麦田云PMS | 麦田云API对接 | ⭐⭐⭐⭐ 高 |
| 直客通 + API不开放 | 引导开放或方案B | ⭐⭐⭐ 中 |
| 绿云PMS + 微信自建 | 绿云API对接（难度高） | ⭐⭐ 中 |
| 锦江WeHotel | 暂缓，需集团层面推动 | ⭐ 低 |
| 没有任何系统 | 建议直客通入驻 | ⭐⭐⭐ 中 |

---

### 4.3 摸底话术模板

```
【开场白】
张总，我们这次来主要想了解一下咱们酒店的数字化现状，
这样我们AHL的AI预订助手才能知道怎么和咱们现有系统对接。

【切入正题】
我想先问一下，咱们酒店现在客人通过微信订房，主要走哪个渠道？
是直客通、麦田云这种第三方平台，还是咱们自己开发的系统？

【对方回答后追问】
哦，XX系统。他们的系统开放API吗？我们AI助手需要查询房态和订单。
如果能对接的话，客人在我们AI助手这里完成需求沟通，直接跳转预订，
体验会非常顺畅。

【如果对方不清楚API情况】
没关系，技术对接的事我们可以和他们的商务再谈。
主要是确认一下你们现在用的是什么系统，这样我们心里有数。
```

---

## 5. Phase 1/2/3 分阶段策略

### Phase 1：现状摸底 + 方案确认（Day 1-3，到达乐山后）

**目标**：确认乐山嘉州的私域SaaS类型和API开放程度。

**执行动作**：
1. 按第4章摸底清单与酒店方沟通
2. 收集：直销SaaS名称、PMS名称、系统截图/截图
3. 判断对接可行性和工作量

**交付物**：
- 《乐山嘉州系统现状确认表》
- Phase 2技术方案调整

**判断标准**：
| Phase 1结论 | 后续路径 |
|-------------|----------|
| 直客通/麦田云 + API可对接 | 立即启动Phase 2 |
| 直客通/麦田云 + API需申请 | Phase 2A（申请API期间准备内容运营） |
| 封闭系统/无系统 | Phase 2B（直客通入驻 or 换酒店试点） |

---

### Phase 2：API对接开发（确认后2-3周）

**目标**：完成AHL与酒店直销SaaS的API对接，实现订单闭环。

**执行动作**：

#### Phase 2A：酒店已有可对接SaaS
1. 联系直客通/麦田云商务，申请API权限
2. 获取API文档和技术对接窗口
3. 开发AHL对接模块（参照第3章代码框架）
4. 联调测试：房态查询→订单创建→支付回调
5. 灰度上线：先跑1-2周内部测试

#### Phase 2B：酒店需入驻直客通
1. 协助酒店联系直客通商务，入驻申请
2. 配置酒店小程序：房型/价格/会员
3. 获得API权限后开发对接
4. 联调测试
5. 上线

**交付物**：
- AHL对接模块代码
- API联调测试报告
- 小程序跳转/订单回调流程验证

**Phase 2完成标志**：
- [ ] AHL能够查询到酒店真实可用房态
- [ ] 用户可在AHL引导下完成预订（跳转小程序）
- [ ] 订单支付成功后AHL收到Webhook回调
- [ ] AHL触发欢迎语/入住指南服务流

---

### Phase 3：私域运营 + 数据闭环（Phase 2完成后持续）

**目标**：基于对接能力，构建完整的私域运营闭环。

**执行动作**：

1. **AHL服务流全链路打通**
   - 预订前：AI需求理解→推荐→预订引导
   - 预订后：订单确认→入住指南→本地推荐
   - 离店后：离店提醒→评价引导→复购推荐

2. **会员数据沉淀**
   - 将AHL服务的客人信息同步到酒店会员系统
   - 基于AHL交互数据打标签（需求偏好/预算段）

3. **营销自动化**
   - 对接酒店营销工具（优惠券/限时折扣）
   - AHL智能推荐触发营销活动

4. **数据复盘**
   - 每周统计：AHL引导预订量/转化率/GMV贡献
   - 优化AHL推荐算法

**Phase 3完成标志**：
- [ ] AHL全流程服务记录可追踪
- [ ] 酒店私域流量带来增量预订
- [ ] 月度GMV贡献可量化

---

## 附录A：直客通API文档申请模板

```
致：直客通商务团队

公司：[AHL运营主体名称]
联系人：[姓名] / [电话] / [邮箱]

合作需求：
我们正在为贵司酒店客户（[酒店名称]）搭建AI智能预订助手，
需要在客人授权同意的前提下，通过API完成以下功能：
1. 查询可用房型及价格
2. 创建订单并获取支付链接
3. 接收订单状态变更回调

请提供：
1. 直客通API接口文档（技术对接用）
2. API权限开通申请流程
3. 技术对接窗口联系方式

感谢！
```

---

## 附录B：术语对照表

| 术语 | 全称 | 说明 |
|------|------|------|
| **SaaS** | Software as a Service | 软件即服务，云端订阅制 |
| **PMS** | Property Management System | 酒店物业管理系统 |
| **CRS** | Central Reservation System | 中央预订系统 |
| **API** | Application Programming Interface | 应用程序接口 |
| **Webhook** | Webhook | 服务器主动推送的事件通知 |
| **NLU** | Natural Language Understanding | 自然语言理解 |
| **DT** | Digital Twin | 数字孪生 |
| **GMV** | Gross Merchandise Volume | 商品交易总额 |

---

## 附录C：相关文档索引

| 文档 | 路径 | 与本文档关系 |
|------|------|-------------|
| AHL-乐山-AI预订助手设计方案-V1.0.md | docs/ | 上游：AI预订助手整体设计 |
| AHL-乐山-PMS系统对接方案-V1.0.md | docs/ | 平行：PMS对接（交易后端） |
| AHL-乐山-内容矩阵私域触达方案-V1.0.md | docs/ | 平行：公域→私域引流 |
| AHL-乐山-私域经营与会员体系-V1.0.md | docs/ | 平行：会员运营策略 |

---

**文档版本**

| 版本 | 日期 | 修订内容 |
|------|------|----------|
| V1.0 | 2026-03-27 | 初始版本，完整覆盖五种SaaS系统 + 三种对接路径 + 代码框架 |
