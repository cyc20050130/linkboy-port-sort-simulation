from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


ROOT = Path(r"D:\linkboy")
LAB = ROOT / "work" / "port_sort.lab"
DESKTOP_LAB = Path.home() / "Desktop" / "port_sort.lab"
REPORT = ROOT / "work" / "port_sort_self_check.md"
ASSET_DIR = ROOT / "资产"
LINKBOY_LIB = ROOT / "linkboy" / "Lib"


def read_gbk(path: Path) -> str:
    return path.read_text(encoding="gb18030", errors="replace")


def require(name: str, ok: bool, detail: str = "") -> tuple[str, bool, str]:
    return name, ok, detail


def all_terms(text: str, terms: list[str]) -> bool:
    return all(term in text for term in terms)


def empty_user_functions(text: str) -> list[str]:
    pattern = re.compile(
        r"//\[指令链接\] @(\d+) NextIns -> @(\d+),\r?\n"
        r"//\[UserFunction结构链接\] @\1 CondiEnd -> @\2,"
    )
    return [match.group(1) for match in pattern.finditer(text)]


def visual_user_function_region(text: str) -> str:
    first = text.find("//[UserFunctionIns],")
    if first < 0:
        return ""
    last = text.rfind("//[/UserFunctionIns],")
    if last < 0:
        return text[first:]
    end = text.find("\n", last)
    if end < 0:
        return text[first:]
    return text[first:end]


def forbidden_user_function_vars(text: str) -> list[str]:
    names = [
        "当前时间", "队首索引", "队尾索引", "货物编号", "点阵图标", "灯号",
    ]
    found = []
    region = visual_user_function_region(text)
    for name in names:
        if f"@VAR {name}" in region:
            found.append(name)
    return found


def forbidden_user_function_calls(text: str) -> list[str]:
    region = visual_user_function_region(text)
    calls = []
    for call in ["@MFUNC 点阵屏 清空", "@MFUNC 点阵屏 点亮"]:
        if call in region:
            calls.append(call)
    return calls


def main() -> int:
    if not LAB.exists():
        print(f"FAIL missing lab: {LAB}")
        return 1
    if not REPORT.exists():
        print(f"FAIL missing report: {REPORT}")
        return 1

    lab = read_gbk(LAB)
    report = REPORT.read_text(encoding="utf-8", errors="replace")
    asset_files = sorted(ASSET_DIR.glob("*.lab"), key=lambda p: p.name)
    includes = re.findall(r"#include\s*<([^>]+)>", lab)
    missing_modules = [module for module in includes if not (LINKBOY_LIB / module).exists()]

    empty_user_function_ids = empty_user_functions(lab)
    bad_user_function_vars = forbidden_user_function_vars(lab)
    bad_user_function_calls = forbidden_user_function_calls(lab)

    checks = [
        require("20 个分解素材存在", len(asset_files) == 20, f"count={len(asset_files)}"),
        require("报告列出 20 个素材", len(re.findall(r"^\| `.*?\.lab` \|", report, flags=re.M)) == 20),
        require("正式工程和桌面副本一致", DESKTOP_LAB.exists() and hashlib.sha256(LAB.read_bytes()).digest() == hashlib.sha256(DESKTOP_LAB.read_bytes()).digest()),
        require("所有代码 include 模块存在", not missing_modules, ",".join(missing_modules)),
        require("正式工程保留可执行代码区", all_terms(lab, ["void main0()", "#param userspaceon", "void 主循环任务()", "void OS_VarInit()"])),
        require("核心可视化组件齐全", all_terms(lab, [
            "//[名称] 控制器", "//[名称] 串口通信", "//[名称] 液晶屏", "//[名称] 信息显示器",
            "//[名称] 矩阵键盘", "//[名称] 无线接收器", "//[名称] 无线遥控器", "//[名称] PPM遥控器",
            "//[名称] 湿度传感器", "//[名称] 称重传感器", "//[名称] 点阵屏", "//[名称] 灯带",
            "//[名称] 舵机", "//[名称] 四按钮", "//[名称] 延时器",
        ])),
        require("LCD I2C 地址显式设置为 PCF8574 常用 0x27", all_terms(lab, ["const int32 液晶屏_地址 = 0x27", "//[参数] Addr = 0x27"])),
        require("舵机使用可视化模块且不是旧空模块", all_terms(lab, ["//[组件路径] ModuleLib output\\servo\\Module.M", "//[名称] 舵机"])),
        require("图形积木结构充足", lab.count("//[组件]") >= 15 and lab.count("//[链接]") >= 40 and lab.count("//[指令链接]") >= 160 and lab.count("//[FuncIns]") >= 50),
        require("有反复执行/循环/如果否则/无值函数积木", all_terms(lab, ["//[ForeverIns]", "//[LoopIns]", "//[IfElseIns]", "//[ElseIns]", "//[UserFunctionIns]"])),
        require("无值函数不是空壳", not empty_user_function_ids, ",".join(empty_user_function_ids)),
        require("无值函数内部含可见功能积木", all_terms(lab, [
            "?void @OPER ( *int32 @MVAR 舵机 角度 ) = ( ?int32 @WORD 90 )",
            "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"QUEUE LEN\" )",
            "?void @MFUNC 灯带 设置第 ( ?int32 @WORD 1 ) 个灯绿色分量为 ( ?int32 @WORD 255 )",
            "//[Loop结构链接]",
        ])),
        require("无值展开块不引用前置未声明变量", not bad_user_function_vars, ",".join(bad_user_function_vars)),
        require("无值展开块不调用不稳定点阵积木", not bad_user_function_calls, ",".join(bad_user_function_calls)),
        require("湿度监测使用 DHT11 并按 PDF 60±10 随机兜底", all_terms(lab, ["湿度传感器.湿度()", "当前湿度 <= 0s", "当前湿度 = 60s + 取随机数(0s, 20s) - 10s", "当前湿度 > 80s"])),
        require("湿度报警和正常输出", all_terms(lab, ["ALARM HUMIDITY HIGH", "ALARM CLEAR", "设置灯带颜色(255s, 0s, 0s)", "设置灯带颜色(0s, 255s, 0s)", "显示报警图标()", "显示正常图标()"])),
        require("HX711 称重优先并限制 0-5000g", all_terms(lab, ["int32 读取称重重量()", "称重传感器.数值()", "临时重量 > 5000s", "取随机数(200s, 4500s)"])),
        require("三档重量分类和舵机角度", all_terms(lab, ["临时重量 < 轻货阈值", "临时重量 <= 重货阈值", "角度 = 0s", "角度 = 90s", "角度 = 180s", "舵机.设置角度为_((角度))", "舵机.设置角度为_((90s))"])),
        require("PDF 5.1 历史数组 10 项循环覆盖并可清空", all_terms(lab, [
            "历史时间[10]", "历史重量[10]", "历史类别[10]", "历史有效数",
            "void 保存历史(", "历史时间[历史写位置] = 时间 / 1000s", "历史重量[历史写位置] = 重量", "历史类别[历史写位置] = 类别",
            "历史写位置 >= 10s", "历史写位置 = 0s", "历史有效数 < 10s", "void 清空历史()", "loop( 10s )",
            "loop( 历史有效数 )", "发送类别到串口(历史类别[清理索引])",
        ])),
        require("PDF 5.2 队列 20 项环形缓冲且满时丢弃新任务", all_terms(lab, [
            "队列编号[20]", "队列重量[20]", "队列时间[20]", "队列时[20]", "队列分[20]", "队列秒[20]",
            "队列长度 >= 20s", "QUEUE FULL DROP NEW ID=", "return 0s",
            "void 计算时分秒( int32 时间 )", "队列时[队尾索引] = 临时时", "队列分[队尾索引] = 临时分", "队列秒[队尾索引] = 临时秒",
            "队尾索引 = (队尾索引 + 1s) % 20s", "队列长度 = 队列长度 + 1s",
            "队首索引 = (队首索引 + 1s) % 20s", "队列长度 = 队列长度 - 1s",
            "void 清空队列()", "队首索引 = 0s", "队尾索引 = 0s", "队列长度 = 0s",
        ])),
        require("PDF 5.3 随机数模拟到达/重量/湿度", all_terms(lab, [
            "int32 取随机数( int32 最小值, int32 最大值 )", "随机种子 = 20260604s",
            "下次间隔 = 取随机数(500s, 3000s)", "取随机数(200s, 4500s)", "当前湿度 = 60s + 取随机数(0s, 20s) - 10s",
        ])),
        require("PDF 5.4 系统状态/阈值/灯带/点阵变量齐全", all_terms(lab, [
            "int32 系统状态", "int32 轻货阈值", "int32 重货阈值", "int32 点阵图标",
            "系统状态 = 0s", "系统状态 = 1s", "系统状态 = 2s",
            "轻货阈值 = 1000s", "重货阈值 = 3000s",
            "设置灯带颜色(255s, 0s, 0s)", "设置灯带颜色(0s, 255s, 0s)", "设置灯带颜色(0s, 0s, 255s)", "设置灯带颜色(255s, 120s, 0s)",
            "显示正常图标()", "显示报警图标()",
        ])),
        require("PDF 硬件连线核心引脚对齐", all_terms(lab, [
            "液晶屏.driver.SDA = 控制器.A4", "液晶屏.driver.SCL = 控制器.A5",
            "矩阵键盘.driver.IN1 = 控制器.D2", "矩阵键盘.driver.OUT4 = 控制器.D9",
            "无线接收器.driver.OUTA = 控制器.D10",
            "点阵屏.driver.DIN = 控制器.D11", "点阵屏.driver.CS = 控制器.D12", "点阵屏.driver.CLK = 控制器.D13",
            "湿度传感器.driver.DS = 控制器.A0", "PPM遥控器.driver.PPM = 控制器.D19",
            "灯带.driver.D = 控制器.D20", "称重传感器.driver.DATA = 控制器.A1", "称重传感器.driver.CLK = 控制器.D18",
            "舵机.driver.D = 控制器.D21", "四按钮.driver.K1 = 控制器.D22", "四按钮.driver.K4 = 控制器.D25",
        ])),
        require("串口 115200 和双向命令", all_terms(lab, ["const int32 串口通信_波特率 = 115200", "处理串口命令()", "GET THRES 1000 3000 HIST RESET", "发送历史到串口()", "发送队列到串口()", "发送状态到串口()"])),
        require("串口扩展命令覆盖", all_terms(lab, [
            "CMD GET THRES 1000 3000 HIST RESET S P E Q C W L M 1 2 3 4",
            "串口命令 == ('S')", "启动系统()",
            "串口命令 == ('P')", "暂停系统()",
            "串口命令 == ('E')", "紧急停止()",
            "串口命令 == ('C')", "清空队列并反馈()",
            "串口命令 == ('W')", "手动称重一次()",
            "串口命令 == ('L')", "灯带测试()",
        ])),
        require("矩阵键盘修改阈值和控制系统", all_terms(lab, [
            "矩阵键盘.按键值 == 1s", "矩阵键盘.按键值 == 2s", "矩阵键盘.按键值 == 3s", "矩阵键盘.按键值 == 4s",
            "矩阵键盘.按键值 == 9s", "启动或暂停系统()",
            "矩阵键盘.按键值 == 10s", "紧急停止()",
            "矩阵键盘.按键值 == 11s", "系统复位()",
            "矩阵键盘.按键值 == 12s", "灯带测试()",
            "轻货阈值", "重货阈值",
        ])),
        require("无线四键按 PDF 6.1 启动/暂停/复位/灯带测试", all_terms(lab, [
            "无线遥控器.按键A按下", "启动系统()",
            "无线遥控器.按键B按下", "暂停系统()",
            "无线遥控器.按键C按下", "系统复位()",
            "无线遥控器.按键D按下", "灯带测试()",
            "遥控A上次", "遥控B上次", "遥控C上次", "遥控D上次",
        ])),
        require("PPM 手动舵机控制并限幅到 1000-2000us", all_terms(lab, [
            "PPM遥控器.读取第_通道数据((1s))", "手动模式 == 1s",
            "临时PPM宽度 < 1000s", "临时PPM宽度 = 1000s",
            "临时PPM宽度 > 2000s", "临时PPM宽度 = 2000s",
            "(临时PPM宽度 - 1000s) * 180s / 1000s",
        ])),
        require("四按钮操作覆盖并可切换手动干预", all_terms(lab, [
            "四按钮.按钮1按下", "手动称重一次()",
            "四按钮.按钮2按下", "清空队列并反馈()",
            "四按钮.按钮3按下", "切换点阵图标()", "切换手动模式()",
            "四按钮.按钮4按下", "发送队列到串口()",
        ])),
        require("LCD 显示湿度重量队列状态和阈值", all_terms(lab, [
            "液晶屏.打开背光()",
            "周期刷新液晶屏();",
            "信息显示器.在第_行第_列向后显示数字_((1s),(5s),(当前湿度))",
            "信息显示器.在第_行第_列向后显示数字_((1s),(12s),(队列长度))",
            "信息显示器.在第_行第_列显示信息_((1s),(16s),(",
            "信息显示器.在第_行第_列向后显示数字_((2s),(6s),(最新重量))",
            "信息显示器.在第_行第_列向后显示数字_((2s),(13s),(轻货阈值))",
            "信息显示器.在第_行第_列向后显示数字_((3s),(8s),(重货阈值))",
        ])),
        require("PDF 6.2 子模块伪代码均有对应函数", all_terms(lab, [
            "void 检测湿度()", "void 清空队列()", "int32 入队(", "int32 出队()",
            "void 生成货物()", "void 处理分拣()", "void 处理串口命令()",
            "SORT ID=", "ANGLE=", "ARRIVE=", "THRES OK", "HISTORY LEN=",
        ])),
        require("PDF 6.1 启动初始化完整", all_terms(lab, [
            "void OS_VarInit()", "系统状态 = 0s", "当前时间 = 0s",
            "上次湿度时间 = 当前时间", "上次生成时间 = 当前时间",
            "下次间隔 = 取随机数(500s, 3000s)", "清空队列();", "清空历史();",
            "舵机空闲标志 = 1s", "舵机.设置角度为_((90s))",
        ])),
        require("PDF 6.1 无限循环主程序包含任务调度", all_terms(lab, [
            "forever {", "主循环任务();", "OS0.Schedule();", "控制器.OS_ClearWatchDog();",
            "void 主循环任务()", "当前时间 = 当前时间 + 10s", "检测湿度();",
            "处理遥控与按钮();", "生成货物();", "处理分拣();", "周期刷新液晶屏();", "延时器.延时_毫秒((10s))",
            "舵机空闲标志 == 1s", "舵机空闲标志 = 0s", "舵机空闲标志 = 1s",
        ])),
    ]

    failed = [item for item in checks if not item[1]]
    for name, ok, detail in checks:
        prefix = "PASS" if ok else "FAIL"
        if detail:
            print(f"{prefix} {name} :: {detail}")
        else:
            print(f"{prefix} {name}")

    if failed:
        print(f"SUMMARY failed={len(failed)} total={len(checks)}")
        return 1
    print(f"SUMMARY failed=0 total={len(checks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
