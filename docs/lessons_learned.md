# 本次 LinkBoy 实现经验

## 1. 先学习本地 `.lab` 素材

用户提供的 `资产/` 目录中有 20 个分解版 `.lab`，这些文件比凭空拼模块更可靠。实现总工程前应先扫描它们的组件路径、事件块、函数块、循环块和连线格式，再把可用范式合并到目标工程。

本次吸收的关键素材包括：

- 无线遥控器和接收器：`2.lab`
- 点阵显示：`3.lab`、`4.lab`、`7.lab`
- 串口通信：`5.lab`、`weweek6-20.20.lab`
- 湿度采集：`6.lab`
- LCD、信息显示器、矩阵键盘：`weweek6-1.20.lab`、`weweek6-11.20.lab`
- HX711 称重：`weweek6-10.20.lab`
- 舵机：`weweek6-12.20.lab`、`weweek6-13.20.lab`
- PPM：`weweek6-8.20.lab`
- 灯带：`weweek6-9.20.lab`
- 四按钮：`weweek6-18.20.lab`、`weweek6-19.20.lab`

## 2. `.lab` 要同时满足代码区和图形区

LinkBoy 打开工程时不仅看代码，还看 `//[图形界面]` 后面的组件、链接和积木元数据。只写代码区会导致用户看不到“图片里的东西”，也会出现模块不完善、连线缺失、无值函数空壳等问题。

本次最终工程同时补齐：

- GUI 组件块
- 硬件连线 `//[链接]`
- `UserFunctionIns` 无值函数
- `FuncIns` 子积木
- `ForeverIns`
- `LoopIns`
- `IfElseIns` / `ElseIns`

## 3. LinkBoy 会自动保存并改写 `.lab`

仿真时 LinkBoy 可能自动保存工程，并把源码段或部分元数据改写掉。因此验证时不要直接跑正式 `work/port_sort.lab`，应先复制临时副本，例如：

```powershell
Copy-Item D:\linkboy\work\port_sort.lab D:\linkboy\work\port_sort_window_verify.lab -Force
```

正式文件只由生成脚本和人工确认后的步骤更新。

## 4. 路径、编码和版本字段很关键

本次稳定做法：

- 使用 `D:\linkboy\work\port_sort.lab` 这种英文短路径，避免 LinkBoy 最近路径或中文路径触发非法字符问题。
- `.lab` 用 GBK 写入，贴合 LinkBoy 官方示例。
- 工作台版本字段对齐本机 LinkBoy `5.56.250511`。
- 组件路径尽量来自本机官方示例和用户素材，不凭空猜。

## 5. PDF 章节存在冲突时要记录取舍

PDF 3.2 写队列满时丢弃最旧任务，但 5.2 和 6.2.2 更具体地写为丢弃新任务。本工程按数据结构设计和伪代码章节执行：队列满时丢弃新任务并报警。

无线遥控也类似：部分章节提到紧急停止，6.1 主流程给出 A/B/C/D 具体映射。本工程按 6.1 做 A 启动、B 暂停、C 复位、D 灯带测试；紧急停止保留在串口 `E` 和矩阵键盘 10。

## 6. LCD 空白问题的处理

不能只依赖隐藏源码段驱动 LCD。需要在图形化无值函数中放入真实 `信息显示器` 子积木，让 LinkBoy 打开和仿真时都能看到显示逻辑。

最终显示内容包括：

- `H:` 湿度
- `Q:` 队列长度
- `S:RUN` / 状态
- `W:` 最近重量
- `L:` 轻货阈值

初始化时还需要打开 LCD 背光并设置初始变量。

## 7. 仿真验证只用窗口级截图

本次将探针从 `Screen.PrimaryScreen + CopyFromScreen` 改为 `Application.OpenForms + DrawToBitmap`，只捕获：

- `v_GForm.GForm`
- `n_SimForm.SimForm`

日志使用 `WINDOW_SCREEN=`，不再输出旧的 `SCREEN=`。这是以后本地 GUI/仿真取证的默认做法。

## 8. 可复现验收信号

本次最有用的验收信号：

- `python tools\check_port_sort_requirements.py`
- `python tools\audit_pdf_alignment.py`
- `RunLinkBoySimulationProbe.exe ... windowcap 25`
- `simulation_probe_windowcap.log` 中出现 `EXITING_OK`
- 日志中 `WINDOW_SCREEN=` 存在且 `SCREEN=` 为 0
- 正式 `port_sort.lab` 和临时验证副本分开

这些信号比“能打开一次”更可靠，也便于以后继续维护。
