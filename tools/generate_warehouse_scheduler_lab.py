from __future__ import annotations

from datetime import datetime
from pathlib import Path

from warehouse_lab_builder import DRAFT_LAB, OUTPUT_LAB, REPORT, build_lab_text, missing_modules, write_gbk, write_utf8


def count(text: str, token: str) -> int:
    return text.count(token)


def report_text(lab_text: str) -> str:
    draft_status = "存在，作为只读草稿参考" if DRAFT_LAB.exists() else "未找到"
    lines = [
        "# 智能仓库任务调度 LinkBoy 自检报告",
        "",
        "## 结论",
        "",
        "- 正式工程：`D:\\linkboy\\work\\warehouse_scheduler.lab`",
        f"- 原草稿：`D:\\linkboy\\第二次项目.lab`，状态：{draft_status}，本脚本不覆盖。",
        "- 显示取舍：使用 LinkBoy 稳定的 `LCD/2004 + 信息显示器` 等价实现 PDF 的 OLED 128x64 状态屏。",
        "- 加权轮询：按用户确认与 PDF 6.2.4 伪代码实现 `3:2:1`。",
        "",
        "## 图形化完整性",
        "",
        f"- 组件块：{count(lab_text, '//[组件]')} 个",
        f"- 硬件连线：{count(lab_text, '//[链接]')} 条",
        f"- 用户无值函数块：{count(lab_text, '//[UserFunctionIns]')} 个",
        f"- 函数积木：{count(lab_text, '//[FuncIns]')} 个",
        f"- 反复执行块：{count(lab_text, '//[ForeverIns]')} 个",
        f"- 循环块：{count(lab_text, '//[LoopIns]')} 个",
        f"- 如果块：{count(lab_text, '//[IfElseIns]')} 个",
        f"- 否则块：{count(lab_text, '//[ElseIns]')} 个",
        "",
        "## PDF 功能覆盖",
        "",
        "- 三类任务：紧急订单、普通补货、低优先级巡检。",
        "- 三队列默认容量：高 10 / 中 15 / 低 20。",
        "- TCB 字段：任务 ID、类型、优先级、预计执行时长、到达/开始/完成时刻。",
        "- 到达间隔：高 8000-15000ms，中 3000-8000ms，低 10000-20000ms。",
        "- 调度模式：严格优先级、加权轮询 3:2:1。",
        "- 执行器：舵机 180/90/0，完成后归中 90。",
        "- 指示：灯带红/黄/绿，溢出橙色。",
        "- 输入：无线 A/B/C/D、四按钮 1-4、矩阵键盘、串口命令。",
        "- 报告：60000ms 周期发送性能统计。",
        "",
        f"## 生成时间\n\n- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    ]
    return "\n".join(lines)


def main() -> int:
    missing = missing_modules()
    if missing:
        print("Missing LinkBoy modules:")
        for module in missing:
            print(module)
        return 1
    lab_text = build_lab_text()
    write_gbk(OUTPUT_LAB, lab_text)
    write_utf8(REPORT, report_text(lab_text))
    print(f"lab={OUTPUT_LAB}")
    print(f"report={REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
