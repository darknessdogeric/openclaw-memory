# 酒店价格查询接入说明

当前主系统里的“酒店/房东竞品价格查询”已经不是旧的独立 demo，而是集成在主项目后端服务里的正式链路。

项目根目录：

```text
文旅项目2/ai-homestay-system
```

核心服务文件：

```text
backend/app/services/price_query_service.py
```

## 1. 当前价格链路

现在的查询顺序是：

1. 打开 `hk.trip.com/hotels`，建立中文/CNY 会话
2. 直接调用 Trip 酒店站的关键词搜索接口 `/htls/getKeyWordSearch`
3. 从返回结果中解析酒店名、酒店 ID、城市、坐标、`searchValue`
4. 生成 Trip 列表页 URL，保留一张桌面结果页截图作为调试断点
5. 以解析出的 `hotel_id` 打开大陆携程移动端详情页
6. 复用移动端详情页真实发出的官方房价接口请求：
   - `getHotelRoomListInland`
   - `getHotelRoomPopInfo`
7. 先取 `getHotelRoomListInland` 的 `hotelDetailBarInfo.price` 作为原始起价
8. 再用 `getHotelRoomPopInfo` 的房型浮层应付价做校验
9. 如果页面存在“登录看低价”门槛，则按展示价对齐规则补偿固定偏移
10. 如果大陆携程链路失败，再回退到 Trip 列表页 DOM/HTML/结构化数据识别

当前主价格来源标记：

```text
ctrip_mobile_detail_api_display_aligned
```

## 2. 口径说明

- 币种已固定为 `CNY`
- 浏览器语言优先为 `zh-CN`
- 大陆携程移动端详情页是当前主口径
- 会保留 `roomList` 与 `roomPopInfo` 两条官方链路的调试结果
- 当详情页正文出现“登录看低价”时，默认会做 `+6 元` 的展示价对齐
- 这个对齐值可通过环境变量 `PRICE_QUERY_CTRIP_DISPLAY_OFFSET` 调整，默认值是 `6`

默认查询人数：

- `2` 位成人
- `0` 位儿童
- `1` 间房

## 3. 依赖安装

先安装 Python 依赖：

```bash
pip install -r requirements.txt
```

再安装 Playwright 浏览器内核：

```bash
python -m playwright install chromium
```

## 4. 可选视觉模型配置

视觉模型现在只做兜底，不再是主价格来源。

可选环境变量：

```env
PRICE_TOOL_API_KEY=your_api_key
PRICE_TOOL_BASE_URL=https://your-openai-compatible-endpoint/v1
PRICE_TOOL_MODEL=your_vision_model
PRICE_QUERY_HEADLESS=false
PRICE_QUERY_CTRIP_DISPLAY_OFFSET=6
```

也兼容旧变量：

```env
ARK_API_KEY=your_api_key
base_url=https://your-openai-compatible-endpoint/v1
model=your_vision_model
```

## 5. 主系统里的使用方式

房东/酒店 Agent 可以直接触发：

- `帮我查全季酒店（滁州万达广场店）和滁州茂业华美达广场酒店的价格`
- `帮我查某某酒店明天的价格`

后端会：

1. 创建价格查询任务
2. 执行 Trip 关键词解析
3. 执行大陆携程移动端详情页价格抓取
4. 自动判断是否存在“登录看低价”门槛并做展示价对齐
5. 保留截图、请求摘要、响应摘要、命中结果
6. 把结果回传到主系统对话

## 6. 调试文件位置

每次任务的调试文件都保存在：

```text
backend/static/debug_screenshots/price_queries/<task_id>/
```

常见文件包括：

- `*_keyword_resolution.json`
- `*_search_results.jpg`
- `*_match.json`
- `*_ctrip_mobile_request.json`
- `*_ctrip_mobile_response.json`
- `*_ctrip_mobile_final.jpg`
- `*_ctrip_mobile_error.json`
- `task_state.json`

静态访问路径：

```text
/debug-screenshots/price_queries/<task_id>/<filename>
```

## 7. 一键启动

整个项目统一从根目录启动：

```text
ai-homestay-system/start.bat
```

这个脚本会一键启动前后端。


---

## 🔗 相关笔记

- [[酒店行业 MOC]]
- [[安逸集团-D-day MOC]]
- [[B166ER 知识库 MOC]]

*该区块由 B166ER 自动注入 (2026-07-28) — 关键词匹配*
