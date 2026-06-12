from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Final


@dataclass(frozen=True, slots=True)
class ContractResult:
    passed: bool
    message: str


@dataclass(frozen=True, slots=True)
class LabModel:
    text: str

    @classmethod
    def from_file(cls, path: Path) -> LabModel:
        return cls(path.read_text(encoding="gb18030", errors="replace"))

    def has_all(self, terms: tuple[str, ...]) -> bool:
        return all(term in self.text for term in terms)

    def missing(self, terms: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(term for term in terms if term not in self.text)

    def contains(self, term: str) -> bool:
        return term in self.text


CheckFn = Callable[[LabModel], ContractResult]


@dataclass(frozen=True, slots=True)
class PDFContract:
    name: str
    check: CheckFn


def require_all(name: str, terms: tuple[str, ...]) -> PDFContract:
    def check(lab: LabModel) -> ContractResult:
        missing = lab.missing(terms)
        if missing:
            return ContractResult(False, f"{name} 缺失: " + " | ".join(missing))
        return ContractResult(True, f"{name} 通过")

    return PDFContract(name, check)


CONTRACTS: Final[tuple[PDFContract, ...]] = (
    require_all(
        "6.1-startup-init-once",
        (
            "OS0.OS_init()",
            "控制器.OS_init()",
            "串口通信.OS_init()",
            "液晶屏.OS_init()",
            "信息显示器.OS_init()",
            "灯带.OS_init()",
            "舵机.OS_init()",
            "舵机.设置角度为_((90s))",
            "高队列最大长度 = 10s",
            "中队列最大长度 = 15s",
            "低队列最大长度 = 20s",
            "吞吐量 = 0s",
            "丢弃数 = 0s",
            "随机种子 = 1234s",
            "系统状态 = 0s",
            "调度模式 = 0s",
            "下次间隔高 = 取随机数(8000s,15000s)",
            "下次间隔中 = 取随机数(3000s,8000s)",
            "下次间隔低 = 取随机数(10000s,20000s)",
            "系统就绪",
        ),
    ),
    require_all(
        "6.1-step1-task-arrival-generation",
        (
            "void 任务到达生成()",
            "if( 系统状态 != 0s ) { return; }",
            "(当前时间 - 上次到达高) >= 下次间隔高",
            "(当前时间 - 上次到达中) >= 下次间隔中",
            "(当前时间 - 上次到达低) >= 下次间隔低",
            "创建任务(1s)",
            "创建任务(2s)",
            "创建任务(3s)",
            "预计执行时长表[任务ID数字] = 取随机数(2000s,6000s)",
            "到达时刻表[任务ID数字] = 当前时间",
            "任务到达: ID=",
            "队列满，丢弃任务 ID=",
            "设置灯带颜色(255s,120s,0s)",
            "取随机数(8000s,15000s)",
            "取随机数(3000s,8000s)",
            "取随机数(10000s,20000s)",
        ),
    ),
    require_all(
        "6.1-step2-dispatch-and-execute",
        (
            "void 调度任务()",
            "if( 当前任务ID > 0s )",
            "if( 系统状态 != 0s ) { return; }",
            "if( 调度模式 == 0s )",
            "选择任务_严格优先级()",
            "选择任务_加权轮询()",
            "轮询计数器 = (轮询计数器 + 1s) % 6s",
            "轮询计数器 < 3s",
            "轮询计数器 < 5s",
            "启动任务(临时任务)",
            "当前任务开始时间 = 当前时间",
            "当前任务剩余时间 = 当前任务执行时长",
            "舵机.设置角度为_((180s))",
            "舵机.设置角度为_((90s))",
            "舵机.设置角度为_((0s))",
            "设置灯带颜色(255s,0s,0s)",
            "设置灯带颜色(255s,180s,0s)",
            "设置灯带颜色(0s,255s,0s)",
            "执行任务 ID:",
        ),
    ),
    require_all(
        "6.1-step3-task-completion-check",
        (
            "void 完成当前任务()",
            "if( 当前时间 >= 当前任务完成时刻 )",
            "完成时刻表[当前任务ID] = 当前时间",
            "等待时间 = 开始执行时刻表[当前任务ID] - 到达时刻表[当前任务ID]",
            "周转时间 = 完成时刻表[当前任务ID] - 到达时刻表[当前任务ID]",
            "历史任务ID表[历史记录数] = 当前任务ID",
            "任务完成: ID=",
            "等待时间=",
            "周转时间=",
            "舵机.设置角度为_((90s))",
            "设置灯带颜色(0s,255s,0s)",
            "当前任务ID = -1s",
        ),
    ),
    require_all(
        "6.1-step4-remote-control",
        (
            "void 处理遥控器()",
            "无线遥控器.按键A按下",
            "调度模式 = 1s - 调度模式",
            "RF A MODE",
            "无线遥控器.按键B按下",
            "系统状态 = 1s",
            "RF B PAUSE AFTER CURRENT",
            "无线遥控器.按键C按下",
            "系统状态 = 0s",
            "RF C RESUME",
            "无线遥控器.按键D按下",
            "创建任务(1s)",
            "RF D ADD URGENT",
        ),
    ),
    require_all(
        "6.1-step5-four-buttons",
        (
            "void 显示队列快照()",
            "队列快照序号 = 队列快照序号 + 1s",
            "队首任务ID",
            "等待时间",
            "void 清空所有队列()",
            "高头 = 0s",
            "中头 = 0s",
            "低头 = 0s",
            "暂停取新任务 = 1s",
            "显示模式 = 1s - 显示模式",
            "void 发送性能报告()",
        ),
    ),
    require_all(
        "6.1-step6-matrix-keypad",
        (
            "void 处理矩阵键盘()",
            "矩阵键盘.按键值",
            "键盘数字缓存",
            "高队列最大长度 = 键盘数字缓存",
            "中队列最大长度 = 键盘数字缓存",
            "低队列最大长度 = 键盘数字缓存",
            "KEYPAD SET HIGH",
            "KEYPAD SET MID",
            "KEYPAD SET LOW",
            "KEYPAD RESET PARAM",
            "KEYPAD SHOW PARAM",
            "更新显示()",
        ),
    ),
    require_all(
        "6.1-step7-serial-command-processing",
        (
            "void 处理串口命令()",
            "串口通信.获取一个数据()",
            "STAT",
            "CLEAR",
            "MODE 0",
            "MODE 1",
            "ADD 1",
            "ADD 2",
            "ADD 3",
            "GETQ",
            "发送JSON统计摘要()",
            "清空统计记录()",
            "调度模式 = 0s",
            "调度模式 = 1s",
            "创建任务(1s)",
            "创建任务(2s)",
            "创建任务(3s)",
            "GETQ H=",
        ),
    ),
    require_all(
        "6.1-step8-periodic-report",
        (
            "void 周期报告()",
            "(当前时间 - 上次报告时间) >= 60000s",
            "发送性能报告()",
            "上次报告时间 = 当前时间",
        ),
    ),
    require_all(
        "6.1-step9-screen-refresh-200ms",
        (
            "if( (当前时间 - 上次显示刷新时间) >= 200s )",
            "void 更新显示()",
            "系统状态",
            "调度模式",
            "H/M/L:",
            "当前任务ID",
            "当前任务剩余时间",
            "平均等待时间",
            "吞吐量",
            "队首任务ID",
        ),
    ),
    require_all(
        "6.1-step10-loop-delay",
        (
            "forever {",
            "主程序无限循环()",
            "延时器.延时_毫秒((10s))",
        ),
    ),
    require_all(
        "linkboy-graphical-blocks-remain-visible",
        (
            "//[UserFunctionIns]",
            "//[EventIns]",
            "//[ForeverIns]",
            "//[LoopIns]",
            "//[IfElseIns]",
            "//[ElseIns]",
            "//[FuncIns]",
            "//[接口] char -> 液晶屏.char",
            "//[接口] receive -> 无线接收器.receive1",
        ),
    ),
)


def build_pdf_contracts() -> tuple[PDFContract, ...]:
    return CONTRACTS
