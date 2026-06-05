# 基于 LINKBOY 的港口货物分拣仿真系统

这个仓库保存本次港口货物分拣仿真作业的可复现成果：从 PDF 方案和 20 个 LinkBoy 分解案例中整合出的总工程、生成脚本、静态审查脚本、窗口级仿真探针和验证证据。

## 核心成果

- 正式工程：`work/port_sort.lab`
- 分解素材：`资产/*.lab`，共 20 个 LinkBoy 案例
- 生成脚本：`tools/generate_port_sort_lab.py`
- PDF 对齐审查：`tools/audit_pdf_alignment.py`
- 功能静态检查：`tools/check_port_sort_requirements.py`
- 本地仿真探针：`tools/RunLinkBoySimulationProbe.cs`
- 窗口级截图工具：`tools/capture_linkboy_windows.ps1`
- 仿真探针编译件：`tools/bin/RunLinkBoySimulationProbe.exe`

## 已实现功能

- 环境监测：DHT11 湿度采集，80% 阈值报警，灯带和点阵状态提示。
- 货物分拣：HX711 称重或随机重量兜底，轻/中/重三档分类，舵机 0/90/180 度分拣并归中。
- 数据结构：10 项历史循环数组，20 项任务环形队列，满队列按 PDF 5.2/6.2.2 丢弃新任务并报警。
- 主流程：初始化硬件、清空历史/队列、设置随机种子、进入无限循环，调度湿度、交互、串口、生成、分拣和屏幕刷新。
- 人机交互：LCD、矩阵键盘、无线四键、PPM、四按钮、串口命令、灯带、点阵屏。
- 图形化可见性：正式 `.lab` 包含控制器、串口、LCD、键盘、无线、PPM、湿度、称重、点阵、灯带、舵机、四按钮和延时器组件，并包含无值函数、反复执行、如果/否则、循环等图形化积木块。

## 验证结果

最近一次窗口级仿真探针验证：

- 临时验证工程：`D:\linkboy\work\port_sort_window_verify.lab`
- 探针日志：`work/simulation_probe_windowcap.log`
- 结果：`EXITING_OK`
- 窗口截图记录：`WINDOW_SCREEN=` 共 7 条
- 旧整屏截图记录：`SCREEN=` 共 0 条
- 主 LinkBoy 窗口截图尺寸：`1812x1230`
- 环境模拟机窗口截图尺寸：`220x93`

静态验收：

```powershell
python tools\check_port_sort_requirements.py
python tools\audit_pdf_alignment.py
```

审查报告见：

- `work/port_sort_self_check.md`
- `work/pdf_alignment_audit.md`
- `work/port_sort_experiment_report.md`

## 使用方式

1. 安装或准备 LinkBoy v5.56，本机验证路径为 `D:\linkboy\linkboy`。
2. 用 LinkBoy 打开 `work/port_sort.lab`。
3. 点击仿真入口，或使用探针自动触发仿真。

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
