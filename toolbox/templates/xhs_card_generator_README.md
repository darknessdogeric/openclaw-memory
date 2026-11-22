# 小红书多图卡片生成器 · 标准范式 v1.0
来源:综合 nexu-io/card-xiaohongshu(Apache-2.0,8.3K stars) + Eric 反复反馈 + 金轩十文 9 图实战
固定:1080x1440(3:4),flex 纵向,每卡一个核心观点,设计 token 锁定

# ============ 不要再踩的坑(从金轩十文 9 图 11 版迭代中学到) ============

# 1. 画布用 grid 4 行严格分配(70px / 150px / 1fr / 170px),不用 absolute
# 2. seg-body 用 justify-content: space-evenly(不用 flex:1 + gap)
# 3. 字号经验证:正文 22px / 表格 17px / KPI 标签 15px / conclusion 20px
# 4. footer-summary 用大字(26px)+ 绿色背景框 = 画面视觉锚点
# 5. Playwright 启动参数加 --no-sandbox --disable-gpu --disable-dev-shm-usage(避免 dashboard 闪退)
# 6. 不要用 single-process(会导致后续 context 失败)
# 7. 每张卡独立 context + 渲染完立即关
# 8. 不要 flex:1 + content-top(我之前 8 版都栽这个)
# 9. 不要 emoji 当图标(廉价 AI 卡)
# 10. 不要深蓝科技渐变 + 大字 + 大空白(反面教材)

