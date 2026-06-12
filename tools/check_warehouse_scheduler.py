from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "work" / "warehouse_scheduler.lab"
DRAFT = ROOT / "资产" / "第二次项目.lab"


def read_gbk(path: Path) -> str:
    return path.read_text(encoding="gb18030", errors="replace")


def require(name: str, ok: bool, detail: str = "") -> tuple[str, bool, str]:
    return (name, ok, detail)


def has_all(text: str, terms: tuple[str, ...]) -> bool:
    return all(term in text for term in terms)


def count(text: str, term: str) -> int:
    return text.count(term)


def empty_user_function_count(text: str) -> int:
    chunks = text.split("//[UserFunctionIns],")[1:]
    empty = 0
    for chunk in chunks:
        end = chunk.find("//[UserFunction结构链接]")
        region = chunk if end < 0 else chunk[:end]
        if "//[FuncIns]," not in region:
            empty += 1
    return empty


def main() -> int:
    if not LAB.exists():
        print(f"Missing LAB: {LAB}")
        return 1
    text = read_gbk(LAB)
    checks = [
        require("正式工程路径存在", LAB.exists(), str(LAB)),
        require("草稿仍存在且未作为输出路径", DRAFT.exists() and LAB != DRAFT, str(DRAFT)),
        require("代码区存在", has_all(text, ("void main0()", "#param userspaceon", "void 主程序无限循环()"))),
        require("图形组件足够", count(text, "//[组件]") >= 24, f"components={count(text, '//[组件]')}"),
        require("硬件连线存在", count(text, "//[链接]") >= 20, f"links={count(text, '//[链接]')}"),
        require("可见无值函数非空", count(text, "//[UserFunctionIns]") >= 12 and empty_user_function_count(text) == 0, f"user_funcs={count(text, '//[UserFunctionIns]')} empty={empty_user_function_count(text)}"),
        require("可见流程块完整", has_all(text, ("//[ForeverIns]", "//[LoopIns]", "//[IfElseIns]", "//[ElseIns]", "//[FuncIns]"))),
        require("核心硬件模块齐全", has_all(text, ("控制器", "串口通信", "液晶屏", "Arduino\\lcd2004PCF8574\\Pack.B", "信息显示器", "无线接收器", "无线遥控器", "四按钮", "矩阵键盘", "舵机", "灯带", "计时器", "延时器"))),
        require("软件接口已连接", has_all(text, ("//[接口] char -> 液晶屏.char", "//[接口] receive -> 无线接收器.receive1"))),
        require("三队列默认容量", has_all(text, ("高队列最大长度 = 10s", "中队列最大长度 = 15s", "低队列最大长度 = 20s", "Number = 10", "Number = 15", "Number = 20"))),
        require("TCB字段覆盖", has_all(text, ("任务ID数字", "任务类型表", "任务优先级表", "预计执行时长表", "到达时刻表", "开始执行时刻表", "完成时刻表"))),
        require("到达间隔覆盖", has_all(text, ("取随机数(8000s,15000s)", "取随机数(3000s,8000s)", "取随机数(10000s,20000s)"))),
        require("严格优先级调度", has_all(text, ("选择任务_严格优先级", "高队列长度 > 0s", "中队列长度 > 0s", "低队列长度 > 0s"))),
        require("加权轮询3:2:1", has_all(text, ("选择任务_加权轮询", "% 6s", "轮询计数器 < 3s", "轮询计数器 < 5s", "WRR 3:2:1")) and "5:3:2" not in text),
        require("舵机角度动作", has_all(text, ("舵机.设置角度为_((180s))", "舵机.设置角度为_((90s))", "舵机.设置角度为_((0s))"))),
        require("灯带状态颜色", has_all(text, ("设置灯带颜色(255s,0s,0s)", "设置灯带颜色(255s,180s,0s)", "设置灯带颜色(0s,255s,0s)", "设置灯带颜色(255s,120s,0s)"))),
        require("LCD/信息显示内容", has_all(text, ("ID:", "T:", "当前时间", "Q:", "Done:", "Drop:", "WRR 3:2:1"))),
        require("无线A/B/C/D", has_all(text, ("无线遥控器.按键A按下", "无线遥控器.按键B按下", "无线遥控器.按键C按下", "无线遥控器.按键D按下", "RF A MODE", "RF B PAUSE", "RF C RESUME", "RF D ADD URGENT"))),
        require("四按钮功能", has_all(text, ("SNAPSHOT", "CLEAR ALL QUEUES", "显示模式 = 1s - 显示模式", "发送性能报告()"))),
        require("矩阵键盘配置", has_all(text, ("digit + A/B/C", "* 重置默认", "# 显示参数", "高队列最大长度", "中队列最大长度", "低队列最大长度"))),
        require("串口命令表", has_all(text, ("STAT", "CLEAR", "MODE 0/1", "ADD 1/2/3", "GETQ"))),
        require("周期报告和10ms循环", has_all(text, ("60000s", "当前时间 = 当前时间 + 10s", "延时器.延时_毫秒((10s))", "周期报告()"))),
        require("随机种子固定", "随机种子 = 1234s" in text),
    ]
    failed = [item for item in checks if not item[1]]
    for name, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        print(f"{status} {name}" + (f" :: {detail}" if detail else ""))
    if failed:
        print(f"SUMMARY failed={len(failed)} total={len(checks)}")
        return 1
    print(f"SUMMARY failed=0 total={len(checks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
