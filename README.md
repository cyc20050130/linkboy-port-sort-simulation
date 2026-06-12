# LinkBoy 仿真项目成果仓库

这个仓库保存 LinkBoy 仿真作业的可复现成果、生成脚本、静态审查脚本、窗口级仿真探针和踩坑经验。

目前包含两个项目：

- 港口货物分拣仿真系统：`work/port_sort.lab`
- 多级优先级队列智能仓库任务调度仿真系统：`work/warehouse_scheduler.lab`

## 港口分拣成果

- 正式工程：`work/port_sort.lab`
- 分解素材：`资产/*.lab`，共 20 个 LinkBoy 案例
- 生成脚本：`tools/generate_port_sort_lab.py`
- PDF 对齐审查：`tools/audit_pdf_alignment.py`
- 功能静态检查：`tools/check_port_sort_requirements.py`
- 本地仿真探针：`tools/RunLinkBoySimulationProbe.cs`
- 窗口级截图工具：`tools/capture_linkboy_windows.ps1`
- 仿真探针编译件：`tools/bin/RunLinkBoySimulationProbe.exe`

### 港口分拣已实现功能

- 环境监测：DHT11 湿度采集，80% 阈值报警，灯带和点阵状态提示。
- 货物分拣：HX711 称重或随机重量兜底，轻/中/重三档分类，舵机 0/90/180 度分拣并归中。
- 数据结构：10 项历史循环数组，20 项任务环形队列，满队列按 PDF 5.2/6.2.2 丢弃新任务并报警。
- 主流程：初始化硬件、清空历史/队列、设置随机种子、进入无限循环，调度湿度、交互、串口、生成、分拣和屏幕刷新。
- 人机交互：LCD、矩阵键盘、无线四键、PPM、四按钮、串口命令、灯带、点阵屏。
- 图形化可见性：正式 `.lab` 包含控制器、串口、LCD、键盘、无线、PPM、湿度、称重、点阵、灯带、舵机、四按钮和延时器组件，并包含无值函数、反复执行、如果/否则、循环等图形化积木块。

## 智能仓库成果

- 原始 PDF：`基于多级优先级队列的智能仓库任务调度仿真系统.pdf`
- 草稿参考：`资产/第二次项目.lab`
- 正式工程：`work/warehouse_scheduler.lab`
- 生成脚本：`tools/generate_warehouse_scheduler_lab.py`
- LinkBoy LAB 构建器：`tools/warehouse_lab_builder.py`
- 功能静态检查：`tools/check_warehouse_scheduler.py`
- PDF 对齐审计：`tools/audit_warehouse_pdf_alignment.py`
- PDF 6.1 运行流程审计：`tools/audit_warehouse_runtime_flow.py`
- TDD 合约：`tools/warehouse_tdd_contracts.py`
- 自动测试：`tests/test_warehouse_*.py`
- 审查报告：`work/warehouse_self_check.md`、`work/warehouse_pdf_alignment_audit.md`、`work/warehouse_runtime_flow_audit.md`
- 窗口级探针日志：`work/warehouse_simulation_probe_windowcap.log`

### 智能仓库已实现功能

- 三类任务：紧急订单、普通补货、低优先级巡检。
- 三队列默认容量：高 10 / 中 15 / 低 20。
- TCB 数据结构：任务 ID、类型、优先级、预计执行时长、到达/开始/完成时刻。
- 到达间隔：高 8000-15000ms，中 3000-8000ms，低 10000-20000ms。
- 调度模式：严格优先级、加权轮询 `3:2:1`。
- 执行器：舵机按任务类型转到 180/90/0 度，完成后归中 90 度。
- 指示：灯带红/黄/绿，溢出橙色。
- 输入：无线 A/B/C/D、四按钮、矩阵键盘、串口命令。
- 显示：用 LinkBoy 稳定的 `LCD/2004 + 信息显示器` 等价实现 OLED 128x64。
- 主循环：本地推进 `当前时间 = 当前时间 + 10ms`，LCD 第一行显示 `T:` 运行时间，避免仿真计时器不递增导致屏幕数字不变。

### 智能仓库关键格式规则

- 图形区 `@USER` 只能调用图形区已有 `UserFunctionIns`，不能直接调用隐藏代码函数，例如禁止 `?void @USER 任务到达生成`。
- 图形化积木不能把运行时变量反复清零，例如禁止在到达生成块里写 `当前时间 = 0`。
- LCD、串口、舵机、灯带等用户可见动作必须在图形区有对应积木，不能只靠代码区。
- 仿真验证用临时副本，避免 LinkBoy 自动保存改写正式 `.lab`。
- 截图只用窗口级 `WINDOW_SCREEN=`，不做全屏 `SCREEN=`。

## 验证结果

最近一次窗口级仿真探针验证：

- 临时验证工程：`D:\linkboy\work\port_sort_window_verify.lab`
- 探针日志：`work/simulation_probe_windowcap.log`
- 结果：`EXITING_OK`
- 窗口截图记录：`WINDOW_SCREEN=` 共 7 条
- 旧整屏截图记录：`SCREEN=` 共 0 条
- 主 LinkBoy 窗口截图尺寸：`1812x1230`
- 环境模拟机窗口截图尺寸：`220x93`

智能仓库最近一次验证：

- `python -m pytest tests -q`：`19 passed`
- `python tools\check_warehouse_scheduler.py`：`SUMMARY failed=0 total=23`
- `python tools\audit_warehouse_pdf_alignment.py`：`SUMMARY failed=0 total=16`
- `python tools\audit_warehouse_runtime_flow.py`：`SUMMARY failed=0 total=10`
- `work/warehouse_simulation_probe_windowcap.log`：`EXITING_OK`

静态验收命令：

```powershell
python tools\check_port_sort_requirements.py
python tools\audit_pdf_alignment.py
python tools\check_warehouse_scheduler.py
python tools\audit_warehouse_pdf_alignment.py
python tools\audit_warehouse_runtime_flow.py
python -m pytest tests -q
```

审查报告见：

- `work/port_sort_self_check.md`
- `work/pdf_alignment_audit.md`
- `work/port_sort_experiment_report.md`

## 使用方式

1. 安装或准备 LinkBoy v5.56，本机验证路径为 `D:\linkboy\linkboy`。
2. 用 LinkBoy 打开 `work/port_sort.lab`。
3. 或打开 `work/warehouse_scheduler.lab` 查看智能仓库项目。
4. 点击仿真入口，或使用探针自动触发仿真。

重新生成智能仓库正式工程：

```powershell
python tools\generate_warehouse_scheduler_lab.py
python tools\check_warehouse_scheduler.py
python -m pytest tests -q
```

探针编译命令：

```powershell
& C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe `
  /nologo /target:winexe `
  /out:D:\linkboy\linkboy\RunLinkBoySimulationProbe.exe `
  /r:System.Windows.Forms.dll /r:System.Drawing.dll `
  D:\linkboy\tools\RunLinkBoySimulationProbe.cs
```

探针运行建议使用临时 `.lab` 副本，避免 LinkBoy 仿真自动保存污染正式文件：

```powershell
Copy-Item D:\linkboy\work\port_sort.lab D:\linkboy\work\port_sort_window_verify.lab -Force
$env:LINKBOY_PROBE_MODE='windowcap'
$env:LINKBOY_PROBE_SECONDS='25'
Start-Process D:\linkboy\linkboy\RunLinkBoySimulationProbe.exe `
  -ArgumentList @('D:\linkboy\work\port_sort_window_verify.lab','windowcap','25') `
  -Wait -WindowStyle Hidden
```

## 截图原则

本仓库的仿真取证只使用窗口级截图，只抓 LinkBoy 主窗口和“环境模拟机”等目标窗口，不抓取整个桌面。这是为了避免影响正在使用的电脑，也避免记录无关桌面内容。

## 目录说明

- `资产/`：用户提供的 20 个分解版 `.lab` 案例。
- `work/`：正式 `.lab`、报告和窗口级验证证据。
- `tools/`：生成、审查和仿真验证工具。
- `docs/`：本次实现经验和维护说明。

第三方 LinkBoy 安装目录、旧整屏截图、临时验证副本和探索性脚本不纳入仓库。
