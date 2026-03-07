# SKILL-PRD-007: AI视频分析安防 (AI Video Analytics for Security)

## 基本信息

| 字段 | 内容 |
|------|------|
**SKILL编号** | SEC-007
**SKILL名称** | AI视频分析安防 (AI Video Analytics for Security)
**所属AGENT** | 安防监控AGENT (Security Agent)
**版本** | v1.0
**创建日期** | 2026-03-04
**优先级** | P0 (安防核心能力)
**开发周期** | 6-8周

---

## 1. 价值定位

### 1.1 解决的问题
传统酒店安防依赖人工监控，面临严峻挑战：

**监控盲区与疲劳**
- 100+路摄像头，安保人员无法同时关注
- 长时间盯屏导致视觉疲劳，重要事件遗漏
- 夜班时段人手不足，安全隐患增大

**事后追溯困难**
- 事件发生后再查录像，效率低下
- 无法第一时间预警，错失处置黄金时间
- 海量录像检索耗时，关键画面难定位

**合规与 liability**
- 宾客安全事件频发，酒店责任压力大
- 消防通道堵塞、禁烟区吸烟等违规难以及时发现
- 保险理赔缺乏客观证据

### 1.2 核心价值
**"从'人眼监控'到'AI眼守护'，7x24小时无死角智能安防"**

- **实时预警**：异常行为秒级识别，第一时间推送告警
- **智能分析**：自动识别20+种安全事件，无需人工盯屏
- **主动防御**：风险行为早期发现，防患于未然
- **证据留存**：关键事件自动标记，快速回溯取证

### 1.3 量化收益

| 指标 | 传统模式 | AI视频分析 | 提升幅度 |
|------|---------|-----------|---------|
监控覆盖率 | 60-70% | 95%+ | **提升50%** |
异常事件发现时间 | 10-30分钟 | <5秒 | **快100倍** |
误报率 | 30-40% | <5% | **降低90%** |
安保人力需求 | 12-15人/班 | 6-8人/班 | **节省40%** |
安全事件处理效率 | 基准值 | +200% | **提升2倍** |

---

## 2. 目标用户

### 2.1 主要用户

| 用户角色 | 使用场景 | 核心痛点 |
|---------|---------|---------|
**安保经理** | 监控中心大屏，处理告警 | 屏幕太多看不过来，漏掉关键事件 |
**保安员** | 巡逻+响应告警 | 夜班困乏，无法时刻保持警惕 |
**房务总监** | 关注客房区域安全 | 客房盗窃、陌生人闯入难以及时发现 |
**总经理** | 重大安全事件的决策 | 安全事件响应慢，影响酒店声誉 |

### 2.2 用户画像

**典型用户：陈经理，40岁，商务酒店安保经理**
- 管理酒店120路摄像头，但只有3个保安能看监控
- 上周有客人投诉物品丢失，查录像花了2小时才找到画面
- 夜班保安经常打瞌睡，他总担心出问题
- 希望能有个系统帮他"看着"所有画面，有异常自动提醒

---

## 3. 功能架构

### 3.1 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    应用层                                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 监控大屏     │ │ 移动端告警   │ │ 事件管理     │            │
│  │ (实时视频)   │ │ (推送通知)   │ │ (处置追踪)   │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                    AI分析层 (边缘+云端)                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 目标检测     │ │ 行为识别     │ │ 人脸识别     │            │
│  │ (YOLOv8)    │ │ (SlowFast)  │ │ (ArcFace)   │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 异常检测     │ │ 轨迹分析     │ │ 人群计数     │            │
│  │ (异常行为)   │ │ (REID)      │ │ (密度估计)   │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                    视频接入层                                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 摄像头      │ │ NVR/DVR     │ │ 视频网关     │            │
│  │ (RTSP)      │ │ (ONVIF)     │ │ (转码/分发)  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 核心功能模块

#### 模块1: 多目标检测与跟踪

**检测能力**
| 目标类型 | 检测精度 | 应用场景 |
|---------|---------|---------|
人员 | 98.5% | 入侵检测、区域管控 |
车辆 | 96.8% | 停车场管理、违章识别 |
行李/包裹 | 94.2% | 遗留物检测、盗窃预警 |
消防器材 | 95.5% | 消防通道堵塞检测 |
烟雾/火焰 | 93.7% | 火灾早期预警 |

**多目标跟踪 (MOT)**
```python
class MultiObjectTracker:
    """多目标跟踪系统"""
    
    def __init__(self):
        self.detector = YOLOv8Detector()
        self.tracker = ByteTrack()  # 高效跟踪算法
        self.reid_model = OSNet()   # 重识别模型
    
    def track(self, frame):
        # 1. 检测
        detections = self.detector.detect(frame)
        
        # 2. 跟踪
        tracks = self.tracker.update(detections)
        
        # 3. 特征提取与重识别
        for track in tracks:
            track.feature = self.reid_model.extract(frame, track.bbox)
        
        return tracks
```

#### 模块2: 行为识别与异常检测

**识别行为类型**

| 行为类别 | 具体行为 | 告警级别 | 适用区域 |
|---------|---------|---------|---------|
**入侵类** | 区域入侵 | 高 | 机房/财务室/厨房 |
| | 越界检测 | 中 | 泳池/天台边界 |
| | 翻墙检测 | 高 | 周界围墙 |
**异常行为** | 徘徊检测 | 中 | 客房走廊/大堂 |
| | 聚集检测 | 中 | 大堂/出入口 |
| | 快速奔跑 | 高 | 全区域 |
| | 打架斗殴 | 高 | 全区域 |
**安全事件** | 跌倒检测 | 高 | 客房/浴室/泳池 |
| | 烟雾/火焰 | 高 | 全区域 |
| | 遗留物 | 中 | 大堂/电梯厅 |
| | 物品拿取 | 中 | 客房/前台 |
**合规检测** | 消防通道堵塞 | 中 | 消防通道 |
| | 吸烟检测 | 低 | 禁烟区域 |
| | 未穿工装 | 低 | 后厨/客房 |

**行为识别模型**
```python
class ActionRecognizer:
    """基于SlowFast的行为识别"""
    
    def __init__(self):
        self.model = SlowFastNetwork(
            slow_pathway_frames=4,   # 慢路径：空间细节
            fast_pathway_frames=32   # 快路径：时序动作
        )
    
    def recognize(self, video_clip):
        """
        输入: 2秒视频片段 (32帧)
        输出: 行为类别 + 置信度
        """
        # Slow路径：每隔8帧采样4帧，捕捉空间细节
        slow_frames = video_clip[::8][:4]
        
        # Fast路径：每帧都采样，捕捉动作时序
        fast_frames = video_clip
        
        # 融合预测
        action_probs = self.model(slow_frames, fast_frames)
        
        return {
            'action': self.get_action_label(action_probs),
            'confidence': max(action_probs),
            'all_probs': action_probs
        }
```

**跌倒检测专项**
```python
class FallDetection:
    """跌倒检测算法"""
    
    def detect_fall(self, pose_keypoints):
        """
        基于姿态估计的跌倒检测
        关键特征:
        1. 人体中心高度骤降
        2. 头部高度低于正常阈值
        3. 身体倾斜角度>45度
        4. 持续倒地时间>3秒
        """
        # 计算关键点
        head = pose_keypoints['nose']
        center = self.calculate_center(pose_keypoints)
        
        # 特征判断
        height_drop = self.previous_center[1] - center[1]
        is_head_low = head[1] > self.height_threshold
        body_angle = self.calculate_body_angle(pose_keypoints)
        
        if height_drop > self.drop_threshold and \
           is_head_low and \
           body_angle > 45:
            self.fall_frame_count += 1
            
            if self.fall_frame_count > self.fall_duration_threshold:
                return {
                    'is_fall': True,
                    'confidence': self.calculate_confidence(),
                    'location': center,
                    'timestamp': datetime.now()
                }
        else:
            self.fall_frame_count = 0
        
        return {'is_fall': False}
```

#### 模块3: 人脸识别与布控

**人脸识别能力**
| 功能 | 精度 | 响应时间 | 应用场景 |
|------|------|---------|---------|
人脸检测 | 99.2% | <50ms | 全场景 |
人脸识别 | 98.5% | <100ms | VIP识别、黑名单 |
人脸属性 | 96.0% | <50ms | 性别/年龄分析 |
活体检测 | 99.0% | <200ms | 防照片欺骗 |

**布控系统**
```python
class FaceRecognitionSystem:
    """人脸识别与布控系统"""
    
    def __init__(self):
        self.detector = RetinaFace()
        self.recognizer = ArcFace()
        self.face_db = FaceDatabase()
    
    def process(self, frame):
        # 1. 人脸检测
        faces = self.detector.detect(frame)
        
        results = []
        for face in faces:
            # 2. 特征提取
            feature = self.recognizer.extract(face.image)
            
            # 3. 库内检索
            matches = self.face_db.search(feature, top_k=5)
            
            # 4. 判断身份
            if matches[0].similarity > 0.85:
                identity = matches[0].identity
                
                # 5. 布控检查
                alert_level = self.check_watchlist(identity)
                
                results.append({
                    'bbox': face.bbox,
                    'identity': identity,
                    'similarity': matches[0].similarity,
                    'alert_level': alert_level,
                    'attributes': self.analyze_attributes(face)
                })
        
        return results
    
    def check_watchlist(self, identity):
        """检查是否在布控名单"""
        watchlists = {
            'blacklist': 'high',      # 黑名单：高危
            'vip': 'info',            # VIP：提示
            'suspected': 'medium',    # 嫌疑人：关注
            'missing_person': 'high'  # 走失人员：高危
        }
        return watchlists.get(identity.type, 'none')
```

**人脸库管理**
```
人脸库类型:
├── VIP库 (酒店常客、重要客户)
│   └── 用途: 自动识别，提供尊贵服务
├── 黑名单 (盗窃前科、闹事情绪失控者)
│   └── 用途: 实时告警，提前防范
├── 员工库 (酒店员工)
│   └── 用途: 考勤管理、区域权限
├── 访客库 (当日访客)
│   └── 用途: 访客轨迹追踪
└── 寻人库 (走失儿童/老人)
    └── 用途: 协助寻找
```

#### 模块4: 智能告警与事件管理

**告警分级**
```yaml
P0 - 紧急告警 (立即响应):
  - 火灾/烟雾检测
  - 严重暴力行为
  - 人员跌倒无响应
  - 非法入侵核心区域
  响应: 立即推送安保经理+自动报警

P1 - 重要告警 (5分钟内响应):
  - 消防通道堵塞
  - 可疑人员徘徊
  - 物品遗留超过10分钟
  - 聚集事件
  响应: 推送值班保安+记录事件

P2 - 一般告警 (15分钟内响应):
  - 吸烟检测
  - 未穿工装
  - 区域人员密度过高
  响应: 记录日志，定期汇总

P3 - 提示信息 (不告警):
  - VIP客户到达
  - 员工考勤
  - 客流统计
  响应: 记录存档
```

**告警推送**
```python
class AlertManager:
    """告警管理器"""
    
    def __init__(self):
        self.alert_rules = load_alert_rules()
        self.notification_channels = {
            'app': AppPush(),
            'sms': SMSNotification(),
            'wechat': WeChatWork(),
            'phone': PhoneCall()
        }
    
    def process_alert(self, event):
        """处理AI检测到的安全事件"""
        
        # 1. 过滤误报
        if self.is_false_positive(event):
            return
        
        # 2. 去重 (同一事件5分钟内不重复告警)
        if self.is_duplicate(event):
            return
        
        # 3. 确定告警级别
        level = self.determine_alert_level(event)
        
        # 4. 生成告警信息
        alert = {
            'id': generate_uuid(),
            'level': level,
            'type': event.type,
            'location': event.camera_location,
            'timestamp': event.timestamp,
            'description': self.generate_description(event),
            'snapshot': event.frame,
            'video_clip': event.clip,
            'suggested_action': self.get_suggested_action(event)
        }
        
        # 5. 推送通知
        self.send_notification(alert)
        
        # 6. 记录事件
        self.log_event(alert)
        
        return alert
    
    def send_notification(self, alert):
        """多渠道告警推送"""
        
        channels = []
        
        if alert['level'] == 'P0':
            # 紧急：全渠道
            channels = ['app', 'sms', 'wechat', 'phone']
        elif alert['level'] == 'P1':
            # 重要：App+企业微信
            channels = ['app', 'wechat']
        elif alert['level'] == 'P2':
            # 一般：仅App
            channels = ['app']
        
        for channel in channels:
            self.notification_channels[channel].send(alert)
```

**移动端告警界面**
```
┌─────────────────────────────────────┐
│ 🔔 安全告警              [设置]     │
├─────────────────────────────────────┤
│                                     │
│  🔴 P0 - 紧急                       │
│  ┌─────────────────────────────┐   │
│  │ [🎥 视频缩略图]              │   │
│  │                             │   │
│  │ ⚠️ 区域入侵检测              │   │
│  │ 位置: 2F财务室              │   │
│  │ 时间: 14:32:15              │   │
│  │                             │   │
│  │ [查看详情] [确认收到]       │   │
│  └─────────────────────────────┘   │
│                                     │
│  🟡 P1 - 重要                       │
│  ┌─────────────────────────────┐   │
│  │ 消防通道堵塞                │   │
│  │ 位置: B1消防通道B           │   │
│  │ 时间: 14:28:33              │   │
│  │ [查看详情]                  │   │
│  └─────────────────────────────┘   │
│                                     │
│  🟢 P2 - 一般                       │
│  ┌─────────────────────────────┐   │
│  │ 吸烟检测                    │   │
│  │ 位置: 大堂卫生间            │   │
│  │ 时间: 14:15:22              │   │
│  └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

#### 模块5: 视频摘要与快速检索

**智能视频摘要**
```python
class VideoSummarizer:
    """视频摘要生成"""
    
    def generate_summary(self, video_path, duration_hours=24):
        """
        将24小时视频浓缩为5分钟精华片段
        """
        
        # 1. 事件检测
        events = self.detect_all_events(video_path)
        
        # 2. 重要性评分
        for event in events:
            event.importance_score = self.score_importance(event)
        
        # 3. 选择Top事件
        top_events = sorted(events, 
                          key=lambda x: x.importance_score, 
                          reverse=True)[:20]
        
        # 4. 生成摘要视频
        summary_clips = []
        for event in top_events:
            clip = self.extract_clip(video_path, 
                                   event.start_time, 
                                   event.end_time)
            summary_clips.append(clip)
        
        return self.concatenate_clips(summary_clips)
```

**自然语言视频检索**
```python
class VideoSearch:
    """自然语言视频检索"""
    
    def __init__(self):
        self.object_detector = ObjectDetector()
        self.action_recognizer = ActionRecognizer()
        self.face_recognizer = FaceRecognizer()
        self.clip_model = CLIP()  # 图文匹配模型
    
    def search(self, query, time_range):
        """
        支持自然语言查询:
        - "昨天下午穿红色上衣的人"
        - "大堂里推行李箱的人"
        - "12点后在泳池边的人"
        """
        
        # 1. 解析查询
        query_features = self.parse_query(query)
        
        # 2. 检索候选片段
        candidates = self.retrieve_candidates(time_range)
        
        # 3. CLIP匹配
        results = []
        for candidate in candidates:
            # 提取视频特征
            video_features = self.extract_video_features(candidate)
            
            # 计算相似度
            similarity = self.clip_model.similarity(
                query_features, 
                video_features
            )
            
            if similarity > 0.7:
                results.append({
                    'video_segment': candidate,
                    'similarity': similarity,
                    'timestamp': candidate.timestamp
                })
        
        # 4. 排序返回
        return sorted(results, key=lambda x: x['similarity'], reverse=True)
```

---

## 4. 技术实现

### 4.1 技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
**视频接入** | FFmpeg + RTSP | 多协议视频接入 |
**目标检测** | YOLOv8 | 实时目标检测 |
**行为识别** | SlowFast | 时序行为分析 |
**人脸识别** | RetinaFace + ArcFace | 检测+识别 |
**多目标跟踪** | ByteTrack | 高效跟踪 |
**边缘计算** | NVIDIA Jetson | 边缘AI推理 |
**云端分析** | Kubernetes + GPU | 大规模分析 |

### 4.2 边缘-云协同架构

```
摄像头 (120路)
    ↓ RTSP
边缘计算节点 (每节点处理8路)
    ├─ 实时目标检测 (YOLOv8)
    ├─ 行为识别 (轻量模型)
    └─ 人脸检测
    ↓ 仅上传异常事件
云端AI平台
    ├─ 深度行为分析
    ├─ 人脸识别比对
    ├─ 全局轨迹分析
    └─ 事件关联分析
    ↓
应用服务
```

### 4.3 API设计

```yaml
# 获取实时视频流
GET /api/v1/video/stream/{camera_id}
返回: WebRTC/RTMP视频流

# 获取AI分析结果
GET /api/v1/analytics/{camera_id}/realtime
返回:
  detections: [目标列表]
  events: [事件列表]
  counts: {人员计数}

# 查询历史事件
GET /api/v1/events/search
参数:
  start_time: timestamp
  end_time: timestamp
  event_types: [string]
  camera_ids: [string]
返回: 事件列表

# 自然语言视频搜索
POST /api/v1/video/search
参数:
  query: string (自然语言描述)
  time_range: {start, end}
返回:
  results: [{
    camera_id, timestamp, 
    confidence, thumbnail, video_clip
  }]

# 人脸库管理
POST /api/v1/face-library
参数:
  action: add/delete/search
  face_image: File
  identity_info: object
返回: 操作结果
```

---

## 5. 界面设计

### 5.1 监控大屏

```
┌─────────────────────────────────────────────────────────────┐
│ 🛡️ 智能安防监控中心                    2026-03-04 14:35:28   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 今日概况                                                 │
│  ┌──────────┬──────────┬──────────┬──────────┐            │
│  │ 正常监控 │ P0告警   │ P1告警   │ P2告警   │            │
│  │ 118路    │ 0        │ 2        │ 5        │            │
│  │ 🟢       │ 🔴       │ 🟡       │ 🟢       │            │
│  └──────────┴──────────┴──────────┴──────────┘            │
│                                                             │
│  🗺️ 监控点位分布                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │    [酒店平面图，摄像头点位状态]                      │   │
│  │                                                     │   │
│  │    🟢 正常  🟡 告警  🔴 紧急  ⚫ 离线               │   │
│  │                                                     │   │
│  │    1F: 🟢🟢🟢🟢🟢🟢🟢🟢                            │   │
│  │    2F: 🟢🟢🟢🟡🟢🟢🟢🟢  ← 208房走廊异常           │   │
│  │    ...                                              │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  📺 重点监控画面 (4画面轮询)                                  │
│  ┌──────────────┬──────────────┐                           │
│  │ [画面1]      │ [画面2]      │                           │
│  │ 大堂主入口   │ 前台区域     │                           │
│  │              │              │                           │
│  │ 人员: 12人   │ 人员: 5人    │                           │
│  └──────────────┴──────────────┘                           │
│  ┌──────────────┴──────────────┐                           │
│  │ [画面3 - 当前告警]           │                           │
│  │ ⚠️ 消防通道堵塞              │                           │
│  │ 位置: B1消防通道B            │                           │
│  │ [查看详情] [派单处理]        │                           │
│  └──────────────────────────────┘                           │
│                                                             │
│  📋 今日事件列表                                             │
│  时间       位置           类型           状态              │
│  14:32     B1消防通道     通道堵塞       待处理             │
│  14:28     大堂           人员聚集       已处理             │
│  14:15     2F走廊         徘徊检测       已确认(员工)       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. 成功指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
检测准确率 | >95% | 行为识别准确率 |
误报率 | <5% | 每路摄像头每天误报<2次 |
告警响应时间 | <3秒 | 从检测到推送 |
人脸识别准确率 | >98% | 1:N检索Top1 |
视频检索速度 | <10秒 | 24小时视频检索 |

---

## 7. 隐私与合规

### 7.1 隐私保护措施
- 人脸数据加密存储，仅保存特征值
- 监控画面保留30天后自动删除
- 公共区域明确标识监控提示
- 宾客要求可提供监控画面删除服务

### 7.2 合规要求
- 符合《个人信息保护法》要求
- 满足酒店行业安全标准
- 通过等保三级认证
- 支持审计日志导出

---

## 8. 实施路径

**Phase 1: 核心区域覆盖 (4周)**
- 大堂、前台、出入口
- 消防通道、电梯厅
- 基础行为检测 (入侵、跌倒)

**Phase 2: 全面覆盖 (4周)**
- 全酒店120路摄像头
- 人脸识别系统上线
- 消防合规检测

**Phase 3: 智能化升级 (4周)**
- 自然语言检索
- 视频摘要
- 预测性安防分析

---

**文档版本**: v1.0 | **创建日期**: 2026-03-04
