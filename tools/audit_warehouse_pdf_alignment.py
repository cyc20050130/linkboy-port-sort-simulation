from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "work" / "warehouse_scheduler.lab"
REPORT = ROOT / "work" / "warehouse_pdf_alignment_audit.md"


def read_gbk(path: Path) -> str:
    return path.read_text(encoding="gb18030", errors="replace")


def evidence(text: str, terms: tuple[str, ...]) -> str:
    missing = [term for term in terms if term not in text]
    if missing:
        return "缺失：" + "、".join(missing)
    return "已覆盖：" + "、".join(terms[:3]) + ("..." if len(terms) > 3 else "")


def main() -> int:
    lab = read_gbk(LAB)
    items = [
        ("三类任务生成", ("创建任务(1s)", "创建任务(2s)", "创建任务(3s)", "紧急订单", "普通补货", "低优先级巡检")),
        ("独立到达间隔", ("8000s,15000s", "3000s,8000s", "10000s,20000s")),
        ("TCB 数据结构", ("任务类型表", "任务优先级表", "预计执行时长表", "到达时刻表", "开始执行时刻表", "完成时刻表")),
        ("三队列容量", ("高队列最大长度 = 10s", "中队列最大长度 = 15s", "低队列最大长度 = 20s")),
        ("严格优先级", ("选择任务_严格优先级", "if( 高队列长度 > 0s )", "if( 中队列长度 > 0s )", "if( 低队列长度 > 0s )")),
        ("加权轮询 3:2:1", ("选择任务_加权轮询", "% 6s", "轮询计数器 < 3s", "轮询计数器 < 5s", "WRR 3:2:1")),
        ("舵机执行", ("180s", "90s", "0s", "舵机.设置角度为_")),
        ("灯带状态", ("255s,0s,0s", "255s,180s,0s", "0s,255s,0s", "255s,120s,0s")),
        ("LCD/2004 等价 OLED", ("液晶屏", "Arduino\\lcd2004PCF8574\\Pack.B", "信息显示器", "ID:", "H/M/L:", "DONE:", "DROP:")),
        ("无线遥控", ("RF A MODE", "RF B PAUSE AFTER CURRENT", "RF C RESUME", "RF D ADD URGENT")),
        ("四按钮", ("SNAPSHOT", "CLEAR ALL QUEUES", "显示模式 = 1s - 显示模式", "发送性能报告()")),
        ("矩阵键盘", ("digit + A/B/C", "* 重置默认", "# 显示参数")),
        ("串口命令", ("STAT", "CLEAR", "MODE 0/1", "ADD 1/2/3", "GETQ")),
        ("主循环无限循环", ("forever {", "主程序无限循环()", "任务到达生成()", "调度任务()", "延时器.延时_毫秒((10s))")),
        ("周期性能报告", ("周期报告()", "60000s", "发送性能报告()")),
        ("图形化而非代码模式", ("//[UserFunctionIns]", "//[ForeverIns]", "//[LoopIns]", "//[IfElseIns]", "//[ElseIns]", "//[FuncIns]")),
    ]
    lines = [
        "# 智能仓库任务调度 PDF 对齐审计",
        "",
        "| PDF 功能点 | 证据 |",
        "| --- | --- |",
    ]
    failed = 0
    for name, terms in items:
        row = evidence(lab, terms)
        if row.startswith("缺失"):
            failed += 1
        lines.append(f"| {name} | {row} |")
    lines.extend([
        "",
        "## 说明",
        "",
        "- PDF 前部需求提到过 `5:3:2`，但用户明确要求最终采用 `3:2:1`，且 PDF 6.2.4 伪代码也写 `3:2:1`。",
        "- OLED 128x64 按用户许可用 LinkBoy 稳定的 `LCD/2004 + 信息显示器` 等价实现。",
        f"- SUMMARY failed={failed} total={len(items)}",
    ])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"report={REPORT}")
    print(f"SUMMARY failed={failed} total={len(items)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
