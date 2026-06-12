from __future__ import annotations

import re
from pathlib import Path


LAB = Path(__file__).resolve().parents[1] / "work" / "warehouse_scheduler.lab"


def read_lab() -> str:
    return LAB.read_text(encoding="gb18030", errors="replace")


def test_lcd_graphical_blocks_use_four_short_rows_with_live_numbers() -> None:
    text = read_lab()

    required_terms = (
        '?void @MFUNC 信息显示器 清空',
        '?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 1 ) 行第 ( ?int32 @WORD 1 ) 列显示信息 ( ?Cstring @WORD "ID:" )',
        '?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 1 ) 行第 ( ?int32 @WORD 4 ) 列向后显示数字 ( ?int32 @VAR 当前任务ID )',
        '?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 1 ) 行第 ( ?int32 @WORD 10 ) 列显示信息 ( ?Cstring @WORD "T:" )',
        '?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 1 ) 行第 ( ?int32 @WORD 12 ) 列向后显示数字 ( ?int32 @VAR 当前时间 )',
        '?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 2 ) 行第 ( ?int32 @WORD 1 ) 列显示信息 ( ?Cstring @WORD "Q:" )',
        '?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 3 ) 行第 ( ?int32 @WORD 1 ) 列显示信息 ( ?Cstring @WORD "Done:" )',
        '?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 4 ) 行第 ( ?int32 @WORD 1 ) 列显示信息 ( ?Cstring @WORD "WRR 3:2:1" )',
    )

    missing = [term for term in required_terms if term not in text]
    assert missing == []

    lcd_literals = re.findall(
        r"信息显示器 在第 \( \?int32 @WORD [1-4] \) 行第 .*?\?Cstring @WORD \"([^\"]*)\"",
        text,
    )
    assert lcd_literals
    assert all(len(item) <= 20 for item in lcd_literals)


def test_main_loop_advances_local_time_so_screen_numbers_change() -> None:
    text = read_lab()

    required_terms = (
        "当前时间 = 当前时间 + 10s;",
        "延时器.延时_毫秒((10s));",
        "if( (当前时间 - 上次显示刷新时间) >= 200s )",
        '信息显示器.在第_行第_列显示信息_((1s),(10s),("T:"));',
        "信息显示器.在第_行第_列向后显示数字_((1s),(12s),(当前时间));",
    )

    missing = [term for term in required_terms if term not in text]
    assert missing == []

    assert "当前时间 = 计时器.计时时间;" not in text


def test_graphical_task_arrival_does_not_reset_screen_time_to_zero() -> None:
    text = read_lab()

    forbidden_terms = (
        "?void @OPER ( *int32 @VAR 当前时间 ) = ( ?int32 @WORD 0 )",
        "?void @OPER ( *int32 @VAR 当前时间 ) = ( ?int32 @WORD 0s )",
        "?void @USER 任务到达生成",
    )

    present = [term for term in forbidden_terms if term in text]
    assert present == []


def test_serial_receive_graphical_blocks_read_data_and_emit_command_responses() -> None:
    text = read_lab()

    required_terms = (
        "?void @OPER ( *int32 @VAR 串口命令 ) = ( ?int32 @MFUNC 串口通信 获取一个数据 )",
        '?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD "STAT JSON" )',
        '?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD "GETQ H=" )',
        '?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD "MODE 0" )',
        '?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD "MODE 1" )',
        '?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD "ADD 1" )',
        '?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD "ADD 2" )',
        '?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD "ADD 3" )',
        '?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD "CLEAR OK" )',
    )

    missing = [term for term in required_terms if term not in text]
    assert missing == []


def test_serial_source_uses_simple_linkboy_conditions_for_getq_aliases() -> None:
    text = read_lab()

    assert "串口命令 == ('G') || 串口命令 == ('Q')" not in text
    assert "if( 串口命令 == ('G') )" in text
    assert "if( 串口命令 == ('Q') )" in text


def test_all_graphical_variable_references_have_visible_variable_blocks() -> None:
    text = read_lab()

    used = set(re.findall(r"@VAR ([^ )]+)", text))
    declared = set(
        re.findall(
            r"//\[名称\] ([^,\r\n]+),\s*//\[常量\] False,\s*//\[类型\] int32",
            text,
        )
    )

    assert used - declared == set()
