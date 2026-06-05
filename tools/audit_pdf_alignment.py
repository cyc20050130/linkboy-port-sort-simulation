from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
import re
import sys


ROOT = Path(r"D:\linkboy")
LAB = ROOT / "work" / "port_sort.lab"
DESKTOP_LAB = Path.home() / "Desktop" / "port_sort.lab"
PDF_TEXT = ROOT / "work" / "pdf_extract.txt"
REPORT = ROOT / "work" / "pdf_alignment_audit.md"
EXPERIMENT_REPORT = ROOT / "work" / "port_sort_experiment_report.md"
SOAK_LOG = ROOT / "work" / "simulation_probe_30min.log"


@dataclass(frozen=True)
class Item:
    section: str
    requirement: str
    terms: tuple[str, ...] = ()
    status_if_pass: str = "通过"
    note: str = ""
    optional: bool = False
    unverifiable: bool = False


def read_gbk(path: Path) -> str:
    return path.read_text(encoding="gb18030", errors="replace")


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def line_for(text: str, term: str) -> int | None:
    for idx, line in enumerate(text.splitlines(), 1):
        if term in line:
            return idx
    return None


def escape_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", "<br>")


def evidence_for(lab: str, terms: tuple[str, ...]) -> str:
    evidence: list[str] = []
    for term in terms[:5]:
        line = line_for(lab, term)
        if line is None:
            evidence.append(f"缺 `{term}`")
        else:
            evidence.append(f"`port_sort.lab:{line}` `{term}`")
    if len(terms) > 5:
        evidence.append(f"另 {len(terms) - 5} 项关键词已检查")
    return "<br>".join(evidence)


def soak_status() -> tuple[str, str]:
    if not SOAK_LOG.exists():
        return "未验证", "尚未跑满 PDF 3.2 的 30 分钟连续运行浸泡测试"
    text = read_utf8(SOAK_LOG)
    bad_terms = ["THREAD_EXCEPTION", "INVOKE_TARGET", "JIT", "Unhandled", "Exception"]
    max_match = re.search(r"^MAX_SECONDS=(\d+)", text, flags=re.M)
    tick_matches = [int(match.group(1)) for match in re.finditer(r"^TICK=(\d+)\b", text, flags=re.M)]
    max_seconds = int(max_match.group(1)) if max_match else 0
    last_tick = max(tick_matches) if tick_matches else 0
    if "EXITING_OK" not in text:
        return "未验证", f"`{SOAK_LOG}` 仍未出现 `EXITING_OK`；当前 `MAX_SECONDS={max_seconds}`、`TICK={last_tick}`"
    before_exit, after_exit = text.split("EXITING_OK", 1)
    runtime_bad = [term for term in bad_terms if term in before_exit]
    post_exit_paint_noise = (
        "THREAD_EXCEPTION" in after_exit
        and "System.Drawing.BufferedGraphics.Render" in after_exit
        and "System.Windows.Forms.Control.WmPaint" in after_exit
    )
    if max_seconds >= 1800 and last_tick >= 1800 and not runtime_bad:
        note = f"`{SOAK_LOG}` 记录 `MAX_SECONDS={max_seconds}`、`TICK={last_tick}`、`EXITING_OK`，运行期未见异常关键词"
        if post_exit_paint_noise:
            note += "；`EXITING_OK` 之后出现 WinForms BufferedGraphics/WmPaint 退出重绘异常，已按退出阶段噪声单独记录"
        return "通过", note
    return "失败", f"`{SOAK_LOG}` 未证明 30 分钟连续运行稳定；MAX_SECONDS={max_seconds}, TICK={last_tick}"


def experiment_report_status() -> tuple[str, str]:
    if not EXPERIMENT_REPORT.exists():
        return "未验证", f"未找到独立实验报告 `{EXPERIMENT_REPORT}`"
    text = read_utf8(EXPERIMENT_REPORT)
    required = [
        "数组在系统中的作用",
        "队列在缓解物流波动中的作用",
        "历史数组",
        "环形队列",
        "缓冲",
        "随机到达",
    ]
    missing = [term for term in required if term not in text]
    if missing:
        return "失败", "实验报告缺少关键词：" + ", ".join(f"`{term}`" for term in missing)
    return "通过", f"`{EXPERIMENT_REPORT}` 已分析数组和队列在缓解物流波动中的作用"


def build_items() -> list[Item]:
    return [
        Item("二/实验目的", "硬件覆盖：控制器、屏幕、矩阵键盘、无线遥控、点阵、串口、湿度、PPM、灯带、称重、舵机、四按钮均出现在图形化工程", (
            "//[名称] 控制器", "//[名称] 液晶屏", "//[名称] 矩阵键盘", "//[名称] 无线遥控器",
            "//[名称] 点阵屏", "//[名称] 串口通信", "//[名称] 湿度传感器", "//[名称] PPM遥控器",
            "//[名称] 灯带", "//[名称] 称重传感器", "//[名称] 舵机", "//[名称] 四按钮",
        )),
        Item("二/实验目的", "数据结构覆盖：数组、队列、随机数用于任务调度", (
            "历史时间[10]", "历史重量[10]", "队列编号[20]", "队列长度", "取随机数(",
        )),
        Item("三/3.1.1", "环境监测：湿度采集、80% 阈值、红色报警/绿色正常、点阵图标、串口报警/解除", (
            "湿度传感器.湿度()", "当前湿度 > 80s", "ALARM HUMIDITY HIGH", "ALARM CLEAR",
            "设置灯带颜色(255s, 0s, 0s)", "设置灯带颜色(0s, 255s, 0s)", "显示报警图标()", "显示正常图标()",
        )),
        Item("三/3.1.2", "货物称重与三档分拣：0-5000g 限制、轻/中/重阈值、舵机 0/90/180、历史保存、串口发送", (
            "称重传感器.数值()", "临时重量 > 5000s", "临时重量 < 轻货阈值", "临时重量 <= 重货阈值",
            "角度 = 0s", "角度 = 90s", "角度 = 180s", "保存历史(", "SORT ID=",
        )),
        Item("三/3.1.3", "无线遥控：A 启动、B 暂停、C 复位、D 灯带测试，按 6.1 具体主流程落地", (
            "无线遥控器.按键A按下", "启动系统()", "无线遥控器.按键B按下", "暂停系统()",
            "无线遥控器.按键C按下", "系统复位()", "无线遥控器.按键D按下", "灯带测试()",
        ), "冲突取舍", "PDF 3.1 同时写到无线紧急停止；PDF 6.1 的 A/B/C/D 具体映射写 B=暂停。本工程按更具体的 6.1 执行，紧急停止保留在串口 E 与矩阵键盘 10。"),
        Item("三/3.1.3", "PPM 手动控制舵机：手动模式下读取 1000-2000us 并映射到 0-180 度", (
            "PPM遥控器.读取第_通道数据((1s))", "手动模式 == 1s", "临时PPM宽度 < 1000s",
            "临时PPM宽度 > 2000s", "(临时PPM宽度 - 1000s) * 180s / 1000s",
        )),
        Item("三/3.1.4", "人机交互：屏幕显示湿度、重量、队列长度、状态、阈值", (
            "液晶屏.打开背光()",
            "信息显示器.在第_行第_列向后显示数字_((1s),(5s),(当前湿度))",
            "信息显示器.在第_行第_列向后显示数字_((2s),(6s),(最新重量))",
            "信息显示器.在第_行第_列向后显示数字_((1s),(12s),(队列长度))",
            "信息显示器.在第_行第_列显示信息_((1s),(16s),(",
            "信息显示器.在第_行第_列向后显示数字_((2s),(13s),(轻货阈值))",
            "信息显示器.在第_行第_列向后显示数字_((3s),(8s),(重货阈值))",
        )),
        Item("三/3.1.4", "矩阵键盘修改轻/重阈值并可启动暂停、急停、复位、灯带测试", (
            "矩阵键盘.按键值 == 1s", "矩阵键盘.按键值 == 2s", "矩阵键盘.按键值 == 3s",
            "矩阵键盘.按键值 == 4s", "矩阵键盘.按键值 == 9s", "矩阵键盘.按键值 == 10s",
            "矩阵键盘.按键值 == 11s", "矩阵键盘.按键值 == 12s",
        )),
        Item("三/3.1.4", "四按钮：手动称重、清空队列、切换点阵图片、发送队列数据", (
            "四按钮.按钮1按下", "手动称重一次()", "四按钮.按钮2按下", "清空队列并反馈()",
            "四按钮.按钮3按下", "切换点阵图标()", "四按钮.按钮4按下", "发送队列到串口()",
        )),
        Item("三/3.1.5", "串口双向通信：上传传感器/队列/报警信息，接收 GET/THRES/HIST/RESET 等命令", (
            "const int32 串口通信_波特率 = 115200", "发送状态到串口()", "发送队列到串口()",
            "ALARM HUMIDITY HIGH", "GET THRES 1000 3000 HIST RESET", "THRES OK", "HISTORY LEN=", "系统复位()",
        )),
        Item("三/3.1.6", "任务调度与缓冲：20 项队列缓存 ID/重量/时间戳，随机到达和重量", (
            "队列编号[20]", "队列重量[20]", "队列时间[20]", "队列时[20]", "队列分[20]", "队列秒[20]",
            "下次间隔 = 取随机数(500s, 3000s)", "取随机数(200s, 4500s)",
        )),
        Item("三/3.2", "湿度数据采集周期为 2 秒", ("(当前时间 - 上次湿度时间) >= 2000s", "上次湿度时间 = 当前时间")),
        Item("三/3.2", "舵机分拣动作 0.5 秒 + 归中 0.2 秒，总动作约 0.7 秒，小于 1 秒", (
            "延时器.延时_毫秒((500s))", "舵机.设置角度为_((90s))", "延时器.延时_毫秒((200s))",
        )),
        Item("三/3.2", "队列容量 20；溢出策略按 5.2/6.2 丢弃新任务并报警", (
            "队列长度 >= 20s", "QUEUE FULL DROP NEW ID=", "报警灯橙色闪烁()", "return 0s",
        ), "冲突取舍", "PDF 3.2 写丢弃最旧任务，但 5.2 与 6.2.2 明确写丢弃新任务；本工程按数据结构和伪代码章节执行。"),
        Item("三/3.2", "串口通信波特率 115200bps", ("const int32 串口通信_波特率 = 115200", "//[参数] baud = 115200")),
        Item("三/3.2", "系统连续运行无死机时间 >=30 分钟", (), unverifiable=True),
        Item("三/3.3", "操作员通过键盘、遥控器、按钮控制；管理员通过串口监控参数", (
            "处理遥控与按钮()", "处理串口命令()", "发送状态到串口()", "发送阈值到串口()",
        )),
        Item("四/硬件设计", "核心引脚映射：LCD A4/A5、键盘 D2-D9、无线 A 路 D10、点阵 D11-D13、湿度 A0、PPM D19、灯带 D20、称重 A1/D18、舵机 D21、四按钮 D22-D25", (
            "液晶屏.driver.SDA = 控制器.A4", "液晶屏.driver.SCL = 控制器.A5",
            "矩阵键盘.driver.IN1 = 控制器.D2", "矩阵键盘.driver.OUT4 = 控制器.D9",
            "无线接收器.driver.OUTA = 控制器.D10", "点阵屏.driver.DIN = 控制器.D11",
            "湿度传感器.driver.DS = 控制器.A0", "PPM遥控器.driver.PPM = 控制器.D19",
            "灯带.driver.D = 控制器.D20", "称重传感器.driver.DATA = 控制器.A1",
            "舵机.driver.D = 控制器.D21", "四按钮.driver.K4 = 控制器.D25",
        ), "等价通过", "PDF 注明 LinkBoy 支持虚拟引脚映射；无线模块实际为四路 OUTA-D，A 路贴 D10，其余三路使用 D26-D28。"),
        Item("五/5.1", "历史数组固定 10 项，记录时间、重量、类别，循环覆盖并跟踪写入位置", (
            "历史时间[10]", "历史重量[10]", "历史类别[10]", "历史写位置",
            "历史时间[历史写位置] = 时间 / 1000s", "历史写位置 >= 10s", "历史写位置 = 0s",
        )),
        Item("五/5.2", "任务队列最大 20，包含编号、重量、到达时间，入队/出队/清空/长度均实现", (
            "队列编号[20]", "队列重量[20]", "队列时[20]", "队尾索引 = (队尾索引 + 1s) % 20s",
            "队首索引 = (队首索引 + 1s) % 20s", "void 清空队列()", "队列长度 = 0s",
        )),
        Item("五/5.3", "随机数：固定种子、到达间隔 500-3000ms、重量 200-4500g、湿度 60±10", (
            "随机种子 = 20260604s", "下次间隔 = 取随机数(500s, 3000s)",
            "取随机数(200s, 4500s)", "当前湿度 = 60s + 取随机数(0s, 20s) - 10s",
        )),
        Item("五/5.4", "其他变量：系统状态 0/1/2、阈值 1000/3000、灯带红绿蓝橙、点阵正常/报警图标", (
            "int32 系统状态", "系统状态 = 0s", "系统状态 = 1s", "系统状态 = 2s",
            "轻货阈值 = 1000s", "重货阈值 = 3000s", "设置灯带颜色(255s, 120s, 0s)",
            "显示正常图标()", "显示报警图标()",
        )),
        Item("六/6.1", "启动初始化：硬件、随机种子、清空队列/历史、运行状态、时间戳、首次随机间隔、舵机归中", (
            "void main0()", "OS_VarInit()", "随机种子 = 20260604s", "清空队列();", "清空历史();",
            "系统状态 = 0s", "上次湿度时间 = 当前时间", "上次生成时间 = 当前时间",
            "下次间隔 = 取随机数(500s, 3000s)", "舵机.设置角度为_((90s))",
        )),
        Item("六/6.1", "无限循环：湿度、键盘/无线/PPM/按钮、串口、货物生成、分拣、屏幕、10ms 延时均被调度", (
            "forever {", "处理串口命令();", "主循环任务();", "检测湿度();", "处理遥控与按钮();",
            "生成货物();", "处理分拣();", "周期刷新液晶屏();", "延时器.延时_毫秒((10s))",
        )),
        Item("六/6.2.1", "湿度监测子程序按伪代码实现", (
            "void 检测湿度()", "(当前时间 - 上次湿度时间) >= 2000s", "当前湿度 > 80s",
            "系统状态 = 2s", "ALARM CLEAR", "上次湿度时间 = 当前时间",
        )),
        Item("六/6.2.2", "队列操作伪代码对应入队/出队/失败返回", (
            "int32 入队(", "if( 队列长度 >= 20s )", "return 0s", "return 1s", "int32 出队()",
        )),
        Item("六/6.2.3", "随机货物生成子程序按独立计时器生成编号、重量、时间并刷新下一间隔", (
            "void 生成货物()", "系统状态 == 0s", "货物编号 = 货物编号 + 1s",
            "最新重量 = 读取称重重量()", "入队(货物编号, 最新重量, 当前时间)", "下次间隔 = 取随机数(500s, 3000s)",
        )),
        Item("六/6.2.4", "分拣处理子程序按空闲标志、出队、分类、舵机动作、历史、串口完成信息实现", (
            "void 处理分拣()", "舵机空闲标志 == 1s", "出队() == 1s", "舵机空闲标志 = 0s",
            "保存历史(临时时间, 临时重量, 类别)", "SORT ID=", "ANGLE=", "舵机空闲标志 = 1s",
        )),
        Item("六/6.2.5", "串口命令解析覆盖 GET/THRES/HIST/RESET", (
            "void 处理串口命令()", "串口命令 == ('G')", "串口命令 == ('T')", "串口命令 == ('H')",
            "串口命令 == ('R')", "串口解析阈值字符()", "发送历史到串口()", "系统复位()",
        )),
        Item("七/7.1", "考核 1：图形化界面连接硬件模块", ("//[组件]", "//[链接]", "//[名称] 舵机", "//[名称] 四按钮")),
        Item("七/7.1", "考核 2：流程图/积木块实现伪代码功能", ("//[ForeverIns]", "//[IfElseIns]", "//[LoopIns]", "//[UserFunctionIns]", "//[FuncIns]")),
        Item("七/7.1", "考核 3：随机货物流与队列调度", ("生成货物()", "取随机数(200s, 4500s)", "队列长度", "处理分拣()")),
        Item("七/7.1", "考核 4：串口观察数据上传并发送阈值指令", ("发送状态到串口()", "发送队列到串口()", "THRES OK", "发送阈值到串口()")),
        Item("七/7.1", "考核 5：实验报告需要分析数组和队列作用", (), "未验证", "当前交付物是 LinkBoy 工程与自检报告，PDF 要求的独立实验报告未作为本轮产物生成。", unverifiable=True),
        Item("七/7.2", "选做：Wi-Fi/MQTT 上传云平台", (), "选做未做", "PDF 标为选做，本轮未实现。", optional=True),
        Item("七/7.2", "选做：点阵屏动态显示货物 ID 条形码", (), "选做未做", "PDF 标为选做，本轮未实现。", optional=True),
        Item("七/7.2", "选做：轻/中/重多级队列优先级调度", (), "选做未做", "PDF 标为选做，本轮未实现。", optional=True),
    ]


def main() -> int:
    if not LAB.exists():
        print(f"FAIL missing lab: {LAB}")
        return 1
    if not PDF_TEXT.exists():
        print(f"FAIL missing pdf extract: {PDF_TEXT}")
        return 1

    lab = read_gbk(LAB)
    pdf = read_utf8(PDF_TEXT)
    rows: list[tuple[Item, str, str, list[str]]] = []
    counts: dict[str, int] = {}

    for item in build_items():
        if item.optional:
            status = item.status_if_pass
            missing: list[str] = []
            evidence = item.note
        elif item.unverifiable and "30 分钟" in item.requirement:
            status, evidence = soak_status()
            missing = []
        elif item.unverifiable and "实验报告" in item.requirement:
            status, evidence = experiment_report_status()
            missing = []
        elif item.unverifiable:
            status = item.status_if_pass
            missing = []
            evidence = item.note
        else:
            missing = [term for term in item.terms if term not in lab]
            status = item.status_if_pass if not missing else "失败"
            evidence = evidence_for(lab, item.terms)
            if item.note:
                evidence += "<br>" + item.note
        counts[status] = counts.get(status, 0) + 1
        rows.append((item, status, evidence, missing))

    desktop_match = DESKTOP_LAB.exists() and hashlib.sha256(LAB.read_bytes()).digest() == hashlib.sha256(DESKTOP_LAB.read_bytes()).digest()
    if desktop_match:
        counts["通过"] = counts.get("通过", 0) + 1
    else:
        counts["失败"] = counts.get("失败", 0) + 1

    lines: list[str] = [
        "# PDF 逐项对齐审查报告",
        "",
        f"- PDF 文本：`{PDF_TEXT}`",
        f"- LinkBoy 工程：`{LAB}`",
        f"- 桌面副本：`{DESKTOP_LAB}`",
        f"- 桌面副本一致性：{'通过' if desktop_match else '失败'}",
        f"- PDF 标题命中：{'通过' if '基于 LINKBOY 的港口货物分拣仿真系统' in pdf else '失败'}",
        "",
        "## 汇总",
        "",
    ]
    for key in ["通过", "等价通过", "冲突取舍", "未验证", "失败", "选做未做"]:
        if key in counts:
            lines.append(f"- {key}: {counts[key]}")
    lines.extend([
        "",
        "## 逐项审查",
        "",
        "| PDF 章节 | 要求 | 结论 | 证据/说明 |",
        "| --- | --- | --- | --- |",
    ])
    for item, status, evidence, missing in rows:
        if missing:
            evidence += "<br>缺失关键词：" + ", ".join(f"`{term}`" for term in missing)
        lines.append(f"| {escape_cell(item.section)} | {escape_cell(item.requirement)} | {status} | {escape_cell(evidence)} |")

    lines.extend([
        "",
        "## 审查口径",
        "",
        "- `通过`：当前 `.lab` 中有直接代码/图形元数据证据。",
        "- `等价通过`：LinkBoy 模块形态或 PDF 注释允许虚拟引脚调整，功能等价且证据存在。",
        "- `冲突取舍`：PDF 不同章节互相冲突，已按更具体的数据结构/主流程伪代码实现。",
        "- `未验证`：需要运行时长测或独立文档产物，当前证据不足，不能算完成。",
        "- `选做未做`：PDF 7.2 明确为选做项。",
    ])

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"audit={REPORT}")
    for key in ["通过", "等价通过", "冲突取舍", "未验证", "失败", "选做未做"]:
        if key in counts:
            print(f"{key}={counts[key]}")

    if counts.get("失败", 0):
        return 1
    if counts.get("未验证", 0):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
