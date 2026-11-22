# AHL 话术SKILL快速实施指南

> **用途**: 快速上手SKILL开发和部署  
> **配套文档**: AHL-管家话术SKILL化架构V1.0.md  
> **预计时间**: 30分钟理解，2小时上手

---

## 一、5分钟快速理解

### SKILL是什么？

```
传统开发:
意图识别 → 硬编码逻辑 → 固定话术 → 输出

SKILL化:
意图识别 → SKILL路由 → 模板选择 → 槽位填充 → 输出生成
         ↑_________↑
           可配置、可替换
```

### 核心概念

| 概念 | 说明 | 示例 |
|------|------|------|
| **SKILL** | 独立场景模块 | "房型推荐SKILL" |
| **Trigger** | 触发条件 | 关键词、意图、上下文 |
| **Slot** | 需要收集的信息 | 入住日期、房型偏好 |
| **Template** | 话术模板 | 带变量的可配置话术 |
| **Action** | 执行动作 | 查库存、创建任务 |

---

## 二、15分钟创建第一个SKILL

### 步骤1: 创建SKILL目录结构

```bash
mkdir -p skills/reservation/RES-01-demand-inquiry/{templates,actions}
touch skills/reservation/RES-01-demand-inquiry/skill.yaml
```

### 步骤2: 编写SKILL配置

```yaml
# skill.yaml
skill_id: "RES-01"
skill_name: "预订需求探询"
version: "1.0.0"

triggers:
  - intent: "预订酒店"
    keywords: ["订房", "预订", "房间"]

slots:
  - name: "check_in_date"
    type: "date"
    required: true
    
  - name: "guest_count"
    type: "integer"
    required: true
    default: 2

templates:
  - id: "greeting"
    variants:
      standard: "欢迎致电[酒店名]！请问今天有什么可以为您安排的？"
      
  - id: "ask_dates"
    variants:
      standard: "请问您计划什么时候入住呢？住几晚？"

actions:
  - type: "collect_slots"
```

### 步骤3: 测试SKILL

```javascript
// test.js
const skillLoader = require('./skill-loader');

async function test() {
  // 加载SKILL
  const skill = await skillLoader.loadSkill('RES-01');
  
  // 模拟对话
  const context = {
    intent: '预订酒店',
    message: '我想订房',
    slots: {}
  };
  
  // 执行SKILL
  const result = await skillLoader.executeSkill('RES-01', context);
  
  console.log('AI回复:', result.response);
  // 输出: "欢迎致电[酒店名]！请问今天有什么可以为您安排的？"
}

test();
```

---

## 三、30分钟理解进阶特性

### 1. 条件路由

```yaml
# 根据客人类型选择不同话术
templates:
  - id: "upsell_offer"
    conditions:
      - guest_type: "商务"
    variants:
      business: "您明天有重要会议吧？升级行政房..."
      
  - id: "upsell_offer"
    conditions:
      - guest_type: "情侣"
    variants:
      romantic: "既然是特别的日子，要不要升级到景观房..."
```

### 2. 槽位填充

```yaml
slots:
  - name: "check_in_date"
    type: "date"
    required: true
    extraction:
      - method: "nlp_date_parser"
      - method: "relative_date"  # "明天"、"后天"
      - fallback: "ask_explicitly"
```

### 3. 话术变体

```yaml
templates:
  - id: "greeting"
    variants:
      # 随机选择，增加多样性
      - "欢迎致电！"
      - "您好，很高兴为您服务！"
      - "欢迎，有什么可以帮您？"
```

---

## 四、SKILL开发规范

### 命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| SKILL ID | `{场景}-{编号}` | `RES-01`, `CHK-03` |
| 文件名 | 小写+连字符 | `ask-dates.yaml` |
| 变量名 | 下划线命名 | `check_in_date` |
| 模板ID | 动词+名词 | `ask-dates`, `confirm-booking` |

### 优先级规则

```yaml
# 模板优先级（数字越大越优先）
templates:
  - id: "vip_greeting"
    priority: 100  # VIP最高
    
  - id: "returning_greeting"
    priority: 80   # 回头客次之
    
  - id: "standard_greeting"
    priority: 10   # 默认最低
```

### 错误处理

```yaml
fallback:
  - condition: "slot_not_recognized"
    response: "抱歉，我没有完全理解。请问您是说{last_message}吗？"
    
  - condition: "missing_required_slot"
    response: "为了更好地为您服务，能再告诉我一下{slot_name}吗？"
    
  - condition: "system_error"
    response: "抱歉系统暂时出现问题，已通知人工处理。"
    action: "transfer_to_human"
```

---

## 五、常用SKILL模板库

### 模板1: 信息收集型SKILL

```yaml
# 适用于：需求探询、身份验证、偏好收集
skill_type: "information_collection"

flow:
  1_opening:
    template: "greeting"
    
  2_slot_filling:
    - slot: "slot1"
      template: "ask_slot1"
      validation: "validate_slot1"
      
    - slot: "slot2"
      template: "ask_slot2"
      condition: "slot1 == 'specific_value'"
      
  3_confirmation:
    template: "confirm_all_slots"
    
  4_handoff:
    next_skill: "{next_skill_id}"
```

### 模板2: 推荐销售型SKILL

```yaml
# 适用于：房型推荐、升房销售、增值服务
skill_type: "recommendation_sales"

flow:
  1_understand_needs:
    # 复用信息收集模板
    
  2_fetch_options:
    action: "query_inventory"
    
  3_present_options:
    template: "recommendation"
    max_options: 3
    
  4_handle_objections:
    - condition: "price_too_high"
      template: "value_explanation"
      
    - condition: "need_comparison"
      template: "show_comparison"
      
  5_close_sale:
    template: "confirmation"
```

### 模板3: 服务执行型SKILL

```yaml
# 适用于：客房服务、维修请求、物品配送
skill_type: "service_execution"

flow:
  1_receive_request:
    template: "acknowledge"
    
  2_clarify_details:
    slots: ["item_type", "quantity", "urgency"]
    
  3_create_task:
    action: "create_service_task"
    params:
      department: "{department}"
      sla: "{sla_minutes}"
      
  4_confirm_delivery:
    template: "delivery_confirmation"
    
  5_follow_up:
    delay: "{sla_minutes}"
    action: "check_completion"
    template: "satisfaction_check"
```

---

## 六、部署检查清单

### 上线前检查

```
□ SKILL配置语法正确
□ 所有模板变量已定义
□ 槽位提取规则完整
□ 兜底话术已配置
□ 单元测试通过
□ 集成测试通过
□ 性能测试通过（响应<1秒）
```

### 监控指标

```yaml
metrics:
  - name: "skill_activation_rate"
    target: "> 95%"  # 触发准确率
    
  - name: "slot_filling_rate"
    target: "> 90%"  # 槽位填充率
    
  - name: "template_render_time"
    target: "< 50ms"  # 模板渲染时间
    
  - name: "fallback_trigger_rate"
    target: "< 5%"   # 兜底话术触发率
```

---

## 七、常见问题

### Q1: 一个意图触发多个SKILL怎么办？

**A**: 按优先级排序，或增加更精确的触发条件：

```yaml
triggers:
  - intent: "预订"
    keywords: ["房间", "住宿"]  # 增加关键词限制
    context: "no_active_booking"  # 增加上下文条件
```

### Q2: 如何处理多轮对话？

**A**: 使用上下文管理：

```yaml
# SKILL A 结束时下上文
actions:
  - type: "set_context"
    key: "booking_in_progress"
    value: true
    
# SKILL B 触发时检查上下文
triggers:
  - context: "booking_in_progress"
    intent: "确认"
```

### Q3: 如何实现话术A/B测试？

**A**: 在模板中配置变体比例：

```yaml
templates:
  - id: "upsell"
    variants:
      - text: "话术A"
        weight: 50  # 50%流量
      - text: "话术B"
        weight: 50  # 50%流量
```

### Q4: 多语言支持怎么做？

**A**: 按语言分离模板文件：

```
templates/
├── zh/
│   └── greeting.yaml
├── en/
│   └── greeting.yaml
└── ja/
    └── greeting.yaml
```

---

## 八、下一步行动

1. **立即行动**
   - [ ] 搭建SKILL开发环境
   - [ ] 实现SKILL加载器
   - [ ] 创建第一个测试SKILL

2. **本周完成**
   - [ ] 迁移3个核心场景为SKILL
   - [ ] 建立话术A/B测试框架
   - [ ] 完成多语言支持

3. **本月目标**
   - [ ] 全部场景SKILL化
   - [ ] 上线运营监控
   - [ ] 持续优化迭代

---

*有问题随时问我，或参考完整架构文档*


---

## 🔗 相关笔记

- [[AHL 平台 MOC]]
- [[AI-Agent MOC]]
- [[工具-系统 MOC]]

*该区块由 B166ER 自动注入 (2026-07-28) — 关键词匹配*
