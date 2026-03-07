# SKILL-PRD-010: 智能排房引擎 (Smart Room Assignment Engine)

## 基本信息

| 字段 | 内容 |
|------|------|
**SKILL编号** | OPS-003
**SKILL名称** | 智能排房引擎 (Smart Room Assignment Engine)
**所属AGENT** | 核心运营AGENT (Core Ops Agent)
**版本** | v1.0
**创建日期** | 2026-03-04
**优先级** | P0 (运营效率核心)
**开发周期** | 4-6周

---

## 1. 价值定位

### 1.1 解决的问题
酒店前台排房面临多重挑战：

**排房效率低下**
- 高峰时段客人集中入住，前台手忙脚乱
- 查找合适房间耗时，客人等待时间长
- 人工排房考虑因素有限，难以全局最优

**客人满意度受损**
- 房间分配不合理(如偏好高楼层却给低楼层)
- 特殊需求被忽略(安静房间、连通房等)
- 回头客偏好未记录，体验不连贯

**运营效率损失**
- 房间未充分利用(如未能有效连续排房)
- 清洁任务分配不合理，人力浪费
- 房间状态更新滞后，超售或空置

### 1.2 核心价值
**"让每一位客人都住进'最合适'的房间，让每一间房都发挥'最大价值'"**

- **秒级排房**：AI 1秒内推荐最优房间，前台效率提升5倍
- **偏好满足**：90%+客人特殊需求被满足，满意度大幅提升
- **收益优化**：智能升级策略提升ADR，连续排房提升效率
- **动态调整**：实时响应变化，自动优化房间分配

### 1.3 量化收益

| 指标 | 传统模式 | 智能排房 | 提升幅度 |
|------|---------|---------|---------|
平均排房时间 | 2-3分钟 | <10秒 | **缩短95%** |
客人等待时间 | 5-8分钟 | 1-2分钟 | **缩短75%** |
特殊需求满足率 | 60-70% | 92%+ | **提升35%** |
房间利用率 | 85% | 92% | **+7pp** |
前台人效 | 基准值 | +200% | **提升2倍** |

---

## 2. 目标用户

### 2.1 主要用户

| 用户角色 | 使用场景 | 核心痛点 |
|---------|---------|---------|
**前台接待员** | 为客人办理入住，分配房间 | 高峰时排房慢，容易出错 |
**前台经理** | 管理房间状态，处理特殊安排 | 房间状态更新不及时，超售风险 |
**房务主管** | 安排清洁任务 | 不知道哪些房间优先清洁 |
**宾客服务经理** | 处理客人投诉和特殊需求 | 客人对房间不满意，需要换房 |

### 2.2 用户画像

**典型用户：小李，25岁，酒店前台接待员**
- 周末高峰期要同时接待5-6位客人
- 每位客人都有不同的需求(高楼层、安静、无烟等)
- 经常因为找不到合适房间而手忙脚乱
- 有时候会给错房间，导致客人投诉

---

## 3. 功能架构

### 3.1 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    应用层                                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 前台排房界面 │ │ 移动端排房   │ │ 房态看板    │            │
│  │ (PMS集成)   │ │ (经理用)     │ │ (可视化)    │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                    排房引擎层 (核心)                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 约束求解器   │ │ 偏好匹配    │ │ 优化算法    │            │
│  │ (CSP)       │ │ (评分模型)  │ │ (遗传算法)  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐                            │
│  │ 预测模型    │ │ 策略引擎    │                            │
│  │ (入住预测)  │ │ (业务规则)  │                            │
│  └─────────────┘ └─────────────┘                            │
└─────────────────────────────────────────────────────────────┘
                              ↕
└─────────────────────────────────────────────────────────────┘
│                    数据层                                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 房间档案    │ │ 客人画像    │ │ 历史数据    │            │
│  │ (属性标签)  │ │ (偏好记录)  │ │ (入住记录)  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 核心功能模块

#### 模块1: 房间档案与标签体系

**房间属性标签**
```yaml
房间基础属性:
  room_number: "1208"
  room_type: "标准间"
  floor: 12
  orientation: "南向"
  size_sqm: 32
  
设施标签:
  bed_type: "双床"
  view: "城市景观"
  bathroom: "浴缸+淋浴"
  balcony: false
  connecting_room: "1206"  # 连通房
  
环境标签:
  noise_level: "安静"  # 靠近电梯/楼梯/机房
  sunlight: "充足"
  ventilation: "良好"
  
状态标签:
  cleanliness: "已清洁"
  maintenance_status: "正常"
  last_renovation: "2025-06"
  
特殊标签:
  accessible: false  # 无障碍房间
  pet_friendly: false
  smoking: false  # 无烟房
```

**房间评分模型**
```python
class RoomScorer:
    """房间质量评分模型"""
    
    def calculate_room_score(self, room):
        """计算房间综合质量分 (0-100)"""
        
        scores = {
            # 设施新旧 (20%)
            'facility': self.score_facility(room),
            
            # 景观视野 (20%)
            'view': self.score_view(room),
            
            # 安静程度 (20%)
            'quietness': self.score_quietness(room),
            
            # 采光通风 (15%)
            'environment': self.score_environment(room),
            
            # 便利性 (15%)
            'convenience': self.score_convenience(room),
            
            # 特殊价值 (10%)
            'special': self.score_special_features(room)
        }
        
        # 加权求和
        weights = {
            'facility': 0.20,
            'view': 0.20,
            'quietness': 0.20,
            'environment': 0.15,
            'convenience': 0.15,
            'special': 0.10
        }
        
        total_score = sum(scores[k] * weights[k] for k in scores)
        
        return {
            'total_score': round(total_score, 1),
            'dimension_scores': scores,
            'quality_level': self.get_level(total_score)
        }
```

#### 模块2: 客人偏好画像

**偏好采集维度**
```yaml
客人偏好档案:
  
  基础偏好:
    preferred_floor: "高楼层"  # 高/中/低/无所谓
    preferred_orientation: "南向"
    bed_type: "大床"  # 大床/双床/无所谓
    view_preference: "景观房"
  
  环境偏好:
    quietness: "非常安静"  # 安静程度要求
    sunlight: "充足阳光"
    away_from_elevator: true
    away_from_ice_machine: true
  
  设施需求:
    bathtub_required: true
    balcony_preferred: false
    connecting_room_needed: false
    accessible_required: false
  
  特殊需求:
    allergies: ["羽绒"]  # 过敏源
    occasion: "蜜月"  # 入住场合
    vip_status: "金卡会员"
  
  历史记录:
    previous_rooms: ["1508", "1608", "1506"]
    satisfaction_history: [5, 5, 4]
    complaints: ["上次房间靠近电梯有点吵"]
```

**偏好匹配算法**
```python
class PreferenceMatcher:
    """客人偏好与房间匹配"""
    
    def match(self, guest_profile, available_rooms):
        """
        为客人匹配最合适的房间
        
        返回: 按匹配度排序的房间列表
        """
        
        matches = []
        
        for room in available_rooms:
            match_score = 0
            match_details = []
            
            # 1. 楼层偏好匹配 (权重20%)
            if guest_profile.get('preferred_floor'):
                floor_score = self.match_floor(
                    room['floor'], 
                    guest_profile['preferred_floor']
                )
                match_score += floor_score * 0.20
                match_details.append({
                    'factor': '楼层偏好',
                    'score': floor_score,
                    'detail': f"房间在{room['floor']}层"
                })
            
            # 2. 安静需求匹配 (权重25%)
            if guest_profile.get('quietness') == '非常安静':
                quiet_score = 100 if room['noise_level'] == '安静' else 50
                match_score += quiet_score * 0.25
                match_details.append({
                    'factor': '安静需求',
                    'score': quiet_score,
                    'detail': f"房间噪音等级: {room['noise_level']}"
                })
            
            # 3. 床型匹配 (权重15%)
            if guest_profile.get('bed_type'):
                bed_score = 100 if room['bed_type'] == guest_profile['bed_type'] else 0
                match_score += bed_score * 0.15
            
            # 4. 景观匹配 (权重15%)
            if guest_profile.get('view_preference'):
                view_score = self.match_view(
                    room['view'],
                    guest_profile['view_preference']
                )
                match_score += view_score * 0.15
            
            # 5. 历史满意度 (权重10%)
            if room['room_number'] in guest_profile.get('previous_rooms', []):
                history_score = 100
                match_score += history_score * 0.10
                match_details.append({
                    'factor': '历史入住',
                    'score': 100,
                    'detail': '客人曾入住此房并满意'
                })
            
            # 6. 特殊需求 (权重15%)
            special_score = self.match_special_requirements(
                room, guest_profile
            )
            match_score += special_score * 0.15
            
            matches.append({
                'room': room,
                'match_score': round(match_score, 1),
                'details': match_details
            })
        
        # 按匹配度排序
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        return matches
```

#### 模块3: 智能排房引擎

**约束条件定义**
```python
class RoomAssignmentConstraints:
    """排房约束条件"""
    
    def get_constraints(self, context):
        """获取当前排房场景的约束条件"""
        
        constraints = {
            # 硬约束 (必须满足)
            'hard': [
                # 房间必须可用
                lambda r: r['status'] == 'available',
                
                # 房间类型匹配
                lambda r, b: r['room_type'] == b['room_type'],
                
                # 无烟房需求
                lambda r, g: not g.get('non_smoking') or r['smoking'] == False,
                
                # 无障碍需求
                lambda r, g: not g.get('accessible_required') or r['accessible'] == True,
            ],
            
            # 软约束 (尽量满足)
            'soft': [
                # 楼层偏好
                {'weight': 20, 'func': self.floor_preference_constraint},
                
                # 安静需求
                {'weight': 25, 'func': self.quietness_constraint},
                
                # 连通房需求
                {'weight': 30, 'func': self.connecting_room_constraint},
                
                # 景观偏好
                {'weight': 15, 'func': self.view_constraint},
                
                # 历史满意度
                {'weight': 10, 'func': self.history_constraint},
            ]
        }
        
        return constraints
```

**排房优化算法**
```python
class SmartRoomAssignment:
    """智能排房核心算法"""
    
    def __init__(self):
        self.scorer = RoomScorer()
        self.matcher = PreferenceMatcher()
        self.constraints = RoomAssignmentConstraints()
    
    def assign_rooms(self, booking_requests, available_rooms, context):
        """
        批量房间分配优化
        
        目标: 最大化总体满意度 + 房间利用率
        """
        
        # 1. 过滤不满足硬约束的房间
        valid_assignments = self.filter_by_hard_constraints(
            booking_requests, 
            available_rooms
        )
        
        # 2. 计算每对(预订,房间)的匹配分
        scores = {}
        for request in booking_requests:
            scores[request['id']] = {}
            for room in valid_assignments[request['id']]:
                match_result = self.matcher.match(
                    request['guest_profile'], 
                    [room]
                )
                scores[request['id']][room['room_number']] = match_result[0]['match_score']
        
        # 3. 使用匈牙利算法/遗传算法求解最优分配
        optimal_assignment = self.solve_assignment_optimization(
            booking_requests,
            available_rooms,
            scores
        )
        
        # 4. 生成排房结果
        assignments = []
        for request in booking_requests:
            assigned_room = optimal_assignment.get(request['id'])
            
            assignments.append({
                'booking_id': request['id'],
                'guest_name': request['guest_name'],
                'assigned_room': assigned_room,
                'match_score': scores[request['id']][assigned_room['room_number']],
                'reasoning': self.explain_assignment(request, assigned_room)
            })
        
        return assignments
    
    def solve_assignment_optimization(self, requests, rooms, scores):
        """
        使用约束满足问题(CSP)求解最优分配
        """
        from ortools.constraint_solver import routing_enums_pb2
        from ortools.constraint_solver import pywrapcp
        
        # 构建CSP模型
        model = cp_model.CpModel()
        
        # 创建变量: request[i] 分配到哪个房间
        assignments = {}
        for i, request in enumerate(requests):
            assignments[i] = model.NewIntVar(
                0, len(rooms) - 1, f'request_{i}_room'
            )
        
        # 添加约束: 一个房间只能分配给一个人
        model.AddAllDifferent(assignments.values())
        
        # 目标: 最大化总匹配分数
        objective_terms = []
        for i, request in enumerate(requests):
            for j, room in enumerate(rooms):
                score = scores[request['id']][room['room_number']]
                # 使用条件变量
                is_assigned = model.NewBoolVar(f'is_assigned_{i}_{j}')
                model.Add(assignments[i] == j).OnlyEnforceIf(is_assigned)
                model.Add(assignments[i] != j).OnlyEnforceIf(is_assigned.Not())
                objective_terms.append(score * is_assigned)
        
        model.Maximize(sum(objective_terms))
        
        # 求解
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            result = {}
            for i, request in enumerate(requests):
                room_idx = solver.Value(assignments[i])
                result[request['id']] = rooms[room_idx]
            return result
        else:
            # 无可行解，使用贪心算法兜底
            return self.greedy_assignment(requests, rooms, scores)
```

#### 模块4: 前台排房界面

**智能推荐界面**
```
┌─────────────────────────────────────┐
│ 🏨 智能排房系统                      │
├─────────────────────────────────────┤
│                                     │
│  👤 当前客人                         │
│  姓名: 张先生                       │
│  房型: 标准间大床房                 │
│  会员: 金卡                         │
│                                     │
│  📋 已知偏好:                        │
│  ├─ 偏好高楼层                      │
│  ├─ 要求安静房间                    │
│  ├─ 曾入住1508(满意)               │
│  └─ 本次: 蜜月旅行                  │
│                                     │
│  💡 AI推荐房间 (已按匹配度排序)       │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 推荐1: 1508房    [匹配度98%]│   │
│  │ ─────────────────────────── │   │
│  │ 楼层: 15F (高楼层) ✓        │   │
│  │ 噪音: 安静 ✓                │   │
│  │ 景观: 城市夜景 ✓            │   │
│  │ 特色: 客人曾入住并好评 ✓    │   │
│  │ ─────────────────────────── │   │
│  │ [确认分配] [查看详情]       │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 推荐2: 1606房    [匹配度85%]│   │
│  │ 楼层: 16F (高楼层) ✓        │   │
│  │ 噪音: 安静 ✓                │   │
│  │ 景观: 园景                  │   │
│  │ [确认分配] [查看详情]       │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 推荐3: 1412房    [匹配度72%]│   │
│  │ ...                         │   │
│  └─────────────────────────────┘   │
│                                     │
│  [手动选择房间] [修改偏好]          │
│                                     │
└─────────────────────────────────────┘
```

**批量排房界面**
```
┌─────────────────────────────────────────────────────────────┐
│ 🏨 批量排房 - 今日预计入住 45人                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 房间状态概览                                             │
│  ┌──────────┬──────────┬──────────┬──────────┐            │
│  │ 总房间   │ 已预订   │ 已分配   │ 待分配   │            │
│  │  200     │   45     │   12     │   33     │            │
│  └──────────┴──────────┴──────────┴──────────┘            │
│                                                             │
│  📋 待分配客人列表                                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 客人    房型      特殊需求        推荐房间   操作   │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ 张先生  标准间    高楼层/安静     1508(98%)  [分配]│   │
│  │ 李女士  大床房    无烟房/景观     1610(92%)  [分配]│   │
│  │ 王先生  双床房    连通房需求      1208+1206  [分配]│   │
│  │ ...                                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [一键智能排房] [批量分配] [导出列表]                        │
│                                                             │
│  💡 智能建议:                                                │
│  ├─ 今日有3对蜜月客人，建议优先分配景观房                   │
│  ├─ 1510房连续3天可排，建议分配给长住客                     │
│  └─ 晚间有VIP入住，建议预留3间高层套房                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 模块5: 预测性排房优化

**入住预测与提前排房**
```python
class PredictiveRoomAssignment:
    """预测性排房优化"""
    
    def optimize_future_assignments(self, horizon=7):
        """
        基于预测优化未来7天的房间分配
        
        策略:
        1. 识别可以连续排房的房间
        2. 预留VIP/特殊需求房间
        3. 优化清洁任务分配
        """
        
        # 获取未来预订
        future_bookings = self.get_bookings(
            checkin_date__gte=today,
            checkin_date__lt=today + timedelta(days=horizon)
        )
        
        # 分析连续性机会
        continuity_opportunities = self.find_continuity_opportunities(
            future_bookings
        )
        
        # 预分配策略
        pre_assignments = {}
        
        for opportunity in continuity_opportunities:
            # 连续多天的预订尽量安排同一房间
            room = self.find_optimal_room_for_continuity(opportunity)
            for booking in opportunity['bookings']:
                pre_assignments[booking['id']] = room
        
        # VIP和特殊需求预留
        vip_bookings = [b for b in future_bookings if b['is_vip']]
        for booking in vip_bookings:
            best_rooms = self.get_best_rooms(5)  # 前5好房间
            pre_assignments[booking['id']] = best_rooms
        
        return pre_assignments
```

**清洁任务优化**
```python
class HousekeepingOptimizer:
    """清洁任务智能分配"""
    
    def optimize_cleaning_schedule(self, checkouts, staff):
        """
        优化退房清洁任务分配
        
        目标: 最小化清洁时间，最大化房间可用性
        """
        
        # 1. 按优先级排序退房房间
        prioritized_rooms = self.prioritize_rooms(checkouts)
        
        # 2. 考虑因素:
        # - 房间类型 (套房>标准间)
        # - 预计清洁时间
        # - 楼层分布 (减少员工走动)
        # - 客人入住时间 (优先清洁早入住的房间)
        
        # 3. 生成清洁任务清单
        tasks = []
        for room in prioritized_rooms:
            tasks.append({
                'room_number': room['room_number'],
                'priority': room['priority'],
                'estimated_time': self.estimate_cleaning_time(room),
                'assigned_to': None,
                'deadline': room['next_checkin_time'] - timedelta(minutes=30)
            })
        
        # 4. 分配给清洁员
        assignments = self.assign_to_staff(tasks, staff)
        
        return assignments
```

---

## 4. 技术实现

### 4.1 技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
**约束求解** | OR-Tools | Google优化工具 |
**匹配算法** | Python + NumPy | 相似度计算 |
**前端** | Vue3 + ElementUI | 排房界面 |
**数据库** | PostgreSQL | 房间/客人数据 |
**缓存** | Redis | 实时房态 |
**集成** | PMS API | 酒店管理系统 |

### 4.2 PMS集成

```python
class PMSIntegration:
    """PMS系统集成"""
    
    def sync_room_status(self):
        """同步房间状态"""
        # 从PMS获取最新房态
        room_status = self.pms_api.get_room_status()
        
        # 更新本地缓存
        for room in room_status:
            self.cache.set(f"room:{room['number']}:status", room['status'])
    
    def assign_room(self, booking_id, room_number):
        """分配房间到预订"""
        result = self.pms_api.assign_room(
            booking_id=booking_id,
            room_number=room_number
        )
        
        # 更新本地状态
        self.cache.set(f"room:{room_number}:status", "occupied")
        
        return result
```

---

## 5. 成功指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
平均排房时间 | <10秒 | 从查询到推荐 |
偏好满足率 | >90% | 客人特殊需求 |
房间利用率 | >92% | 对比传统方式 |
前台效率提升 | >150% | 每小时办理入住数 |
换房率降低 | <5% | 因房间不满意换房 |

---

## 6. 实施路径

**Phase 1: 基础版 (3周)**
- 房间档案系统
- 基础匹配算法
- 前台界面开发

**Phase 2: 智能版 (3周)**
- 客人偏好画像
- 约束求解优化
- PMS系统集成

**Phase 3: 预测版 (2周)**
- 预测性排房
- 清洁任务优化
- 数据分析报表

---

**文档版本**: v1.0 | **创建日期**: 2026-03-04
