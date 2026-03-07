# SKILL-PRD-006: RFP智能应答 (RFP Auto-Response)

## 基本信息

| 字段 | 内容 |
|------|------|
**SKILL编号** | GRW-019
**SKILL名称** | RFP智能应答 (RFP Auto-Response)
**所属AGENT** | 营销增长AGENT (Growth Agent)
**版本** | v1.0
**创建日期** | 2026-03-04
**优先级** | P0 (MICE销售核心)
**开发周期** | 4-6周

---

## 1. 价值定位

### 1.1 解决的问题
酒店MICE销售处理RFP(Request for Proposal)面临严峻挑战：

**响应速度慢**
- 客户要求48-72小时回复，销售团队加班加点
- 复杂的RFP需要跨部门协作，协调耗时
- 紧急RFP错过截止时间，直接出局

**响应质量参差**
- 不同销售撰写的方案水平差异大
- 关键信息遗漏，专业性不足
- 缺乏针对性，千篇一律"套模板"

**知识难以沉淀**
- 优秀销售的方案经验无法复制
- 历史方案散落各处，无法复用
- 新人上手慢，培养周期长

### 1.2 核心价值
**"让销售从'写手'变为'策略师'，AI 30分钟生成专业方案"**

- **极速响应**：AI 30分钟生成初稿，销售专注策略优化
- **质量保证**：基于最佳实践模板，专业度统一高标准
- **个性定制**：深度理解客户需求，千人千面定制方案
- **知识沉淀**：每一次响应都是学习，方案库持续进化

### 1.3 量化收益

| 指标 | 传统模式 | AI智能应答 | 提升幅度 |
|------|---------|-----------|---------|
方案撰写时间 | 8-16小时 | 30-60分钟 | **缩短90%** |
响应速度 | 2-3天 | 当天响应 | **提升3倍** |
中标率 | 15-20% | 25-35% | **提升75%** |
销售人效 | 基准值 | +300% | **提升3倍** |
客户满意度 | 70% | 90% | **提升29%** |

---

## 2. 目标用户

### 2.1 主要用户

| 用户角色 | 使用场景 | 核心痛点 |
|---------|---------|---------|
**MICE销售经理** | 收到客户RFP，需要快速生成方案 | 时间紧、任务重，写方案到凌晨 |
**宴会销售总监** | 审核销售提交的方案，把控质量 | 方案质量参差不齐，审核耗时 |
**收益经理** | 提供定价建议，评估风险 | 定价策略复杂，RFP要求多样 |
**餐饮/宴会经理** | 提供菜单/场地等专业内容 | 反复沟通需求，信息传递失真 |

### 2.2 用户画像

**典型用户：刘经理，35岁，会议酒店MICE销售经理**
- 手上同时跟进5-6个RFP，每个都要写几十页方案
- 上周为了赶一个紧急RFP，加班到凌晨2点
- 很多RFP的问题都差不多，但每次都重新写
- 希望能有个工具帮他快速生成初稿，他只需要修改优化

---

## 3. 功能架构

### 3.1 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    应用层                                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ RFP解析器   │ │ 方案生成器   │ │ 方案编辑器   │            │
│  │ (NLP)       │ │ (AIGC)      │ │ (协同编辑)   │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                    AI处理层 (核心)                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 意图理解    │ │ 知识检索    │ │ 内容生成    │            │
│  │ (DeepSeek)  │ │ (RAG)       │ │ (GPT-4o)    │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐                            │
│  │ 定价计算    │ │ 方案优化    │                            │
│  │ (规则引擎)  │ │ (强化学习)  │                            │
│  └─────────────┘ └─────────────┘                            │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                    知识库层                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 方案模板库   │ │ 案例库      │ │ 价格库      │            │
│  │ (结构化)     │ │ (中标案例)  │ │ (动态定价)  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐                            │
│  │ 菜品库      │ │ 场地库      │                            │
│  │ (图文)      │ │ (3D/VR)     │                            │
│  └─────────────┘ └─────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 核心功能模块

#### 模块1: RFP智能解析

**支持格式**
- PDF文件 (扫描件需OCR)
- Word文档 (.doc/.docx)
- Excel表格 (.xls/.xlsx)
- 邮件正文
- 在线表单

**解析内容**
```python
class RFPParser:
    """RFP文档智能解析"""
    
    def parse(self, document):
        """解析RFP文档，提取关键信息"""
        
        parsed_data = {
            # 客户信息
            'client': {
                'company_name': self.extract_company_name(),
                'industry': self.extract_industry(),
                'contact_person': self.extract_contact(),
                'contact_info': self.extract_contact_info()
            },
            
            # 活动信息
            'event': {
                'event_type': self.extract_event_type(),  # 会议/宴会/婚礼等
                'event_name': self.extract_event_name(),
                'date': self.extract_event_date(),
                'duration': self.extract_duration(),
                'participants': self.extract_participant_count(),
                'budget_range': self.extract_budget()
            },
            
            # 场地需求
            'venue_requirements': {
                'meeting_rooms': self.extract_meeting_rooms(),
                'banquet_hall': self.extract_banquet_requirements(),
                'breakout_rooms': self.extract_breakout_rooms(),
                'exhibition_space': self.extract_exhibition_space()
            },
            
            # 餐饮需求
            'catering': {
                'meal_types': self.extract_meal_types(),  # 桌餐/自助/茶歇
                'dietary_restrictions': self.extract_dietary_restrictions(),
                'menu_preferences': self.extract_menu_preferences(),
                'bar_service': self.extract_bar_requirements()
            },
            
            # 住宿需求
            'accommodation': {
                'room_nights': self.extract_room_nights(),
                'room_types': self.extract_room_types(),
                'vip_rooms': self.extract_vip_requirements()
            },
            
            # 特殊要求
            'special_requirements': {
                'av_equipment': self.extract_av_requirements(),
                'decoration': self.extract_decoration_requirements(),
                'transportation': self.extract_transportation(),
                'other': self.extract_other_requirements()
            },
            
            # 商务条款
            'commercial': {
                'response_deadline': self.extract_deadline(),
                'decision_criteria': self.extract_evaluation_criteria(),
                'contract_terms': self.extract_contract_terms(),
                'payment_terms': self.extract_payment_terms()
            }
        }
        
        return parsed_data
```

**解析示例**
```
输入: PDF格式的RFP文档

AI解析结果:
{
  "client": {
    "company_name": "XX科技有限公司",
    "industry": "互联网/科技",
    "contact_person": "张女士",
    "contact_info": "zhang@xxtech.com, 138****8888"
  },
  "event": {
    "event_type": "年度经销商大会",
    "event_name": "2026 XX科技渠道伙伴峰会",
    "date": "2026-05-15 至 2026-05-17",
    "duration": "3天2晚",
    "participants": 300,
    "budget_range": "30-50万"
  },
  "venue_requirements": {
    "main_hall": "500人宴会厅，LED大屏",
    "breakout_rooms": "3间80人会议室",
    "exhibition": "200㎡产品展示区"
  },
  "catering": {
    "meals": ["欢迎晚宴桌餐", "2次午餐自助", "3次茶歇"],
    "dietary": ["素食", "清真"],
    "special": "需要主题蛋糕"
  },
  "accommodation": {
    "room_nights": 600,
    "types": "标准间为主，10间套房"
  },
  "deadline": "2026-03-20 18:00"
}
```

#### 模块2: 知识库RAG检索

**知识库构成**
```
知识库:
├── 方案模板库
│   ├── 会议活动模板 (20套)
│   ├── 婚宴模板 (15套)
│   ├── 企业年会模板 (10套)
│   ├── 发布会模板 (10套)
│   └── 定制模板 (历史优秀方案)
│
├── 案例库
│   ├── 中标方案全文 (500+份)
│   ├── 案例摘要 (客户/规模/亮点)
│   ├── 客户评价反馈
│   └── 中标/落标分析
│
├── 产品知识库
│   ├── 场地信息 (面积/层高/设施)
│   ├── 菜品库 (图文/成本/售价)
│   ├── AV设备清单
│   └── 服务流程SOP
│
└── 价格库
    ├── 历史成交价
    ├── 竞争对手价格
    ├── 季节性价格策略
    └── 客户分级定价
```

**RAG检索流程**
```python
class RFPKnowledgeRetriever:
    """基于RAG的方案知识检索"""
    
    def __init__(self):
        self.embedding_model = load_embedding_model()
        self.vector_store = load_vector_store()
    
    def retrieve(self, rfp_data, top_k=5):
        """检索相关知识和案例"""
        
        # 1. 构建查询向量
        query_text = self.build_query_text(rfp_data)
        query_embedding = self.embedding_model.encode(query_text)
        
        # 2. 多路召回
        retrieved_items = []
        
        # 相似案例召回
        similar_cases = self.vector_store.similarity_search(
            query_embedding, 
            collection='cases',
            top_k=top_k
        )
        
        # 模板召回
        matching_templates = self.match_templates(rfp_data)
        
        # 产品知识召回
        product_knowledge = self.retrieve_product_info(rfp_data)
        
        # 3. 重排序
        reranked_results = self.rerank(
            similar_cases + matching_templates + product_knowledge,
            rfp_data
        )
        
        return reranked_results
    
    def build_query_text(self, rfp_data):
        """构建检索查询文本"""
        return f"""
        活动类型: {rfp_data['event']['event_type']}
        规模: {rfp_data['event']['participants']}人
        行业: {rfp_data['client']['industry']}
        需求: {rfp_data['venue_requirements']}
        餐饮: {rfp_data['catering']['meals']}
        """
```

#### 模块3: AI方案生成

**生成流程**
```
RFP解析结果 + 检索知识
        ↓
Prompt工程 (结构化输入)
        ↓
DeepSeek/GPT-4o生成
        ↓
多轮优化迭代
        ↓
结构化方案输出
```

**Prompt模板**
```
角色: 资深MICE销售专家，拥有10年酒店宴会销售经验
任务: 为以下RFP生成专业响应方案

酒店背景:
- 酒店名称: {hotel_name}
- 星级: {star_rating}
- 特色: {hotel_highlights}

客户RFP信息:
{rfp_summary}

参考案例:
{similar_cases}

方案要求:
1. 结构完整，包含以下章节:
   - 公司介绍与资质
   - 活动理解与客户痛点分析
   - 场地解决方案
   - 餐饮方案
   - 住宿安排
   - AV技术与服务支持
   - 项目团队介绍
   - 详细报价
   - 应急预案
   - 成功案例

2. 语言风格:
   - 专业、热情、自信
   - 突出酒店独特优势
   - 针对客户行业特点定制

3. 内容要求:
   - 具体数据支撑(面积、容量、价格)
   - 可视化描述(可配合图片)
   - 差异化卖点(为什么选择我们)

4. 格式:
   - 使用Markdown格式
   - 章节清晰，层次分明
   - 重要内容加粗突出

请生成完整的方案初稿。
```

**方案结构示例**
```markdown
# XX科技有限公司2026渠道伙伴峰会
## 酒店响应方案

---

## 一、公司介绍

### 1.1 酒店概况
[酒店简介、地理位置、荣誉资质]

### 1.2 MICE服务优势
- 5000㎡会议空间，可容纳10-1000人活动
- 专业MICE团队，人均8年以上经验
- 年度承接300+场会议活动，客户满意度98%

---

## 二、活动理解与方案亮点

### 2.1 客户痛点理解
基于贵司互联网行业特点和300人规模，我们理解关键需求：
- **科技感呈现**: 需要现代化AV设备和创意展示空间
- **高效流程**: 紧凑的3天议程需要无缝衔接
- **成本优化**: 在预算范围内最大化活动效果

### 2.2 我们的解决方案亮点
✨ **亮点1**: 800㎡无柱宴会厅 + 4K LED大屏，打造沉浸式发布体验
✨ **亮点2**: 专属项目经理 + 3天全程驻场服务
✨ **亮点3**: 科技主题茶歇 + 定制伴手礼

---

## 三、场地解决方案

### 3.1 主会场: 大宴会厅
- 面积: 800㎡
- 层高: 8米无柱
- 容量: 剧院式400人 / 课桌式300人 / 宴会式35桌
- 配置: LED大屏(10m×4m)、专业灯光音响

### 3.2 分会场
- 会议室A: 150㎡，容纳80人
- 会议室B: 150㎡，容纳80人  
- 会议室C: 100㎡，容纳50人

### 3.3 展示区
- 产品展示区: 200㎡(宴会厅前厅)
- 签到处: 50㎡
- 茶歇区: 100㎡

[... 其他章节 ...]

---

## 八、投资预算

| 项目 | 明细 | 单价 | 数量 | 小计 |
|------|------|------|------|------|
| 场地租赁 | 大宴会厅(3天) | ¥30,000 | 3 | ¥90,000 |
| 餐饮 | 欢迎晚宴(35桌) | ¥3,888 | 35 | ¥136,080 |
| 住宿 | 标准间(2晚) | ¥580 | 280间 | ¥324,800 |
| AV设备 | LED大屏+音响 | - | 1套 | ¥45,000 |
| 服务费 | 15%服务费 | - | - | ¥89,682 |
| **合计** | | | | **¥685,562** |

**优惠方案**: 确认签约可享受9折优惠，实付 **¥617,006**

---

## 九、项目团队

- **项目经理**: 王经理，10年MICE经验，服务过华为、腾讯等客户
- **宴会经理**: 李经理，西餐厨师长出身，精通创意菜单设计
- **销售经理**: 刘经理，您的专属联系人，24小时响应

---

## 十、成功案例

### 案例1: 某知名互联网公司2025年会
- 规模: 500人
- 亮点: 主题定制、无缝执行
- 客户评价: "专业度超出预期，明年继续合作"

[... 更多案例 ...]
```

#### 模块4: 智能定价引擎

**定价策略**
```python
class PricingEngine:
    """智能定价引擎"""
    
    def calculate_price(self, rfp_data, strategy='balanced'):
        """
        策略选项:
        - aggressive: 激进定价，优先拿单
        - balanced: 平衡定价，兼顾利润和中标率
        - premium: 溢价定价，强调差异化价值
        """
        
        # 基础成本
        base_cost = self.calculate_base_cost(rfp_data)
        
        # 市场参考价
        market_price = self.get_market_price(rfp_data)
        
        # 客户价值评估
        client_value = self.evaluate_client_value(rfp_data)
        
        # 竞争强度评估
        competition_level = self.assess_competition(rfp_data)
        
        # 时间压力
        urgency = self.assess_urgency(rfp_data)
        
        # 综合定价
        if strategy == 'aggressive':
            price = base_cost * 1.15  # 15%毛利
        elif strategy == 'balanced':
            price = min(market_price * 0.95, base_cost * 1.25)
        elif strategy == 'premium':
            price = market_price * 1.1
        
        # 根据竞争和紧急程度微调
        if competition_level == 'high':
            price *= 0.95
        if urgency == 'high':
            price *= 0.98
        
        return {
            'base_cost': base_cost,
            'suggested_price': price,
            'margin_rate': (price - base_cost) / price,
            'win_probability': self.estimate_win_probability(price, competition_level),
            'price_breakdown': self.generate_breakdown(rfp_data, price)
        }
```

**价格敏感性分析**
```
建议报价: ¥617,006 (9折后)

价格敏感性分析:
┌──────────────┬──────────┬───────────┐
│ 报价方案       │ 利润率    │ 中标概率   │
├──────────────┼──────────┼───────────┤
│ ¥550,000 (85折)│ 12%      │ 65%       │
│ ¥617,006 (9折) │ 18%      │ 55%       │ ← 推荐
│ ¥685,562 (原价)│ 25%      │ 35%       │
└──────────────┴──────────┴───────────┘

建议: 采用9折方案，平衡利润和中标概率
```

#### 模块5: 协同编辑与审核

**协同工作流**
```
AI生成初稿 (30分钟)
    ↓
销售经理编辑优化 (1-2小时)
    ↓
收益经理审核定价 (30分钟)
    ↓
宴会/餐饮经理补充专业内容 (1小时)
    ↓
销售总监终审 (30分钟)
    ↓
提交客户
```

**审核检查清单**
```yaml
内容完整性:
  - [ ] 所有RFP问题都有回应
  - [ ] 场地信息准确无误
  - [ ] 菜单和价格已确认
  - [ ] 团队成员信息正确

专业度检查:
  - [ ] 无明显错别字
  - [ ] 数据逻辑一致
  - [ ] 图片清晰、排版美观
  - [ ] 突出差异化优势

商务条款:
  - [ ] 价格计算正确
  - [ ] 付款条款合理
  - [ ] 取消政策明确
  - [ ] 违约条款保护酒店利益

风险提示:
  - [ ] 场地是否已被预订
  - [ ] 人力是否充足
  - [ ] 是否有特殊要求超出能力
```

---

## 4. 技术实现

### 4.1 技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
**文档解析** | Python + PyPDF2/Docx | 多格式文档解析 |
**NLP** | DeepSeek-V3 / GPT-4o | 意图理解、内容生成 |
**RAG** | LangChain + ChromaDB | 知识检索增强 |
**协同编辑** | Yjs / ProseMirror | 实时协同编辑 |
**文档生成** | Markdown + Pandoc | 多格式输出 |

### 4.2 API设计

```yaml
# 上传并解析RFP
POST /api/v1/rfp/parse
参数:
  file: File (PDF/Word/Excel)
返回:
  rfp_id: string
  parsed_data: object (结构化RFP数据)
  confidence: float

# 生成方案初稿
POST /api/v1/rfp/{rfp_id}/generate
参数:
  strategy: string (aggressive/balanced/premium)
  tone: string (professional/friendly/luxury)
返回:
  proposal_id: string
  content: string (Markdown格式)
  generated_at: timestamp

# 检索相似案例
GET /api/v1/rfp/{rfp_id}/similar-cases
返回:
  cases: [{
    case_id, similarity_score, summary, highlights
  }]

# 计算定价建议
POST /api/v1/rfp/{rfp_id}/pricing
返回:
  suggested_price: float
  breakdown: object
  scenarios: [price_option]

# 导出最终方案
GET /api/v1/proposal/{proposal_id}/export
参数:
  format: string (pdf/word/ppt)
返回:
  download_url: string
```

---

## 5. 界面设计

### 5.1 销售端界面

**RFP上传与解析**
```
┌─────────────────────────────────────┐
│ 📝 RFP智能应答系统                   │
├─────────────────────────────────────┤
│                                     │
│  📤 上传RFP文档                     │
│  ┌─────────────────────────────┐   │
│  │  拖拽文件到此处 或 点击上传   │   │
│  │  支持PDF、Word、Excel格式     │   │
│  └─────────────────────────────┘   │
│                                     │
│  [📎 示例: XX科技RFP.pdf]           │
│                                     │
│  [开始解析]                         │
│                                     │
└─────────────────────────────────────┘
```

**解析结果确认**
```
┌─────────────────────────────────────┐
│ ← 返回          解析结果确认        │
├─────────────────────────────────────┤
│                                     │
│  📋 RFP关键信息提取                  │
│                                     │
│  客户: XX科技有限公司 ✓             │
│  行业: 互联网/科技 ✓                │
│  活动: 年度经销商大会 ✓             │
│  规模: 300人 ✓                      │
│  日期: 2026-05-15 至 17 ✓           │
│  预算: 30-50万 ⚠️ (AI推测，需确认)  │
│                                     │
│  [编辑信息] [确认无误，生成方案]    │
│                                     │
└─────────────────────────────────────┘
```

**方案编辑界面**
```
┌─────────────────────────────────────────────────────────────┐
│ 📝 方案编辑: XX科技渠道峰会          [保存] [预览] [导出]    │
├─────────────────────────────────────────────────────────────┤
│ 章节 │ 内容                                                    │
├─────────────────────────────────────────────────────────────┤
│ ✓ 公司介绍                                                    │
│ ✓ 活动理解                                                    │
│ ✓ 场地方案                                                    │
│ → 餐饮方案      [当前编辑]                                    │
│ ○ 住宿安排                                                    │
│ ○ AV技术                                                       │
│ ○ 团队介绍                                                     │
│ ○ 报价                                                         │
│ ○ 案例                                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ## 四、餐饮方案                                              │
│                                                             │
│  ### 4.1 欢迎晚宴                                            │
│                                                             │
│  [AI生成内容...]                                             │
│  建议菜单:                                                   │
│  - 八彩碟 (中西合璧开胃菜)                                   │
│  - 鸡茸粟米羹                                                │
│  - ...                                                       │
│                                                             │
│  💡 AI建议: 科技行业客户偏好创意菜品，建议增加分子料理元素   │
│                                                             │
│  [采纳建议] [忽略]                                           │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  当前进度: 60%    预计完成时间: 30分钟                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. 成功指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
方案生成时间 | <60分钟 | 从RFP到初稿 |
RFP响应及时率 | >95% | 72小时内响应 |
方案专业度评分 | >4.5/5 | 内部审核评分 |
中标率提升 | >30% | 同比提升 |
销售满意度 | >90% | 使用体验调研 |

---

## 7. 实施路径

**Phase 1: 基础版 (4周)**
- RFP解析功能
- 基础方案模板
- AI内容生成

**Phase 2: 增强版 (4周)**
- RAG知识检索
- 智能定价引擎
- 多格式导出

**Phase 3: 智能版 (4周)**
- 协同编辑
- 自动审核
- 效果反馈闭环

---

**文档版本**: v1.0 | **创建日期**: 2026-03-04
