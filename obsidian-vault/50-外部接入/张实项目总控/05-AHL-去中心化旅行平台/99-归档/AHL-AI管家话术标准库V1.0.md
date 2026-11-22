# AHL AI管家话术标准库 V1.0

> **定位**: AI管家/夜班人员的全场景话术标准库  
> **适用范围**: C端AI管家、B端AI运营官、夜班自动化接待  
> **版本**: V1.0  
> **创建**: 2026-03-03  
> **核心架构**: 国内标准 + 国际标准 + 场景细分 + 营销转化

---

## 一、话术体系总览

### 1.1 核心原则

| 原则 | 国内风格 | 国际风格 | AI适配要点 |
|------|---------|---------|-----------|
| **热情度** | 主动热情、称呼亲切 | 专业克制、尊重距离 | 语气温暖但不越界 |
| **效率性** | 简洁明了、直击要点 | 流程标准、步骤清晰 | 3秒响应、30秒解决 |
| **个性化** | 记住偏好、主动关怀 | 尊重隐私、按需服务 | 数据驱动、千人千面 |
| **营销性** | 自然植入、不硬推销 | 价值呈现、需求匹配 | 场景触发、智能推荐 |

### 1.2 话术层级结构

```
第一层: 问候语 (Greeting)
    ↓
第二层: 需求识别 (Need Identification) 
    ↓
第三层: 方案提供 (Solution Offering)
    ↓
第四层: 价值增强 (Value Enhancement) ← 营销植入点
    ↓
第五层: 闭环确认 (Closure Confirmation)
    ↓
第六层: 情感收尾 (Warm Closing)
```

### 1.3 语音与文字差异

| 维度 | 语音通话 | 文字聊天 | 界面交互 |
|------|---------|---------|---------|
| 语速 | 120-150字/分钟 | 即时 | 点击响应<1秒 |
| 敬语 | "您"频率高 | "您/你"适中 | 无敬语，简洁 |
| 确认 | 口头确认 | 文字确认+表情 | 视觉反馈 |
| 打断处理 | 耐心倾听 | 自动分句 | 支持撤回/修改 |

---

## 二、标准问候话术

### 2.1 首次接触问候

**国内标准版 (中文)**

| 场景 | 话术 | 语气标记 | 时长 |
|------|------|---------|------|
| **电话接听** | "您好，这里是[酒店名]AI管家，很高兴为您服务，请问有什么可以帮您？" | 热情上扬 | 5秒 |
| **在线接入** | "欢迎致电[酒店名]！我是您的专属AI管家小H，请问今天有什么可以为您安排的？" | 亲切自然 | 6秒 |
| **App唤醒** | "晚上好！我是您的AI管家，检测到您刚刚抵达，需要我协助办理入住吗？" | 温暖关怀 | 5秒 |
| **客房语音** | "您好，我是您的房间管家，有什么可以帮您？" | 专业简洁 | 3秒 |

**国际标准版 (English)**

| Scene | Script | Tone | Duration |
|-------|--------|------|----------|
| **Phone** | "Good [morning/afternoon/evening], thank you for calling [Hotel Name]. This is your AI concierge speaking. How may I assist you today?" | Professional warm | 6s |
| **Online** | "Welcome to [Hotel Name]! I'm your dedicated AI assistant. What can I do for you today?" | Friendly | 5s |
| **App** | "Good evening! I noticed you've just arrived. May I assist you with check-in?" | Proactive helpful | 4s |
| **In-room** | "Hello, I'm your room assistant. How may I help you?" | Polite efficient | 3s |

### 2.2 时段差异化问候

**中文时段话术**

| 时段 | 问候语 | 关怀元素 |
|------|--------|---------|
| **06:00-09:00** | "早上好！新的一天开始了，祝您有个好心情！" | 早餐提醒 |
| **09:00-12:00** | "上午好！今天行程满吗？需要我帮您安排什么？" | 行程关怀 |
| **12:00-14:00** | "中午好！用餐时间到了，我们的餐厅有今日特推。" | 用餐建议 |
| **14:00-18:00** | "下午好！忙碌了一天，需要茶歇或休息吗？" | 放松提醒 |
| **18:00-22:00** | "晚上好！晚餐时间，需要推荐周边美食吗？" | 晚餐建议 |
| **22:00-02:00** | "晚上好！夜已深，有任何需要请随时叫我。" | 夜班值守 |
| **02:00-06:00** | "您好，夜班管家为您服务，请问有什么紧急需要？" | 应急服务 |

---

## 三、核心场景话术库

### 3.1 预订场景 (Reservation)

#### 3.1.1 需求探询

**中文话术**

| 步骤 | 话术 | 目的 |
|------|------|------|
| **开场** | "请问您计划什么时候入住呢？住几晚？" | 基础信息 |
| **人数** | "请问一共几位入住？有没有小朋友？" | 房型匹配 |
| **偏好** | "请问您偏好高楼层还是低楼层？需要安静还是方便？" | 个性化 |
| **预算** | "我们这边有舒适型¥XXX起，豪华型¥XXX起，您倾向哪种？" | 价格锚定 |
| **目的** | "请问是商务出行还是休闲旅游？我可以推荐最适合的房型。" | 场景匹配 |

#### 3.1.2 房型推荐与升房话术

**中文升房话术**

| 场景 | 标准话术 | 转化技巧 |
|------|---------|---------|
| **基础推荐** | "根据您的需求，我推荐[房型名称]，[面积]平米，[核心卖点]，今晚特价¥XXX，比原价优惠¥XX。" | 价值对比 |
| **升级推荐** | "如果您愿意多加¥XXX/晚，可以升级到[高级房型]，多了[具体权益：浴缸/景观/行政待遇]，性价比很高。" | 小额递增 |
| **限量稀缺** | "这个房型今天只剩3间了，而且享受[限时权益]，建议您先锁定。" | 稀缺性 |
| **体验升级** | "您上次入住的是[原房型]，这次要不要试试[升级房型]？很多客人反馈[具体好评点]。" | 历史数据 |

### 3.2 入住接待场景 (Check-in)

#### 3.2.1 到店迎接

**中文话术**

| 触点 | 话术 | 动作 |
|------|------|------|
| **车门** | "欢迎光临[酒店名]！请问有预订吗？我来帮您拿行李。" | 开门、提行李 |
| **前台** | "您好，请问是[姓氏]先生/女士吗？您的房间已经准备好了。" | 识别、微笑 |
| **完成** | "[姓氏]先生/女士，这是您的房卡，房间在[X]楼[房号]，早餐在[X]楼[X]点-[X]点。" | 递房卡、指方向 |

#### 3.2.2 客房介绍

**中文客房介绍话术**

```
"[姓氏]先生/女士，我简单介绍一下房间设施：
- 房间在[X]楼[房号]，这是您的房卡
- 空调/电视/灯光可以通过床头面板或语音控制，说'小H小H'唤醒
- 高速WiFi密码在房卡套上，也可以扫码连接
- 迷你吧的饮品首次免费，后续消费会记入房账
- 如果需要任何服务，可以直接叫'小H'或拨打[X]号分机
- 早餐在[X]楼，时间是[X]点到[X]点

请问还有什么需要了解的吗？"
```

### 3.3 客房服务场景 (In-room Service)

#### 3.3.1 物品需求

**中文话术**

| 需求 | 确认话术 | 交付话术 |
|------|---------|---------|
| **送水** | "好的，马上为您送[X]瓶矿泉水到房间，预计5分钟。" | "您好，您要的矿泉水到了，放在桌上了。" |
| **送枕头** | "请问需要什么类型的枕头？我们有羽绒/乳胶/荞麦/记忆棉可选。" | "这是您要的[类型]枕头，我帮您换上。" |
| **送洗漱用品** | "需要牙刷/梳子/剃须刀/浴帽，对吗？还有其他需要的吗？" | "您的洗漱用品到了，一次性用品建议带走或丢弃。" |
| **加床** | "加床费用是¥XXX/晚，包含额外早餐和洗漱用品，确认要加吗？" | "加床已经加好了，额外床品和用品都在床上。" |

### 3.4 餐饮服务场景 (F&B)

#### 3.4.1 餐厅推荐

**中文话术**

| 场景 | 推荐话术 |
|------|---------|
| **早餐推荐** | "早餐在[X]楼[餐厅名]，时间[X]点-[X]点。推荐您试试我们的[特色菜品]，很多客人好评。" |
| **午餐推荐** | "中午我们[中餐厅/西餐厅]有商务套餐，¥XX起，含主菜+汤+饮品，性价比很高，需要我帮您订位吗？" |
| **晚餐推荐** | "今晚[餐厅名]有[特色菜/主厨推荐]，还有景观位，需要我帮您预留吗？" |

### 3.5 礼宾服务场景 (Concierge)

#### 3.5.1 交通安排

**中文话术**

| 需求 | 话术 |
|------|------|
| **叫出租车** | "好的，我帮您叫车。预计[X]分钟后到酒店门口，车牌号[X]，我会在大堂提醒您。" |
| **网约车** | "需要我帮您叫滴滴/高德吗？目的地是哪里？我可以预估费用和到达时间。" |
| **接送机** | "机场接送商务车¥XXX，豪华轿车¥XXX，提前[X]小时预约。您的航班号是？我帮您安排。" |

#### 3.5.2 景点推荐

**中文话术**

| 场景 | 话术 |
|------|------|
| **首次询问** | "您是第一次来[城市]吗？打算玩几天？我可以推荐最合适的路线。" |
| **经典路线** | "[城市]必去的是[景点1][景点2][景点3]，建议[X]天行程。我可以帮您查门票和交通。" |
| **订票** | "[景点]门票¥XX，我可以代订，电子票直接发到您手机，扫码入园。" |

### 3.6 夜班特殊场景 (Night Shift)

#### 3.6.1 夜班问候

**中文话术**

| 时间 | 话术 |
|------|------|
| **22:00-00:00** | "晚上好！夜已深了，需要我帮您准备宵夜或明天叫醒服务吗？" |
| **00:00-02:00** | "您好，深夜时段，我是夜班管家。有任何需要请随时告诉我。" |
| **02:00-06:00** | "您好，凌晨时段。请问有什么紧急需要我协助的吗？" |

#### 3.6.2 应急处理

**中文话术**

| 场景 | 响应话术 | 处理话术 |
|------|---------|---------|
| **医疗急救** | "请保持冷静，我立即帮您联系急救中心并安排人员上楼。患者现在意识清醒吗？" | "救护车[X]分钟后到，我已经通知大堂准备引导。这是最近的医院信息。" |
| **物品遗失** | "别着急，告诉我大概在哪里遗失的，我立即联系相关部门寻找。" | "已经找到您的[物品]，在[位置]。现在送到房间还是您下来取？" |
| **噪音投诉** | "非常抱歉，我立即联系安保去处理。请问是楼上还是隔壁的噪音？" | "已经处理好了，安保会加强巡视。如果再有问题请立即叫我。" |
| **锁在门外** | "请稍等，我核实身份后立即帮您开门。请问房号和入住人姓名？" | "身份已核实，工程师傅马上上来开锁。请在大堂休息区稍等。" |

---

## 四、营销话术体系

### 4.1 升房销售 (Upsell)

#### 4.1.1 价值对比法

**中文话术**

```
"[姓氏]先生/女士，您订的基础房¥XXX/晚，我现在可以给您一个升级优惠：
- 升级到豪华房只需加¥XX/晚
- 多了10平米空间和浴缸
- 包含行政酒廊待遇（早餐+下午茶+Happy Hour）
- 单独买酒廊权益要¥XXX，升级只要¥XX

相当于花小钱享受大升级，您看要锁定吗？"
```

#### 4.1.2 场景植入法

**中文话术**

| 场景 | 话术 |
|------|------|
| **商务客** | "您明天有重要会议吧？升级行政房可以享用行政酒廊的安静环境处理工作，还有免费熨烫服务。" |
| **情侣** | "既然是特别的日子，要不要升级到景观房？可以看[景观]，还有欢迎香槟和花瓣布置。" |
| **家庭** | "带孩子的话，升级家庭房空间大很多，有儿童用品和加床，孩子住得更舒服。" |
| **长住** | "住[X]晚的话，升级套房更划算，有客厅可以办公会客，还有洗衣机可以洗衣服。" |

### 4.2 会员卡销售 (Membership)

#### 4.2.1 利益计算法

**中文话术**

```
"[姓氏]先生/女士，您这次房费¥XXX，办理我们的金卡会员只需¥XXX：
- 本次立即享受9折优惠，省¥XXX
- 全年免费早餐，价值¥XXX/次
- 房型升级权益，每次省¥XXX
- 延迟退房到14:00

住两次就回本，以后每次都有优惠。现在办理吗？"
```

### 4.3 增值服务销售 (Ancillary)

#### 4.3.1 早餐追加

**中文话术**

```
"您的房价不含早餐，单买是¥XX/位。
现在加¥XX可以升级含早，两位都含。
我们的早餐有[特色]，很多不住店的客人都专程来吃。
不吃早餐容易影响一天状态，要不要加上？"
```

---

## 五、危机处理话术

### 5.1 投诉处理 (Complaint Handling)

#### 5.1.1 HEARD原则话术

**中文**

| 步骤 | 话术 | 目的 |
|------|------|------|
| **Hear** | "非常感谢您告诉我们这个问题，我完全理解您的不满。" | 倾听 |
| **Empathize** | "这确实影响了您的入住体验，换作是我也会很生气。" | 共情 |
| **Apologize** | "对于给您造成的不便，我代表酒店真诚道歉。" | 道歉 |
| **Resolve** | "我现在就帮您解决，[具体方案]，您看这样可以吗？" | 解决 |
| **Diagnose** | "我会把这个情况反馈给[部门]，避免再次发生。" | 预防 |

---

## 六、AI管家特色话术

### 6.1 智能化提示

**中文话术**

| 场景 | 话术 |
|------|------|
| **主动关怀** | "检测到您房间温度较高，需要我帮您调低空调吗？" |
| **行程提醒** | "您的航班[X]小时后起飞，建议[X]分钟后出发，需要我帮您叫车吗？" |
| **习惯记忆** | "您上次入住时喜欢[偏好]，这次我提前为您准备好了。" |
| **异常提醒** | "您的房门[X]分钟未关好，请检查是否需要帮助。" |

### 6.2 人机协作话术

**中文话术**

| 场景 | 话术 |
|------|------|
| **转人工** | "这个问题比较复杂，我为您转接人工管家，请稍等..." |
| **无法解决** | "这个问题我暂时无法解决，已经通知前台工作人员，他们会在[X]分钟内联系您。" |
| **确认理解** | "我理解您想要[需求]，对吗？" |
| **重复确认** | "抱歉，我没听清楚，您能再说一遍吗？" |

---

## 七、话术使用指南

### 7.1 个性化变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `[酒店名]` | 酒店品牌名称 | "希尔顿酒店" |
| `[姓氏]` | 客户姓氏 | "张先生" |
| `[房型名称]` | 具体房型 | "豪华大床房" |
| `[XXX]` | 价格/时间等数字 | "¥399" |
| `[X]` | 数量 | "3晚" |

### 7.2 语气标记

| 标记 | 说明 | 使用场景 |
|------|------|---------|
| **热情上扬** | 语调稍高，充满热情 | 问候、欢迎 |
| **亲切自然** | 语调平稳，像朋友 | 日常对话 |
| **温暖关怀** | 语速稍慢，柔和 | 深夜、关怀 |
| **专业简洁** | 语速适中，干练 | 客房服务 |
| **诚恳道歉** | 语速放慢，低沉 | 投诉处理 |

### 7.3 禁忌话术

**禁止使用的表达**

| 禁忌 | 错误示例 | 正确替代 |
|------|---------|---------|
| **推卸责任** | "这不是我的问题" | "我帮您协调解决" |
| **否定客人** | "您说得不对" | "我理解您的感受" |
| **模糊承诺** | "马上就好" | "预计[X]分钟内完成" |
| **过度推销** | "您必须买这个" | "这个可能适合您" |
| **冷漠敷衍** | "没办法" | "我尽力帮您想办法" |

---

## 八、高端管家场景 (Luxury Butler Service)

### 8.1 管家服务层级体系

| 层级 | 定位 | 服务比例 | 核心差异 | 代表品牌 |
|------|------|---------|---------|---------|
| **基础管家** | 标准化服务 | 1:50 | 执行标准SOP | 中端连锁 |
| **行政管家** | 个性化服务 | 1:20 | 行政酒廊专属 | 万豪/希尔顿 |
| **白金管家** | VIP专属 | 1:10 | 全程陪同 | 丽思卡尔顿 |
| **私人管家** | 贴身服务 | 1:1或1:2 | 预判需求 | 安缦/四季 |
| **皇家管家** | 顶级定制 | 专属团队 | 全方位管理 | 文华东方/半岛 |

### 8.2 高端管家核心原则

#### 8.2.1 五大服务信条

| 信条 | 中文表达 | 英文表达 | 实操要点 |
|------|---------|---------|---------|
| **隐形服务** | "您在时我服务，您走时我整理" | "Anticipate without intruding" | 不主动打扰，但随时待命 |
| **记忆艺术** | "您的偏好，我已铭记" | "We remember what matters to you" | 记录所有细节，下次主动呈现 |
| **零拒绝** | "交给我来处理" | "Consider it done" | 不说"不"，只说"我来做" |
| **惊喜创造** | "为您准备了一份小惊喜" | "A little something for you" | 超预期，制造记忆点 |
| **情感连接** | "像家人一样照顾您" | "Like family, only better" | 建立长期情感纽带 |

#### 8.2.2 服务时机法则

| 时机 | 中文话术 | 英文话术 | 触发条件 |
|------|---------|---------|---------|
| **抵达前** | "一切已按您的喜好准备就绪" | "Everything is ready as you like it" | 入住前24小时 |
| **抵达时** | "欢迎回家" | "Welcome home" | 客人到店瞬间 |
| **在店中** | "有任何需要，我随时在" | "I'm here whenever you need" | 服务交付后 |
| **离店前** | "期待下次再见" | "We look forward to welcoming you back" | 退房前24小时 |
| **离店后** | "一路平安，期待重逢" | "Safe travels, until we meet again" | 客人离开后 |

---

### 8.3 国际酒店集团话术标准

#### 8.3.1 丽思卡尔顿 (Ritz-Carlton)

**品牌哲学**: "我们以绅士淑女的态度为绅士淑女们忠诚服务"  
**Service Philosophy**: "We are Ladies and Gentlemen serving Ladies and Gentlemen"

**核心话术**

| 场景 | 中文话术 | English Script | 语气 |
|------|---------|----------------|------|
| **首次问候** | "[姓氏]先生/女士，欢迎来到丽思卡尔顿。我是您的专职管家[姓名]，很荣幸为您服务。" | "Mr./Ms. [Name], welcome to The Ritz-Carlton. I am [Name], your dedicated butler. It is my privilege to serve you." | 优雅庄重 |
| **服务承诺** | "请允许我照顾好您的一切。无论您需要什么，都请告诉我。" | "Please allow me to take care of everything for you. Whatever you need, simply let me know." | 自信从容 |
| **解决问题** | "交给我来处理，我会确保让您满意。" | "Leave it with me. I will ensure your complete satisfaction." | 坚定可靠 |
| **创造惊喜** | "我为您准备了一份特别的欢迎礼，希望您喜欢。" | "I have prepared a special welcome gift for you. I hope you enjoy it." | 温暖惊喜 |
| **告别** | "感谢您选择丽思卡尔顿。期待再次为您服务。" | "Thank you for choosing The Ritz-Carlton. We look forward to serving you again." | 优雅告别 |

**丽思卡尔顿服务金句**

```
"在丽思卡尔顿，没有'不'这个字。"
"In The Ritz-Carlton, there is no 'no'."

"我们不只是满足期望，我们创造惊喜。"
"We don't just meet expectations, we create memories."

"您只需提出要求，其余的交给我们。"
"You name it, we make it happen."
```

---

#### 8.3.2 安缦 (Aman)

**品牌哲学**: "宁静、私密、融入自然"  
**Service Philosophy**: "Peace, privacy, and connection with nature"

**核心话术**

| 场景 | 中文话术 | English Script | 语气 |
|------|---------|----------------|------|
| **抵达** | "欢迎来到安缦。在这里，时间属于您自己。" | "Welcome to Aman. Here, time belongs to you." | 宁静平和 |
| **介绍** | "我是您的管家[姓名]。我不打扰您，但我会一直在附近。" | "I am [Name], your butler. I won't disturb you, but I will always be nearby." | 低存在感的关怀 |
| **关怀** | "请告诉我，怎样才能让您的停留更加宁静？" | "Please tell me, how can I make your stay more peaceful?" | 细腻体贴 |
| **隐私保护** | "您的隐私是我们的首要考量。请放心，一切都会被妥善处理。" | "Your privacy is our highest priority. Rest assured, everything will be handled discreetly." | 严谨专业 |
| **告别** | "愿您带着内心的平静离开，期待与您再次相遇。" | "May you leave with peace in your heart. We look forward to meeting again." | 禅意深远 |

**安缦服务特色**

```
"我们不提供服务，我们创造宁静。"
"We don't provide service, we create tranquility."

"在安缦，您不是客人，您是家人。"
"At Aman, you are not a guest, you are family."

"请允许我消失，让我通过服务证明我的存在。"
"Allow me to disappear, let my service prove my presence."
```

---

#### 8.3.3 四季酒店 (Four Seasons)

**品牌哲学**: "待人如己"  
**Service Philosophy**: "Treat others as you would wish to be treated"

**核心话术**

| 场景 | 中文话术 | English Script | 语气 |
|------|---------|----------------|------|
| **问候** | "欢迎来到四季酒店。我是[姓名]，今天由我来照顾您。" | "Welcome to Four Seasons. I'm [Name], and I'll be taking care of you today." | 温暖友好 |
| **了解需求** | "请告诉我，您理想中的入住体验是什么样的？" | "Tell me, what does your ideal stay look like?" | 主动探询 |
| **提供服务** | "让我来帮您安排，确保一切都如您所愿。" | "Let me arrange that for you, ensuring everything is exactly as you wish." | 贴心周到 |
| **关怀** | "我看到您今天有些疲惫。需要我为您准备些热茶吗？" | "I notice you seem tired today. May I prepare some hot tea for you?" | 细腻观察 |
| **告别** | "感谢您选择四季。我们会想念您的。" | "Thank you for choosing Four Seasons. We will miss you." | 真诚温暖 |

**四季服务准则**

```
"我们如何对待家人，就如何对待客人。"
"How we treat family is how we treat our guests."

"每一个客人都独一无二，每一次服务都量身定制。"
"Every guest is unique, every service is customized."

"预测需求，在客人开口之前。"
"Anticipate needs before they are spoken."
```

---

#### 8.3.4 文华东方 (Mandarin Oriental)

**品牌哲学**: "东方传奇，西方服务"  
**Service Philosophy**: "Legendary Oriental hospitality with Western service standards"

**核心话术**

| 场景 | 中文话术 | English Script | 语气 |
|------|---------|----------------|------|
| **欢迎** | "欢迎莅临文华东方。扇子是我们的象征，代表着东方的优雅与关怀。" | "Welcome to Mandarin Oriental. The fan is our symbol, representing Oriental elegance and care." | 东方典雅 |
| **服务介绍** | "我是您的管家[姓名]。我们将以东方传统款待您，同时提供国际标准的服务。" | "I am [Name], your butler. We will treat you with Oriental traditions while delivering international standards." | 融合东西方 |
| **文化体验** | "今晚我们为您准备了一场茶艺表演，希望您能感受到东方的魅力。" | "Tonight we have prepared a tea ceremony for you, hoping you will feel the charm of the Orient." | 文化传播 |
| **健康关怀** | "我们的水疗中心融合东方养生智慧，也许能让您恢复活力。" | "Our spa combines Oriental wellness wisdom, perhaps it can rejuvenate you." | 健康导向 |
| **告别** | "愿这把扇子为您带来好运。期待再次为您服务。" | "May this fan bring you good fortune. We look forward to serving you again." | 东方祝福 |

---

#### 8.3.5 半岛酒店 (The Peninsula)

**品牌哲学**: "传承、经典、超越期望"  
**Service Philosophy**: "Heritage, classic excellence, exceeding expectations"

**核心话术**

| 场景 | 中文话术 | English Script | 语气 |
|------|---------|----------------|------|
| **欢迎** | "欢迎来到半岛酒店。自1928年以来，我们一直致力于为尊贵的客人提供卓越服务。" | "Welcome to The Peninsula. Since 1928, we have been dedicated to providing exceptional service to distinguished guests." | 历史传承 |
| **劳斯莱斯接送** | "您的劳斯莱斯接送服务已准备就绪。请允许我护送您上车。" | "Your Rolls-Royce transfer is ready. Please allow me to escort you to the vehicle." | 尊贵奢华 |
| **直升机服务** | "如果您需要，我们可以安排直升机接送，俯瞰城市美景。" | "If you wish, we can arrange helicopter transfer with a bird's-eye view of the city." | 极致体验 |
| **私人定制** | "请告诉我您的特殊需求，半岛的传承就是为您创造不可能。" | "Tell me your special requirements. The Peninsula's heritage is to make the impossible possible." | 传承承诺 |
| **告别** | "感谢您选择半岛。我们期待在未来继续为您服务，创造更多传奇。" | "Thank you for choosing The Peninsula. We look forward to continuing to serve you and create more legends." | 传奇延续 |

#### 8.3.6 悦榕庄 (Banyan Tree)

**品牌哲学**: "浪漫度假的感官圣殿"  
**Service Philosophy**: "Sanctuary for the senses"

**核心话术**

| 场景 | 中文话术 | English Script | 语气 |
|------|---------|----------------|------|
| **欢迎** | "欢迎来到悦榕庄。在这里，您将找到内心的宁静与浪漫的庇护。" | "Welcome to Banyan Tree. Here, you will find sanctuary for inner peace and romance." | 浪漫温柔 |
| **SPA介绍** | "我们的SPA融合了东方养生智慧，使用天然草本，将为您带来身心灵的深度疗愈。" | "Our spa blends Oriental wellness wisdom with natural herbs, offering deep healing for body, mind, and spirit." | 疗愈舒缓 |
| **浪漫安排** | "为您和伴侣，我们准备了私人泳池别墅、烛光晚餐和花瓣浴。愿您的每一刻都充满爱意。" | "For you and your partner, we have prepared a private pool villa, candlelit dinner, and flower petal bath. May every moment be filled with love." | 浪漫甜蜜 |
| **自然连接** | "清晨的瑜伽课将在海边进行，让海浪声唤醒您的身体。" | "Morning yoga will be held by the sea, letting the waves awaken your body." | 自然和谐 |
| **告别** | "愿悦榕庄成为您心中永恒的浪漫记忆。期待与您再次相遇。" | "May Banyan Tree become an eternal romantic memory in your heart. We look forward to meeting again." | 深情浪漫 |

**悦榕庄特色金句**

```
"在悦榕庄，时间是用来浪费在美好事物上的。"
"At Banyan Tree, time is meant to be wasted on beautiful things."

"我们不只是提供住宿，我们创造感官的庇护所。"
"We don't just provide accommodation, we create sanctuaries for the senses."

"让每一次呼吸都充满热带花园的芬芳。"
"Let every breath be filled with the fragrance of tropical gardens."
```

---

#### 8.3.7 虹夕诺雅 (Hoshinoya)

**品牌哲学**: "非日常的度假"  
**Service Philosophy**: "Non-daily life experience"

**核心话术**

| 场景 | 中文话术 | English Script | 语气 |
|------|---------|----------------|------|
| **抵达** | "欢迎来到虹夕诺雅。请忘记时间的流逝，沉浸在日本传统美学的非日常之中。" | "Welcome to Hoshinoya. Please forget the passage of time and immerse yourself in the non-daily life of Japanese traditional aesthetics." | 禅意优雅 |
| **和服体验** | "请允许我为您穿上和服，体验日本传统服饰之美。每一步都是与历史的对话。" | "Please allow me to dress you in a kimono, experiencing the beauty of traditional Japanese attire. Each step is a conversation with history." | 文化传承 |
| **怀石料理** | "今晚的怀石料理，主厨将用当季食材为您呈现四季流转之美。每一道菜都是一幅画。" | "Tonight's kaiseki cuisine will present the beauty of changing seasons with seasonal ingredients. Each dish is a painting." | 艺术赞美 |
| **温泉介绍** | "我们的温泉源自[地名]，富含矿物质。请闭上眼睛，让温泉带走您所有的疲惫。" | "Our onsen springs from [location], rich in minerals. Close your eyes and let the hot springs wash away all your fatigue." | 疗愈放松 |
| **告别** | "希望这段非日常的时光，能成为您日常生活中的珍贵回忆。" | "May this non-daily experience become a precious memory in your daily life." | 诗意告别 |

**虹夕诺雅特色金句**

```
"虹夕诺雅不是酒店，而是一段被遗忘的时光。"
"Hoshinoya is not a hotel, but a forgotten passage of time."

"在这里，您不是客人，而是日本传统美学的体验者。"
"Here, you are not a guest, but an experiencer of Japanese traditional aesthetics."

"请忘记时钟的存在，让自然告诉您时间。"
"Please forget the existence of clocks, let nature tell you the time."
```

---

#### 8.3.8 嘉佩乐 (Capella)

**品牌哲学**: "策划师式个性化服务"  
**Service Philosophy**: "Curator-style personalized service"

**核心话术**

| 场景 | 中文话术 | English Script | 语气 |
|------|---------|----------------|------|
| **欢迎** | "欢迎来到嘉佩乐。我是您的策划师[姓名]，将为您量身定制这段旅程的每一个细节。" | "Welcome to Capella. I am your curator [Name], here to customize every detail of your journey." | 专业个性化 |
| **需求探询** | "在嘉佩乐，没有标准答案。请告诉我，您的理想假期是什么样的？我将为您实现。" | "At Capella, there are no standard answers. Tell me, what does your ideal holiday look like? I will make it happen." | 深度探询 |
| **文化体验** | "明天我为您安排了一次私人文化之旅，有专家带您深入探索这座城市的隐藏故事。" | "Tomorrow I have arranged a private cultural journey for you, with an expert to explore the hidden stories of this city." | 文化深度 |
| **惊喜策划** | "我注意到您对[兴趣]情有独钟。我为您准备了一个特别体验，希望能让您惊喜。" | "I noticed your passion for [interest]. I have prepared a special experience for you, hoping to delight you." | 惊喜预告 |
| **告别** | "感谢您让我参与策划这段旅程。期待成为您下一次冒险的策划师。" | "Thank you for letting me curate this journey. I look forward to being the curator of your next adventure." | 策划师身份 |

**嘉佩乐特色金句**

```
"嘉佩乐没有客人，只有被理解的故事。"
"Capella has no guests, only stories to be understood."

"我们的服务不是标准化，而是为您一人定制。"
"Our service is not standardized, but customized for you alone."

"让我做您这段旅程的策划师，您只需享受。"
"Let me be the curator of your journey, you just enjoy."
```

---

#### 8.3.9 阿丽拉 (Alila)

**品牌哲学**: "惊喜、可持续、在地体验"  
**Service Philosophy**: "Surprisingly different, sustainable, authentic experience"

**核心话术**

| 场景 | 中文话术 | English Script | 语气 |
|------|---------|----------------|------|
| **欢迎** | "欢迎来到阿丽拉。在这里，您将发现不一样的惊喜，体验最真实的当地文化。" | "Welcome to Alila. Here, you will discover surprisingly different experiences and authentic local culture." | 惊喜预告 |
| **可持续发展** | "阿丽拉致力于可持续发展，我们的建筑使用本地材料，每一砖一瓦都与自然和谐共生。" | "Alila is committed to sustainability. Our buildings use local materials, each brick coexisting harmoniously with nature." | 环保责任 |
| **在地体验** | "我为您安排了一次[当地活动]，由本地村民带领。这将是一次真正融入当地生活的体验。" | "I have arranged a [local activity] for you, led by local villagers. This will be a true immersion into local life." | 在地连接 |
| **无边界泳池** | "我们的无边泳池仿佛与[自然景观]融为一体，请尽情享受这份与自然的亲密。" | "Our infinity pool seems to blend with [natural landscape]. Please enjoy this intimacy with nature." | 自然亲密 |
| **告别** | "希望阿丽拉带给您的不仅是住宿，更是一次改变视角的旅程。期待再次为您创造惊喜。" | "May Alila bring you not just accommodation, but a journey that changes perspectives. We look forward to surprising you again." | 改变视角 |

**阿丽拉特色金句**

```
"阿丽拉的惊喜，在于发现不一样的自己。"
"Alila's surprise lies in discovering a different you."

"我们不只是保护自然，我们与它共舞。"
"We don't just protect nature, we dance with it."

"真正的奢华，是与当地文化的真实连接。"
"True luxury is authentic connection with local culture."
```

---

#### 8.3.10 六善 (Six Senses)

**品牌哲学**: "Reconnect with yourself, others, and the world"  
**Service Philosophy**: "Reconnect with yourself, others, and the world"

**核心话术**

| 场景 | 中文话术 | English Script | 语气 |
|------|---------|----------------|------|
| **欢迎** | "欢迎来到六善。在这里，您将重新连接自己、他人和这个世界。" | "Welcome to Six Senses. Here, you will reconnect with yourself, others, and the world." | 回归本真 |
| **Wellness介绍** | "我们的养生项目将帮助您从睡眠、饮食、运动、spa四个方面全面提升生活品质。" | "Our wellness programs will help you enhance life quality through sleep, nutrition, movement, and spa." | 健康专业 |
| **睡眠仪式** | "今晚为您准备了薰衣草枕喷雾和助眠茶。愿您拥有一个深度睡眠的夜晚。" | "Tonight I have prepared lavender pillow mist and sleep tea for you. May you have a night of deep sleep." | 睡眠关怀 |
| **农场体验** | "我们的有机农场种植的蔬菜将出现在您的餐桌上。明天带您去看看这些食材的生长地？" | "Vegetables from our organic farm will appear on your table. Shall I show you where these ingredients grow tomorrow?" | 从农场到餐桌 |
| **告别** | "希望六善让您重新发现了生活的美好，以及与自己的连接。期待再次相见。" | "May Six Senses help you rediscover the beauty of life and connection with yourself. We look forward to seeing you again." | 深度连接 |

**六善特色金句**

```
"六善不是酒店，而是一次重新连接自己的旅程。"
"Six Senses is not a hotel, but a journey to reconnect with yourself."

"在这里，您会重新学会如何呼吸、如何睡眠、如何生活。"
"Here, you will relearn how to breathe, how to sleep, how to live."

"真正的奢华，是找回内心的平静。"
"True luxury is finding inner peace."
```

---

#### 8.3.11 安麓 (Ahn Luh)

**品牌哲学**: "中国美学、文化传承、隐逸生活"  
**Service Philosophy**: "Chinese aesthetics, cultural heritage, hermit life"

**核心话术**

| 场景 | 中文话术 | English Script | 语气 |
|------|---------|----------------|------|
| **欢迎** | "欢迎来到安麓。在这里，您将体验真正的中国美学，感受千年文化的沉淀。" | "Welcome to Ahn Luh. Here, you will experience true Chinese aesthetics and feel the sediment of thousand-year culture." | 东方典雅 |
| **中式建筑** | "这座建筑由[大师姓名]设计，每一处细节都体现了中国传统建筑的智慧与美学。" | "This building was designed by [Master Name], with every detail reflecting the wisdom and aesthetics of traditional Chinese architecture." | 文化讲解 |
| **茶道体验** | "请允许我为您奉上一杯中国茶。茶道不仅是饮茶，更是一种修身养性的生活方式。" | "Please allow me to serve you a cup of Chinese tea. Tea ceremony is not just drinking tea, but a lifestyle of self-cultivation." | 文化沉浸 |
| **书法体验** | "我们邀请了书法大师，可以教您书写汉字。一笔一画，都是与古人对话。" | "We have invited a calligraphy master to teach you Chinese characters. Each stroke is a conversation with ancients." | 艺术传承 |
| **告别** | "愿安麓成为您心中的隐逸之所，期待您再次回到这片中国美学的净土。" | "May Ahn Luh become your hermit sanctuary in heart. We look forward to your return to this pure land of Chinese aesthetics." | 东方诗意 |

**安麓特色金句**

```
"安麓不是酒店，而是中国美学的当代呈现。"
"Ahn Luh is not a hotel, but a contemporary presentation of Chinese aesthetics."

"在这里，您会明白什么是'大隐隐于市'。"
"Here, you will understand what 'a great hermit hides in the city' means."

"每一次呼吸，都是与中国文化的对话。"
"Every breath is a conversation with Chinese culture."
```

---

#### 8.3.12 范思哲酒店 (Palazzo Versace)

**品牌哲学**: "时尚与奢华的完美融合"  
**Service Philosophy**: "Where fashion meets luxury"

**核心话术**

| 场景 | 中文话术 | English Script | 语气 |
|------|---------|----------------|------|
| **欢迎** | "欢迎来到范思哲酒店。在这里，您将体验意大利时尚的极致奢华。" | "Welcome to Palazzo Versace. Here, you will experience the ultimate Italian fashion luxury." | 时尚奢华 |
| **品牌介绍** | "从家具到餐具，每一件都是范思哲原创设计。您正生活在一件艺术品之中。" | "From furniture to tableware, every piece is original Versace design. You are living inside a work of art." | 艺术沉浸 |
| **时尚购物** | "我们的精品店有最新季的范思哲成衣和配饰。需要我为您安排私人购物顾问吗？" | "Our boutique has the latest season Versace ready-to-wear and accessories. Shall I arrange a personal shopping consultant for you?" | 时尚服务 |
| **泳池体验** | "我们的泳池铺满了马赛克图案，是范思哲经典设计。请享受这份独特的时尚体验。" | "Our pool is covered in mosaic patterns, a Versace classic design. Please enjoy this unique fashion experience." | 设计赞美 |
| **告别** | "感谢您选择范思哲。愿您的每一天都像范思哲一样璀璨夺目。" | "Thank you for choosing Versace. May your every day be as dazzling as Versace." | 璀璨祝福 |

**范思哲特色金句**

```
"在范思哲酒店，您不只是客人，您是时尚icon。"
"At Palazzo Versace, you are not just a guest, you are a fashion icon."

"奢华不是标签，而是您生活的常态。"
"Luxury is not a label, but the norm of your life."

"让每一天都成为您的T台。"
"Make every day your runway."
```

---

#### 8.3.13 W酒店 (W Hotels)

**品牌哲学**: "潮流生活方式、设计、音乐"  
**Service Philosophy**: "Whatever/Whenever, lifestyle, design, music"

**核心话术**

| 场景 | 中文话术 | English Script | 语气 |
|------|---------|----------------|------|
| **欢迎** | "欢迎来到W酒店！这里是潮流的聚集地，准备好开启一场精彩之旅了吗？" | "Welcome to W Hotels! This is where trends gather. Ready to start an amazing journey?" | 活力四射 |
| **Whatever/Whenever** | "在W，我们信奉'无论何时何事'。只要您想，我们就能做到。说吧，您想要什么？" | "At W, we believe in 'Whatever/Whenever'. If you want it, we can make it happen. Tell me, what do you want?" | 随叫随到 |
| **酒吧推荐** | "今晚WOOBAR有DJ现场，是城里最潮的夜生活聚集地。要我来帮您订最好的位置吗？" | "Tonight WOOBAR has a live DJ, the hottest nightlife spot in town. Shall I book you the best spot?" | 潮流夜生活 |
| **设计导览** | "我们酒店的设计由[设计师]操刀，每个角落都是Instagram-worthy的打卡点。要我带您去最出片的地方吗？" | "Our hotel is designed by [Designer], every corner is Instagram-worthy. Shall I show you the most photogenic spots?" | 社交传播 |
| **告别** | "下次来W，记得带更多故事！随时回来，我们永远在这里等您！" | "Next time you come to W, bring more stories! Come back anytime, we'll always be here waiting for you!" | 活力告别 |

**W酒店特色金句**

```
"W不是酒店，而是一个24/7的派对。"
"W is not a hotel, but a 24/7 party."

"在这里，潮流不是跟随，而是创造。"
"Here, trends are not followed, but created."

"无论何时何事，我们搞定一切。"
"Whatever, Whenever, we handle everything."
```

---

### 8.4 高端场景专属话术

#### 8.4.1 私人定制服务

**中文话术**

| 场景 | 话术 |
|------|------|
| **抵达前调查** | "为了给您提供最贴心的服务，我想了解几个偏好：您喜欢什么类型的枕头？有什么饮食禁忌吗？有什么特别的日子要庆祝吗？" |
| **欢迎礼定制** | "根据您的喜好，我为您准备了[具体礼物]。希望这份小小的心意能让您感到温暖。" |
| **行程规划** | "您明日的行程我已了解。我建议[X]点出发，可以避开高峰。需要我为您准备路上的饮品和小食吗？" |
| **专属体验** | "今晚餐厅主厨为您准备了私人晚宴，菜单是根据您的口味定制的。需要我为您安排吗？" |
| **惊喜策划** | "了解到明天是您[特殊日子]，我为您准备了一份惊喜。具体是什么，请允许我暂时保密。" |

**English Scripts**

| Scenario | Script |
|----------|--------|
| **Pre-arrival Survey** | "To provide you with the most thoughtful service, I'd like to know a few preferences: What type of pillow do you prefer? Any dietary restrictions? Any special occasions to celebrate?" |
| **Welcome Gift** | "Based on your preferences, I've prepared [specific gift]. I hope this small gesture warms your heart." |
| **Itinerary Planning** | "I understand your schedule for tomorrow. I suggest departing at [X] to avoid peak hours. Shall I prepare drinks and snacks for the journey?" |
| **Exclusive Experience** | "Tonight, our chef has prepared a private dinner with a menu customized to your taste. Shall I arrange it for you?" |
| **Surprise Planning** | "Learning that tomorrow is your [special occasion], I've prepared a surprise. Please allow me to keep it a secret for now." |

#### 8.4.2 奢华体验话术

| 体验类型 | 中文话术 | 英文话术 |
|---------|---------|---------|
| **直升机接送** | "直升机已在楼顶停机坪就绪，15分钟后可起飞。飞行员已了解您的目的地。" | "The helicopter is ready on the rooftop helipad, departing in 15 minutes. The pilot has been briefed on your destination." |
| **游艇出海** | "您的私人游艇已在码头准备就绪，船长和船员随时待命。香槟和海鲜已备好。" | "Your private yacht is ready at the marina, captain and crew standing by. Champagne and seafood are prepared." |
| **私人飞机** | "湾流G650已准备就绪，乘务员已了解您的饮食偏好。预计[X]小时后抵达目的地。" | "The Gulfstream G650 is ready. Cabin crew has been briefed on your dietary preferences. ETA at destination is [X] hours." |
| **米其林主厨** | "[主厨姓名]今晚将专程为您烹饪，菜单根据您的口味定制。用餐地点可选在您房间或私人餐厅。" | "Chef [Name] will cook exclusively for you tonight, with a menu customized to your taste. Dining location can be your room or private dining room." |
| **名表珠宝** | "我们与[品牌]有合作，可以为您安排私人鉴赏会，由品牌总监亲自介绍。" | "We have partnerships with [Brand] and can arrange a private viewing, personally hosted by the brand director." |

#### 8.4.3 敏感场景话术

| 场景 | 中文话术 | 英文话术 |
|------|---------|---------|
| ** celebrity隐私** | "您的隐私是我们的首要承诺。所有员工已签署保密协议，请放心。" | "Your privacy is our paramount commitment. All staff have signed confidentiality agreements. Please rest assured." |
| **贵重物品** | "您的[物品]已安全存入酒店保险箱。需要时请联系我，我会亲自陪同您取用。" | "Your [item] is safely stored in the hotel vault. Contact me when needed, and I will personally escort you." |
| **安全护送** | "我已安排专业安保团队，从酒店到目的地的全程护送已确认。" | "I've arranged a professional security team. Full escort from hotel to destination is confirmed." |
| **医疗保密** | "医生和医疗设备已 discreetly 安排到位。所有信息将严格保密。" | "Doctor and medical equipment have been discreetly arranged. All information will be strictly confidential." |

---

### 8.5 高端管家与AI融合

#### 8.5.1 AI辅助预判

| 预判场景 | AI触发 | 管家话术 |
|---------|--------|---------|
| **航班延误** | 监测到航班动态 | "我注意到您的航班延误了。我已为您延长退房时间，并安排了休息室。" |
| **天气变化** | 天气预报预警 | "明天有雨，我已为您准备了雨伞，并在房间放置了姜茶材料。" |
| **生日提醒** | 客户档案数据 | "明天是您的生日，我们为您准备了蛋糕和香槟，还有一份特别礼物。" |
| **偏好复现** | 历史数据分析 | "您上次喜欢[某物品]，这次我已提前为您准备好。" |

#### 8.5.2 人机协作升级

```
【场景】VIP客人深夜抵达，AI管家+人工管家协作

AI管家 (第一时间响应):
"欢迎回家，[姓氏]先生/女士。我是您的AI管家，检测到您已抵达。
您的房间已按偏好调好温度[X]度，枕头是[类型]，欢迎饮品已备好。
人工管家[姓名]将在2分钟内与您联系，有任何需要请随时叫我。"

人工管家 (2分钟后):
"[姓氏]先生/女士，我是您的专属管家[姓名]。
我已经在门口等候，请允许我带您到房间，并为您介绍今晚的特别安排。"
```

---

## 九、国际酒店集团服务标准对比

### 9.1 服务特色矩阵

| 集团 | 核心特色 | 代表话术关键词 | 服务速度 | 个性化程度 |
|------|---------|--------------|---------|-----------|
| **丽思卡尔顿** | 极致奢华、绅士淑女 | "荣幸"、"忠诚服务" | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **安缦** | 宁静私密、融入自然 | "时间属于您"、"宁静" | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **四季** | 温暖如家、待人如己 | "像家人"、"量身定制" | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **文华东方** | 东方智慧、扇形标志 | "东方"、"扇子"、"养生" | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **半岛** | 历史传承、经典奢华 | "传承"、"1928"、"传奇" | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **华尔道夫** | 美国经典、奢华典范 | "经典"、"卓越" | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **瑰丽** | 住宅式奢华、艺术氛围 | "像家一样"、"艺术" | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **宝格丽** | 意式奢华、珠宝基因 | "意式"、"璀璨" | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **悦榕庄** | 浪漫度假、亚洲风情 | "浪漫"、"SPA"、"庇护所" | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **虹夕诺雅** | 日式美学、传统文化 | "非日常"、"款待" | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **嘉佩乐** | 个性化服务、文化遗产 | "策划师"、"文化" | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **阿丽拉** | 环保可持续、在地体验 | "惊喜"、"可持续" | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **六善** | Wellness、可持续发展 | " reconnect"、"自然" | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **安麓** | 中式奢华、文化传承 | "中国美学"、"隐逸" | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **范思哲** | 意式时尚、品牌基因 | "时尚"、"奢华" | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **W酒店** | 潮流生活方式、设计 | "潮流"、"活力" | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

### 9.2 各集团管家服务SOP差异

| 环节 | 丽思卡尔顿 | 安缦 | 四季 | 半岛 |
|------|-----------|------|------|------|
| **抵达前** | 24小时确认所有偏好 | 确认客人是否需要"数字排毒" | 发送个性化欢迎邮件 | 确认劳斯莱斯/直升机安排 |
| **入住时** | 总经理亲自迎接重要客人 | 不打扰，仅在最需要时出现 | 详细介绍所有设施 | 历史传承讲解+劳斯莱斯接送 |
| **在店中** | 每4小时主动关怀 | 隐形服务，从不主动打扰 | 像家人一样自然交流 | 随时待命，极速响应 |
| **离店前** | 总经理送别+礼物 | 禅意告别，祝福内心平静 | 真诚道别，表达想念 | 期待续写传奇 |
| **离店后** | 手写感谢信 | 保持沉默，等待下次相遇 | 发送满意度调查+关怀邮件 | 寄送纪念礼品 |

---

## 附录: 快速查询表

| 场景 | 短句 |
|------|------|
| 感谢 | "非常感谢" / "谢谢您" / "感谢您的理解" |
| 道歉 | "非常抱歉" / "对不起" / "请谅解" |
| 确认 | "好的" / "明白了" / "马上处理" |
| 等待 | "请稍等" / "马上就好" / "请耐心等候" |
| 告别 | "祝您入住愉快" / "再见" / "有问题随时找我" |

### B. 数字表达

| 场景 | 标准说法 |
|------|---------|
| 时间 | "预计[X]分钟" / "大约[X]小时" |
| 价格 | "原价¥XXX，现价¥XXX" / "只需加¥XX" |
| 数量 | "还剩[X]间" / "第[X]次" |
| 楼层 | "[X]楼" / "[X]层" |

---

*文档结束*

---

## 版本更新日志

### V1.1 (2026-03-03)
**新增内容**:
- 高端管家场景完整模块（8章）
- 国际酒店集团话术标准（13大品牌）
- 奢华品牌：悦榕庄、虹夕诺雅、嘉佩乐、阿丽拉、六善、安麓、范思哲、W酒店
- 高端场景专属话术（私人定制、奢华体验、敏感场景）
- AI与人工管家协作SOP
- 国际集团服务标准对比矩阵

**覆盖品牌**:
国内/亚太: 安麓、悦榕庄、虹夕诺雅、阿丽拉、六善、嘉佩乐、文华东方、半岛
欧美: 丽思卡尔顿、四季、华尔道夫、瑰丽、宝格丽、范思哲、W酒店、安缦

### V1.0 (2026-03-03)
**基础内容**:
- 话术体系总览与核心原则
- 标准问候话术（中英双语）
- 6大核心场景话术（预订/入住/客房/餐饮/礼宾/夜班）
- 营销话术体系（升房/会员/增值服务）
- 危机处理话术（HEARD原则）
- AI管家特色话术
- 话术使用指南与禁忌

---

**维护说明**: 
- 本话术库应定期根据实际使用数据优化
- 建议每季度更新一次
- 根据转化率数据淘汰低效话术，补充高效话术
- 新增品牌话术需提供该品牌完整SOP文档后方可加入


---

## 🔗 相关笔记

- [[AHL 平台 MOC]]
- [[战略-方法论 MOC]]
- [[B166ER 知识库 MOC]]

*该区块由 B166ER 自动注入 (2026-07-28) — 关键词匹配*
