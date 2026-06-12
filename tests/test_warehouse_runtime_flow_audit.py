from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "audit_warehouse_runtime_flow.py"
REPORT = ROOT / "work" / "warehouse_runtime_flow_audit.md"


def test_runtime_flow_audit_maps_probe_and_pdf_61_steps() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    report = REPORT.read_text(encoding="utf-8")

    assert "LinkBoy 仿真壳层证据" in report
    assert "业务串口内容捕获状态" in report
    assert "当前窗口级探针未直接捕获业务串口输出" in report

    expected_steps = (
        "启动初始化一次",
        "任务到达生成",
        "调度与任务执行",
        "任务执行完成检查",
        "遥控器信号处理",
        "四按钮独立按键处理",
        "矩阵键盘扫描",
        "串口接收处理",
        "周期性性能报告",
        "屏幕刷新与10ms循环延时",
    )
    for step in expected_steps:
        assert f"| {step} | PASS |" in report

    assert "SUMMARY failed=0 total=10" in result.stdout
