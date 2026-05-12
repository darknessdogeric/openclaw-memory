# Cross-Border Trade Skill

跨境贸易全流程技能，让你立即上手。

## 快速开始

### 立即要做什么（Day 1）

1. **注册亚马逊卖家账号**
   → amazon.com → Sell → Start Selling

2. **完成税务信息**
   → 卖家后台 → 账户信息 → 税务信息 → 填写W-8BEN

3. **开始选品调研**
   → 使用 product_research.py 生成调研模板

4. **用 profit_calculator.py 计算利润**
   → 确认毛利率>40%再继续

## 工具使用

### 利润计算器
```bash
python profit_calculator.py          # 交互式计算
python profit_calculator.py --example  # 查看示例
python profit_calculator.py --help     # 帮助
```

### 选品调研工具
```bash
python product_research.py
# 选择生成:
# 1. 竞品分析报告
# 2. 利润计算表
# 3. 备货计划表
# 4. 供应商询价表
# 5. Listing上架检查表
# 6. 全部生成
```

## 核心流程

```
Day 1     → 注册账号 + 完成税务
Day 2-3   → 选品调研（用product_research.py）
Day 4-10  → 找供应商打样
Day 11-17 → 确认样品 + 利润核算（用profit_calculator.py）
Day 18-25 → Listing优化 + 上架
Day 26-30 → FBA发货 + 等待上架
Day 31+   → 广告投放 + 评价积累
```

## 关键指标

| 指标 | 健康值 | 警示 |
|------|--------|------|
| 毛利率 | >40% | <25% |
| ACOS | <25% | >40% |
| CTR | >0.5% | <0.3% |
| CVR | >10% | <5% |
| ODR | <1% | >2% |
| 好评率 | >90% | <80% |
| 退货率 | <5% | >10% |

## 文件结构

```
cross-border-trade/
├── SKILL.md              # 主技能文档
├── README.md             # 本文件
├── profit_calculator.py  # 利润计算器
└── product_research.py   # 选品调研工具
```

## 常见问题

**Q: 没有产品怎么办？**
A: 参考SKILL.md第二节选品流程，从3C配件/智能家居/户外用品开始。

**Q: 资金有限怎么办？**
A: 先用直邮小包测款（<$5000），爆款再转FBA。

**Q: 不知道卖什么？**
A: 用卖家精灵/鸥鹭等工具调研热门品类，找差异化机会。

**Q: 怕侵权？**
A: 上架前用Google Patents + WIPO查询专利， USPTO查询商标。

**Q: 不知道怎么定价？**
A: 用profit_calculator.py计算，确保毛利率>40%。

## 触发场景

当你说以下内容时，我会调用这个skill：

- "我要做跨境电商"
- "帮我选品"
- "亚马逊开店"
- "计算利润"
- "分析竞品"
- "FBA发货"
- "广告投放"
- "怎么提高评价"
- "账号被封了"
- "竞品分析"
- "产品上架"
- "选品调研"

## 版本

- V1.0: 2026-04-02 初始版本
