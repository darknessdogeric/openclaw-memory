# OTA平台探测报告

## 已知有效平台

### 携程 (Ctrip) ✅ 完全掌握
- **PC端**: `https://hotels.ctrip.com/hotels/detail/?cityId={cityId}&hotelId={hotelId}`
- **城市ID映射**: 大理=36, 滁州=214, 重庆=4, 乐山=36, 成都=28
- **搜索**: `https://hotels.ctrip.com/hotels/list/?cityName={城市}&cityId={cityId}`
- **方法**: chrome-devtools + AI视觉解析
- **成功率**: 100%

---

## 待探测平台（需要找到正确URL）

### 美团酒店 (Meituan Hotel)
**状态**: ❌ 未找到正确入口

**已尝试**:
- `https://i.meituan.com/meituan.com/s/滁州君家酒店` → 404
- `https://hotel.m.meituan.com/search` → 连接失败
- `https://hotel.meituan.com/search` → 被重定向到Google

**需要探索**:
- [ ] 找到美团酒店的正确移动端URL格式
- [ ] 确认是否需要登录态
- [ ] 找到酒店详情页的URL pattern

**猜测格式**:
- `https://whotelhotel.meituan.com/hotel/滁州/xxx`
- `https://i.meituan.com/deal/xxx`

**搜索关键词**: 美团酒店移动端 URL格式 site:meituan.com hotel

---

### 飞猪 (Fliggy/Alibaba) 
**状态**: ❌ 未找到正确入口

**已尝试**:
- `https://h5.fliggy.com/search` → 连接失败
- `https://www.fliggy.com/hotel/search` → 超时

**需要探索**:
- [ ] 飞猪酒店的URL格式（阿里系）
- [ ] 是否需要淘宝/支付宝账号
- [ ] 移动端专用域名

**猜测格式**:
- `https://m.fliggy.com`
- `https://h5.fliggy.com/hotel`

---

### 去哪儿 (Qunar)
**状态**: ❌ URL格式错误

**已尝试**:
- `https://www.qunar.com/site/oneshot/滁州/君家酒店.htm` → 404

**需要探索**:
- [ ] 去哪儿酒店搜索的正确URL
- [ ] 移动端域名

**搜索关键词**: 去哪儿酒店 mobile URL pattern

---

### 途牛旅游 (Tuniu)
**状态**: ⏳ 未测试

**需要探索**:
- [ ] PC端酒店页面
- [ ] 移动端域名

---

### 马蜂窝 (Mafengwo)
**状态**: ⏳ 未测试

**需要探索**:
- [ ] 酒店预订页面URL
- [ ] 移动端

---

## 酒店官方渠道

### 酒店官网直订
**状态**: ⏳ 需要酒店提供URL

**方法**:
1. 百度搜索: `site:酒店名.com 酒店预订`
2. 携程详情页通常有官网链接
3. 微信搜索酒店名找官网

---

### 微信微官网/小程序
**状态**: ❌ 基本无法爬取

**原因**:
- 小程序数据在微信客户端内，无法通过HTTP访问
- 微官网需要微信公众号授权
- 技术壁垒极高

**替代方案**:
- 让酒店提供微官网截图
- 通过酒店销售/市场部门获取价格

---

## TMC平台

### 已知的TMC平台
| 平台 | 说明 | 爬取难度 |
|------|------|---------|
| 携程商旅 | 最大的企业差旅平台 | 高（需要企业账号）|
| 差旅壹号 | 企业商旅管理 | 高（需要企业账号）|
| 觅星 | 商务旅行管理 | 高（企业账号）|
| 悦程 | 企业差旅 | 高（企业账号）|
| 在路上 | 企业TMC | 高（企业账号）|

**核心问题**: TMC平台需要企业账号登录，普通用户无法访问价格

**可能的替代**:
- [ ] 搜索TMC公开的企业酒店协议价格（如招标公告）
- [ ] 通过LinkedIn/脉脉找TMC行业数据
- [ ] 招聘网站看TMC公司的技术文档

---

## 探测行动计划

### Phase 1: 平台URL发现（本次任务）
对每个平台：
1. 搜索正确的URL格式
2. 测试1-2个已知酒店的URL
3. 记录成功的URL pattern

### Phase 2: 移动端适配
对支持移动端的平台：
1. 确认移动端URL
2. 测试user agent伪装
3. 验证截图+AI解析流程

### Phase 3: 官方渠道整合
1. 收集各试点酒店的官网URL
2. 测试官网直订价格获取
3. 建立"酒店资料包"获取SOP

---

## 探测日志

### 2026-04-03 23:43

**美团酒店 (Meituan)**:
- 测试1: `https://i.meituan.com/meituan.com/s/滁州君家酒店` → 404 "信息未找到"
- 测试2: `https://hotel.m.meituan.com/search?keyword=滁州君家酒店&city=滁州` → ERR_CONNECTION_ABORTED
- 问题: 找不到正确的移动端URL格式

**去哪儿 (Qunar)**:
- 测试1: `https://www.qunar.com/site/oneshot/滁州/君家酒店.htm` → 404
- 问题: URL格式不正确，需要找到正确的pattern

**飞猪 (Fliggy)**:
- 测试1: `https://h5.fliggy.com/search?keyword=滁州君家酒店` → ERR_CONNECTION_ABORTED
- 问题: 域名可能已变更或需要特殊访问方式
