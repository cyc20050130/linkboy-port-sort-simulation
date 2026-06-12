from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from warehouse_runtime_flow_contract import FLOW_STEPS, FlowStep


ROOT: Final = Path(__file__).resolve().parents[1]
LAB: Final = ROOT / "work" / "warehouse_scheduler.lab"
WAREHOUSE_LOG: Final = ROOT / "work" / "warehouse_simulation_probe_windowcap.log"
GENERIC_LOG: Final = ROOT / "work" / "simulation_probe_windowcap.log"
LOG: Final = WAREHOUSE_LOG if WAREHOUSE_LOG.exists() else GENERIC_LOG
REPORT: Final = ROOT / "work" / "warehouse_runtime_flow_audit.md"


@dataclass(frozen=True, slots=True)
class AuditResult:
    name: str
    passed: bool
    evidence: str
    note: str


def read_text(path: Path, encoding: str) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding=encoding, errors="replace")


def status_text(passed: bool) -> str:
    if passed:
        return "PASS"
    return "FAIL"


def summarize_missing(text: str, terms: tuple[str, ...]) -> tuple[bool, str]:
    missing = [term for term in terms if term not in text]
    if missing:
        return False, "缺失：" + "、".join(missing)
    return True, "已覆盖：" + "、".join(terms[:4]) + ("..." if len(terms) > 4 else "")


def audit_flow_steps(lab_text: str) -> list[AuditResult]:
    results: list[AuditResult] = []
    for step in FLOW_STEPS:
        passed, evidence = summarize_missing(lab_text, step.evidence_terms)
        results.append(AuditResult(step.name, passed, evidence, step.note))
    return results


def probe_checks(log_text: str) -> list[AuditResult]:
    window_count = log_text.count("WINDOW_SCREEN=")
    full_screen_count = log_text.count("\nSCREEN=")
    exception_terms = ("THREAD_EXCEPTION", "INVOKE_TARGET", "JIT", "FAIL")
    exception_hits = [term for term in exception_terms if term in log_text]
    checks = (
        AuditResult("LinkBoy 主窗体打开", "CALL U.U.Main" in log_text and "GHead=n_Head.Head" in log_text, "CALL U.U.Main / GHead", "证明工程被 LinkBoy 加载。"),
        AuditResult("仿真入口触发", "INVOKED SimuButton_MouseDownEvent" in log_text and "环境模拟机" in log_text, "SimuButton + 环境模拟机", "证明已进入仿真界面。"),
        AuditResult("运行按钮触发", "INVOKED ButtonRunClick" in log_text, "ButtonRunClick", "证明环境模拟机点击了运行。"),
        AuditResult("窗口级截图", window_count > 0 and full_screen_count == 0, f"WINDOW_SCREEN={window_count}, SCREEN={full_screen_count}", "符合只做窗口级截图的偏好。"),
        AuditResult("无探针异常", "EXITING_OK" in log_text and not exception_hits, "EXITING_OK" if not exception_hits else "异常：" + "、".join(exception_hits), "证明探针流程正常退出。"),
    )
    return list(checks)


def business_log_status(log_text: str) -> AuditResult:
    business_terms = ("任务到达", "执行任务", "任务完成", "STAT JSON", "GETQ H=")
    hits = [term for term in business_terms if term in log_text]
    if hits:
        return AuditResult("业务串口内容捕获状态", True, "捕获：" + "、".join(hits), "探针日志已包含业务串口文本。")
    return AuditResult(
        "业务串口内容捕获状态",
        False,
        "当前窗口级探针未直接捕获业务串口输出",
        "这不等于业务逻辑缺失；业务流程证据来自正式工程代码区和图形区结构。",
    )


def write_report(probe: list[AuditResult], business: AuditResult, flow: list[AuditResult]) -> None:
    failed = sum(1 for item in flow if not item.passed)
    lines = [
        "# 智能仓库运行流程审计",
        "",
        "## 结论",
        "",
        f"- LinkBoy 仿真壳层证据：{status_text(all(item.passed for item in probe))}",
        f"- PDF 6.1 十环节工程证据：{status_text(failed == 0)}",
        f"- 业务串口内容捕获状态：{business.evidence}",
        "",
        "## LinkBoy 仿真壳层证据",
        "",
        "| 检查项 | 状态 | 证据 | 说明 |",
        "| --- | --- | --- | --- |",
    ]
    for item in probe:
        lines.append(f"| {item.name} | {status_text(item.passed)} | {item.evidence} | {item.note} |")
    lines.extend(
        [
            "",
            "## 业务串口内容捕获状态",
            "",
            f"- {business.evidence}。",
            f"- {business.note}",
            "",
            "## PDF 6.1 主程序流程逐项映射",
            "",
            "| 环节 | 状态 | 工程证据 | 说明 |",
            "| --- | --- | --- | --- |",
        ],
    )
    for item in flow:
        lines.append(f"| {item.name} | {status_text(item.passed)} | {item.evidence} | {item.note} |")
    lines.extend(
        [
            "",
            "## 审计边界",
            "",
            "- 当前 `RunLinkBoySimulationProbe.exe` 能确认 LinkBoy 打开、进入环境模拟机、点击运行、窗口存活和无异常。",
            "- 当前探针不读取 LinkBoy 内部串口/信息显示器控件文本，因此不能把窗口级探针日志冒充为完整业务串口日志。",
            "- 若后续要拿到真实业务串口输出，需要继续增强探针，捕获 LinkBoy 串口窗口或在工程中加入可见运行计数/状态探针。",
            "",
            f"SUMMARY failed={failed} total={len(flow)}",
        ],
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    lab_text = read_text(LAB, "gb18030")
    log_text = read_text(LOG, "utf-8")
    probe = probe_checks(log_text)
    business = business_log_status(log_text)
    flow = audit_flow_steps(lab_text)
    write_report(probe, business, flow)
    failed = sum(1 for item in flow if not item.passed)
    probe_failed = sum(1 for item in probe if not item.passed)
    print(f"report={REPORT}")
    print(f"probe_failed={probe_failed} business_serial_captured={business.passed}")
    print(f"SUMMARY failed={failed} total={len(flow)}")
    return 1 if failed or probe_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
