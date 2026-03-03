# AHL 管家话术SKILL化架构方案 V1.0

> **定位**: 将话术库拆解为可插拔的SKILL模块  
> **适用范围**: C端AI管家、B端AI运营官、夜班自动化  
> **版本**: V1.0  
> **创建**: 2026-03-03  
> **核心架构**: 大模型中枢 + 场景SKILL + 话术模板

---

## 一、SKILL化架构总览

### 1.1 核心理念

```
传统架构                    SKILL化架构
┌──────────────┐          ┌─────────────────────────────┐
│   大模型     │          │        大模型中枢            │
│  (单一)      │          │    (意图识别 + 路由分发)      │
└──────┬───────┘          └─────────────┬───────────────┘
       │                                │
       ↓                    ┌───────────┼───────────┐
  固定话术逻辑              ↓           ↓           ↓
                       ┌──────┐  ┌──────┐  ┌──────┐
                       │SKILL1│  │SKILL2│  │SKILL3│
                       │预订  │  │入住  │  │服务  │
                       └──────┘  └──────┘  └──────┘
                            可插拔、可替换、可组合
```

### 1.2 SKILL模块标准结构

每个SKILL模块包含：

```yaml
skill_name: "场景名称"
version: "1.0.0"
triggers:          # 触发条件
  - 意图关键词
  - 上下文状态
  - 时间/事件条件

slots:            # 需要填充的槽位
  - slot_name: 变量名
    type: 类型
    required: 是否必填
    default: 默认值

templates:        # 话术模板库
  - template_id: "模板ID"
    conditions:   # 使用条件
      - 条件表达式
    variants:     # 变体话术
      - "话术1"
      - "话术2"
    variables:    # 模板变量
      - "{variable_name}"

actions:          # 执行动作
  - action_type: 动作类型
    params: 参数

fallback:         # 兜底话术
  - "默认话术"
```

---

## 二、场景SKILL矩阵

### 2.1 一级场景分类

| 场景ID | 场景名称 | 适用对象 | 触发频率 | 复杂度 |
|--------|---------|---------|---------|--------|
| **RES** | 预订场景 | C端AI管家 | 高 | ⭐⭐⭐ |
| **CHK** | 入住接待 | C端AI管家 | 高 | ⭐⭐⭐⭐ |
| **ROM** | 客房服务 | C端AI管家 | 高 | ⭐⭐ |
| **F_B** | 餐饮服务 | C端AI管家 | 中 | ⭐⭐⭐ |
| **CON** | 礼宾服务 | C端AI管家 | 中 | ⭐⭐⭐⭐ |
| **NIG** | 夜班值守 | C端AI管家 | 低 | ⭐⭐⭐⭐⭐ |
| **MKT** | 营销转化 | B端AI运营官 | 中 | ⭐⭐⭐⭐ |
| **CRM** | 会员管理 | B端AI运营官 | 中 | ⭐⭐⭐ |
| **REV** | 收益管理 | B端AI运营官 | 低 | ⭐⭐⭐⭐⭐ |
| **EMG** | 应急处理 | 双端通用 | 低 | ⭐⭐⭐⭐⭐ |

### 2.2 二级场景拆解

```
RES 预订场景
├── RES-01 需求探询SKILL
├── RES-02 房型推荐SKILL
├── RES-03 升房销售SKILL
├── RES-04 价格谈判SKILL
└── RES-05 预订确认SKILL

CHK 入住接待
├── CHK-01 到店迎接SKILL
├── CHK-02 身份验证SKILL
├── CHK-03 客房介绍SKILL
├── CHK-04 特殊需求处理SKILL
└── CHK-05 入住完成SKILL

ROM 客房服务
├── ROM-01 物品需求SKILL
├── ROM-02 维修服务SKILL
├── ROM-03 清洁服务SKILL
├── ROM-04 换房延住SKILL
└── ROM-05 退房服务SKILL
```

---

## 三、核心SKILL详细设计

### 3.1 RES-01 需求探询SKILL

```yaml
skill_id: "RES-01"
skill_name: "预订需求探询"
description: "识别客人预订需求，收集关键信息"
version: "1.0.0"

# 触发条件
triggers:
  - intent: "预订酒店"
    keywords: ["订房", "预订", "房间", "住宿"]
  - intent: "查询房型"
    keywords: ["有什么房间", "房型", "房价"]
  - context: "首次对话"
    condition: "no_previous_booking"

# 槽位定义
slots:
  - name: "check_in_date"
    type: "date"
    required: true
    description: "入住日期"
    
  - name: "check_out_date"
    type: "date"
    required: true
    description: "离店日期"
    
  - name: "guest_count"
    type: "integer"
    required: true
    default: 2
    description: "入住人数"
    
  - name: "room_type_pref"
    type: "string"
    required: false
    description: "房型偏好"
    
  - name: "budget_range"
    type: "string"
    required: false
    options: ["经济", "舒适", "豪华", "奢华"]
    
  - name: "travel_purpose"
    type: "string"
    required: false
    options: ["商务", "休闲", "家庭", "情侣"]

# 话术模板库
templates:
  # 开场话术
  - id: "greeting"
    priority: 1
    conditions:
      - step: "opening"
    variants:
      standard: "欢迎致电[酒店名]！我是您的专属AI管家小H，请问今天有什么可以为您安排的？"
      luxury: "欢迎致电[酒店名]。我是您的管家[姓名]，很荣幸为您服务。请问有什么可以帮您安排？"
      night: "晚上好！我是夜班管家，请问有什么可以帮您？"
    
  # 日期询问
  - id: "ask_dates"
    priority: 2
    conditions:
      - step: "dates"
      - missing_slots: ["check_in_date", "check_out_date"]
    variants:
      standard: "请问您计划什么时候入住呢？住几晚？"
      follow_up: "请问具体入住日期是哪天？"
      clarification: "好的，{check_in_date}入住，住{stay_nights}晚，对吗？"
    variables:
      - "{check_in_date}"
      - "{stay_nights}"
    
  # 人数询问
  - id: "ask_guests"
    priority: 3
    conditions:
      - step: "guests"
      - missing_slots: ["guest_count"]
    variants:
      standard: "请问一共几位入住？有没有小朋友？"
      family: "请问是几位大人和几位小朋友呢？"
      business: "请问就您一位入住吗？"
      
  # 偏好询问
  - id: "ask_preferences"
    priority: 4
    conditions:
      - step: "preferences"
      - missing_slots: ["room_type_pref", "budget_range"]
    variants:
      standard: "请问您偏好高楼层还是低楼层？需要安静还是方便？"
      budget: "我们这边有舒适型¥{budget_min}起，豪华型¥{budget_max}起，您倾向哪种？"
      purpose: "请问是商务出行还是休闲旅游？我可以推荐最适合的房型。"
    variables:
      - "{budget_min}"
      - "{budget_max}"

# 执行动作
actions:
  - type: "collect_slots"
    params:
      slots: ["check_in_date", "check_out_date", "guest_count", "room_type_pref", "budget_range", "travel_purpose"]
      
  - type: "calculate"
    params:
      operation: "stay_nights"
      inputs: ["check_in_date", "check_out_date"]
      
  - type: "route"
    params:
      next_skill: "RES-02"
      condition: "all_required_slots_filled"

# 兜底话术
fallback:
  - "抱歉，我没有完全理解。请问您是说{last_message}吗？"
  - "为了更好地为您服务，能再告诉我一下{missing_slot}吗？"
```

---

### 3.2 RES-02 房型推荐SKILL

```yaml
skill_id: "RES-02"
skill_name: "房型推荐"
description: "根据需求推荐合适房型，执行升房销售"
version: "1.0.0"

triggers:
  - context: "RES-01完成"
  - intent: "推荐房型"
  - intent: "升房"

slots:
  - name: "recommended_room"
    type: "object"
    required: true
    properties:
      - room_type
      - price
      - area
      - features
      
  - name: "upgrade_room"
    type: "object"
    required: false
    properties:
      - room_type
      - price
      - upgrade_cost
      - benefits
      
  - name: "guest_response"
    type: "string"
    required: false
    options: ["接受", "拒绝", "考虑", "需要比较"]

templates:
  # 基础推荐
  - id: "base_recommendation"
    priority: 1
    conditions:
      - step: "recommendation"
    variants:
      standard: "根据您的需求，我推荐{room_type}，{area}平米，{features}，今晚特价¥{price}，比原价优惠¥{discount}。"
      luxury: "为您精选了{room_type}，这是我们家最受欢迎的房型，{features}，今晚特别价¥{price}。"
      scarce: "这个房型今天只剩{remaining}间了，而且享受{special_offer}，建议您先锁定。"
    variables:
      - "{room_type}"
      - "{area}"
      - "{features}"
      - "{price}"
      - "{discount}"
      - "{remaining}"
      - "{special_offer}"
      
  # 升房推荐
  - id: "upsell_offer"
    priority: 2
    conditions:
      - step: "upsell"
      - guest_profile: ["商务", "情侣", "家庭"]
    variants:
      value_comparison: |
        {guest_name}先生/女士，您订的基础房¥{base_price}/晚，我现在可以给您一个升级优惠：
        - 升级到{upgrade_room}只需加¥{upgrade_cost}/晚
        - 多了{extra_area}平米空间和{extra_features}
        - 包含{benefits}
        - 单独买这些权益要¥{benefits_value}，升级只要¥{upgrade_cost}
        相当于花小钱享受大升级，您看要锁定吗？
      
      scenario_business: |
        您明天有重要会议吧？升级行政房可以享用行政酒廊的安静环境处理工作，还有免费熨烫服务。
        每晚只需加¥{upgrade_cost}，值得为您的成功投资。
      
      scenario_couple: |
        既然是特别的日子，要不要升级到景观房？可以看{view_feature}，还有欢迎香槟和花瓣布置。
        只需加¥{upgrade_cost}，让这晚更难忘。
      
      scenario_family: |
        带孩子的话，升级家庭房空间大很多，有儿童用品和加床，孩子住得更舒服。
        加¥{upgrade_cost}就能让全家都舒适，很划算。
      
      history_based: |
        您上次入住的是{previous_room}，这次要不要试试{upgrade_room}？很多客人反馈{guest_feedback}。
        现在升级只要加¥{upgrade_cost}。
    variables:
      - "{guest_name}"
      - "{base_price}"
      - "{upgrade_room}"
      - "{upgrade_cost}"
      - "{extra_area}"
      - "{extra_features}"
      - "{benefits}"
      - "{benefits_value}"
      - "{view_feature}"
      - "{previous_room}"
      - "{guest_feedback}"

  # 价格谈判
  - id: "price_negotiation"
    priority: 3
    conditions:
      - step: "negotiation"
      - guest_response: "太贵了"
    variants:
      - "我理解您的考虑。这个价格在同类酒店中其实很有竞争力，而且包含{included_services}。"
      - "如果您能确定预订，我可以申请给您{discount_percent}的优惠，这是我能争取的最大力度了。"
      - "或者您看这样，我送您{complimentary_service}，价值¥{service_value}，这样性价比就更高了。"
    variables:
      - "{included_services}"
      - "{discount_percent}"
      - "{complimentary_service}"
      - "{service_value}"

actions:
  - type: "fetch_inventory"
    params:
      check_in: "{check_in_date}"
      check_out: "{check_out_date}"
      guests: "{guest_count}"
      
  - type: "recommend_rooms"
    params:
      strategy: "best_match"
      upsell: true
      
  - type: "calculate_upgrade"
    params:
      base_room: "{recommended_room}"
      upgrade_options: ["deluxe", "suite", "executive"]

fallback:
  - "让我为您查一下还有哪些房型可选..."
  - "抱歉，{room_type}已经被预订了。我为您推荐另一个也很好的选择..."
```

---

### 3.3 CHK-01 到店迎接SKILL

```yaml
skill_id: "CHK-01"
skill_name: "到店迎接"
description: "客人到店时的迎接服务"
version: "1.0.0"

triggers:
  - event: "guest_arrival"
  - location: "酒店入口"
  - time: "any"

slots:
  - name: "guest_name"
    type: "string"
    required: true
    source: "预订系统"
    
  - name: "arrival_method"
    type: "string"
    required: false
    options: ["出租车", "网约车", "私家车", "步行"]
    
  - name: "luggage_count"
    type: "integer"
    required: false
    default: 0
    
  - name: "vip_level"
    type: "string"
    required: false
    options: ["普通", "银卡", "金卡", "白金", "黑卡"]

templates:
  # 车门迎接
  - id: "car_greeting"
    priority: 1
    conditions:
      - location: "酒店入口"
      - arrival_method: ["出租车", "网约车", "私家车"]
    variants:
      standard: "欢迎光临{hotel_name}！请问有预订吗？我来帮您拿行李。"
      luxury: "欢迎莅临{hotel_name}。我是您的管家{name}，请允许我为您开门。"
      vip: "{guest_name}先生/女士，欢迎回家！您的房间已经准备好了，请随我来。"
      night: "晚上好！欢迎光临，请问有预订吗？小心台阶。"
    variables:
      - "{hotel_name}"
      - "{name}"
      - "{guest_name}"
      
  # 前台识别
  - id: "front_desk_recognition"
    priority: 2
    conditions:
      - location: "前台"
      - guest_identified: true
    variants:
      standard: "您好，请问是{guest_name}先生/女士吗？您的房间已经准备好了。"
      vip: "{guest_name}先生/女士，欢迎回家。我是您的专属管家{name}，很高兴再次见到您。"
      first_time: "{guest_name}先生/女士，欢迎首次光临{hotel_name}。我是您的管家{name}，将全程为您服务。"
    variables:
      - "{guest_name}"
      - "{hotel_name}"
      - "{name}"
      
  # 等待安抚
  - id: "waiting_comfort"
    priority: 3
    conditions:
      - status: "processing"
      - wait_time: "> 1 minute"
    variants:
      - "请稍等2分钟，我正在为您办理入住手续，您可以先享用欢迎饮品。"
      - "不好意思让您久等了，这是您的欢迎茶饮，请慢用。"
      - "马上就好，这是给您的小点心，请稍事休息。"

actions:
  - type: "identify_guest"
    params:
      method: ["车牌识别", "面部识别", "预订信息"]
      
  - type: "fetch_booking"
    params:
      guest_name: "{guest_name}"
      
  - type: "assign_butler"
    params:
      vip_level: "{vip_level}"
      language: "{guest_preferred_language}"

fallback:
  - "欢迎光临！请问怎么称呼您？"
  - "您好！请问有预订吗？我可以帮您查询。"
```

---

### 3.4 ROM-01 物品需求SKILL

```yaml
skill_id: "ROM-01"
skill_name: "客房物品需求"
description: "处理客人对各类物品的需求"
version: "1.0.0"

triggers:
  - intent: "物品需求"
    keywords: ["送", "需要", "要", "拿"]
  - location: "客房内"
  - channel: ["语音", "App", "电话"]

slots:
  - name: "item_type"
    type: "string"
    required: true
    options: ["水", "枕头", "洗漱用品", "毛巾", "被子", "充电线", "文具", "药品"]
    
  - name: "item_spec"
    type: "string"
    required: false
    description: "具体规格"
    
  - name: "quantity"
    type: "integer"
    required: false
    default: 1
    
  - name: "urgency"
    type: "string"
    required: false
    options: ["普通", "紧急"]
    default: "普通"

templates:
  # 接单确认
  - id: "order_confirmation"
    priority: 1
    conditions:
      - step: "receiving"
    variants:
      water: "好的，马上为您送{quantity}瓶{water_type}到房间，预计{delivery_time}分钟。"
      pillow: "请问需要什么类型的枕头？我们有羽绒/乳胶/荞麦/记忆棉可选。"
      toiletries: "需要牙刷/梳子/剃须刀/浴帽，对吗？还有其他需要的吗？"
      blanket: "好的，马上为您加{blanket_type}，预计{delivery_time}分钟送到。"
      charger: "我们有Type-C/苹果/安卓充电线，请问您需要哪种接口？"
    variables:
      - "{quantity}"
      - "{water_type}"
      - "{delivery_time}"
      - "{blanket_type}"
      
  # 规格确认
  - id: "specification_confirm"
    priority: 2
    conditions:
      - step: "specification"
      - item_type: ["枕头", "水", "充电线"]
    variants:
      pillow_types: |
        我们有以下几种枕头可选：
        1. 羽绒枕 - 柔软舒适，适合喜欢软枕的客人
        2. 乳胶枕 - 支撑性好，适合颈椎不适的客人
        3. 荞麦枕 - 传统硬枕，适合习惯硬枕的客人
        4. 记忆棉枕 - 贴合头部，适合侧睡客人
        请问您偏好哪种？
      water_types: |
        我们有：
        1. 矿泉水
        2. 苏打水
        3. 气泡水
        请问您要哪种？
        
  # 交付话术
  - id: "delivery"
    priority: 3
    conditions:
      - step: "delivery"
    variants:
      standard: "您好，您要的{item_name}到了，放在{location}了。"
      pillow: "这是您要的{pillow_type}枕头，我帮您换上。旧枕头需要收走吗？"
      toiletries: "您的洗漱用品到了，一次性用品建议带走或丢弃。还需要其他物品吗？"
      charger: "这是您要的充电线，用完请归还前台。请问还需要其他帮助吗？"
    variables:
      - "{item_name}"
      - "{location}"
      - "{pillow_type}"

actions:
  - type: "create_task"
    params:
      department: "客房部"
      item: "{item_type}"
      quantity: "{quantity}"
      urgency: "{urgency}"
      
  - type: "estimate_time"
    params:
      base_time: 5
      factor: "{urgency}"
      
  - type: "notify_guest"
    params:
      channel: ["App推送", "短信"]
      message: "您的{item_type}已送出，预计{delivery_time}分钟送达。"

fallback:
  - "好的，我记录下来。请问您房间号是多少？"
  - "抱歉，这个物品我们暂时没有。我可以为您推荐替代品..."
```

---

## 四、SKILL编排与组合

### 4.1 对话流程编排

```yaml
# 预订流程编排
booking_flow:
  name: "完整预订流程"
  
  steps:
    - skill: "RES-01"
      name: "需求探询"
      next: 
        condition: "slots_complete"
        skill: "RES-02"
        
    - skill: "RES-02"
      name: "房型推荐"
      branches:
        - condition: "guest_accepts"
          skill: "RES-05"
        - condition: "guest_needs_comparison"
          skill: "RES-02"
          params:
            show_alternatives: true
        - condition: "guest_rejects"
          skill: "RES-04"
          
    - skill: "RES-04"
      name: "价格谈判"
      next:
        condition: "agreement_reached"
        skill: "RES-05"
        
    - skill: "RES-05"
      name: "预订确认"
      terminal: true
```

### 4.2 条件路由配置

```yaml
# 根据客人类型路由不同话术风格
routing_rules:
  - condition: "vip_level == '黑卡'"
    style: "royal"
    skills:
      - "RES-02-luxury"
      - "CHK-01-luxury"
      - "ROM-01-premium"
      
  - condition: "vip_level == '金卡' or vip_level == '白金'"
    style: "luxury"
    skills:
      - "RES-02-luxury"
      - "CHK-01-standard"
      - "ROM-01-premium"
      
  - condition: "time >= '22:00' or time <= '06:00'"
    style: "night_shift"
    skills:
      - "NIG-01"
      - "EMG-01"
      
  - condition: "travel_purpose == '商务'"
    style: "business"
    upsell_focus: ["行政房", "会议室", "行政酒廊"]
    
  - condition: "travel_purpose == '情侣'"
    style: "romantic"
    upsell_focus: ["景观房", "浪漫套餐", "SPA"]
```

---

## 五、SKILL实施技术方案

### 5.1 文件结构

```
ahl-butler-skills/
├── config/
│   ├── skill-registry.yaml      # SKILL注册表
│   ├── routing-rules.yaml       # 路由规则
│   └── templates-config.yaml    # 模板配置
│
├── skills/
│   ├── reservation/
│   │   ├── RES-01-demand-inquiry/
│   │   │   ├── skill.yaml
│   │   │   ├── templates/
│   │   │   │   ├── greeting.yaml
│   │   │   │   ├── ask-dates.yaml
│   │   │   │   └── ask-guests.yaml
│   │   │   └── actions/
│   │   │       └── collect-slots.js
│   │   │
│   │   ├── RES-02-room-recommendation/
│   │   └── RES-03-upsell/
│   │
│   ├── checkin/
│   │   ├── CHK-01-arrival-greeting/
│   │   ├── CHK-02-id-verification/
│   │   └── CHK-03-room-introduction/
│   │
│   ├── room-service/
│   ├── f-b/
│   ├── concierge/
│   ├── night-shift/
│   └── emergency/
│
├── shared/
│   ├── templates/               # 共享模板
│   │   ├── common-greetings.yaml
│   │   ├── apology-templates.yaml
│   │   └── farewell-templates.yaml
│   │
│   ├── utils/                   # 工具函数
│   │   ├── date-parser.js
│   │   ├── price-formatter.js
│   │   └── i18n-helper.js
│   │
│   └── data/                    # 共享数据
│       ├── room-types.yaml
│       ├── amenities.yaml
│       └── policies.yaml
│
└── tests/
    ├── unit/
    └── integration/
```

### 5.2 SKILL加载器伪代码

```javascript
// SKILL加载器
class SkillLoader {
  constructor() {
    this.skillRegistry = new Map();
    this.templateEngine = new TemplateEngine();
  }
  
  // 加载单个SKILL
  async loadSkill(skillId) {
    const skillPath = `./skills/${skillId}/skill.yaml`;
    const skillConfig = await yaml.load(skillPath);
    
    // 加载模板
    skillConfig.templates = await this.loadTemplates(skillId);
    
    // 注册到路由
    this.skillRegistry.set(skillId, skillConfig);
    
    return skillConfig;
  }
  
  // 根据意图路由到对应SKILL
  routeSkill(intent, context, slots) {
    // 1. 意图匹配
    const matchedSkills = Array.from(this.skillRegistry.values())
      .filter(skill => skill.triggers.some(t => 
        t.intent === intent || t.keywords?.includes(intent)
      ));
    
    // 2. 条件过滤
    const eligibleSkills = matchedSkills.filter(skill =>
      this.checkConditions(skill.conditions, context, slots)
    );
    
    // 3. 优先级排序
    return eligibleSkills.sort((a, b) => b.priority - a.priority)[0];
  }
  
  // 执行SKILL
  async executeSkill(skillId, context) {
    const skill = this.skillRegistry.get(skillId);
    
    // 1. 槽位填充
    const filledSlots = await this.fillSlots(skill.slots, context);
    
    // 2. 选择模板
    const template = this.selectTemplate(skill.templates, filledSlots);
    
    // 3. 渲染话术
    const response = this.templateEngine.render(template, filledSlots);
    
    // 4. 执行动作
    const actions = await this.executeActions(skill.actions, filledSlots);
    
    return {
      response,
      actions,
      nextSkill: this.determineNextSkill(skill, filledSlots)
    };
  }
  
  // 模板选择
  selectTemplate(templates, slots) {
    // 按条件筛选
    const eligibleTemplates = templates.filter(t => 
      !t.conditions || t.conditions.every(c => this.evaluateCondition(c, slots))
    );
    
    // 按优先级排序
    const sorted = eligibleTemplates.sort((a, b) => b.priority - a.priority);
    
    // 随机选择变体（增加话术多样性）
    const selected = sorted[0];
    const variants = Object.values(selected.variants);
    return variants[Math.floor(Math.random() * variants.length)];
  }
}
```

---

## 六、SKILL化收益

### 6.1 开发效率提升

| 指标 | 传统方式 | SKILL化方式 | 提升 |
|------|---------|------------|------|
| 新场景开发 | 2-3天 | 4-8小时 | 5x |
| 话术修改 | 改代码 | 改配置 | 10x |
| A/B测试 | 开发两套 | 配置两套 | 5x |
| 多语言支持 | 重写话术 | 翻译配置 | 10x |

### 6.2 运营灵活性

- ✅ 话术热更新，无需重启服务
- ✅ 不同品牌配置不同SKILL组合
- ✅ 快速响应市场变化
- ✅ 支持灰度发布

### 6.3 质量保障

- ✅ 单元测试每个SKILL
- ✅ 话术版本管理
- ✅ 效果数据追踪
- ✅ 持续优化迭代

---

*本文档为AHL场景SKILL化架构设计，可根据实际技术选型调整实现细节*
