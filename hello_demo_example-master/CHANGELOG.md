# 更新日志

## [1.0.1] - 2026-07-06

### 修复
- 修复 JogAnyJ_SDK 和 JogAnyJ_Double_SDK 在 Windows 上编译失败的问题
- 修复多个指令示例在 Windows 控制台上中文乱码的问题

## [1.0.0] - 2026-06-29

### 新增
- 上传擎枢控制系统指令手册（指令手册-合-v1.7.5.pdf）
- 添加全部 SDK 示例代码（C++ 和 Python 版本）：
  - DragInCST_SDK（拖拽示教）
  - ForcePositionHybridControl_SDK（力位混合控制）
  - IOModule_SDK（IO 模块）
  - JogAnyJ_SDK / JogAnyJ_Double_SDK（关节点动）
  - JogC_SDK（笛卡尔点动）
  - MoveAbsJ_SDK / MoveAbsJ_Double_SDK（关节绝对运动）
  - MoveBlend_SDK（混合运动）
  - MoveS_SDK（S 曲线运动）
  - MoveSeriesToppJ_SDK（串联关节运动）
  - SubLoop_SDK（子循环控制）
  - SyncAsync_SDK（同步异步控制）
  - Topic_SDK（话题通信）
- 添加 common 公共库（rpc 和 topic 通信基础组件）
- 添加 README.md 项目说明文档
