# TB6 R5 机械臂全面参考手册

> 基于泰科智能（贞实科技 TRUE）TB6 R5 协作机器人，整合指令手册 V1.7.4 + 用户手册 VG1.2 + Web 使用手册 V1.7.2 + 建模手册 V1.2 + URDF 模型 + 实际例程，适合零基础查阅。

---

## 目录

- [一、文档版本与关键改动](#一文档版本与关键改动)
- [二、设备速查](#二设备速查)
- [三、网络连接](#三网络连接)
- [四、通信架构](#四通信架构)
- [五、控制器状态机（初始化序列）](#五控制器状态机初始化序列)
- [六、变量系统](#六变量系统)
- [七、基础运动指令](#七基础运动指令)
- [八、在线规划指令](#八在线规划指令)
- [九、常用系统指令](#九常用系统指令)
- [十、高级规划指令（轨迹融合）](#十高级规划指令轨迹融合)
- [十一、力控指令](#十一力控指令)
- [十二、常见奇异点](#十二常见奇异点)
- [十三、Topic 状态订阅](#十三topic-状态订阅)
- [十四、Web 界面操作](#十四web-界面操作)
- [十五、图形化编程（Blockly）](#十五图形化编程blockly)
- [十六、工具与工件坐标系标定](#十六工具与工件坐标系标定)
- [十七、动力学辨识与手动拖动](#十七动力学辨识与手动拖动)
- [十八、工艺包（Web 端）](#十八工艺包web-端)
- [十九、关节链与 URDF 参数](#十九关节链与-urdf-参数)
- [二十、IO 与硬件接口](#二十io-与硬件接口)
- [二十一、驱动器报错代码](#二十一驱动器报错代码)
- [二十二、排错速查](#二十二排错速查)
- [二十三、Python 代码模板](#二十三python-代码模板)

---

## 一、文档版本与关键改动

### 1.1 版本修订历史

| 版本 | 修订日期 |
|------|----------|
| 1.3 | 2025-08-21 |
| 1.4 | 2025-08-30 |
| 1.5 | 2025-09-18 |
| 1.6 | 2025-10-14 |
| 1.7 | 2025-10-28 |
| 1.7.1 | 2025-12-15 |
| 1.7.2 | 2025-12-30 |
| 1.7.3 | 2026-01-16 |
| 1.7.4 | 2026-01-22 |

### 1.2 版本关键改动

| 版本 | 改动内容 |
|------|----------|
| **V1.5** | 底层架构使用 1.3.18 版本，驱动版本最低 1.3.4；JogJ、JogJ1-6、MoveAbsJ 删去加速度等参数，与速度匹配，**简化指令结构** |
| **V1.6** | 底层使用 1.3.20，驱动最低 1.3.6；**MoveAbsJ 的 Tool、Wobj、Load 参数删除** |
| **V1.7.1** | MoveSeriesToppJ 改为 MoveSeriesToppJ2；JogWithSP、MoveJ、MoveBlend 的 load/wobj/tool 参数删除 |
| **V1.7.2** | **Var 新增 `--degree_unit` 参数**，支持角度输入 |
| **V1.7.3** | **合并力控相关指令**；更新部分指令及参数 |
| **V1.7.4** | 最新版本（当前） |

---

## 二、设备速查

### 2.1 TB6-R5 基本信息

| 项目 | 值 |
|------|-----|
| 品牌/厂商 | 泰科智能 / 贞实科技 (TRUE Techsoft Robots) |
| 型号 | 7260501-000000-001 TB6-R5-RevA1 |
| 关节数 | 6（全部旋转关节，revolute） |
| 自由度 | 6 |
| 工作半径 | 933 mm |
| 自重 | ~23 kg（机械臂本体） |
| 最大有效荷载 | 5 kg |
| 重复定位精度 | < ±0.05 mm |
| 供电 | 48V DC（机械臂）/ 220V AC（控制柜） |
| 通信 | 控制器 ↔ 机械臂：EtherCAT；电脑 ↔ 控制器：TCP/IP |
| 防护等级 | IP64 |
| 额定寿命 | 20000 h |
| 环境温度 | -20 ~ 45°C |
| 环境湿度 | 25% ~ 85% 无冷凝 |
| 噪音 | ≤60 dB |
| Python | 3.10（必须，`.pyd` 编译绑定） |
| 抱闸类型 | 24/12V DC 电磁摩擦式 |
| 安装方式 | 任意角度（正装/壁装/吊装/侧装） |

### 2.2 TB6 全系列对比

| 型号 | 自重 | 最大荷载 | 臂展 | 功耗 |
|------|------|----------|------|------|
| TB6-R3 | 11.5 kg | 3 kg | 550 mm | ~150W |
| **TB6-R5** | **23 kg** | **5 kg** | **933 mm** | **~300W** |
| TB6-R10 | 37 kg | 10 kg | 1333 mm | ~500W |
| TB6-R20L | 60 kg | 20 kg | 1500 mm | ~960W |

### 2.3 TB6-R5 关节极限

| 关节 | 范围 | 最大速度 | 备注 |
|------|------|----------|------|
| J1 | ±180° (±3.1416 rad) | 150°/s | 底座旋转 |
| J2 | ±180° (±3.1416 rad) | 150°/s | 肩部 |
| J3 | ±164° (±2.8623 rad) | 150°/s | **受限关节** |
| J4 | ±180° (±3.1416 rad) | 180°/s | 肘部 |
| J5 | ±180° (±3.1416 rad) | 180°/s | 腕部 |
| J6 | ±180° (±3.1416 rad) | 180°/s | 末端旋转 |

末端最大速度：≤2 m/s

### 2.4 TB6-R5 各连杆质量（来自 URDF）

| 连杆 | 质量 |
|------|------|
| base_link | 5.049 kg |
| Link1 | 13.203 kg |
| Link2 | 46.802 kg |
| Link3 | 20.240 kg |
| Link4 | 4.614 kg |
| Link5 | 4.768 kg |
| ee_Link | 2.546 kg |
| **合计** | **~97.2 kg** |

---

## 三、网络连接

### 3.1 IP 地址

- Web 界面默认 URL：`192.168.11.11`
- 控制器默认 IP：`192.168.11.11`（X16 网口 NIC3）
- PC 端静态 IP 示例：`192.168.11.12`，子网掩码 `255.255.255.0`，默认网关 `192.168.11.1`
- **实际 IP 以 Web 界面或示教器网络配置页面看到的为准**

### 3.2 端口

| 端口 | 协议 | 用途 | Python 库 |
|------|------|------|-----------|
| `5868` | TCP (Protobuf) | RPC 下发指令 | `rpc.pyd` |
| `19091` | TCP (ZMQ Pub/Sub) | Topic 订阅状态 | `topic.pyd` |

### 3.3 双网络方案

用网线或 USB 无线网卡让 PC 同时连机械臂 WiFi + 互联网，互不干扰。

测试端口连通性：
```python
import socket
s = socket.socket(); s.settimeout(3)
r = s.connect_ex(('192.168.50.1', 5868))
print('OK' if r == 0 else f'不通({r})')
s.close()
```

---

## 四、通信架构

### 4.1 整体架构

```
┌─────────────────────────────────┐
│         你的 Python 程序           │
│   import rpc       import topic  │
│      │                  │        │
│   Protobuf           ZMQ/Protobuf│
│   TCP:5868          TCP:19091    │
│      │                  │        │
│   ┌──┴──────────────────┴──┐     │
│   │      机械臂控制器         │     │
│   │   (EtherCAT ↔ 关节电机)  │     │
│   └────────────────────────┘     │
└─────────────────────────────────┘
```

### 4.2 RPC 通信（发指令）

- **同步调用 `CallAwait`**：发送指令，等待指令执行完成才返回（阻塞）
- **异步调用 `CallAsync`**：发送指令立即返回，不等待执行完成（非阻塞），结果通过回调接收
- 每条 RPC 指令需设置 `msgID` 和 `msgSeqID`

### 4.3 Topic 通信（收状态）

- **`system_rtstate`**（实时状态）：高频推送，含关节位置/力矩/使能状态/TCP 位姿/六维力等
- **`system_nrtstate`**（非实时状态）：低频推送，含关节限位/工具列表/工件列表/负载列表/示教点/从站状态等
- 通过 `topic.Node` 创建节点，`CreateSubscriptionRT` / `CreateSubscriptionNRT` 订阅

---

## 五、控制器状态机（初始化序列）

机械臂必须经过初始化序列才能运动，**顺序不可乱**：

```
Clear → Disable → Mode → SetMaxToq → Recover → SetRate → Enable
 清错    下电     设模式    设力矩上限    同步      设速率     上电
```

### 5.1 每条指令的作用与参数

| 序号 | 指令 | 作用 | 默认参数 |
|------|------|------|----------|
| 1 | `{Clear}` | 清除 ERROR 级错误（不清除 Var 变量） | 无参数 |
| 2 | `{Disable}` | 关节下电（刹车抱闸） | `--all --limit_time=5000` |
| 3 | `{Mode}` | 设工作模式：8=CSP(位置), 9=CSV(速度), 10=CST(力矩) | `--all --mode=8` |
| 4 | `{SetMaxToq}` | 设最大力矩上限 | — |
| 5 | `{Recover}` | 同步模型状态与实际状态（CST→CSP 前必调） | 无参数 |
| 6 | `{SetRate}` | **全局速度百分比（1-100），不给值默认为极慢** | 建议 `{SetRate 30}` 起步 |
| 7 | `{Enable}` | 关节上电（使能，释放抱闸） | `--all --limit_time=5000` |

### 5.2 Mode 模式说明

| 模式编号 | 名称 | 含义 | 适用场景 |
|----------|------|------|----------|
| 8 | CSP | 周期同步位置模式 | 一般运动（最常用） |
| 9 | CSV | 周期同步速度模式 | 速度控制 |
| 10 | CST | 周期同步力矩模式 | 力矩控制/拖动示教 |

### 5.3 控制模式切换注意

- CST → CSP 前必须先 `{Recover}`，否则无法通过 Show 指令获取机器人当前实际状态
- 任一模式切换失败会抛出 WARNING 级别异常

---

## 六、变量系统

所有运动指令都用变量名引用目标。Var 变量是**临时的，重启丢失**；要持久化使用 `DefineParam`。

### 6.1 变量类型速查

#### 6.1.1 load（负载变量）

```
Var --type=load --name=piece --value={mass, mass*cogx, mass*cogy, mass*cogz, 0, 0, 0, 0, 0, 0}
```

- 10 个 double 参数，描述末端负载质量分布特性
- `mass`：质量 (kg)
- `cogx, cogy, cogz`：质心在基坐标系下 x, y, z 方向偏移量 (m)
- 后 6 个为惯性张量矩阵参数 (ixx, iyy, izz, ixy, ixz, iyz)，无数据写 0
- 坐标系默认为末端法兰盘坐标系
- **注意**：添加负载后 SetPayload 时，需将基坐标系绕 Z 轴旋转 180° 计算（参考建模手册）

#### 6.1.2 jointtarget（关节目标）—— 最常用

```
Var --type=jointtarget --name=J --value={J0,J1,J2,J3,J4,J5,J6,J7,J8,J9}
```

- 10 个 double 参数：前 6 个（J0-J5）为关节角度 (rad)，后 4 个为外部轴位置 (m 或 rad)
- 目标关节角度与外部轴总数不得超过 10 个
- 加 `--degree_unit=1` 可用**角度**输入：
  ```
  Var --type=jointtarget --name=j1 --value={10,-30,0,0,0,0,0,0,0,0} --degree_unit=1
  ```
- `--degree_unit=0`（默认）表示 value 单位为弧度

#### 6.1.3 robottarget（笛卡尔目标）—— 给定 XYZ 位置

```
Var --type=robottarget --name=p1 --value={x, y, z, q1, q2, q3, q4}
```

- 7 个 double：x, y, z 位置 (m) + q1, q2, q3, q4 四元数 (对应 x, y, z, w)
- 适用于 MoveJ / MoveL / MoveC 指令

#### 6.1.4 speed（速度参数）

```
Var --type=speed --name=v50 --value={per, tcp, ori, exj_r, exj_l}
```

- `per`：关节速度百分比（相对 max_vel，如 0.1 表示 max_vel 的 10%）
- `tcp`：末端线速度 (m/s)
- `ori`：旋转速度 (rad/s)
- `exj_l`：外部轴线速度
- `exj_r`：外部轴角速度
- XML 中有预设 speed：如 `v100={0.1, 0.1, 3.4906585, 0, 0}`

#### 6.1.5 zone（转弯区 / 融合区）

```
Var --type=zone --name=z5 --value={distance_mm, percent}
```

- `distance`：笛卡尔转弯区大小 (mm)，适用于 MoveL 等
- `percent`：转弯区占运动时间百分比，适用于 MoveJ/MoveL/MoveC
- 转弯区不能超过前后两条待融合路径长度的一半（超过自动缩小）
- 转弯区时间不能超过前后运动时间的一半
- 使用转弯区**避免频繁启停**，显著减少节拍时间

**预设 Zone 值对照表**：

| 名称 | distance(mm) | percent |
|------|-------------|---------|
| z1 | 0.001 | 0.01 |
| z5 | 0.005 | 0.03 |
| z10 | 0.01 | 0.05 |
| z15 | 0.015 | 0.08 |
| z20 | 0.02 | 0.1 |
| z30 | 0.03 | 0.15 |
| z40 | 0.04 | 0.2 |
| z50 | 0.05 | 0.25 |
| z60 | 0.06 | 0.3 |
| z80 | 0.08 | 0.4 |
| z100 | 0.1 | 0.45 |
| z150 | 0.2 | 0.45 |
| z200 | 0.06 | 0.3 |

#### 6.1.6 tool（工具坐标系）

```
Var --type=tool --name=t1 --value={hold, x, y, z, q1, q2, q3, q4}
```

- 记录工具 TCP、姿态
- `hold`：布尔值（true=1, false=0），是否启用
- `x, y, z`：TCP 相对法兰盘坐标系偏移量 (mm)
- `q1-q4`：工具坐标系相对法兰坐标系的姿态四元数
- `pose` 子结构：`pose1={x, y, z, q1, q2, q3, q4}`
- 支持固定工具世界坐标系定义

#### 6.1.7 wobj（工件/基坐标系）

```
Var --type=wobj --name=w1 --value={x, y, z, q1, q2, q3, q4}
```

- 所有运动指令中的位置在工件坐标系下定义
- 未指定时默认在世界坐标系 `wobj0` 下

### 6.2 变量管理指令

#### 6.2.1 Var —— 定义变量

```
Var --type=<类型> --name=<名称> --value=<值> [--degree_unit=0|1]
Var --clear  // 清除所有 Var 变量
```

- 支持类型：`Number`, `Matrix`, `String`, `pos`, `orient`, `pose`, `speed`, `robottarget`, `zone`, `jointtarget`, `tool`, `wobj`
- value 可以是单个值，也可用大括号包含的矩阵
- Var 为临时变量，**重启后不保存**
- 调用方式：`--jointtarget_var`、`--robottarget_var`、`--speed_var` 等
- 变量名不支持纯数字，需以英文字母开头
- `--degree_unit=1` 仅 jointtarget 类型有效
- **Var --clear**：清除所有 Var 变量（不影响 DefineParam 定义的参数）

#### 6.2.2 DeleteVar —— 删除变量

```
DeleteVar --name=<变量名>
```

- 删除单个变量
- 也可用 `Var --clear` 统一清除所有 Var 变量

#### 6.2.3 DisplayVar —— 打印变量

```
DisplayVar --type=<类型> --name=<变量名>
```

- 打印结果通过**驱动日志**查看

#### 6.2.4 ReVarValue —— 变量重赋值

```
ReVarValue --type=<类型> --name=<变量名> --value=<新值>
```

- 匹配原变量类型和名称

#### 6.2.5 DefineParam —— 定义参数（持久化）

```
DefineParam --type=<类型> --name=<名称> --value=<值>
```

- 支持类型与 Var 一致
- 参数持久化，重启后保留

#### 6.2.6 DeleteParam —— 删除参数

```
DeleteParam --name=<参数名>
```

#### 6.2.7 RenameParam —— 参数重命名

```
RenameParam --raw_name=<原名称> --new_name=<新名称> --type=<类型>
```

---

## 七、基础运动指令

### 7.1 Enable —— 上使能

```
Enable [--all | --motion_id=<i>] [--limit_time=<ms>] [--load=<load> | --load_var=<load_var>]
```

- 使能全部或指定伺服电机
- `--limit_time`：超时时间 (ms)，超时未完成抛出 ERROR
- `--all`：所有电机；`--motion_id=i`：第 i+1 个电机
- 默认等价：`Enable --all --limit_time=5000 --load=load0`
- 示例：
  ```
  Enable
  Enable --motion_id=0 --limit_time=4000 --load_var=load1
  ```

### 7.2 Disable —— 下使能

```
Disable [--all | --motion_id=<i>] [--limit_time=<ms>] [--load_var=<load_var>]
```

- 参数和用法同上使能
- 默认等价：`Disable --all --limit_time=5000 --load=load0`
- 下使能后电机进入抱闸状态

### 7.3 Recover —— 状态同步

```
Recover
```

- 无参数
- 同步模型状态与实际被控对象状态
- **CST → CSP 前必须使用**
- 初始化序列中也调用一次

### 7.4 Start —— 启动

```
Start [--last_count=<N>]
```

- 将被 Pause/Stop 暂停或停止的运动重新启动
- `--last_count`：重启到位的控制周期数（默认 10）
- **Start 与 Stop 一一对应**

### 7.5 Stop —— 紧急停止

```
Stop [--last_count=<N>]
```

- 停止运动，跳出当前指令，**后续缓冲指令均不执行**
- `--last_count`：完全停止所需的控制周期数（默认 10）
- 多条指令阻塞调用时，一个 Stop 只能终止一条指令
- 可用于紧急停止

### 7.6 Pause —— 暂停

```
Pause [--last_count=<N>]
```

- 暂停运动，**不跳出指令**，Start 后可继续
- `--last_count`：完全暂停所需的控制周期数（默认 10）
- 后续缓冲指令**会继续执行**（与 Stop 关键区别）

### 7.7 JogJoint —— 关节点动

```
JogJoint --speed=<speed_var> --motion_id=<0~5> --direction=<1|-1> [--increase_count=<N>]
```

- `--motion_id`：0~5 对应 joint1~joint6
- `--direction`：1=正方向，-1=反方向
- `--increase_count`：加速过程周期数
- `--speed`：关节速度 (rad/s)
- 示例：
  ```
  JogJoint --speed=v100 --motion_id=0 --increase_count=50 --direction=1
  JogJoint --speed=v100 --motion_id=1 --increase_count=50 --direction=-1
  ```

### 7.8 MoveAbsJ —— 关节空间绝对运动（最常用）

```
MoveAbsJ --jointtarget_var=<j_var> [--speed=<s> | --speed_var=<s_var>] [--zone=<z> | --zone_var=<z_var>]
```

- 关节同时到达目标角度，沿非线性路径运动
- **同步模式**：指令等运动完成才返回
- V1.6 起 Tool、Wobj、Load 参数已删除
- 示例：
  ```
  MoveAbsJ --jointtarget_var=j0
  MoveAbsJ --jointtarget_var=j1 --speed=v200
  ```

### 7.9 JogCartesian —— 笛卡尔点动

```
JogCartesian --moving_type=<0~5> --direction=<1|-1> --speed=<speed_var> --coordinate=<0|1> [--increase_count=<N>]
```

- `--moving_type`：0=X, 1=Y, 2=Z(平动)；3=RX, 4=RY, 5=RZ(转动)
- `--coordinate`：0=世界坐标系，1=工具坐标系
- `--speed`：六维笛卡尔速度 (m/s 平动 / rad/s 转动)
- 示例：
  ```
  JogCartesian --moving_type=0 --direction=1 --speed=v100 --coordinate=0 --increase_count=50
  JogCartesian --moving_type=3 --direction=1 --speed=v100 --coordinate=0 --increase_count=50
  ```

### 7.10 SpeedL —— 笛卡尔空间速度控制（在线规划）

```
SpeedL --vel={vx,vy,vz,wx,wy,wz} --acc={ax,ay,az,awx,awy,awz} --jerk={jx,jy,jz,jwx,jwy,jwz} --last_count=<N> [--coordinate=<0|1>]
```

- 持续以给定速度运动，**可被异步打断**——发新 SpeedL 即切换速度
- `--last_count`：指令保留时间（控制周期数，≈ms）
- `--coordinate`：0=基坐标系，1=工具坐标系
- `--vel`：六维速度 {vx,vy,vz, wx,wy,wz}，单位 m/s 和 rad/s
- 加 `--stop` 平滑减速停止
- 示例：
  ```
  SpeedL --vel={0.1,0,0,0,0,0} --acc={2,2,2,2,2,2} --jerk={5,5,5,5,5,5} --last_count=100 --coordinate=0
  SpeedL --vel={-0.1,0,0,0,0,0} --acc={2,2,2,2,2,2} --jerk={5,5,5,5,5,5} --last_count=100 --coordinate=0
  ```

### 7.11 MoveJ —— 笛卡尔坐标逆解→关节运动

```
MoveJ --robottarget_var=<p_var> [--speed=<s> | --speed_var=<s_var>] [--acc=<a>] [--dec=<d>] [--jerk=<j>] [--zone=<z>]
```

- 给 XYZ 位置，控制器自动逆解算关节角
- **不适用于七轴机械臂**
- 有姿态变化时比 MoveAbsJ 慢
- V1.7.1 起 load、wobj、tool 参数已删除
- 示例：
  ```
  MoveJ --robottarget_var=p0 --zone=z5 --acc=5 --jerk=20
  MoveJ --robottarget_var=p0 --speed=v200 --acc=6 --dec=-6 --jerk=18
  ```

---

## 八、在线规划指令

在线规划指令支持**运行中实时更改**运动目标。

### 8.1 SpeedJ —— 关节空间速度控制（在线规划）

```
SpeedJ --vel={jv1,jv2,...} --acc={ja} --dec={jd} --jerk={jj} --last_count=<N>
SpeedJ --stop
```

- 设置一组关节期望速度、最大加速度、最大加加速度
- 可再用本指令发新的期望运动实时更改关节运动
- 默认参数 `--stop`（指令无后缀默认将速度减为 0 退出）
- **同步调用**：运行完整 last_count
- **异步调用**：可打断正在执行的运动，进行新运动，运动时间为下发间隔时间
- 示例：
  ```
  SpeedJ --vel={0.1} --acc={10} --dec={10} --jerk={10} --last_count=1000
  # 等待 ~950ms 后
  SpeedJ --vel={-0.1} --acc={10} --dec={10} --jerk={10} --last_count=1000
  SpeedJ --stop
  ```

### 8.2 JogAnyJ —— 关节位置（在线规划）

```
JogAnyJ --joint_pos={p1,p2,...} --joint_vel={v} --joint_acc={a} [--joint_dec={d}] [--last_count=<N>]
```

- 设置一组关节期望位置，实时规划连续轨迹
- 可再次发新指令实时更改
- 到达期望位置后开始自动退出计时，`last_count` 后自动退出
- **同步调用**：运行到目标点；**异步调用**：可打断
- 示例：
  ```
  JogAnyJ --joint_pos={0.2,0.2,0.2,0.3,0.6,0.2,0.6} --joint_vel={0.3} --joint_acc={1}
  # 等待 ~950ms 后在线更改
  JogAnyJ --joint_pos={-0.2,-0.2,-0.2,0.1,-0.6,-0.2,-0.6} --joint_vel={0.1} --joint_acc={1}
  ```

---

## 九、常用系统指令

### 9.1 Mode —— 模式设置

```
Mode [--all | --motion_id=<i>] [--mode=<8|9|10>] [--limit_time=<ms>] [--load_var=<load>]
```

- 仅支持 8(CSP) / 9(CSV) / 10(CST)，其他值抛出 WARNING
- 默认：`Mode --all --limit_time=5000 --load=load0 --mode=8`

### 9.2 Clear —— 错误清理

```
Clear
```

- 清除异常等级为 ERROR 的异常，恢复系统正常状态
- **不会清除 Var 变量**
- 无参数

### 9.3 SetPayload —— 设置负载

```
SetPayload --load_var=<load_var> [--part_id=-1]
```

- 负载设定以**基坐标系为参考基准**，以关节 0 位时位姿进行设置与运算
- 数据格式：{m, m×x, m×y, m×z, 0, 0, 0, 0, 0, 0}
- 实际操作时可在 m×h 前乘以调整系数
- 示例：
  ```
  Var --type=load --name=loaddd --value={m, m*x, m*y, m*z, 0, 0, 0, 0, 0, 0}
  SetPayload --part_id=-1 --load_var=loaddd
  ```

### 9.4 SetTool —— 设置工具坐标系

```
SetTool --tool_var=<tool_var>
```

- 基于**末端法兰盘坐标系**下，期望的新 tool 坐标
- 示例：
  ```
  Var --type=tool --name=tool_new --value={0.161739, 0, 0.185219, 0, 0.57358, 0, 0.81915}
  SetTool --tool_var=tool_new
  ```

### 9.5 SetWobj —— 设置基坐标系

```
SetWobj --wobj_var=<wobj_var>
```

- 基于 **base 坐标系**下，期望的新 wobj 坐标
- 示例：
  ```
  Var --type=wobj --name=wobj_new --value={0.392367, -0.024387, 0, 0, 0, 0, 0}
  SetWobj --wobj_var=wobj_new
  ```

### 9.6 SetUsingSP —— 奇异点求解

```
SetUsingSP --state=on
SetUsingSP --state=off
```

- 开启/关闭奇异点求解模式
- 七轴机械臂运行 BlendL/BlendC 时必须开启

---

## 十、高级规划指令（轨迹融合）

### 10.1 MoveBlend —— 笛卡尔局部轨迹融合

```
MoveBlend --type=first_insert                     // 起点标记（固定）
MoveBlend --type=insert_line --robottarget_var=p1 --zone={d,p} --speed=v300   // 直线轨迹点
MoveBlend --type=insert_circle --mid_robottarget_var=p2 --robottarget_var=p3 --zone={d,p} --speed=v300  // 圆弧轨迹点
MoveBlend --type=start                           // 执行
```

- 对相邻两段运动拐点进行**局部轨迹融合**，引入过渡曲线避免速度突变和频繁启停
- zone 越大越平滑但精度越低，越小越精确
- 轨迹点姿态**可以变化**，但会降低速度
- 插值类型：`first_insert`(起点)、`insert_line`(直线)、`insert_circle`(圆弧)、`start`(执行)
- **每段速度单独决定**，由标记字段 speed 决定
- 示例：
  ```
  MoveBlend --type=first_insert
  MoveBlend --type=insert_line --robottarget_var=p1 --zone={0.1,0.1} --speed=v300
  MoveBlend --type=insert_circle --mid_robottarget_var=p2 --robottarget_var=p3 --zone={0.1,0.1} --speed=v300
  MoveBlend --type=start
  ```

### 10.2 MoveBlendScurve —— 笛卡尔匀速轨迹融合（S 曲线）

```
MoveBlend --type=first_insert
MoveBlend --type=insert_line --robottarget_var=p1 --zone={d,p}
MoveBlend --type=insert_line --robottarget_var=p2 --zone={d,p}
MoveBlendScurve --speed_var=v100 [--acc=<a>] [--jerk=<j>]
```

- S 曲线插值，运动线速度按指定曲线运动
- 适用于**涂胶、打磨**等恒速场景
- 轨迹仅执行位置变化，**不执行姿态变化**（不会报错）
- **每段速度不可单独决定**，由 MoveBlendScurve 指令的 speed 统一决定
- 运动类型无 `insert_circle` 和 `start`，由 MoveBlendScurve 直接执行

### 10.3 MoveBlendOptimalpos —— 笛卡尔最大速轨迹融合

```
MoveBlend --type=first_insert
MoveBlend --type=insert_line --robottarget_var=p1 --zone={d,p} --is_optimal=1
MoveBlend --type=insert_line --robottarget_var=p2 --zone={d,p} --is_optimal=1
MoveBlendOptimalpos --acc_coef={0.9} --vel_coef={0.9} [--dynamics_constraint=0|1]
```

- 满足关节最大速度/加速度/力矩前提下**尽快完成运动**
- `--acc_coef`：加速度系数 (0,1]，越大加速越快（默认 0.95）
- `--vel_coef`：速度系数 (0,1]，越大运行越快（默认 0.95）
- `--dynamics_constraint`：1=启用动力学约束(默认), 0=忽略
- 轨迹点姿态**不要变化**（否则可能计算失败）
- **标记点必须加 `--is_optimal=1`**

### 10.4 MoveS —— 笛卡尔全局轨迹融合（全程样条）

```
MoveS --type=first_insert
MoveS --type=insert --robottarget_var=p1
MoveS --type=insert --robottarget_var=p2
MoveS --type=start --speed=v200 [--ratio=<weight>]
```

- 对多个路径点进行**整体样条拟合**，生成全局连续平滑轨迹
- `--ratio`：全局平滑权重
- 轨迹点姿态**可以变化**，但有姿态变化时速度降低
- 速度由 `MoveS --type=start` 后的 speed 统一决定

### 10.5 ServoSeries —— 关节空间轨迹融合

```
ServoSeries --joint_set={j11,j12,j13,j14} --time={t1,t2,t3,t4} [--scale=<s>] [--stop_time=<t>]
```

- 发送一系列关节空间目标点，在不同关节位置间插值
- `--joint_set`：关节位置列表
- `--time`：对应完成时间列表，最终执行时间 = time × scale
- `--scale`：时间缩放比例
- `--stop_time`：完成后的减速时间
- 适用于实时控制和柔顺运动场景
- 示例：
  ```
  MoveAbsJ --jointtarget_var=j11  // 先到起始点
  ServoSeries --joint_set={j11,j12,j13,j14} --time={1,3,5,9} --scale=1
  ```

### 10.6 MoveSeriesToppJ2 —— 关节空间最大速轨迹融合

```
MoveSeriesToppJ2 --type=first_insert
MoveSeriesToppJ2 --type=insert --jointtarget_var=j1
MoveSeriesToppJ2 --type=insert --jointtarget_var=j2
MoveSeriesToppJ2 --type=start [--acc_coef=<a>] [--vel_coef=<v>]
```

- **时间最优**方式执行一系列关节点
- `--acc_coef`：加速度系数 (0,1]（默认 0.95）
- `--vel_coef`：速度系数 (0,1]（默认 0.95）
- 轨迹点应事先设定顺序连续，**避免大角度跳变**
- 点之间不能出现突变或不可达配置

---

## 十一、力控指令

### 11.1 六维力传感器概述

- 测量机械臂末端**三维力** (Fx, Fy, Fz) 和**三维力矩** (Mx, My, Mz)
- 支撑力控拖拽、阻抗控制等指令
- 需：零漂补偿与标定、设置死区与力阈值、对齐传感器与工具坐标系
- 安装在末端执行器与工具之间，需固定牢靠
- 设置 `SetTool` 匹配实际工具方向

### 11.2 CalibFtDyn —— 动态标定及负载辨识

```
CalibFtDyn --positive_limit=<jointtarget> --negative_limit=<jointtarget> [--sample_num=<N>] [--interval=<T>] [--freq=<f>] [--cutoff_freq=<cf>]
```

- positive_limit 各关节角必须大于 negative_limit 对应关节角
- 机械臂初始位置需在关节角上下限之间
- 机械臂缓慢运动采集数据计算零点
- 更换工具或平台需重新标定
- 示例：
  ```
  Var --type=jointtarget --name=neg_lim --value={-1.5,-1.5,-1.5,-1.5,-1.5,-1.5,-1.5,0,0,0}
  Var --type=jointtarget --name=pos_lim --value={1.5,1.5,1.5,1.5,1.5,1.5,1.5,0,0,0}
  CalibFtDyn --positive_limit=pos_lim --negative_limit=neg_lim
  ```

### 11.3 DragFtInCartesian —— 笛卡尔空间力控拖拽

```
DragFtInCartesian --force_direction={d0,...,d5} --force_gain={g0,...,g5} [--vel_limit={...}] [--acc_limit={...}] [--coordinate=<0|1>] [--cutoff_freq=<f>]
```

- 机器人末端沿设定方向感受到外力时做出运动响应
- `--force_direction`：1=启用，0=禁用（6 维对应 X,Y,Z,RX,RY,RZ）
- `--force_gain`：灵敏度参数，值越大越易拖动
- `--vel_limit`：拖动速度限制
- `--coordinate`：0=基坐标系，1=工具坐标系(默认)
- 需确保六维力传感器坐标系与工具坐标系对齐
- 示例（仅开启 Z 方向拖动）：
  ```
  DragFtInCartesian --force_direction={0,0,1,0,0,0} --force_gain={0.03,0.03,0.03,0.3,0.3,0.5}
  ```

### 11.4 DragFtInJoint —— 关节空间力控拖拽

```
DragFtInJoint --gain={g} --force_gain={g0,...,g5} [--vel_limit={...}] [--acc_limit={...}] [--cutoff_freq=<f>]
```

- 通过力传感器控制各关节角度变化，类似"手把手"推关节
- `--gain`：整体响应增益，值越大越灵敏
- `--force_gain`：各关节灵敏度参数
- 示例：
  ```
  DragFtInJoint --gain={0.1} --force_gain={0.01,0.01,0.01,0.01,0.01,0.01}
  ```

### 11.5 ImpedanceMoveL —— 阻抗控制直线运动

```
ImpedanceMoveL --robottarget_var=<p> --force_direction={...} [--stiffness={...}] [--vel_gain={...}] [--speed=<s>] [--auto_quit=<0|1>] [--cutoff_freq=<f>]
```

- 力-位置混合控制，运动过程中具备柔顺性，对外力进行力反馈
- 基于末端力/力矩反馈实现**末端刚度控制**
- `--stiffness`：刚度系数
- `--vel_gain`：阻尼参数
- `--auto_quit=1`：运动到目标位置后自动退出
- `--ft_pm`：传感器坐标系相对工具坐标系的位姿变换矩阵
- 示例（直线运动到 p1，过程开启 Y 方向力控）：
  ```
  ImpedanceMoveL --robottarget_var=p1 --speed=v30 --force_direction={0,1,0,0,0,0}
  ```

### 11.6 WrenchPoseMoveL —— 力控直线运动（强调目标力）

```
WrenchPoseMoveL --robottarget_var=<p> --force_target={...} --force_direction={...} [--force_gain={...}] [--speed=<s>] [--auto_quit=<0|1>]
```

- 强调末端力/力矩达到设定**目标值**的运动
- `--force_target`：力控自由度的期望力
- `--force_gain`：力控灵敏度参数
- 死区设置示例：`{1.0, 1.0, 1.0, 0.5, 0.5, 0.5}`，力差超过此值才会运动（过滤噪音）
- 示例（期望 Y 方向力 6N）：
  ```
  WrenchPoseMoveL --robottarget_var=p1 --speed=v30 --force_target={15,6,15,1,1,1} --force_direction={0,1,0,0,0,0}
  ```

### 11.7 WrenchPose —— 目标力/力矩控制

```
WrenchPose --force_target={...} --force_direction={...} [--force_gain={...}] [--vel_gain={...}] [--vel_limit={...}] [--coordinate=<0|1>]
```

- 在指定自由度方向上产生期望力，**力误差转化为运动加速度**
- 死区：力差超过阈值才运动，过滤噪音提高稳定性
- 示例（Y 方向期望力 6N）：
  ```
  WrenchPose --force_target={15,6,15,1,1,1} --force_direction={0,1,0,0,0,0}
  ```

### 11.8 WrenchPoseV2 —— 精简目标力/力矩控制

```
WrenchPoseV2 --force_target={...} --force_direction={...} [--vel_gain={...}] [--vel_limit={...}] [--coordinate=<0|1>]
```

- WrenchPose 的简化版，**力误差转化为运动速度**
- 参数更少，用于快速部署简单力控任务
- 死区设置同 WrenchPose
- 示例：
  ```
  WrenchPoseV2 --force_target={6,6,6,1,1,1} --force_direction={0,1,0,0,0,0}
  ```

### 11.9 力控关键参数总结

| 参数 | 含义 | 典型值 |
|------|------|--------|
| `force_direction` | 力控自由度（1=启用, 0=禁用） | `{0,0,1,0,0,0}` (仅 Z) |
| `force_target` | 期望力/力矩 (N / N·m) | `{0,0,6,0,0,0}` |
| `force_gain` | 力控灵敏度，越大越灵敏 | 平动 0.01~0.05，转动 0.3~0.5 |
| `stiffness` | 刚度系数 | — |
| `vel_gain` | 阻尼参数 | — |
| `vel_limit` | 力控引起的速度上限 | — |
| `cutoff_freq` | 低通滤波器截止频率 (Hz) | 5~20 |
| `coordinate` | 参考坐标系 | 0=基坐标系, 1=工具坐标系 |
| 死区 | 力差阈值，超过才运动 | `{5,5,5,0.5,0.5,0.5}` |

---

## 十二、常见奇异点

机器人某些姿态下运动学求解失效或关节速度异常大。

### 12.1 Wrist Singularity（手腕奇异点）

- **条件**：J4 轴和 J6 轴重合（J5 ≈ 0°）
- **发生概率**：**最常见**，关节机器人最容易遇到
- **表现**：J4 和 J6 旋转效果相同，控制器可能命令极高速旋转

### 12.2 Elbow Singularity（肘关节奇异点）

- **条件**：J5 中心点处于 J1、J2 组成的平面上
- **发生概率**：**极少遇到**，多数机器人大臂不会完全伸直

### 12.3 Shoulder Singularity（肩部奇异点）

- **条件**：J5 中心点处于通过 J1 且平行 J2 轴的平面上
- **发生概率**：靠底座时可能出现
- **特点**：非常复杂，逆运算存在**无数解**

### 12.4 解决方案

1. 绕开奇异点区域重新设置目标点位
2. 使用 `SetUsingSP --state=on` 开启奇异点求解
3. 七轴运行 BlendL/BlendC 时必须开启

---

## 十三、Topic 状态订阅

### 13.1 实时状态 (system_rtstate) 数据结构

| 层级 | 字段 | 类型 | 说明 |
|------|------|------|------|
| 头部 | `header_timestamp` | int | 时间戳 |
| 头部 | `header_frame_id` | int | 帧 ID |
| 系统 | `system_running_state` | int | 0=正常 |
| 控制器 | `controller_name` | str | 控制器名称 |
| 控制器 | `control_cycle` | float | 控制周期 |
| 控制器 | `global_count` | int | 全局计数 |
| 控制器 | `master_info` | str | 主控信息 |
| 控制器 | `is_link_up` | bool | 链路是否在线 |
| 控制器 | `ftvalues[]` | FtvalueInfo | 六维力传感器数据 |
| 模型 | `model_name` | str | 模型名称 |
| 模型 | `model_type` | str | 模型类型 |
| 模型 | `error_code` | int | 错误码（0 正常） |
| 模型 | `error_msg` | str | 错误描述 |
| 模型 | `model_state` | int | 模型状态 |
| 模型 | `current_func_name` | str | 当前执行函数名 |
| 模型 | `func_count` | int | 函数计数 |
| 关节 | `joint_type` | str | 关节类型 |
| 关节 | `position` | float | 当前位置 (rad) |
| 关节 | `torque` | float | 当前力矩 (Nm) |
| 关节 | `is_enabled` | bool | 是否上电使能 |
| 关节 | `mode` | int | 控制模式 |
| 关节 | `error_code` | int | 关节错误码 |
| 关节 | `digit_output` | int | 数字输出状态（10 路 IO） |
| 关节 | `digit_input` | int | 数字输入状态（10 路 IO） |
| 当前点 | `point_name` | str | 点位名称 |
| 当前点 | `tool_name` | str | 工具名称 |
| 当前点 | `wobj_name` | str | 工件坐标系名称 |
| 当前点 | `robottarget` | float[7] | 当前笛卡尔位姿 XYZ+四元数 |
| 当前点 | `jointtarget` | float[10] | 当前指令目标关节角 |
| 六维力 | `fx, fy, fz` | float | 三维力 (N) |
| 六维力 | `mx, my, mz` | float | 三维力矩 (Nm) |

### 13.2 非实时状态 (system_nrtstate) 数据结构

| 层级 | 字段 | 说明 |
|------|------|------|
| 从站 | `slave_name`, `phy_id`, `alias` | 从站信息 |
| 从站 | `slave_state`, `is_online`, `is_virtual`, `is_error` | 从站状态 |
| 模型 | `is_using_sp` | 是否开启奇异点求解 |
| 模型 | `is_collision_detection` | 是否开启碰撞检测 |
| 关节 | `max/min position` | 软限位 |
| 关节 | `max/min vel, acc` | 速度/加速度限制 |
| 关节 | `max_collision_torque` | 碰撞检测力矩阈值 |
| 工具 | `tool_name`, `data[]` | 已定义的工具坐标系 |
| 工件 | `wobj_name`, `data[]` | 已定义的 wobj |
| 负载 | `load_name`, `data[]` | 已定义的负载 |
| 示教点 | `point_name`, `robottarget`, `jointtarget` | 已保存的点位 |
| 子系统 | `subsystem_name`, `id`, `state` | 子系统状态 |
| 传感器 | `sensor_name`, `id`, `state` | 传感器状态 |
| 接口 | `interface_name`, `id`, `state` | 接口状态 |

### 13.3 Python 用法

```python
import time
import topic
import message
import threading

print_lock = threading.Lock()

def safe_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)

# 回调函数：实时状态
def on_system_rtstate(tt: topic.SystemRtState):
    parm_rt = message.SystemStateData()
    message.display_rt(tt, parm_rt)

    safe_print(f"系统运行状态: {parm_rt.system_running_state}")
    safe_print(f"链路在线: {parm_rt.controller.is_link_up}")
    safe_print(f"全局计数: {parm_rt.controller.global_count}")

    # 关节位置
    for model_idx in range(len(parm_rt.models)):
        joints_per_model = len(parm_rt.models_joints) // len(parm_rt.models)
        for j_idx in range(joints_per_model):
            joint = parm_rt.models_joints[model_idx * joints_per_model + j_idx]
            safe_print(f"  Joint{j_idx}: pos={joint.position:.3f}, enabled={joint.is_enabled}")

    # TCP 位姿
    for i, pt in enumerate(parm_rt.models_current_points):
        safe_print(f"  TCP{i}: {pt.robottarget}")

    # 六维力
    for i, ft in enumerate(parm_rt.controller.ftvalues):
        safe_print(f"  FT{i}: F=({ft.fx:.2f},{ft.fy:.2f},{ft.fz:.2f}) M=({ft.mx:.2f},{ft.my:.2f},{ft.mz:.2f})")

# 回调函数：非实时状态
def on_system_nrtstate(tt: topic.SystemNrtState):
    parm_nrt = message.SystemStateData()
    message.display_nrt(tt, parm_nrt)

    # 从站状态
    for slave in parm_nrt.slaves:
        safe_print(f"  {slave.slave_name}: online={slave.is_online}, state={slave.slave_state}")

    # 工具/工件/负载列表
    for model_idx, model in enumerate(parm_nrt.models):
        safe_print(f"Model {model_idx}: SP={model.is_using_sp}, Collision={model.is_collision_detection}")

# 配置节点
options = topic.NodeOptions()
options.node_name = 'my_monitor'
options.sub_url = 'tcp://192.168.50.1:19091'

# 创建节点并启动
node = topic.Node(options)
if node.Start():
    print("节点启动成功")

# 创建订阅
sub_rt = node.CreateSubscriptionRT("system_rtstate", on_system_rtstate)
sub_nrt = node.CreateSubscriptionNRT("system_nrtstate", on_system_nrtstate)

# 保持运行
try:
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    node.Shutdown()
```

---

## 十四、Web 界面操作

### 14.1 Web 界面分区

```
┌──────────────────────────────────────────────────────┐
│ 顶部菜单栏：界面切换 | 机器人选择 | 速度 | 全屏 | 清错 | 使能 | 语言 │
├──────────────────────────────────────────────────────┤
│ 中间功能区：                                          │
│  ┌─────────────┐  ┌──────────────┐                   │
│  │ TCP 位姿控制  │  │  仿真显示区    │                   │
│  │ (位置+方向)  │  │  (3D 模型)    │                   │
│  ├─────────────┤  │              │                   │
│  │ 关节位置控制  │  │  TCP 位姿显示 │                   │
│  │ (J1~J7 滑块) │  │  (XYZ/RxRyRz)│                   │
│  └─────────────┘  └──────────────┘                   │
├──────────────────────────────────────────────────────┤
│ 底部菜单栏：连接状态 | ⏸暂停 ▶开始 ⏹停止 | 全局速率倍数 │
└──────────────────────────────────────────────────────┘
```

### 14.2 顶部菜单栏功能

| 功能 | 说明 |
|------|------|
| 语言切换 | 点击用户头像 → "语言"，中/英文 |
| 使能按键 | 绿色 Enable → 红色 Disable（上/下使能） |
| 错误处理 | 报错后需点击才能下一步动作 |
| 全屏 | 全屏/退出全屏显示 |
| 速度调节 | 10 档速度，从上到下依次增大 |
| 机器人选取框 | 切换控制的机器人，可选"所有机器人" |

### 14.3 TCP 位姿控制区

- **位置区**：点击 X/Y/Z 方向按钮，末端法兰沿该方向平移
- **方向区**：点击 RX/RY/RZ 转向按钮，末端法兰绕轴旋转

### 14.4 关节位置控制区

- 每个关节操作位含：状态灯（红=未使能，绿=已使能）、关节编号、角度控制器（正/负方向按钮）、角度显示器
- 逆时针转动为正，顺时针为负
- 理论范围 -180°~180°，实际需考虑碰撞调整

### 14.5 设置界面功能

| 模块 | 功能 |
|------|------|
| 奇异点检测 | 开启后运动经过奇异点不报错停止，七轴运行 BlendL/C 需开启 |
| 碰撞检测 | 感知碰撞并响应停止，可调灵敏度百分比（越大越不灵敏） |
| 动力学辨识 | 采集运动数据建立动力学模型，用于重力/摩擦力补偿 |
| 机器人拖动 | 基于动力学模型的零力示教，手动牵引录制轨迹 |
| 预设程序 | 预存运动点位实现点到点运动 |
| 机器人重力 | 设定重力矢量方向，抵消自重对关节扭矩影响 |
| 关节参数 | 调整关节正负转向方向 |
| 示教点位 | 记录/保存运动点位，添加/删除/保存参数 |
| 六维力显示 | 实时显示 Fx,Fy,Fz,Mx,My,Mz |

### 14.6 连接状态

- **虚化状态（白色）**：未连接实机，仿真模式
- **实机状态（黄色）**：已连接实机
- 无法使能时检查 STO 是否连接

### 14.7 全局启停

- **暂停**：当前运动暂停，点"开始"后继续
- **停止（单击）**：停止当前运动
- **停止（双击/多次）**：清空当前所有指令

---

## 十五、图形化编程（Blockly）

位于 Web 界面设置区 → 编程栏。

### 15.1 模块区分类

#### 移动模块

| 指令 | 功能 |
|------|------|
| MoveAbsJ | 关节空间运动，指定关节角度 |
| BlendL | 笛卡尔直线运动，指定 robottarget + zone |
| BlendC | 笛卡尔圆弧运动，指定 mid_robottarget + robottarget |
| MoveBlend | 轨迹融合指令，与 BlendL/C 配套使用 |
| MoveBlendScurve | 匀速轨迹融合，适用于涂胶/打磨 |

注意：Blend 指令控制七轴时需要开启"奇异点检测"。

#### 逻辑模块

- "如果（条件）执行（指令）"：条件填 true 必执行，false 必禁行
- "变量 = 数字"：比较运算
- "条件 A 并且/或条件 B"：与非判断
- "true/false"：布尔值

#### 循环模块

- "重复 N 次，执行（指令）"
- "当条件满足时重复 / 重复直到条件满足"
- "变量 i 的 for 循环"
- "遍历列表"
- "跳出循环"

#### 数学模块

算术运算、比较数值、数学函数（开平方根、三角函数等）。

#### 文本模块

创建备注，帮助记录或理解编程思路。

#### 变量模块

创建变量并为变量赋值。

#### 函数模块

将经常使用的指令序列封装为可重复调用的指令块。

### 15.2 编程区注意事项

1. 所有项目必须在"新建编程"之下
2. 通过机器人选取框选定机器人后再编程
3. 删除指令：选中按 Delete 或拖到垃圾桶
4. 复制粘贴：Ctrl+C / Ctrl+V
5. 编程结束后用底部全局启停控制程序运行

### 15.3 多臂编程

1. 选定"所有机器人"
2. 添加"Robot 1"、"Robot 2"模块，分别编写
3. **各机器人指令条数必须一致**，否则优先执行指令较少者
4. 对齐方式：
   - MoveAbsJ：重复上一条 MoveAbsJ
   - MoveBlend：用 BlendL 重复上一位姿
   - 使用 `NotRunExecute` 块补齐

---

## 十六、工具与工件坐标系标定

### 16.1 工具坐标系标定（Web 工艺包）

#### 四点法

标定工具偏移 (x, y, z)：

1. 选择"四点法"
2. 选择空间中工具可到达的固定点
3. 以**不同姿态**接触该固定点，记录 4 个点位 (P1~P4)
4. 将 4 个点填入 R1~R4
5. 点击"标定"，输入工具名称，确定
6. 在 SetTool 栏选择新增工具，设置

#### 五点法

在四点法基础上确定工具 Z 轴方向：

1. 前四步同四点法
2. 从第四点沿新工具 Z 轴正方向移动一段距离，记录第五点（**末端姿态需与第四点一致**）
3. 将 5 个点填入 R1~R5，标定

#### 六点法

完整标定工具偏移 + 姿态：

1. 前五步同五点法
2. 从第四点沿新工具 Y 轴正方向移动一段距离，记录第六点（姿态需一致）
3. 将 6 个点填入 R1~R6，标定

**操作技巧**：记录第四点时，将姿态调整至与基坐标轴重合，方便后续记录第五、第六点。

### 16.2 工件坐标系标定（三点模式）

1. 操作末端到达目标工件坐标系**原点**，记录 T1
2. 到达目标工件坐标系**X 轴正方向**上一点，记录 T2
3. 到达目标工件坐标系**Y 轴正方向**上一点，记录 T3
4. 填入 R1~R3，标定，命名（如 wobj2）
5. 在 SetWobj 栏选择，设置

---

## 十七、动力学辨识与手动拖动

### 17.1 配置流程（Web 端）

```
状态检查 → 模型配置 → 重力参数设置 → 正负限位设置 → 动力学辨识 → 手动拖动
```

### 17.2 状态检查

检查以下三项全为绿灯：
- 后端程序状态
- 前端程序状态 (Nginx)
- 机器人驱动程序状态

检查连接状态为"实机状态"（黄色图标），使能按钮正常切换，机械臂正常蜂鸣。

### 17.3 模型配置

1. 断开控制器与机器人接线
2. 在设置页面点击"设置模型名称"→"添加"
3. 选择对应型号的 controller 和 model
4. 多臂需重复添加多组（顺序：controller, controller... model, model...）
5. 命名后保存，重启驱动和后端节点（连接实机）

### 17.4 重力参数设置

1. 一般基座标系 Z 轴垂直地面朝上：`gravity={0, 0, -9.81}`
2. 实际安装角度不同（侧装/壁装/倒装等）需重新配置
3. 求当前基座标系转到"Z 轴垂直朝上"的 ZYX 欧拉角
4. 在"机器人重力"中选择"任意装"，填入欧拉角

### 17.5 正负限位设置

为动力学辨识设定尽可能大的运动范围：

1. 上使能
2. 调节 J1→J6 角度至增大的最大安全极限（不碰撞），保存正限位
3. 调节 J1→J6 角度至减小的最小安全极限，保存负限位

### 17.6 动力学辨识

1. 确保重力参数正确、正负限位设置成功
2. 上使能
3. 点击"开始辨识"，机械臂会在限位内自主运动
4. 等待运动停止 + 模型求解完成
5. 所有机器人均完成后再点击"保存全部动力学参数"
6. 重启驱动节点和后端节点

### 17.7 手动拖动

- 前提：重力参数正确 + 动力学辨识完成
- 这是**电流环拖动**，不依赖外部传感器
- 步骤：选择机器人 → 点击"开始拖动" → 手动拖动机器人 → "停止拖动"
- 拖动参数：VF（粘性摩擦）、CF（库伦摩擦）滑块可调整拖动手感
- 拖动回放：选择"所有机器人"后开始拖动自动记录轨迹，停止后可回放

---

## 十八、工艺包（Web 端）

### 18.1 六维力控操作台

- **实时显示**：Fx, Fy, Fz (N) + Mx, My, Mz (Nm) 数字刷新
- **动态标定**：四步——设正限位、设负限位、动态标定、保存参数
- **拖拽控制**：笛卡尔空间（六方向增益）+ 关节空间（暂未开通）
- **恒力控制 (WrenchPose)**：设置目标力/力矩 + 力控开关，适用擦拭/打磨/接触检测
- **混合控制**：
  - **WrenchPoseMoveL**：沿直线轨迹运动 + 指定方向施加恒定力
  - **ImpedanceMoveL**：阻抗模型柔顺控制，受外力时位移响应与柔顺回弹，适用贴合/抛光/人机协作

### 18.2 SpeedL（工艺包）

在笛卡尔空间给定速度，持续发送指令，拖动滑块实时调整运动方向和速度。

- 初始值全 0，拖动滑块调整
- 推荐速度 0.05 m/s 左右

### 18.3 JogAnyJ2（工艺包）

在关节空间给定目标位置，持续发送指令，拖动滑块实时调整目标位置。

### 18.4 恒力控制注意事项

- 目标力初始值不超过 ±20N，防止突发力过大
- 目标力初始值需 > 5N 才会运动（保护设置）
- 使用前必须完成负载辨识和零偏标定
- WrenchPoseMoveL 若仅需法向恒力，可只启用单一方向

---

## 十九、关节链与 URDF 参数

### 19.1 关节链

```
base_link → joint1 → Link1 → joint2 → Link2 → joint3 → Link3
         → joint4 → Link4 → joint5 → Link5 → joint6 → ee_Link
```

所有关节旋转轴均为 Z 轴 `(0, 0, 1)`。

### 19.2 DH 参数（从 URDF joint origin 推算）

| 关节 | parent→child 偏移 (x, y, z) | rpy (roll, pitch, yaw) | 下限 | 上限 |
|------|---------------------------|------------------------|------|------|
| joint1 | (0, 0, 0.062) | (0, 0, 0) | -3.1416 | 3.1416 |
| joint2 | (0, 0.078, 0.0675) | (1.5708, 1.5708, 0) | -3.1416 | 3.1416 |
| joint3 | (0, 0.442, 0) | (0, 0, 0) | -2.8623 | 2.8623 |
| joint4 | (0, 0.386, 0.005) | (3.1416, 0, 0) | -3.1416 | 3.1416 |
| joint5 | (0.054, 0, 0.051) | (1.5708, 0, 1.5708) | -3.1416 | 3.1416 |
| joint6 | (0, 0.054, 0.051) | (-1.5708, 0, 0) | -3.1416 | 3.1416 |

### 19.3 连杆惯量参数

| 连杆 | 质量 (kg) | Ixx | Iyy | Izz |
|------|-----------|-----|-----|-----|
| base_link | 5.0487 | 0.01674 | 0.00753 | 0.01814 |
| Link1 | 13.203 | 0.03603 | 0.03530 | 0.02526 |
| Link2 | 46.802 | 1.4978 | 0.09634 | 1.4760 |
| Link3 | 20.240 | 0.42906 | 0.02134 | 0.42608 |
| Link4 | 4.6142 | 0.00375 | 0.00683 | 0.00670 |
| Link5 | 4.7679 | 0.00746 | 0.00382 | 0.00733 |
| ee_Link | 2.5464 | 0.00118 | 0.00120 | 0.00204 |

### 19.4 建模手册要点

- 基座标系 (world frame) 和末端工具系 (tool frame) 如图定义
- 零位下各关节坐标系参考右手坐标系
- **添加负载后 SetPayload 时，需将基座标系绕 Z 轴旋转 180° 计算**（不需要 SetWobj）
- 关节 Z 轴朝向与 ROBODK 中 UR5e 模型保持一致
- 关节正负方向参考右手定则

---

## 二十、IO 与硬件接口

### 20.1 机器人手臂接口（EtherCAT）

| 引脚 | 信号 |
|------|------|
| 1 | 未使用 |
| 2 | EtherCAT TX- |
| 3 | EtherCAT TX+ |
| 4 | EtherCAT RX- |
| 5 | EtherCAT RX+ |
| 6 | 48V+ |
| 7 | 48V- |
| 8 | PE |

### 20.2 控制柜通讯接口

| 接口 | 说明 |
|------|------|
| RJ45 (X16/NIC3) | 控制器以太网，默认 IP 192.168.11.11 |
| RJ45 (X15/NIC4) | 示教器以太网 |
| USB | USB 接口 |
| COM | RS232 串口 (DB9) |

### 20.3 I/O 模块

EtherCAT 总线型，16 路 DI + 16 路 DO + 2 路 AI + 2 路 AO，公共端 24V。

### 20.4 工具法兰 I/O（AX58200 连接器）

| 引脚 | 信号 | 颜色 |
|------|------|------|
| 1 | 24V（电源输出） | 红色 |
| 2 | 0V（电源地） | 蓝色 |
| 3 | DO2（数字输出 2） | 紫色 |
| 4 | DO1（数字输出 1） | 黄色 |
| 5 | DI2（数字输入 2） | 白色 |
| 6 | DI1（数字输入 1） | 黑色 |
| 7 | AI2（模拟输入 2） | 粉色 |
| 8 | AI1（模拟输入 1） | 棕色 |

- 供电：24V/12V，最大 600mA
- DO：NPN 型，电压 < 30V，灌电流 < 600mA
- DI：NPN 型
- AI：0~10V 模拟电压输入

---

## 二十一、驱动器报错代码

### 21.1 RGT 驱动器常见故障

| 故障码 (Hex) | 故障信息 |
|-------------|----------|
| 3240 | 短路 |
| 3120 | 欠压 |
| 3130 | 缺相 |
| 3310 | 过压 |
| 4310 | 驱动器过温 |
| 7121 | 电机堵转 |
| 7300 | 反馈错误 |
| 7382 | 电机启动换向失败 |
| 8311 | 过峰值电流 |
| 8480 | 速度跟踪错误 |
| 8481 | 超过速度限制 |
| 8611 | 位置跟踪错误 |
| 8680 | 超出位置限制 |

### 21.2 RDM 驱动器常见故障

| 故障码 (Hex) | 故障信息 |
|-------------|----------|
| 2280 | 反馈错误 |
| 2310 | 电流限制 |
| 2320 | 短路 |
| 3110 | 过压 |
| 3120 | 欠压 |
| 3310 | 电压限制 |
| 4210 | 驱动器过温 |
| 4300 | 电机过温 |
| 5080 | 无其它紧急情况的故障 |
| 61FF | 命令错误 |
| 7122 | 相位错误 |
| 7380 | 正限位触发 |
| 7381 | 负限位触发 |
| 7390 | 跟踪错误 |
| 73A0 | 位置环绕 |
| 8130 | 节点保护错误 |

---

## 二十二、排错速查

| 现象 | 可能原因 | 解决 |
|------|----------|------|
| 连不上 / 端口不通 | IP 不对 / API 服务没开 / 防火墙 | 确认 Web 界面 IP，开启 API/远程控制服务 |
| 初始化失败 | 顺序不对 / 有未清 Error | 先 `{Clear}` 再重试 |
| 动了但极慢 | `{SetRate}` 没给参数 | 改成 `{SetRate 50}` |
| Ctrl+C 后不运动 | 没发 Disable，控制器还在运行态 | Web 界面点 Clear → Disable → Enable |
| MoveAbsJ 卡住 | 同步模式，运动未完成 / 已在目标位 | 确认关节不在目标位置，或用异步模式 |
| 无法使能 (Enable) | STO 未连接 / 急停未释放 | 检查 STO 连接，释放急停按钮 |
| 动力学辨识误差大 | 重力参数设置错误 | 检查并重新设置重力参数 |
| 碰撞检测频繁触发 | 灵敏度设置过高 | 增大碰撞检测灵敏度百分比，或临时关闭 |
| 六维力漂移 | 未标定零漂 | 执行 CalibFtDyn |
| MoveBlend 七轴报错 | 未开启奇异点检测 | `SetUsingSP --state=on` |
| 驱动器报错 | 硬件故障 | 参考驱动器报错码对照表 |
| 多臂指令不同步 | 指令条数不一致 | 用 NotRunExecute 或重复指令补齐 |
| 变量名称不生效 | 纯数字或格式错误 | 以英文字母开头，支持字母+数字+下划线 |

---

## 二十三、Python 代码模板

### 23.1 RPC 通信 + 急停示例

```python
import rpc
import random
import time
import threading

# 急停事件
stop_event = threading.Event()

# 初始化命令列表
init_cmds = [
    "{Clear}",
    "{Disable}",
    "{Mode}",
    "{SetMaxToq}",
    "{Recover}",
    "{SetRate 30}",
    "{Enable}",
    "{Var --clear}",
    "{Recover}",
    "{Var --type=jointtarget --name=j0 --value={0,0,0,0,0,0,0,0,0,0}}",
    "{Var --type=jointtarget --name=j1 --value={0.1,-1.5,0,0,0,0,0,0,0,0}}",
    "{Var --type=jointtarget --name=j2 --value={0.2,0,0,0,0,0,0,0,0,0}}",
    "{Var --type=jointtarget --name=j3 --value={-0.1,0,0,0,0,0,0,0,0,0}}",
    "{Var --type=jointtarget --name=j4 --value={-0.2,0,0,0,0,0,0,0,0,0}}",
]

# 动作序列：{目标, 停留时间(秒)}
action_sequence = [
    ("j1", 1.0),
    ("j2", 1.0),
    ("j3", 1.0),
    ("j4", 1.0),
    ("j0", 0.0),   # 回零点
]

estop_cmds = ["{Stop}", "{Disable}"]


def wait_for_enter():
    """按回车触发急停"""
    input()
    stop_event.set()
    print("\n>>> 急停触发！")


def e_stop(client):
    """执行急停"""
    print(">>> 发送 Stop + Disable ...")
    for cmd in estop_cmds:
        msg = rpc.Msg(cmd)
        msg.setMsgID(10001)
        msg.setMsgSeqID(random.randint(1, 10000))
        client.CallAwait(msg, 3000)
    print(">>> 机械臂已停止并下电")


def send_rpcsy(client, cmd_list, timeout_ms, sleep_time_s):
    """批量同步发送 RPC 指令"""
    for cmd in cmd_list:
        if stop_event.is_set():
            return
        msg = rpc.Msg(cmd)
        msg.setMsgID(10001)
        msg.setMsgSeqID(random.randint(1, 10000))
        status, resp_list = client.CallAwait(msg, timeout_ms)
        if status == 0:
            for r in resp_list:
                code = "OK" if r.code == 0 else f"ERR({r.code})"
                print(f"  [{code}] {r.message}")
        else:
            print(f"  [FAIL] status={status}")
            client.ClearErr()
        time.sleep(sleep_time_s)


def main():
    listener = threading.Thread(target=wait_for_enter, daemon=True)
    listener.start()

    IP = "192.168.50.1"   # 改成实际 IP
    PORT = 5868
    print(f"Connecting to {IP}:{PORT}...")
    client = rpc.CPPClient(IP, PORT)
    print("Connected!")

    # 初始化
    print(">>> 初始化中...")
    send_rpcsy(client, init_cmds, 500, 0.1)

    # 回零点
    if stop_event.is_set():
        e_stop(client)
        return
    print(">>> 回零点 (j0)")
    send_rpcsy(client, ["{MoveAbsJ --jointtarget_var=j0}"], 50000, 0.01)

    # 执行动作序列
    for target, stay in action_sequence:
        if stop_event.is_set():
            e_stop(client)
            return
        print(f">>> 移动到 {target}，停留 {stay}s")
        send_rpcsy(client, [f"{{MoveAbsJ --jointtarget_var={target}}}"], 50000, 0.01)
        if stay > 0 and not stop_event.is_set():
            time.sleep(stay)

    print(">>> 动作序列完成！按 Ctrl+C 退出")
    print(">>> (随时按回车可以急停)")

    try:
        while True:
            if stop_event.is_set():
                e_stop(client)
                break
            time.sleep(0.1)
    except KeyboardInterrupt:
        e_stop(client)


if __name__ == "__main__":
    print("=" * 50)
    print("TB6 机械臂动作演示 - 随时按回车急停")
    print("=" * 50)
    main()
```

### 23.2 最小可跑代码

```python
import rpc, random, time

IP = "192.168.50.1"   # 改成你的实际 IP
PORT = 5868

client = rpc.CPPClient(IP, PORT)

# 初始化
init_cmds = [
    "{Clear}",
    "{Disable}",
    "{Mode}",
    "{SetMaxToq}",
    "{Recover}",
    "{SetRate 30}",
    "{Enable}",
    "{Var --clear}",
    "{Recover}",
    "{Var --type=jointtarget --name=j0 --value={0,0,0,0,0,0,0,0,0,0}}",
    "{Var --type=jointtarget --name=j1 --value={0.1,-1.5,0,0,0,0,0,0,0,0}}",
]

for cmd in init_cmds:
    msg = rpc.Msg(cmd)
    msg.setMsgID(10001)
    msg.setMsgSeqID(random.randint(1, 10000))
    status, resp = client.CallAwait(msg, 500)
    print(f"[{'OK' if status==0 else 'FAIL'}] {cmd}")

# 运动
for target in ["j0", "j1"]:
    cmd = f"{{MoveAbsJ --jointtarget_var={target}}}"
    msg = rpc.Msg(cmd)
    msg.setMsgID(10001)
    msg.setMsgSeqID(random.randint(1, 10000))
    status, resp = client.CallAwait(msg, 50000)
    print(f"{target} done, status={status}")
```

### 23.3 多臂控制时的 RPC 返回说明

- `CallAwait` 返回 `(status, resp_list)`
- `status == 0` 表示通信成功（不代表指令执行成功）
- `resp_list` 中每条响应有 `code`（0=成功）和 `message`
- 指令执行失败时调用 `client.ClearErr()` 清错后重试

---

## 附录：快速命令索引

### 初始化序列（必须按顺序）
```
{Clear}
{Disable}
{Mode}
{SetMaxToq}
{Recover}
{SetRate 30}
{Enable}
```

### 变量定义常用写法
```
Var --type=jointtarget --name=j0 --value={0,0,0,0,0,0,0,0,0,0}
Var --type=jointtarget --name=j1 --value={0.1,-0.5,0,0,0,0,0,0,0,0} --degree_unit=1
Var --type=robottarget --name=p1 --value={0.5,0.1,0.3,0,0,0,1}
Var --type=speed --name=v50 --value={0.5,0.1,3.14,0,0}
Var --type=zone --name=z10 --value={0.01,0.05}
Var --type=tool --name=t1 --value={1,0,0,0.1,0,0,0,1}
Var --type=wobj --name=w1 --value={0.1,0,0,0,0,0,1}
Var --type=load --name=ld --value={2,0.1,0,0.05,0,0,0,0,0,0}
Var --clear
```

### 运动指令常用写法
```
MoveAbsJ --jointtarget_var=j0
MoveAbsJ --jointtarget_var=j1 --speed=v100 --zone=z20
MoveJ --robottarget_var=p1 --speed=v50 --zone=z5
SpeedL --vel={0.1,0,0,0,0,0} --acc={2,2,2,2,2,2} --jerk={5,5,5,5,5,5} --last_count=1000 --coordinate=0
SpeedJ --vel={0.1} --acc={10} --dec={10} --jerk={10} --last_count=1000
JogJoint --speed=v100 --motion_id=0 --direction=1 --increase_count=50
JogCartesian --moving_type=0 --direction=1 --speed=v100 --coordinate=0 --increase_count=50
```

### 系统设置
```
SetTool --tool_var=t1
SetWobj --wobj_var=w1
SetPayload --load_var=ld
SetUsingSP --state=on
Clear
Stop
Pause
Start
```
