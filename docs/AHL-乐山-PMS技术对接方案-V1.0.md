# AHL 乐山锦江嘉州宾馆 PMS数据对接技术方案 V1.0

> **版本**: V1.0  
> **日期**: 2026-03-27  
> **试点酒店**: 四川乐山锦江嘉州宾馆  
> **模块**: 模块1（技术深化任务）  
> **状态**: 基于行业知识的技术方案，待实地调研验证  

---

## 文档目的

本方案解决一个核心问题：**AHL数字员工如何在不知道酒店实际PMS系统的情况下，准备好一套可执行的PMS数据对接方案？**

核心原则：**不要假设。基于概率分布准备方案，用最小成本覆盖最可能场景。**

---

## 一、PMS系统现状调研

### 1.1 锦江嘉州宾馆PMS系统概率分析

> ⚠️ **重要声明**：以下为基于行业知识的概率推断，**必须实地调研确认**。

**锦江/安逸集团PMS使用格局**：

| PMS系统 | 适用档次 | 锦江集团内占比估算 | API开放程度 | 锦江嘉州宾馆概率 |
|---------|---------|------------------|------------|----------------|
| **蓝凤凰** | 中高端（3-4星） | ~50% | REST API开放，需申请 | **60%**（最可能） |
| **Opera (Oracle)** | 高端（4-5星） | ~20% | OPERA Cloud API，需Oracle授权 | 20% |
| **石基** | 全档次 | ~15% | 石基云API，开放程度中等 | 10% |
| **别样红** | 中端 | ~10% | 云API，开放 | 5% |
| **其他/自研** | 各档次 | ~5% | 不确定 | 5% |

**为什么蓝凤凰概率最高（60%）**：
- 锦江嘉州宾馆定位为**中高端旅游酒店**（推测150-200间）
- 蓝凤凰是锦江集团旗下**最广泛部署的PMS**，尤其在中档连锁品牌
- 蓝凤凰对国内酒店集团的适配性好，本地化支持完善
- 相对Opera，**蓝凤凰的API申请门槛更低**（不需要Oracle原厂授权）

**Opera概率次高（20%）**：
- 如果锦江嘉州宾馆实际为4星或挂5星，可能使用Opera
- Opera的优势：国际品牌通用，API标准化程度最高
- Opera的劣势：**申请周期长（4-8周）**，需要通过Oracle/锦江集团IT中转

---

### 1.2 三种PMS的API能力对比

#### 蓝凤凰（LanFengHuang）API

**官方文档**：
- 官网：`https://www.lanfeng.cn/` （需实地确认具体产品线）
- API文档：通常在酒店集团IT部门内部，不对外公开

**API能力**：

```yaml
REST_API:
  认证方式: API Key + Secret (HMAC签名)
  协议: HTTPS + JSON
  接口数量: 约20-30个核心接口
  数据格式: UTF-8 JSON

可获取数据:
  订单/预订:
    - reservation.list: 预订列表查询
    - reservation.get: 预订详情
    - reservation.create: 创建预订
    - reservation.update: 修改预订
    - reservation.cancel: 取消预订
  住客:
    - guest.list: 住客列表
    - guest.get: 住客详情（含联系方式）
  房态:
    - room.status: 房态查询
    - room.availability: 可用房量
  夜审:
    - night_audit.get: 夜审数据
  房价:
    - rate.plan.list: 房价计划
    - rate.availability: 价格可用性

Sandbox环境:
  ⚠️ 蓝凤凰通常不提供公开Sandbox
  ✅ 替代方案：酒店测试账号（需酒店IT协助开通）

数据延迟:
  实时接口: <1秒延迟
  批量查询: T+1（如历史报表）
```

**申请流程**：
1. 联系安逸集团IT部（或锦江集团IT中台）
2. 说明数据用途（收益管理/数据分析）
3. 签署数据安全协议
4. 获取API Key + Secret
5. 技术对接（通常1-2周）
6. **预计总周期：2-4周**

---

#### Opera (Oracle OPERA Cloud) API

**官方文档**：
- OPERA Cloud API: `https://docs.oracle.com/en/industries/hospitality/opera-cloud.html`
- 酒店技术标准文档通常由Oracle直供，或通过集团IT中转

**API能力**：

```yaml
OPERA_Cloud_REST_API:
  认证方式: OAuth 2.0 (Client Credentials)
  协议: HTTPS + REST + JSON
  覆盖范围: 预订/住客/房态/价格/财务全模块

核心接口:
  预订模块:
    - GET /reservations: 查询预订
    - POST /reservations: 创建预订
    - PUT /reservations/{id}: 更新预订
  住客模块:
    - GET /guests: 住客查询
    - GET /guests/{id}: 住客详情
  房态模块:
    - GET /room/availability: 可用房量
    - GET /room/status: 房态
  财务模块:
    - GET /nightAudit: 夜审数据
  价格模块:
    - GET /ratePlans: 房价计划
    - PUT /ratePlans/{id}: 更新房价

数据字段（关键）:
  reservation:
    - reservationStatus: 预订状态
    - arrivalDate: 入住日期
    - departureDate: 离店日期
    - roomType: 房型
    - rateCode: 房价码
    - guestName: 住客姓名
    - contactPhone: 联系电话
    - totalAmount: 总金额
    - sourceCode: 订单来源

Sandbox:
  ❌ 通常不提供公开Sandbox
  ✅ 需要通过Oracle销售/集团IT申请测试环境
  ⚠️ 申请周期：4-8周（最长）

数据延迟: 实时同步
```

**申请流程**：
1. 通过锦江集团IT部向Oracle申请
2. 说明酒店信息（物业ID/Opera Property ID）
3. Oracle审批（需集团担保）
4. 签署数据使用协议
5. 获取OAuth凭证
6. **预计总周期：4-12周**（最慢方案）

---

#### 石基（Shiji）API

**官方文档**：
- 石基云平台：`https://www.shijicloud.com/`
- 酒店PMS API文档通常需要石基账号

**API能力**：

```yaml
石基云API:
  认证方式: Token (API Token)
  协议: HTTPS + JSON
  接口风格: RESTful
  
核心接口:
  - order/query: 订单查询
  - guest/query: 住客查询
  - room/query: 房态查询
  - report/night_audit: 夜审报表

数据延迟: 实时
Sandbox: 有测试环境，需申请

申请周期: 2-3周（中等）
```

---

### 1.3 实地调研必查清单

> ⚠️ **必须实地确认以下信息**

| 问题 | 目的 | 确认方法 |
|------|------|---------|
| PMS系统是什么？ | 确定API方案 | 问酒店IT或前台电脑 |
| PMS版本号是多少？ | 确认API版本 | 系统登录界面/设置页 |
| 是否已开通API接口？ | 判断是否需额外申请 | 酒店IT部门 |
| 哪个部门管IT/系统？ | 找对接口人 | 酒店管理层 |
| 是否有测试账号？ | API调试用 | IT部门 |
| 网络是否开放外网？ | 影响云端API直连 | 网络环境测试 |
| 数据导出权限在谁手里？ | 申请数据权限 | 前厅/IT/财务 |

**实地操作**：到达酒店后，第一时间查看前台电脑的PMS系统——系统界面通常有明显Logo可识别。

---

## 二、数据字段对照表

### 2.1 核心订单数据字段对照

> 以下为**行业标准字段**，适配蓝凤凰/Opera/石基三大主流PMS

| AHL内部字段 | 蓝凤凰字段 | Opera字段 | 石基字段 | 数据类型 | 说明 |
|------------|-----------|-----------|---------|---------|------|
| `order_id` | `reservation_id` | `ReservationID` | `order_id` | VARCHAR(32) | 订单唯一标识 |
| `hotel_id` | `hotel_id` | `PropertyID` | `hotel_id` | VARCHAR(16) | 酒店标识 |
| `guest_name` | `guest_name` | `GuestName` | `guest_name` | VARCHAR(64) | 住客姓名 |
| `guest_phone` | `phone` | `PhoneNumber` | `mobile` | VARCHAR(20) | 联系电话 |
| `checkin_date` | `arrival_date` | `ArrivalDate` | `checkin_date` | DATE | 入住日期 |
| `checkout_date` | `departure_date` | `DepartureDate` | `checkout_date` | DATE | 离店日期 |
| `room_type` | `room_type_code` | `RoomType` | `room_type` | VARCHAR(16) | 房型代码 |
| `room_no` | `room_number` | `RoomNumber` | `room_no` | VARCHAR(8) | 房间号 |
| `rate_code` | `rate_code` | `RateCode` | `rate_code` | VARCHAR(16) | 房价码 |
| `room_revenue` | `room_amount` | `RoomRevenue` | `room_revenue` | DECIMAL(10,2) | 房费收入 |
| `total_revenue` | `total_amount` | `TotalRevenue` | `total_revenue` | DECIMAL(10,2) | 总收入 |
| `channel` | `source_code` | `SourceCode` | `channel` | VARCHAR(16) | 订单来源 |
| `channel_order_id` | `ota_order_id` | `ExtConfirmationNo` | `ext_order_id` | VARCHAR(32) | OTA订单号 |
| `status` | `reservation_status` | `ReservationStatus` | `status` | VARCHAR(16) | 订单状态 |
| `payment_status` | `payment_status` | `PaymentStatus` | `pay_status` | VARCHAR(16) | 支付状态 |
| `adult_count` | `adults` | `Adults` | `adult_num` | INT | 成人数 |
| `child_count` | `children` | `Children` | `child_num` | INT | 儿童数 |
| `create_time` | `create_time` | `CreateDateTime` | `create_time` | DATETIME | 订单创建时间 |
| `modify_time` | `update_time` | `UpdateDateTime` | `modify_time` | DATETIME | 最后修改时间 |

---

### 2.2 住客数据字段对照

| AHL内部字段 | 蓝凤凰字段 | Opera字段 | 石基字段 | 数据类型 |
|------------|-----------|-----------|---------|---------|
| `guest_id` | `guest_id` | `GuestID` | `guest_id` | VARCHAR(32) |
| `guest_name` | `guest_name` | `GuestName` | `name` | VARCHAR(64) |
| `phone` | `phone` | `PhoneNumber` | `mobile` | VARCHAR(20) |
| `gender` | `gender` | `Gender` | `sex` | VARCHAR(2) |
| `id_type` | `id_type` | `IDType` | `id_type` | VARCHAR(8) |
| `id_no` | `id_number` | `IDNumber` | `id_no` | VARCHAR(32) |
| `email` | `email` | `Email` | `email` | VARCHAR(64) |
| `membership_level` | `member_level` | `MembershipType` | `member_level` | VARCHAR(16) |
| `membership_no` | `member_no` | `MembershipNumber` | `member_no` | VARCHAR(32) |
| `address` | `address` | `Address` | `address` | VARCHAR(128) |
| `birthday` | `birthday` | `BirthDate` | `birthday` | DATE |

---

### 2.3 房态数据字段对照

| AHL内部字段 | 蓝凤凰字段 | Opera字段 | 石基字段 | 数据类型 |
|------------|-----------|-----------|---------|---------|
| `date` | `report_date` | `BusinessDate` | `date` | DATE |
| `room_type` | `room_type_code` | `RoomType` | `room_type` | VARCHAR(16) |
| `total_rooms` | `total_rooms` | `TotalRooms` | `total_num` | INT |
| `available` | `available_rooms` | `AvailableRooms` | `available` | INT |
| `occupied` | `occupied_rooms` | `OccupiedRooms` | `occupied` | INT |
| `occupied_pct` | `occupancy_rate` | `OccupancyPercent` | `occupancy` | DECIMAL(5,2) |
| `revenue` | `day_revenue` | `RoomRevenue` | `revenue` | DECIMAL(10,2) |
| `adr` | `average_rate` | `AverageRate` | `adr` | DECIMAL(10,2) |
| `revpar` | `revpar` | `RevPAR` | `revpar` | DECIMAL(10,2) |

---

### 2.4 夜审数据字段对照

| AHL内部字段 | 蓝凤凰字段 | Opera字段 | 石基字段 | 数据类型 |
|------------|-----------|-----------|---------|---------|
| `audit_date` | `night_date` | `BusinessDate` | `audit_date` | DATE |
| `total_revenue` | `total_revenue` | `TotalRevenue` | `total_revenue` | DECIMAL(12,2) |
| `room_revenue` | `room_revenue` | `RoomRevenue` | `room_revenue` | DECIMAL(10,2) |
| `fnb_revenue` | `fnb_revenue` | `FoodBeverageRevenue` | `fnb_revenue` | DECIMAL(10,2) |
| `other_revenue` | `other_revenue` | `OtherRevenue` | `other_revenue` | DECIMAL(10,2) |
| `total_rooms` | `room_inventory` | `RoomInventory` | `total_rooms` | INT |
| `occupied_rooms` | `occupied_rooms` | `OccupiedRooms` | `occupied` | INT |
| `vacant_rooms` | `vacant_rooms` | `VacantRooms` | `vacant` | INT |
| `oo_rooms` | `out_of_order` | `OutOfOrder` | `ooo` | INT |
| `complimentary` | `complimentary` | `Complimentary` | `free` | INT |
| `house_use` | `house_use` | `HouseUse` | `house_use` | INT |

---

## 三、Python数据拉取脚本模板

### 3.1 蓝凤凰PMS数据拉取脚本

```python
#!/usr/bin/env python3
"""
蓝凤凰PMS数据拉取脚本
AHL乐山锦江嘉州宾馆专用

功能：定时从蓝凤凰PMS API拉取订单、住客、房态数据
依赖：requests, pandas, python-dateutil
作者：AHL技术组
版本：v1.0
"""

import requests
import pandas as pd
import json
import hashlib
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any
from pathlib import Path

# ============================================================
# 配置区 - 需根据实际环境修改
# ============================================================

CONFIG = {
    # API基础配置（需向安逸集团IT申请）
    "api_base_url": "https://pms-api.lanfeng.cn/v1",  # 蓝凤凰API地址（需确认）
    
    # 认证配置（申请后获取）
    "api_key": "YOUR_API_KEY_HERE",
    "api_secret": "YOUR_API_SECRET_HERE",
    
    # 酒店配置
    "hotel_id": "JZZS001",  # 锦江嘉州宾馆酒店ID（需确认）
    
    # 采集配置
    "data_dir": "./data/lanfenghuang",
    "log_dir": "./logs/lanfenghuang",
    
    # 采集参数
    "request_timeout": 30,  # 请求超时（秒）
    "retry_times": 3,       # 重试次数
    "retry_delay": 5,       # 重试间隔（秒）
}

# ============================================================
# 日志配置
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{CONFIG['log_dir']}/pms_pull_{datetime.now().strftime('%Y%m%d')}.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# 工具函数
# ============================================================

def generate_signature(secret: str, timestamp: str, params: Dict) -> str:
    """
    生成蓝凤凰API签名（HMAC-SHA256）
    
    原理：对参数按字典序排序后拼接，用secret签名
    这样可以验证请求未被篡改
    """
    sorted_params = sorted(params.items())
    param_str = "&".join([f"{k}={v}" for k, v in sorted_params])
    sign_str = f"{timestamp}{param_str}{secret}"
    return hashlib.sha256(sign_str.encode('utf-8')).hexdigest()


def request_with_retry(url: str, method: str = "GET", 
                       params: Optional[Dict] = None,
                       data: Optional[Dict] = None,
                       headers: Optional[Dict] = None) -> Dict:
    """
    带重试的HTTP请求
    
    原理：网络不稳定时自动重试，避免因临时故障导致数据采集失败
    """
    for attempt in range(CONFIG["retry_times"]):
        try:
            timestamp = str(int(time.time()))
            
            # 生成签名参数
            if params is None:
                params = {}
            params["api_key"] = CONFIG["api_key"]
            params["timestamp"] = timestamp
            
            # 生成签名
            signature = generate_signature(CONFIG["api_secret"], timestamp, params)
            
            # 添加签名到请求头
            if headers is None:
                headers = {}
            headers["X-Signature"] = signature
            headers["Content-Type"] = "application/json"
            
            if method == "GET":
                response = requests.get(
                    url, 
                    params=params, 
                    headers=headers, 
                    timeout=CONFIG["request_timeout"]
                )
            else:
                response = requests.post(
                    url, 
                    json=data, 
                    headers=headers, 
                    timeout=CONFIG["request_timeout"]
                )
            
            response.raise_for_status()
            result = response.json()
            
            # 检查业务错误码
            if result.get("code") != 0:
                logger.error(f"API业务错误: {result.get('message')}")
                raise ValueError(f"API error: {result.get('message')}")
            
            return result.get("data", {})
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"请求失败（第{attempt+1}次）: {e}")
            if attempt < CONFIG["retry_times"] - 1:
                time.sleep(CONFIG["retry_delay"])
            else:
                logger.error(f"请求最终失败: {e}")
                raise


# ============================================================
# 数据拉取函数
# ============================================================

def pull_reservations(start_date: str, end_date: str) -> pd.DataFrame:
    """
    拉取指定日期范围内的预订/订单数据
    
    参数:
        start_date: 开始日期，格式YYYY-MM-DD
        end_date: 结束日期，格式YYYY-MM-DD
    
    返回:
        DataFrame: 订单数据
    
    原理: 查询指定日期范围内的所有入住/离店/在店订单
    """
    url = f"{CONFIG['api_base_url']}/reservation/list"
    
    params = {
        "hotel_id": CONFIG["hotel_id"],
        "start_date": start_date,
        "end_date": end_date,
        "status": "all",  # 查询所有状态订单
    }
    
    try:
        data = request_with_retry(url, params=params)
        
        if not data or "reservations" not in data:
            logger.warning("未获取到订单数据")
            return pd.DataFrame()
        
        # 转换为DataFrame便于处理
        df = pd.DataFrame(data["reservations"])
        
        # 字段映射：PMS字段 -> AHL标准字段
        field_mapping = {
            "reservation_id": "order_id",
            "guest_name": "guest_name",
            "phone": "guest_phone",
            "arrival_date": "checkin_date",
            "departure_date": "checkout_date",
            "room_type_code": "room_type",
            "rate_code": "rate_code",
            "room_amount": "room_revenue",
            "total_amount": "total_revenue",
            "source_code": "channel",
        }
        
        df = df.rename(columns=field_mapping)
        
        # 标准化日期格式
        for date_col in ["checkin_date", "checkout_date"]:
            df[date_col] = pd.to_datetime(df[date_col]).dt.strftime("%Y-%m-%d")
        
        # 添加元数据
        df["hotel_id"] = CONFIG["hotel_id"]
        df["data_source"] = "lanfenghuang"
        df["pull_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        logger.info(f"成功拉取{len(df)}条订单数据")
        return df
        
    except Exception as e:
        logger.error(f"拉取订单数据失败: {e}")
        return pd.DataFrame()


def pull_guests(reservation_ids: List[str]) -> pd.DataFrame:
    """
    拉取住客详细信息
    
    参数:
        reservation_ids: 订单ID列表
    
    返回:
        DataFrame: 住客数据
    """
    url = f"{CONFIG['api_base_url']}/guest/list"
    
    guests_list = []
    
    # 分批查询，避免单次请求数据量过大
    batch_size = 100
    for i in range(0, len(reservation_ids), batch_size):
        batch_ids = reservation_ids[i:i+batch_size]
        
        params = {
            "hotel_id": CONFIG["hotel_id"],
            "reservation_ids": ",".join(batch_ids),
        }
        
        try:
            data = request_with_retry(url, params=params)
            
            if data and "guests" in data:
                guests_list.extend(data["guests"])
                
        except Exception as e:
            logger.warning(f"拉取住客批次{i//batch_size + 1}失败: {e}")
            continue
    
    if not guests_list:
        return pd.DataFrame()
    
    df = pd.DataFrame(guests_list)
    
    # 字段映射
    field_mapping = {
        "guest_id": "guest_id",
        "name": "guest_name",
        "mobile": "phone",
        "gender": "gender",
        "id_type": "id_type",
        "id_number": "id_no",
        "email": "email",
    }
    
    df = df.rename(columns=field_mapping)
    
    logger.info(f"成功拉取{len(df)}条住客数据")
    return df


def pull_room_status(date: str) -> pd.DataFrame:
    """
    拉取指定日期的房态数据
    
    参数:
        date: 日期，格式YYYY-MM-DD
    
    返回:
        DataFrame: 房态数据
    """
    url = f"{CONFIG['api_base_url']}/room/status"
    
    params = {
        "hotel_id": CONFIG["hotel_id"],
        "date": date,
    }
    
    try:
        data = request_with_retry(url, params=params)
        
        if not data or "rooms" not in data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data["rooms"])
        
        field_mapping = {
            "room_type_code": "room_type",
            "total_rooms": "total_rooms",
            "available_rooms": "available",
            "occupied_rooms": "occupied",
            "occupancy_rate": "occupied_pct",
            "day_revenue": "revenue",
        }
        
        df = df.rename(columns=field_mapping)
        df["date"] = date
        df["hotel_id"] = CONFIG["hotel_id"]
        df["data_source"] = "lanfenghuang"
        
        return df
        
    except Exception as e:
        logger.error(f"拉取房态数据失败: {e}")
        return pd.DataFrame()


def pull_night_audit(date: str) -> Dict:
    """
    拉取指定日期的夜审数据
    
    夜审是酒店PMS的核心数据节点，标志着一天营业正式结束
    夜审后数据才完整（包含所有入离结账）
    
    参数:
        date: 日期，格式YYYY-MM-DD
    
    返回:
        Dict: 夜审数据
    """
    url = f"{CONFIG['api_base_url']}/night_audit/get"
    
    params = {
        "hotel_id": CONFIG["hotel_id"],
        "date": date,
    }
    
    try:
        data = request_with_retry(url, params=params)
        logger.info(f"成功拉取{date}夜审数据")
        return data
        
    except Exception as e:
        logger.error(f"拉取夜审数据失败: {e}")
        return {}


# ============================================================
# 数据存储函数
# ============================================================

def save_to_json(df: pd.DataFrame, filename: str):
    """保存DataFrame到JSON文件"""
    Path(CONFIG["data_dir"]).mkdir(parents=True, exist_ok=True)
    filepath = Path(CONFIG["data_dir"]) / filename
    df.to_json(filepath, orient="records", force_ascii=False, indent=2)
    logger.info(f"数据已保存: {filepath}")


def save_night_audit(data: Dict, date: str):
    """保存夜审数据"""
    Path(CONFIG["data_dir"]).mkdir(parents=True, exist_ok=True)
    filepath = Path(CONFIG["data_dir"]) / f"night_audit_{date}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    logger.info(f"夜审数据已保存: {filepath}")


# ============================================================
# 主执行函数
# ============================================================

def main():
    """
    主执行函数：每日定时拉取PMS数据
    
    执行时间建议：每日凌晨2:00（夜审完成后）
    这样可以确保当天所有数据都已夜审完毕
    """
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    logger.info(f"========== PMS数据拉取任务开始 ==========")
    logger.info(f"执行日期: {today}")
    
    # 1. 拉取近7天订单数据（覆盖可能的数据更新）
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        start_date = date
        end_date = date
        
        df_orders = pull_reservations(start_date, end_date)
        if not df_orders.empty:
            save_to_json(df_orders, f"orders_{date}.json")
    
    # 2. 拉取昨日夜审数据
    audit_data = pull_night_audit(yesterday)
    if audit_data:
        save_night_audit(audit_data, yesterday)
    
    # 3. 拉取昨日房态
    df_room_status = pull_room_status(yesterday)
    if not df_room_status.empty:
        save_to_json(df_room_status, f"room_status_{yesterday}.json")
    
    logger.info(f"========== PMS数据拉取任务完成 ==========")


if __name__ == "__main__":
    main()
```

**使用说明**：

```bash
# 首次使用前安装依赖
pip install requests pandas python-dateutil

# 执行数据拉取
python lanfenghuang_pms_pull.py

# 配置定时任务（每日凌晨2点执行）
# Windows任务计划程序
schtasks /create /tn "AHL_PMS_Pull" /tr "python lanfenghuang_pms_pull.py" /sc daily /st 02:00

# Linux crontab
# 0 2 * * * /usr/bin/python3 /path/to/lanfenghuang_pms_pull.py
```

---

### 3.2 Opera PMS数据拉取脚本

```python
#!/usr/bin/env python3
"""
Opera (Oracle OPERA Cloud) PMS数据拉取脚本
AHL乐山锦江嘉州宾馆专用

功能：通过OPERA Cloud REST API拉取订单、住客、房态数据
依赖：requests, pandas, python-dateutil
作者：AHL技术组
版本：v1.0

注意：Opera使用OAuth 2.0认证，需要定期刷新Token
"""

import requests
import pandas as pd
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from pathlib import Path

# ============================================================
# 配置区
# ============================================================

CONFIG = {
    # OPERA Cloud API配置
    "api_base_url": "https://api.oracle.com/opera/v1",  # OPERA Cloud API地址
    "property_id": "JZZS001",  # Opera Property ID（需确认）
    
    # OAuth认证配置（申请后获取）
    "oauth_url": "https://api.oracle.com/oauth/v2/token",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    
    # 数据配置
    "hotel_id": "JZZS001",
    "data_dir": "./data/opera",
    "log_dir": "./logs/opera",
    
    "request_timeout": 30,
    "retry_times": 3,
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{CONFIG['log_dir']}/opera_pull_{datetime.now().strftime('%Y%m%d')}.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# OAuth认证
# ============================================================

class OperaAuth:
    """
    Opera OAuth 2.0认证管理
    
    原理：Opera使用Client Credentials模式获取访问令牌
    令牌有效期通常为1小时，需要自动刷新
    """
    
    def __init__(self, client_id: str, client_secret: str, token_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.access_token = None
        self.token_expires_at = 0
    
    def get_token(self) -> str:
        """获取访问令牌，自动刷新"""
        # 如果令牌还未过期，直接返回
        if self.access_token and time.time() < self.token_expires_at - 60:
            return self.access_token
        
        # 申请新令牌
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        
        response = requests.post(self.token_url, data=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        self.access_token = result["access_token"]
        
        # 假设令牌有效期为3600秒，留60秒缓冲
        self.token_expires_at = time.time() + result.get("expires_in", 3600) - 60
        
        logger.info("Opera OAuth令牌已刷新")
        return self.access_token


class OperaClient:
    """Opera API客户端"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.auth = OperaAuth(
            config["client_id"],
            config["client_secret"],
            config["oauth_url"]
        )
    
    def request(self, method: str, endpoint: str, 
                params: Optional[Dict] = None,
                data: Optional[Dict] = None) -> Dict:
        """发送API请求"""
        url = f"{self.config['api_base_url']}{endpoint}"
        
        headers = {
            "Authorization": f"Bearer {self.auth.get_token()}",
            "Content-Type": "application/json",
            "X-PropertyId": self.config["property_id"],
        }
        
        for attempt in range(self.config["retry_times"]):
            try:
                if method == "GET":
                    response = requests.get(url, params=params, headers=headers,
                                          timeout=self.config["request_timeout"])
                else:
                    response = requests.post(url, json=data, headers=headers,
                                            timeout=self.config["request_timeout"])
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"请求失败（第{attempt+1}次）: {e}")
                if attempt < self.config["retry_times"] - 1:
                    time.sleep(5)
                else:
                    raise
    
    def pull_reservations(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        拉取预订数据
        
        Opera使用OAuth + PropertyId进行认证
        """
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "includeGuestInfo": "true",
        }
        
        result = self.request("GET", "/reservations", params=params)
        
        if not result or "items" not in result:
            return pd.DataFrame()
        
        df = pd.DataFrame(result["items"])
        
        # Opera字段 -> AHL标准字段
        field_mapping = {
            "ReservationID": "order_id",
            "GuestName": "guest_name",
            "PhoneNumber": "guest_phone",
            "ArrivalDate": "checkin_date",
            "DepartureDate": "checkout_date",
            "RoomType": "room_type",
            "RateCode": "rate_code",
            "RoomRevenue": "room_revenue",
            "TotalRevenue": "total_revenue",
            "SourceCode": "channel",
            "ReservationStatus": "status",
        }
        
        df = df.rename(columns=field_mapping)
        
        for date_col in ["checkin_date", "checkout_date"]:
            if date_col in df.columns:
                df[date_col] = pd.to_datetime(df[date_col]).dt.strftime("%Y-%m-%d")
        
        df["hotel_id"] = self.config["hotel_id"]
        df["data_source"] = "opera"
        
        return df


def main():
    """主执行函数"""
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    logger.info("========== Opera PMS数据拉取开始 ==========")
    
    client = OperaClient(CONFIG)
    
    # 拉取近7天订单
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        df = client.pull_reservations(date, date)
        if not df.empty:
            Path(CONFIG["data_dir"]).mkdir(parents=True, exist_ok=True)
            df.to_json(f"{CONFIG['data_dir']}/orders_{date}.json", 
                      orient="records", force_ascii=False, indent=2)
    
    logger.info("========== Opera PMS数据拉取完成 ==========")


if __name__ == "__main__":
    main()
```

---

### 3.3 通用Excel导入适配器

> 场景：API暂未打通时，作为**过渡方案**使用
> 原理：将酒店Excel导出文件转换为AHL标准数据格式

```python
#!/usr/bin/env python3
"""
Excel数据导入适配器
AHL乐山锦江嘉州宾馆专用

功能：将酒店导出的Excel文件转换为AHL标准数据格式
支持：蓝凤凰、Opera、石基三大主流PMS的导出格式

原理：
1. 读取酒店Excel
2. 根据PMS类型应用不同的字段映射
3. 输出AHL标准JSON格式
4. 触发数据处理管道
"""

import pandas as pd
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# PMS类型与字段映射配置
# ============================================================

# 蓝凤凰Excel导出字段映射
LANFENGHUANG_MAPPING = {
    "订单号": "order_id",
    "客人姓名": "guest_name",
    "联系电话": "guest_phone",
    "入住日期": "checkin_date",
    "离店日期": "checkout_date",
    "房型": "room_type",
    "房价码": "rate_code",
    "房费": "room_revenue",
    "总消费": "total_revenue",
    "来源": "channel",
    "订单状态": "status",
}

# Opera Excel导出字段映射
OPERA_MAPPING = {
    "Reservation ID": "order_id",
    "Guest Name": "guest_name",
    "Phone": "guest_phone",
    "Arrival": "checkin_date",
    "Departure": "checkout_date",
    "Room Type": "room_type",
    "Rate Code": "rate_code",
    "Room Revenue": "room_revenue",
    "Total Revenue": "total_revenue",
    "Source": "channel",
    "Status": "status",
}

# 石基Excel导出字段映射
SHIJI_MAPPING = {
    "订单ID": "order_id",
    "住客姓名": "guest_name",
    "手机号": "guest_phone",
    "入住": "checkin_date",
    "离店": "checkout_date",
    "房型": "room_type",
    "价格码": "rate_code",
    "房费收入": "room_revenue",
    "总收入": "total_revenue",
    "渠道": "channel",
    "状态": "status",
}

# PMS类型注册表
PMS_MAPPINGS = {
    "lanfenghuang": LANFENGHUANG_MAPPING,
    "opera": OPERA_MAPPING,
    "shiji": SHIJI_MAPPING,
    # 自动检测
    "auto": None,
}


class ExcelImportAdapter:
    """
    Excel导入适配器
    
    功能：根据PMS类型自动识别并转换数据格式
    原理：字段名匹配 + 类型推断
    """
    
    def __init__(self, pms_type: str = "auto"):
        self.pms_type = pms_type
        self.mappings = PMS_MAPPINGS
    
    def detect_pms_type(self, df: pd.DataFrame) -> str:
        """
        自动检测PMS类型
        
        原理：根据列名字段判断属于哪种PMS
        返回值：pms_type字符串
        """
        columns = set(df.columns)
        
        # 检查每个PMS的特有字段
        for pms_type, mapping in self.mappings.items():
            if mapping is None:
                continue
            
            matches = sum(1 for col in columns if col in mapping)
            if matches >= 3:  # 匹配3个以上字段认为是该类型
                logger.info(f"自动检测到PMS类型: {pms_type}")
                return pms_type
        
        # 无法检测，返回未知
        logger.warning("无法自动检测PMS类型，请手动指定")
        return "unknown"
    
    def standardize_date(self, date_val) -> str:
        """
        标准化日期格式
        
        支持多种输入格式：
        - 2024-03-15
        - 2024/03/15
        - 03/15/2024
        - 20240315
        """
        if pd.isna(date_val):
            return ""
        
        date_str = str(date_val).strip()
        
        # 尝试多种日期格式
        formats = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%Y%m%d",
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
        
        # 无法解析，返回原值
        logger.warning(f"无法解析日期: {date_val}")
        return date_str
    
    def standardize_amount(self, amount_val) -> float:
        """标准化金额格式"""
        if pd.isna(amount_val):
            return 0.0
        
        amount_str = str(amount_val).strip()
        
        # 去除货币符号和千分位
        amount_str = amount_str.replace("¥", "").replace(",", "").replace("元", "")
        
        try:
            return float(amount_str)
        except ValueError:
            logger.warning(f"无法解析金额: {amount_val}")
            return 0.0
    
    def convert(self, excel_path: str, output_dir: str = "./data/imported") -> Dict:
        """
        转换Excel文件为AHL标准格式
        
        参数:
            excel_path: Excel文件路径
            output_dir: 输出目录
        
        返回:
            Dict: 转换结果统计
        """
        logger.info(f"开始导入: {excel_path}")
        
        # 读取Excel
        df = pd.read_excel(excel_path)
        logger.info(f"读取到{len(df)}行数据")
        
        # 检测或使用指定PMS类型
        if self.pms_type == "auto":
            detected_type = self.detect_pms_type(df)
        else:
            detected_type = self.pms_type
        
        if detected_type == "unknown":
            raise ValueError("无法确定PMS类型，请检查Excel列名")
        
        # 获取字段映射
        mapping = self.mappings.get(detected_type, {})
        
        # 执行字段映射
        df_standard = pd.DataFrame()
        
        for pms_col, ahl_col in mapping.items():
            if pms_col in df.columns:
                df_standard[ahl_col] = df[pms_col]
            else:
                logger.warning(f"字段缺失: {pms_col}")
                df_standard[ahl_col] = None
        
        # 标准化日期和金额字段
        for date_col in ["checkin_date", "checkout_date"]:
            if date_col in df_standard.columns:
                df_standard[date_col] = df_standard[date_col].apply(self.standardize_date)
        
        for amount_col in ["room_revenue", "total_revenue"]:
            if amount_col in df_standard.columns:
                df_standard[amount_col] = df_standard[amount_col].apply(self.standardize_amount)
        
        # 添加元数据
        df_standard["hotel_id"] = "JZZS001"
        df_standard["data_source"] = detected_type
        df_standard["import_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 保存
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_file = Path(output_dir) / f"orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        df_standard.to_json(output_file, orient="records", force_ascii=False, indent=2)
        
        result = {
            "status": "success",
            "pms_type": detected_type,
            "total_rows": len(df_standard),
            "output_file": str(output_file),
        }
        
        logger.info(f"导入完成: {result}")
        return result


def batch_import(folder_path: str, output_dir: str = "./data/imported") -> List[Dict]:
    """
    批量导入文件夹中的所有Excel文件
    
    参数:
        folder_path: 包含Excel文件的文件夹路径
        output_dir: 输出目录
    
    返回:
        List[Dict]: 每个文件的导入结果
    """
    import glob
    
    excel_files = glob.glob(f"{folder_path}/*.xlsx") + glob.glob(f"{folder_path}/*.xls")
    
    results = []
    adapter = ExcelImportAdapter(pms_type="auto")
    
    for excel_file in excel_files:
        try:
            result = adapter.convert(excel_file, output_dir)
            results.append(result)
        except Exception as e:
            logger.error(f"导入失败 {excel_file}: {e}")
            results.append({
                "status": "failed",
                "file": excel_file,
                "error": str(e),
            })
    
    return results


if __name__ == "__main__":
    # 单文件导入示例
    adapter = ExcelImportAdapter(pms_type="auto")
    result = adapter.convert(
        excel_path="./exports/orders_2026_03_27.xlsx",
        output_dir="./data/imported"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

---

## 四、Excel导入数据字典

### 4.1 标准订单导出格式（CSV/Excel）

> 适用场景：PMS API暂未打通时，手工导出导入

**文件命名规范**：
```
orders_YYYYMMDD.csv          # 每日订单导出
guests_YYYYMMDD.csv          # 每日住客导出
room_status_YYYYMMDD.csv     # 每日房态导出
night_audit_YYYYMMDD.csv     # 每日夜审导出
```

**编码要求**：`UTF-8`（重要！中文乱码通常是这个原因）

**分隔符**：逗号`,`

---

### 4.2 订单数据字段字典

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| `order_id` | VARCHAR(32) | ✅ | 订单唯一编号 | ORD20260327001 |
| `guest_name` | VARCHAR(64) | ✅ | 住客姓名 | 张三 |
| `guest_phone` | VARCHAR(20) | ✅ | 联系电话 | 13800138000 |
| `checkin_date` | DATE | ✅ | 入住日期 | 2026-03-27 |
| `checkout_date` | DATE | ✅ | 离店日期 | 2026-03-29 |
| `room_type` | VARCHAR(16) | ✅ | 房型代码 | DBL/STD/SUI |
| `room_no` | VARCHAR(8) | ❌ | 房间号 | 801 |
| `rate_code` | VARCHAR(16) | ❌ | 房价码 | BAR/RACK/PKG |
| `room_revenue` | DECIMAL(10,2) | ✅ | 房费金额 | 580.00 |
| `total_revenue` | DECIMAL(10,2) | ✅ | 总消费 | 680.00 |
| `channel` | VARCHAR(16) | ✅ | 订单来源 | CTRIP/MEITUAN/FTXC |
| `channel_order_id` | VARCHAR(32) | ❌ | OTA订单号 | 123456789 |
| `status` | VARCHAR(16) | ✅ | 订单状态 | CHECKIN/CHECKOUT/CANCEL |
| `payment_status` | VARCHAR(16) | ❌ | 支付状态 | PAID/UNPAID/PARTIAL |
| `adult_count` | INT | ❌ | 成人数 | 2 |
| `child_count` | INT | ❌ | 儿童数 | 0 |
| `create_time` | DATETIME | ❌ | 订单创建时间 | 2026-03-25 14:30:00 |
| `remark` | VARCHAR(256) | ❌ | 备注 | 延迟退房 |

---

### 4.3 房态数据字段字典

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| `date` | DATE | ✅ | 数据日期 | 2026-03-27 |
| `room_type` | VARCHAR(16) | ✅ | 房型代码 | DBL |
| `total_rooms` | INT | ✅ | 总房量 | 50 |
| `available` | INT | ✅ | 可售房量 | 35 |
| `occupied` | INT | ✅ | 在住房量 | 12 |
| `vacant` | INT | ❌ | 空房量（待清扫） | 3 |
| `ooo` | INT | ❌ | 不可售（维修等） | 0 |
| `revenue` | DECIMAL(10,2) | ✅ | 当日房费收入 | 15600.00 |
| `adr` | DECIMAL(10,2) | ✅ | 平均房价 | 312.00 |
| `revpar` | DECIMAL(10,2) | ✅ | 每房收益 | 187.20 |
| `occupancy_pct` | DECIMAL(5,2) | ✅ | 入住率 | 76.00 |

---

### 4.4 夜审数据字段字典

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| `audit_date` | DATE | ✅ | 夜审日期 | 2026-03-26 |
| `total_revenue` | DECIMAL(12,2) | ✅ | 总收入 | 45800.00 |
| `room_revenue` | DECIMAL(10,2) | ✅ | 客房收入 | 38600.00 |
| `fnb_revenue` | DECIMAL(10,2) | ❌ | 餐饮收入 | 5200.00 |
| `other_revenue` | DECIMAL(10,2) | ❌ | 其他收入 | 2000.00 |
| `total_rooms` | INT | ✅ | 总房量 | 180 |
| `occupied` | INT | ✅ | 在住房量 | 142 |
| `vacant` | INT | ❌ | 空房量 | 35 |
| `ooo` | INT | ❌ | 不可售 | 3 |
| `complimentary` | INT | ❌ | 免费房 | 2 |
| `house_use` | INT | ❌ | 店用房 | 1 |
| `inhouse_guests` | INT | ❌ | 在店客人数 | 198 |
| `arrivals` | INT | ❌ | 当日入住 | 45 |
| `departures` | INT | ❌ | 当日离店 | 38 |
| `advancer` | INT | ❌ | 未来预订数 | 128 |

---

## 五、过渡方案：手工导入SOP

### 5.1 触发机制设计

**方案A：定时自动导入（推荐）**

```python
# 定时任务配置
SCHEDULE_CONFIG = {
    # 每日凌晨2点执行（夜审完成后）
    "orders": {
        "cron": "0 2 * * *",
        "source_folder": "D:/酒店导出/订单",
        "pattern": "orders_*.xlsx",
        "action": "import_and_move",  # 导入后移动到已处理文件夹
    },
    # 每周一导入上周数据
    "weekly_report": {
        "cron": "0 3 * * 1",
        "source_folder": "D:/酒店导出/夜审",
        "pattern": "night_audit_*.csv",
        "action": "import_and_archive",
    },
}
```

**方案B：手动触发（紧急/临时）**

```bash
# 手动导入单文件
python excel_import.py --file ./exports/orders_20260327.xlsx --pms auto

# 手动导入整个文件夹
python excel_import.py --folder ./exports/ --pms lanfenghuang

# 强制覆盖已有数据
python excel_import.py --file ./exports/orders_20260327.xlsx --force
```

### 5.2 数据校验规则

```python
# 数据校验配置
VALIDATION_RULES = {
    "orders": {
        "required_fields": ["order_id", "guest_name", "checkin_date", "checkout_date", "room_type"],
        "date_range": {
            "min": "2020-01-01",
            "max": "2030-12-31",
        },
        "amount_range": {
            "room_revenue": {"min": 0, "max": 10000},
            "total_revenue": {"min": 0, "max": 50000},
        },
        "referential_integrity": {
            "room_type": ["DBL", "STD", "SUI", "TWN", "FAM"],  # 有效的房型代码
            "channel": ["CTRIP", "MEITUAN", "FTXC", "WECHAT", "WALKIN", "MEMBER"],
            "status": ["RESERVE", "CHECKIN", "CHECKOUT", "CANCEL", "NOSHOW"],
        },
        "uniqueness": ["order_id"],  # 订单号不能重复
    }
}
```

---

## 六、技术对接组织

### 6.1 申请渠道

| PMS类型 | 申请渠道 | 负责部门 | 预期周期 |
|---------|---------|---------|---------|
| 蓝凤凰 | 安逸集团IT部 → 蓝凤凰 | 安逸集团IT | 2-4周 |
| Opera | 锦江集团IT部 → Oracle | 锦江集团IT | 4-12周 |
| 石基 | 安逸集团IT部 → 石基 | 石基销售 | 2-3周 |

### 6.2 关键对接人识别

**第一步：找谁？**

```
1. 前厅经理 → 知道用什么PMS
2. 财务经理 → 知道夜审数据在哪里
3. 酒店IT（如果有）→ 直接负责系统对接
4. 店长/总经理 → 决策人，需要签署数据协议
5. 安逸集团IT → 集团IT部门，可协调PMS厂商
```

**第二步：怎么说？**

```
开场话术：
"您好，我们是AHL团队，正在为锦江嘉州宾馆部署数字员工系统。
这个系统可以帮助酒店自动计算收益指标、监控竞品价格、生成日报等。
为了实现这些功能，我们需要与PMS系统进行数据对接。
在这个过程中，需要您这边配合几件事..."
```

**第三步：要什么？**

```
1. 确认PMS系统类型和版本
2. 申请API测试账号（或Excel导出权限）
3. 确认数据安全协议签署流程
4. 了解网络环境（是否可访问外网）
```

### 6.3 数据安全协议模板

> ⚠️ 以下为协议框架，实际使用需法务审核

```text
数据使用协议（框架）

甲方：四川乐山锦江嘉州宾馆
乙方：AHL团队

一、数据使用目的
- 仅用于酒店收益管理数据分析
- 仅在本地存储，不上传至第三方
- 数据仅供甲方酒店使用，不共享给其他酒店

二、数据范围
- 订单数据（入住/离店/房价/客源）
- 住客基础信息（姓名+联系方式）
- 房态和夜审数据

三、安全保障
- 乙方承诺不对外泄露数据
- 乙方员工均签署保密协议
- 数据存储采用加密存储
- 协议终止后7日内删除所有数据

四、双方责任
- 甲方提供必要的系统接入权限
- 乙方负责技术对接和数据处理
- 如有数据泄露，双方依法承担责任

签署日期：__________
甲方签字：__________ 乙方签字：__________
```

---

## 七、风险与应对

| 风险 | 级别 | 应对方案 |
|------|------|---------|
| **PMS API申请被拒** | 🔴 高 | 立即切换手工Excel导入，确保SKILL可运行 |
| **申请周期超4周** | 🟡 中 | 先用Excel方案跑通，同时等待API |
| **酒店不愿开放数据** | 🔴 高 | 强调数据安全协议，以收益日报为诱饵 |
| **PMS版本过旧，API能力弱** | 🟡 中 | 降级到只读字段，优先拉取订单和房态 |
| **网络不通，无法API直连** | 🟡 中 | 改用酒店内网部署方案，或手工导入 |
| **字段映射不准确** | 🟡 中 | 现场实地对照PMS界面和Excel导出 |

---

## 八、下一步动作

### 立即可执行（不依赖API申请）

- [ ] **编写Excel导入适配器脚本**（已提供模板）
- [ ] **设计标准Excel导出模板**（发给酒店）
- [ ] **搭建数据存储目录结构**
- [ ] **配置定时任务框架**

### 需实地确认后执行

- [ ] 确认PMS系统类型（蓝凤凰/Opera/石基）
- [ ] 申请API账号或Excel导出权限
- [ ] 确认网络环境（能否访问外网）
- [ ] 签署数据安全协议

### API申请后执行

- [ ] 获取API Key并配置
- [ ] 测试API连通性
- [ ] 验证数据准确性（与Excel对比）
- [ ] 切换到API自动拉取，废弃手工导入

---

## 附录：参考资料

| 文档 | 来源 | 用途 |
|------|------|------|
| 蓝凤凰API文档 | 安逸集团IT部内部 | API对接参考 |
| OPERA Cloud API文档 | Oracle官网 | API对接参考 |
| 石基云API文档 | 石基官网 | API对接参考 |
| 锦江集团IT对接流程 | 安逸集团IT部 | 申请流程确认 |

---

**文档状态**: V1.0（技术深化版）  
**下次更新**: 实地调研后更新PMS类型和API配置  
**负责人**: AHL技术组
