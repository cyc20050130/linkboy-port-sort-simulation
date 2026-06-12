# noqa: SIZE_OK - LinkBoy LAB template generator: cohesive data-driven builder, splitting the template would make IDs harder to audit.
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Final


ROOT: Final = Path(__file__).resolve().parents[1]
DEFAULT_LINKBOY_DIR: Final = ROOT / "linkboy"
FALLBACK_LINKBOY_DIR: Final = ROOT.parent / "linkboy"
LINKBOY_DIR: Final = Path(
    os.environ.get(
        "LINKBOY_DIR",
        str(DEFAULT_LINKBOY_DIR if DEFAULT_LINKBOY_DIR.exists() else FALLBACK_LINKBOY_DIR),
    ),
)
WORK_DIR: Final = ROOT / "work"
OUTPUT_LAB: Final = WORK_DIR / "warehouse_scheduler.lab"
REPORT: Final = WORK_DIR / "warehouse_self_check.md"
DRAFT_LAB: Final = ROOT / "资产" / "第二次项目.lab"


@dataclass(frozen=True, slots=True)
class Component:
    name: str
    path: str
    x: int
    y: int
    params: tuple[str, ...] = ()
    events: tuple[str, ...] = ()
    interfaces: tuple[str, ...] = ()
    keys: str = ""


MODULES: Final[tuple[str, ...]] = (
    r"system\predefine.txt",
    r"Arduino\2560\Pack.B",
    r"Arduino\UART-PC\Pack.B",
    r"Arduino\lcd2004PCF8574\Pack.B",
    r"engine\Text_v2\Text.B",
    r"group1\Key4_4\Pack.B",
    r"group1\RFpad_linker\Pack.B",
    r"group1\RFpad\Pack.B",
    r"driver\RGB_lightArray\Pack.B",
    r"common\servo\Pack.B",
    r"common\button4\Pack.B",
    r"software\count_up\count_up.B",
    r"software\delayer\delayer.B",
    r"system\CommonRef\Servo.txt",
    r"system\os\os.txt",
)


COMPONENTS: Final[tuple[Component, ...]] = (
    Component("控制器", r"Arduino\2560\Pack.B", -680, -170, events=("StartEvent -> 控制器_初始化", "IdleEvent -> 控制器_反复执行")),
    Component("串口通信", r"Arduino\UART-PC\Pack.B", -680, -400, params=("max_length = 160", "baud = 115200"), events=("receive_event -> 串口通信_接收缓冲区有数据时",)),
    Component("液晶屏", r"Arduino\lcd2004PCF8574\Pack.B", -300, -330, params=("Addr = 0x27",)),
    Component("信息显示器", r"engine\Text_v2\Text.B", -300, -125, interfaces=("char -> 液晶屏.char",)),
    Component("矩阵键盘", r"group1\Key4_4\Pack.B", -680, 80),
    Component("无线接收器", r"group1\RFpad_linker\Pack.B", -300, 120),
    Component("无线遥控器", r"group1\RFpad\Pack.B", -300, 300, interfaces=("receive -> 无线接收器.receive1",), keys="0,0,0,0"),
    Component("四按钮", r"common\button4\Pack.B", 55, 85, events=("key1_event -> 四按钮_按钮1按下时", "key2_event -> 四按钮_按钮2按下时", "key3_event -> 四按钮_按钮3按下时", "key4_event -> 四按钮_按钮4按下时")),
    Component("舵机", r"output\servo\Module.M", 55, -300),
    Component("灯带", r"output\RGB_lightArray\Module.M", 390, -300, params=("N = 8",)),
    Component("计时器", r"software\count_up\count_up.B", 390, -60),
    Component("延时器", r"software\delayer\delayer.B", 390, 110),
    Component("紧急订单队列", r"software\Queue\Pack.B", 700, -330, params=("Number = 10",)),
    Component("普通补货队列", r"software\Queue\Pack.B", 700, -185, params=("Number = 15",)),
    Component("低优先级巡检队列", r"software\Queue\Pack.B", 700, -40, params=("Number = 20",)),
    Component("任务ID表", r"software\Arrary\Pack.B", 1030, -330, params=("Number = 45",)),
    Component("任务类型表", r"software\Arrary\Pack.B", 1030, -220, params=("Number = 45",)),
    Component("任务优先级表", r"software\Arrary\Pack.B", 1030, -110, params=("Number = 45",)),
    Component("预计执行时长表", r"software\Arrary\Pack.B", 1030, 0, params=("Number = 45",)),
    Component("到达时刻表", r"software\Arrary\Pack.B", 1030, 110, params=("Number = 45",)),
    Component("开始执行时刻表", r"software\Arrary\Pack.B", 1030, 220, params=("Number = 45",)),
    Component("完成时刻表", r"software\Arrary\Pack.B", 1030, 330, params=("Number = 45",)),
    Component("高到达随机数", r"software\random\random.B", 1360, -330, params=("MinValue = 8000", "MaxValue = 15000")),
    Component("中到达随机数", r"software\random\random.B", 1360, -220, params=("MinValue = 3000", "MaxValue = 8000")),
    Component("低到达随机数", r"software\random\random.B", 1360, -110, params=("MinValue = 10000", "MaxValue = 20000")),
    Component("执行时长随机数", r"software\random\random.B", 1360, 0, params=("MinValue = 2000", "MaxValue = 6000")),
)


LINKS: Final[tuple[str, ...]] = (
    "串口通信 PORT ->#0 控制器 PORT",
    "液晶屏 SDA ->#1 控制器 A4",
    "液晶屏 SCL ->#2 控制器 A5",
    "矩阵键盘 IN1 ->#3 控制器 D30",
    "矩阵键盘 IN2 ->#4 控制器 D31",
    "矩阵键盘 IN3 ->#5 控制器 D32",
    "矩阵键盘 IN4 ->#6 控制器 D33",
    "矩阵键盘 OUT1 ->#7 控制器 D34",
    "矩阵键盘 OUT2 ->#8 控制器 D35",
    "矩阵键盘 OUT3 ->#9 控制器 D36",
    "矩阵键盘 OUT4 ->#0 控制器 D37",
    "无线接收器 OUTA ->#1 控制器 D15",
    "无线接收器 OUTB ->#2 控制器 D16",
    "无线接收器 OUTC ->#3 控制器 D17",
    "无线接收器 OUTD ->#4 控制器 D18",
    "舵机 D ->#5 控制器 D13",
    "舵机 VCC ->#6 控制器 #22",
    "舵机 GND ->#7 控制器 #21",
    "灯带 D ->#8 控制器 D25",
    "灯带 VCC ->#9 控制器 #22",
    "灯带 GND ->#0 控制器 #21",
    "四按钮 K1 ->#1 控制器 D26",
    "四按钮 K2 ->#2 控制器 D27",
    "四按钮 K3 ->#3 控制器 D28",
    "四按钮 K4 ->#4 控制器 D29",
    "四按钮 #0 ->#5 控制器 #21",
)


def source_code() -> str:
    return r"""
//[图形界面],
//以下配置信息和程序代码由linkboy图形界面自动生成,请勿手动修改
//可在www.linkboy.cc下载最新版软件打开此文件

#include <system\predefine.txt>
#define $run$ run
#define $board$ 2560
#define $freq$ 16000000
#define $chip$ MEGA2560
#define $cpu$ MEGA2560
#define $tick$ 1
#define $voffset$ 0
#setcpu $chip$
#.$chip$ = #.COM_MCU;
#define $language$ chinese

public 控制器 =
#include <Arduino\2560\Pack.B>

串口通信.driver.PORT = 控制器.PORT;
串口通信.最大长度 = 串口通信_最大长度;
const int16 串口通信_最大长度 = 160;
串口通信.波特率 = 串口通信_波特率;
const int32 串口通信_波特率 = 115200;
#define $language$ chinese
public 串口通信 =
#include <Arduino\UART-PC\Pack.B>

液晶屏.driver.SDA = 控制器.A4;
液晶屏.driver.SCL = 控制器.A5;
液晶屏.地址 = 液晶屏_地址;
const int32 液晶屏_地址 = 0x27;
#define $language$ chinese
public 液晶屏 =
#include <Arduino\lcd2004PCF8574\Pack.B>

信息显示器.char = 液晶屏.char;
#define $language$ chinese
public 信息显示器 =
#include <engine\Text_v2\Text.B>

矩阵键盘.driver.IN1 = 控制器.D30;
矩阵键盘.driver.IN2 = 控制器.D31;
矩阵键盘.driver.IN3 = 控制器.D32;
矩阵键盘.driver.IN4 = 控制器.D33;
矩阵键盘.driver.OUT1 = 控制器.D34;
矩阵键盘.driver.OUT2 = 控制器.D35;
矩阵键盘.driver.OUT3 = 控制器.D36;
矩阵键盘.driver.OUT4 = 控制器.D37;
#define $language$ chinese
public 矩阵键盘 =
#include <group1\Key4_4\Pack.B>

无线接收器.driver.OUTA = 控制器.D15;
无线接收器.driver.OUTB = 控制器.D16;
无线接收器.driver.OUTC = 控制器.D17;
无线接收器.driver.OUTD = 控制器.D18;
#define $language$ chinese
public 无线接收器 =
#include <group1\RFpad_linker\Pack.B>

无线遥控器.receive = 无线接收器.receive1;
#define $language$ chinese
public 无线遥控器 =
#include <group1\RFpad\Pack.B>

灯带.driver.D = 控制器.D25;
灯带.数量 = 灯带_数量;
const int32 灯带_数量 = 8;
#define $language$ chinese
public 灯带 =
#include <driver\RGB_lightArray\Pack.B>

舵机.driver.D = 控制器.D13;
#define $language$ chinese
public 舵机 =
#include <common\servo\Pack.B>
舵机.driver.ID = SYS_ServoID0;
const uint8 SYS_ServoID0 = 0;

四按钮.driver.K1 = 控制器.D26;
四按钮.driver.K2 = 控制器.D27;
四按钮.driver.K3 = 控制器.D28;
四按钮.driver.K4 = 控制器.D29;
#define $language$ chinese
public 四按钮 =
#include <common\button4\Pack.B>

#define $language$ chinese
public 计时器 =
#include <software\count_up\count_up.B>

#define $language$ chinese
public 延时器 =
#include <software\delayer\delayer.B>

#include <system\CommonRef\Servo.txt>
#param FUNCTION_USED
void SYS_Servo_Clear()
{
	#.舵机.driver.D.D0_OUT = 0;
}
#param FUNCTION_USED
void SYS_Servo_SetPin()
{
	#asm "sbrc r31,0"
	#.舵机.driver.D.D0_OUT = 1;
	#asm "sbrs r31,0"
	#.舵机.driver.D.D0_OUT = 0;
}

OS0 =
#include <system\os\os.txt>
const uint8 x0_OS_R0 = 7; OS0.RUN_NUMBER = x0_OS_R0;
const uint8 x0_OS_R1 = 0; OS0.RUN100us_NUMBER = x0_OS_R1;
const uint8 x0_OS_R2 = 12; OS0.TASK_NUMBER = x0_OS_R2;
#.start = main0;
#.OS = OS0;

void main0()
{
	OS0.OS_init();
	控制器.OS_init();
	串口通信.OS_init();
	液晶屏.OS_init();
	信息显示器.OS_init();
	矩阵键盘.OS_init();
	无线遥控器.OS_init();
	灯带.OS_init();
	舵机.OS_init();
	四按钮.OS_init();
	计时器.OS_init();
	延时器.OS_init();
	OS0.CreateDriver( (#addr 控制器.OS_run), 控制器.OS_time );
	OS0.CreateDriver( (#addr 矩阵键盘.OS_run), 矩阵键盘.OS_time );
	OS0.CreateDriver( (#addr 无线遥控器.OS_run), 无线遥控器.OS_time );
	OS0.CreateDriver( (#addr 舵机.OS_run), 舵机.OS_time );
	OS0.CreateDriver( (#addr 四按钮.OS_run), 四按钮.OS_time );
	OS0.CreateTask( #addr dispatch );
	SYS_Servo.OS_init();
	OS_VarInit();
	液晶屏.打开背光();
	计时器.开始计时();
	更新显示();
	OS0.Start();
	dispatch:
	forever {
		控制器.OS_thread();
		串口通信.OS_thread();
		if( 串口通信.OS_EventFlag.0(bit) == 1 ) {
			串口通信.OS_EventFlag.0(bit) = 0;
			处理串口命令();
		}
		液晶屏.OS_thread();
		灯带.OS_thread();
		主程序无限循环();
		OS0.Schedule();
		控制器.OS_ClearWatchDog();
	}
}

#param userspaceon
int32 系统状态;              // 0=运行, 1=暂停
int32 调度模式;              // 0=严格优先级, 1=加权轮询3:2:1
int32 显示模式;              // 0=性能, 1=队列详情
int32 当前时间;
int32 随机种子;
int32 任务ID数字;
int32 当前任务ID;
int32 当前任务类型;
int32 当前任务剩余时间;
int32 当前任务开始时间;
int32 当前任务执行时长;
int32 当前任务完成时刻;
int32 等待时间;
int32 周转时间;
int32 历史记录数;
int32 队首任务ID;
int32 平均等待时间;
int32 暂停取新任务;
int32 串口命令;
int32 串口解析模式;
int32 上次矩阵键值;
int32 高队列最大长度;
int32 中队列最大长度;
int32 低队列最大长度;
int32 高队列长度;
int32 中队列长度;
int32 低队列长度;
int32 高头; int32 高尾; int32 中头; int32 中尾; int32 低头; int32 低尾;
int32 高队列[10]; int32 中队列[15]; int32 低队列[20];
int32 任务类型表[46]; int32 任务优先级表[46]; int32 预计执行时长表[46];
int32 到达时刻表[46]; int32 开始执行时刻表[46]; int32 完成时刻表[46];
int32 历史任务ID表[46]; int32 历史等待时间表[46]; int32 历史周转时间表[46];
int32 上次到达高; int32 上次到达中; int32 上次到达低;
int32 下次间隔高; int32 下次间隔中; int32 下次间隔低;
int32 轮询计数器; int32 吞吐量; int32 丢弃数;
int32 总等待高; int32 总等待中; int32 总等待低;
int32 完成高; int32 完成中; int32 完成低;
int32 上次显示刷新时间; int32 上次报告时间;
int32 键盘数字缓存; int32 队列快照序号; int32 清理索引; int32 临时任务;
int32 入队结果;
int32 遥控A上次; int32 遥控B上次; int32 遥控C上次; int32 遥控D上次;

int32 取随机数( int32 最小值, int32 最大值 )
{
	随机种子 = ((随机种子 * 1103515245s) + 12345s) % 2147483647s;
	if( 随机种子 < 0s ) { 随机种子 = 0s - 随机种子; }
	return 最小值 + (随机种子 % ((最大值 - 最小值) + 1s));
}

void 设置灯带颜色( int32 红, int32 绿, int32 蓝 )
{
	清理索引 = 1s;
	loop( 8s ) {
		灯带.设置第_个灯红色分量为_((清理索引),(红));
		灯带.设置第_个灯绿色分量为_((清理索引),(绿));
		灯带.设置第_个灯蓝色分量为_((清理索引),(蓝));
		清理索引 = 清理索引 + 1s;
	}
}

void 溢出报警()
{
	丢弃数 = 丢弃数 + 1s;
	设置灯带颜色(255s,120s,0s);
	串口通信.发送字符串_(("队列满，丢弃任务 ID="));
	串口通信.以字符串形式发送数字_((任务ID数字));
	串口通信.发送换行符();
	延时器.延时_毫秒((200s));
}

int32 入队高( int32 编号 )
{
	if( 高队列长度 >= 高队列最大长度 ) { 溢出报警(); return 0s; }
	高队列[高尾] = 编号; 高尾 = (高尾 + 1s) % 10s; 高队列长度 = 高队列长度 + 1s; return 1s;
}
int32 入队中( int32 编号 )
{
	if( 中队列长度 >= 中队列最大长度 ) { 溢出报警(); return 0s; }
	中队列[中尾] = 编号; 中尾 = (中尾 + 1s) % 15s; 中队列长度 = 中队列长度 + 1s; return 1s;
}
int32 入队低( int32 编号 )
{
	if( 低队列长度 >= 低队列最大长度 ) { 溢出报警(); return 0s; }
	低队列[低尾] = 编号; 低尾 = (低尾 + 1s) % 20s; 低队列长度 = 低队列长度 + 1s; return 1s;
}

int32 出队高(){ if( 高队列长度 <= 0s ) { return 0s; } 临时任务 = 高队列[高头]; 高头 = (高头 + 1s) % 10s; 高队列长度 = 高队列长度 - 1s; return 临时任务; }
int32 出队中(){ if( 中队列长度 <= 0s ) { return 0s; } 临时任务 = 中队列[中头]; 中头 = (中头 + 1s) % 15s; 中队列长度 = 中队列长度 - 1s; return 临时任务; }
int32 出队低(){ if( 低队列长度 <= 0s ) { return 0s; } 临时任务 = 低队列[低头]; 低头 = (低头 + 1s) % 20s; 低队列长度 = 低队列长度 - 1s; return 临时任务; }

void 创建任务( int32 类型 )
{
	任务ID数字 = 任务ID数字 + 1s;
	if( 任务ID数字 > 45s ) { 任务ID数字 = 1s; }
	任务类型表[任务ID数字] = 类型;
	任务优先级表[任务ID数字] = 类型;
	预计执行时长表[任务ID数字] = 取随机数(2000s,6000s);
	到达时刻表[任务ID数字] = 当前时间;
	if( 类型 == 1s ) { 入队结果 = 入队高(任务ID数字); }
	else if( 类型 == 2s ) { 入队结果 = 入队中(任务ID数字); }
	else { 入队结果 = 入队低(任务ID数字); }
	if( 入队结果 == 1s ) {
		串口通信.发送字符串_(("任务到达: ID="));
		串口通信.以字符串形式发送数字_((任务ID数字));
		串口通信.发送字符串_((", 类型="));
		串口通信.以字符串形式发送数字_((类型));
		串口通信.发送换行符();
		更新显示();
	}
}

void 任务到达生成()
{
	if( 系统状态 != 0s ) { return; }
	if( (当前时间 - 上次到达高) >= 下次间隔高 ) { 创建任务(1s); 上次到达高 = 当前时间; 下次间隔高 = 取随机数(8000s,15000s); }
	if( (当前时间 - 上次到达中) >= 下次间隔中 ) { 创建任务(2s); 上次到达中 = 当前时间; 下次间隔中 = 取随机数(3000s,8000s); }
	if( (当前时间 - 上次到达低) >= 下次间隔低 ) { 创建任务(3s); 上次到达低 = 当前时间; 下次间隔低 = 取随机数(10000s,20000s); }
}

int32 选择任务_严格优先级()
{
	if( 高队列长度 > 0s ) { return 出队高(); }
	if( 中队列长度 > 0s ) { return 出队中(); }
	if( 低队列长度 > 0s ) { return 出队低(); }
	return 0s;
}

int32 选择任务_加权轮询()
{
	轮询计数器 = (轮询计数器 + 1s) % 6s;
	if( 轮询计数器 < 3s && 高队列长度 > 0s ) { return 出队高(); }
	if( 轮询计数器 < 5s && 中队列长度 > 0s ) { return 出队中(); }
	if( 低队列长度 > 0s ) { return 出队低(); }
	if( 高队列长度 > 0s ) { return 出队高(); }
	if( 中队列长度 > 0s ) { return 出队中(); }
	if( 低队列长度 > 0s ) { return 出队低(); }
	return 0s;
}

void 启动任务( int32 编号 )
{
	当前任务ID = 编号; 当前任务类型 = 任务类型表[编号];
	当前任务执行时长 = 预计执行时长表[编号]; 当前任务开始时间 = 当前时间;
	当前任务剩余时间 = 当前任务执行时长;
	开始执行时刻表[编号] = 当前时间; 当前任务完成时刻 = 当前时间 + 当前任务执行时长;
	if( 当前任务类型 == 1s ) { 舵机.设置角度为_((180s)); 设置灯带颜色(255s,0s,0s); }
	else if( 当前任务类型 == 2s ) { 舵机.设置角度为_((90s)); 设置灯带颜色(255s,180s,0s); }
	else { 舵机.设置角度为_((0s)); 设置灯带颜色(0s,255s,0s); }
	串口通信.发送字符串_(("执行任务 ID:"));
	串口通信.以字符串形式发送数字_((当前任务ID));
	串口通信.发送换行符();
	更新显示();
}

void 完成当前任务()
{
	完成时刻表[当前任务ID] = 当前时间; 吞吐量 = 吞吐量 + 1s;
	等待时间 = 开始执行时刻表[当前任务ID] - 到达时刻表[当前任务ID];
	周转时间 = 完成时刻表[当前任务ID] - 到达时刻表[当前任务ID];
	历史记录数 = 历史记录数 + 1s;
	if( 历史记录数 > 45s ) { 历史记录数 = 1s; }
	历史任务ID表[历史记录数] = 当前任务ID;
	历史等待时间表[历史记录数] = 等待时间;
	历史周转时间表[历史记录数] = 周转时间;
	if( 当前任务类型 == 1s ) { 完成高 = 完成高 + 1s; 总等待高 = 总等待高 + 等待时间; }
	else if( 当前任务类型 == 2s ) { 完成中 = 完成中 + 1s; 总等待中 = 总等待中 + 等待时间; }
	else { 完成低 = 完成低 + 1s; 总等待低 = 总等待低 + 等待时间; }
	串口通信.发送字符串_(("任务完成: ID="));
	串口通信.以字符串形式发送数字_((当前任务ID));
	串口通信.发送字符串_((", 等待时间="));
	串口通信.以字符串形式发送数字_((等待时间));
	串口通信.发送字符串_((" ms, 周转时间="));
	串口通信.以字符串形式发送数字_((周转时间));
	串口通信.发送字符串_((" ms"));
	串口通信.发送换行符();
	舵机.设置角度为_((90s)); 当前任务ID = -1s; 当前任务类型 = 0s; 当前任务剩余时间 = 0s; 设置灯带颜色(0s,255s,0s);
}

void 调度任务()
{
	if( 当前任务ID > 0s ) {
		当前任务剩余时间 = 当前任务完成时刻 - 当前时间;
		if( 当前时间 >= 当前任务完成时刻 ) { 完成当前任务(); }
		return;
	}
	if( 系统状态 != 0s ) { return; }
	if( 暂停取新任务 == 1s ) { return; }
	if( 调度模式 == 0s ) { 临时任务 = 选择任务_严格优先级(); } else { 临时任务 = 选择任务_加权轮询(); }
	if( 临时任务 > 0s ) { 启动任务(临时任务); }
}

void 计算显示指标()
{
	队首任务ID = -1s;
	if( 高队列长度 > 0s ) { 队首任务ID = 高队列[高头]; }
	else if( 中队列长度 > 0s ) { 队首任务ID = 中队列[中头]; }
	else if( 低队列长度 > 0s ) { 队首任务ID = 低队列[低头]; }
	if( 吞吐量 > 0s ) { 平均等待时间 = (总等待高 + 总等待中 + 总等待低) / 吞吐量; }
	else { 平均等待时间 = 0s; }
}

void 更新显示()
{
	计算显示指标();
	信息显示器.清空();
	信息显示器.在第_行第_列显示信息_((1s),(1s),("ID:"));
	信息显示器.在第_行第_列向后显示数字_((1s),(4s),(当前任务ID));
	信息显示器.在第_行第_列显示信息_((1s),(10s),("T:"));
	信息显示器.在第_行第_列向后显示数字_((1s),(12s),(当前时间));
	信息显示器.在第_行第_列显示信息_((2s),(1s),("H/M/L:"));
	信息显示器.在第_行第_列向后显示数字_((2s),(8s),(高队列长度));
	信息显示器.在第_行第_列向后显示数字_((2s),(11s),(中队列长度));
	信息显示器.在第_行第_列向后显示数字_((2s),(14s),(低队列长度));
	信息显示器.在第_行第_列显示信息_((2s),(17s),("R:"));
	信息显示器.在第_行第_列向后显示数字_((2s),(19s),(当前任务剩余时间));
	信息显示器.在第_行第_列显示信息_((3s),(1s),("DONE:"));
	信息显示器.在第_行第_列向后显示数字_((3s),(7s),(吞吐量));
	信息显示器.在第_行第_列显示信息_((3s),(11s),("DROP:"));
	信息显示器.在第_行第_列向后显示数字_((3s),(17s),(丢弃数));
	if( 显示模式 == 0s ) {
		信息显示器.在第_行第_列显示信息_((4s),(1s),("WRR 3:2:1"));
		信息显示器.在第_行第_列显示信息_((4s),(11s),("M:"));
		信息显示器.在第_行第_列向后显示数字_((4s),(13s),(调度模式));
		信息显示器.在第_行第_列显示信息_((4s),(15s),("S:"));
		信息显示器.在第_行第_列向后显示数字_((4s),(17s),(系统状态));
	} else {
		信息显示器.在第_行第_列显示信息_((4s),(1s),("Head:"));
		信息显示器.在第_行第_列向后显示数字_((4s),(7s),(队首任务ID));
	}
	上次显示刷新时间 = 当前时间;
}

void 发送性能报告()
{
	计算显示指标();
	串口通信.发送字符串_(("STAT H=")); 串口通信.以字符串形式发送数字_((高队列长度));
	串口通信.发送字符串_((" M=")); 串口通信.以字符串形式发送数字_((中队列长度));
	串口通信.发送字符串_((" L=")); 串口通信.以字符串形式发送数字_((低队列长度));
	串口通信.发送字符串_((" DONE=")); 串口通信.以字符串形式发送数字_((吞吐量));
	串口通信.发送字符串_((" DROP=")); 串口通信.以字符串形式发送数字_((丢弃数));
	串口通信.发送字符串_((" AVG=")); 串口通信.以字符串形式发送数字_((平均等待时间));
	串口通信.发送字符串_((" MODE=")); 串口通信.以字符串形式发送数字_((调度模式));
	串口通信.发送换行符();
}

void 发送JSON统计摘要()
{
	计算显示指标();
	串口通信.发送字符串_(("{\"done\":"));
	串口通信.以字符串形式发送数字_((吞吐量));
	串口通信.发送字符串_((",\"drop\":"));
	串口通信.以字符串形式发送数字_((丢弃数));
	串口通信.发送字符串_((",\"avgWait\":"));
	串口通信.以字符串形式发送数字_((平均等待时间));
	串口通信.发送字符串_((",\"mode\":"));
	串口通信.以字符串形式发送数字_((调度模式));
	串口通信.发送字符串_(("}"));
	串口通信.发送换行符();
}

void 清空统计记录()
{
	吞吐量 = 0s; 丢弃数 = 0s; 总等待高 = 0s; 总等待中 = 0s; 总等待低 = 0s;
	完成高 = 0s; 完成中 = 0s; 完成低 = 0s; 历史记录数 = 0s; 平均等待时间 = 0s;
	串口通信.发送字符串_(("CLEAR STATS"));
	串口通信.发送换行符();
}

void 发送队列长度到串口()
{
	串口通信.发送字符串_(("GETQ H=")); 串口通信.以字符串形式发送数字_((高队列长度));
	串口通信.发送字符串_((" M=")); 串口通信.以字符串形式发送数字_((中队列长度));
	串口通信.发送字符串_((" L=")); 串口通信.以字符串形式发送数字_((低队列长度));
	串口通信.发送换行符();
}

void 处理串口命令()
{
	串口命令 = 串口通信.获取一个数据();
	if( 串口解析模式 == 1s ) {
		if( 串口命令 == ('0') ) { 调度模式 = 0s; 串口通信.发送字符串_(("MODE 0")); 串口通信.发送换行符(); }
		if( 串口命令 == ('1') ) { 调度模式 = 1s; 串口通信.发送字符串_(("MODE 1")); 串口通信.发送换行符(); }
		串口解析模式 = 0s;
		return;
	}
	if( 串口解析模式 == 2s ) {
		if( 串口命令 == ('1') ) { 创建任务(1s); 串口通信.发送字符串_(("ADD 1")); 串口通信.发送换行符(); }
		if( 串口命令 == ('2') ) { 创建任务(2s); 串口通信.发送字符串_(("ADD 2")); 串口通信.发送换行符(); }
		if( 串口命令 == ('3') ) { 创建任务(3s); 串口通信.发送字符串_(("ADD 3")); 串口通信.发送换行符(); }
		串口解析模式 = 0s;
		return;
	}
	if( 串口命令 == ('S') ) { 串口通信.发送字符串_(("STAT JSON")); 串口通信.发送换行符(); 发送JSON统计摘要(); }
	if( 串口命令 == ('C') ) { 清空所有队列(); 清空统计记录(); 串口通信.发送字符串_(("CLEAR OK")); 串口通信.发送换行符(); }
	if( 串口命令 == ('M') ) { 串口解析模式 = 1s; 串口通信.发送字符串_(("MODE 0/1")); 串口通信.发送换行符(); }
	if( 串口命令 == ('A') ) { 串口解析模式 = 2s; 串口通信.发送字符串_(("ADD 1/2/3")); 串口通信.发送换行符(); }
	if( 串口命令 == ('0') ) { 调度模式 = 0s; 串口通信.发送字符串_(("MODE 0")); 串口通信.发送换行符(); }
	if( 串口命令 == ('1') ) { 创建任务(1s); 串口通信.发送字符串_(("ADD 1")); 串口通信.发送换行符(); }
	if( 串口命令 == ('2') ) { 创建任务(2s); 串口通信.发送字符串_(("ADD 2")); 串口通信.发送换行符(); }
	if( 串口命令 == ('3') ) { 创建任务(3s); 串口通信.发送字符串_(("ADD 3")); 串口通信.发送换行符(); }
	if( 串口命令 == ('G') ) { 发送队列长度到串口(); }
	if( 串口命令 == ('Q') ) { 发送队列长度到串口(); }
}

void 清空所有队列()
{
	高头 = 0s; 高尾 = 0s; 高队列长度 = 0s; 中头 = 0s; 中尾 = 0s; 中队列长度 = 0s; 低头 = 0s; 低尾 = 0s; 低队列长度 = 0s;
	暂停取新任务 = 1s;
	串口通信.发送字符串_(("CLEAR ALL QUEUES")); 串口通信.发送换行符();
}

void 显示队列快照()
{
	计算显示指标();
	队列快照序号 = 队列快照序号 + 1s;
	串口通信.发送字符串_(("SNAPSHOT 队首任务ID="));
	串口通信.以字符串形式发送数字_((队首任务ID));
	串口通信.发送字符串_((" 等待时间="));
	if( 队首任务ID > 0s ) { 串口通信.以字符串形式发送数字_((当前时间 - 到达时刻表[队首任务ID])); }
	else { 串口通信.以字符串形式发送数字_((0s)); }
	串口通信.发送换行符();
	信息显示器.清空();
	信息显示器.在第_行第_列显示信息_((1s),(1s),("队首任务ID"));
	信息显示器.在第_行第_列向后显示数字_((1s),(11s),(队首任务ID));
	信息显示器.在第_行第_列显示信息_((2s),(1s),("等待时间"));
}

void 处理遥控器()
{
	if( 无线遥控器.按键A按下 == 1s && 遥控A上次 == 0s ) { 调度模式 = 1s - 调度模式; 串口通信.发送字符串_(("RF A MODE")); 串口通信.发送换行符(); }
	if( 无线遥控器.按键B按下 == 1s && 遥控B上次 == 0s ) { 系统状态 = 1s; 串口通信.发送字符串_(("RF B PAUSE AFTER CURRENT")); 串口通信.发送换行符(); }
	if( 无线遥控器.按键C按下 == 1s && 遥控C上次 == 0s ) { 系统状态 = 0s; 串口通信.发送字符串_(("RF C RESUME")); 串口通信.发送换行符(); }
	if( 无线遥控器.按键D按下 == 1s && 遥控D上次 == 0s ) { 创建任务(1s); 串口通信.发送字符串_(("RF D ADD URGENT")); 串口通信.发送换行符(); }
	遥控A上次 = 无线遥控器.按键A按下; 遥控B上次 = 无线遥控器.按键B按下; 遥控C上次 = 无线遥控器.按键C按下; 遥控D上次 = 无线遥控器.按键D按下;
}

void 处理四按钮_按钮1(){ 显示队列快照(); }
void 处理四按钮_按钮2(){ 清空所有队列(); }
void 处理四按钮_按钮3(){ 显示模式 = 1s - 显示模式; 更新显示(); }
void 处理四按钮_按钮4(){ 发送性能报告(); }

void 处理矩阵键盘()
{
	// digit + A/B/C 修改队列容量，* 重置默认，# 显示参数。
	if( 矩阵键盘.按键值 != 上次矩阵键值 ) {
		if( 矩阵键盘.按键值 >= 1s && 矩阵键盘.按键值 <= 9s ) { 键盘数字缓存 = 矩阵键盘.按键值; }
		if( 矩阵键盘.按键值 == 10s ) {
			高队列最大长度 = 键盘数字缓存;
			串口通信.发送字符串_(("KEYPAD SET HIGH"));
			串口通信.发送换行符();
		}
		if( 矩阵键盘.按键值 == 11s ) {
			中队列最大长度 = 键盘数字缓存;
			串口通信.发送字符串_(("KEYPAD SET MID"));
			串口通信.发送换行符();
		}
		if( 矩阵键盘.按键值 == 12s ) {
			低队列最大长度 = 键盘数字缓存;
			串口通信.发送字符串_(("KEYPAD SET LOW"));
			串口通信.发送换行符();
		}
		if( 矩阵键盘.按键值 == 13s ) {
			高队列最大长度 = 10s; 中队列最大长度 = 15s; 低队列最大长度 = 20s;
			串口通信.发送字符串_(("KEYPAD RESET PARAM"));
			串口通信.发送换行符();
		}
		if( 矩阵键盘.按键值 == 14s ) {
			串口通信.发送字符串_(("KEYPAD SHOW PARAM"));
			串口通信.发送换行符();
			发送性能报告();
		}
		上次矩阵键值 = 矩阵键盘.按键值;
		更新显示();
	}
}

void 周期报告()
{
	if( (当前时间 - 上次报告时间) >= 60000s ) { 发送性能报告(); 上次报告时间 = 当前时间; }
}

void 主程序无限循环()
{
	当前时间 = 当前时间 + 10s;
	任务到达生成();
	处理遥控器();
	处理矩阵键盘();
	调度任务();
	if( (当前时间 - 上次显示刷新时间) >= 200s ) { 更新显示(); }
	周期报告();
	延时器.延时_毫秒((10s));
}

void 可视化初始化系统(){ OS_VarInit(); 更新显示(); }
void 可视化任务到达生成(){ 任务到达生成(); }
void 可视化严格优先级调度(){ 选择任务_严格优先级(); }
void 可视化加权轮询调度(){ 选择任务_加权轮询(); }
void 可视化执行任务舵机灯带(){ 启动任务(当前任务ID); }
void 可视化完成任务统计(){ 完成当前任务(); }
void 可视化串口命令(){ 处理串口命令(); }
void 可视化无线遥控(){ 处理遥控器(); }
void 可视化四按钮(){ 处理四按钮_按钮1(); }
void 可视化矩阵键盘配置(){ 处理矩阵键盘(); }
void 可视化LCD2004状态显示(){ 更新显示(); }
void 可视化周期报告(){ 发送性能报告(); }
void 控制器_初始化(){ 可视化初始化系统(); }
void 控制器_反复执行(){ 主程序无限循环(); }
void 串口通信_接收缓冲区有数据时(){ 处理串口命令(); }
void 四按钮_按钮1按下时(){ 处理四按钮_按钮1(); }
void 四按钮_按钮2按下时(){ 处理四按钮_按钮2(); }
void 四按钮_按钮3按下时(){ 处理四按钮_按钮3(); }
void 四按钮_按钮4按下时(){ 处理四按钮_按钮4(); }
#param userspaceoff

void OS_VarInit()
{
	系统状态 = 0s; 调度模式 = 0s; 显示模式 = 0s; 当前时间 = 0s; 随机种子 = 1234s;
	任务ID数字 = 0s; 当前任务ID = -1s; 当前任务类型 = 0s; 当前任务完成时刻 = 0s; 当前任务剩余时间 = 0s;
	等待时间 = 0s; 周转时间 = 0s; 历史记录数 = 0s; 队首任务ID = -1s; 平均等待时间 = 0s; 暂停取新任务 = 0s; 串口命令 = 0s; 串口解析模式 = 0s; 上次矩阵键值 = 0s; 入队结果 = 0s;
	高队列最大长度 = 10s; 中队列最大长度 = 15s; 低队列最大长度 = 20s;
	高头 = 0s; 高尾 = 0s; 高队列长度 = 0s; 中头 = 0s; 中尾 = 0s; 中队列长度 = 0s; 低头 = 0s; 低尾 = 0s; 低队列长度 = 0s;
	上次到达高 = 0s; 上次到达中 = 0s; 上次到达低 = 0s;
	下次间隔高 = 取随机数(8000s,15000s); 下次间隔中 = 取随机数(3000s,8000s); 下次间隔低 = 取随机数(10000s,20000s);
	轮询计数器 = 0s; 吞吐量 = 0s; 丢弃数 = 0s; 总等待高 = 0s; 总等待中 = 0s; 总等待低 = 0s; 完成高 = 0s; 完成中 = 0s; 完成低 = 0s;
	上次显示刷新时间 = -500s; 上次报告时间 = 0s; 键盘数字缓存 = 0s; 队列快照序号 = 0s;
	舵机.设置角度为_((90s)); 设置灯带颜色(0s,0s,80s);
}
"""


def block(kind: str, block_id: int, parameter: str, x: int, y: int) -> str:
    extra = "//[展开] True,\n" if kind in {"UserFunctionIns", "EventIns", "ForeverIns"} else ""
    parameter_line = f"//[参数] {parameter},\n" if parameter else ""
    return f"""//[{kind}],
//[名称] @{block_id},
//[禁用] False,
{parameter_line}//[坐标] X = {x},
//[坐标] Y = {y},
//[角度] 0,
{extra}//[/{kind}],
"""


def component_text(component: Component) -> str:
    events = "".join(f"//[事件] {event},\n" for event in component.events)
    params = "".join(f"//[参数] {param},\n" for param in component.params)
    interfaces = "".join(f"//[接口] {interface},\n" for interface in component.interfaces)
    return f"""//[组件],
//[组件路径] ModuleLib {component.path},
//[名称] {component.name},
//[语言] chinese,
{events}{params}{interfaces}//[坐标] X = {component.x},
//[坐标] Y = {component.y},
//[角度] 0,
//[翻转] False,
//[仿真] 0,0,0,False,180,90,
//[仿真M] False,5,50,50,
//[键值] {component.keys},
//[组件结束],
"""


def variable_text(name: str, x: int, y: int) -> str:
    return f"""//[变量],
//[名称] {name},
//[常量] False,
//[类型] int32,
//[存储] ,
//[参数],
//[参数结束],
//[坐标] X = {x},
//[坐标] Y = {y},
//[尺寸] Width = 112,
//[尺寸] Height = 28,
//[变量结束],
"""


VISUAL_FUNCS: Final[tuple[tuple[str, tuple[str, ...]], ...]] = (
    ("可视化初始化系统", ("?void @OPER ( *int32 @VAR 高队列最大长度 ) = ( ?int32 @WORD 10 )", "?void @OPER ( *int32 @VAR 中队列最大长度 ) = ( ?int32 @WORD 15 )", "?void @OPER ( *int32 @VAR 低队列最大长度 ) = ( ?int32 @WORD 20 )", "?void @MFUNC 液晶屏 打开背光", "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 1 ) 行第 ( ?int32 @WORD 1 ) 列显示信息 ( ?Cstring @WORD \"系统就绪\" )", "?void @OPER ( *int32 @MVAR 舵机 角度 ) = ( ?int32 @WORD 90 )")),
    ("可视化任务到达生成", ("?void @OPER ( *int32 @VAR 任务ID数字 ) = ( ?int32 @OPER ( ?int32 @VAR 任务ID数字 ) + ( ?int32 @WORD 1 ) )", "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"到达扫描\" )")),
    ("可视化高优先级入队", ("?void @OPER ( *int32 @VAR 高队列长度 ) = ( ?int32 @OPER ( ?int32 @VAR 高队列长度 ) + ( ?int32 @WORD 1 ) )", "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"紧急订单入队\" )")),
    ("可视化中优先级入队", ("?void @OPER ( *int32 @VAR 中队列长度 ) = ( ?int32 @OPER ( ?int32 @VAR 中队列长度 ) + ( ?int32 @WORD 1 ) )", "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"普通补货入队\" )")),
    ("可视化低优先级入队", ("?void @OPER ( *int32 @VAR 低队列长度 ) = ( ?int32 @OPER ( ?int32 @VAR 低队列长度 ) + ( ?int32 @WORD 1 ) )", "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"低优先级巡检入队\" )")),
    ("可视化严格优先级调度", ("?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"严格优先级\" )", "?void @OPER ( *int32 @VAR 调度模式 ) = ( ?int32 @WORD 0 )")),
    ("可视化加权轮询调度", ("?void @OPER ( *int32 @VAR 轮询计数器 ) = ( ?int32 @WORD 0 )", "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"WRR 3:2:1\" )")),
    ("可视化执行任务舵机灯带", ("?void @OPER ( *int32 @MVAR 舵机 角度 ) = ( ?int32 @WORD 180 )", "?void @OPER ( *int32 @MVAR 舵机 角度 ) = ( ?int32 @WORD 90 )", "?void @OPER ( *int32 @MVAR 舵机 角度 ) = ( ?int32 @WORD 0 )", "?void @MFUNC 灯带 设置第 ( ?int32 @WORD 1 ) 个灯红色分量为 ( ?int32 @WORD 255 )", "?void @MFUNC 灯带 设置第 ( ?int32 @WORD 1 ) 个灯绿色分量为 ( ?int32 @WORD 255 )")),
    ("可视化完成任务统计", ("?void @OPER ( *int32 @VAR 吞吐量 ) = ( ?int32 @OPER ( ?int32 @VAR 吞吐量 ) + ( ?int32 @WORD 1 ) )", "?void @OPER ( *int32 @MVAR 舵机 角度 ) = ( ?int32 @WORD 90 )")),
    (
        "可视化串口命令",
        (
            "?void @OPER ( *int32 @VAR 串口命令 ) = ( ?int32 @MFUNC 串口通信 获取一个数据 )",
            "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"STAT JSON\" )",
            "?void @MFUNC 串口通信 发送换行符",
            "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"GETQ H=\" )",
            "?void @MFUNC 串口通信 以字符串形式发送数字 ( ?int32 @VAR 高队列长度 )",
            "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \" M=\" )",
            "?void @MFUNC 串口通信 以字符串形式发送数字 ( ?int32 @VAR 中队列长度 )",
            "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \" L=\" )",
            "?void @MFUNC 串口通信 以字符串形式发送数字 ( ?int32 @VAR 低队列长度 )",
            "?void @MFUNC 串口通信 发送换行符",
            "?void @OPER ( *int32 @VAR 调度模式 ) = ( ?int32 @WORD 0 )",
            "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"MODE 0\" )",
            "?void @OPER ( *int32 @VAR 调度模式 ) = ( ?int32 @WORD 1 )",
            "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"MODE 1\" )",
            "?void @OPER ( *int32 @VAR 高队列长度 ) = ( ?int32 @OPER ( ?int32 @VAR 高队列长度 ) + ( ?int32 @WORD 1 ) )",
            "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"ADD 1\" )",
            "?void @OPER ( *int32 @VAR 中队列长度 ) = ( ?int32 @OPER ( ?int32 @VAR 中队列长度 ) + ( ?int32 @WORD 1 ) )",
            "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"ADD 2\" )",
            "?void @OPER ( *int32 @VAR 低队列长度 ) = ( ?int32 @OPER ( ?int32 @VAR 低队列长度 ) + ( ?int32 @WORD 1 ) )",
            "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"ADD 3\" )",
            "?void @OPER ( *int32 @VAR 高队列长度 ) = ( ?int32 @WORD 0 )",
            "?void @OPER ( *int32 @VAR 中队列长度 ) = ( ?int32 @WORD 0 )",
            "?void @OPER ( *int32 @VAR 低队列长度 ) = ( ?int32 @WORD 0 )",
            "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"CLEAR OK\" )",
            "?void @MFUNC 串口通信 发送换行符",
        ),
    ),
    ("可视化无线遥控", ("?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"A模式 B暂停 C恢复 D紧急\" )", "?void @MFUNC 串口通信 发送换行符")),
    ("可视化四按钮", ("?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"1快照 2清空 3切屏 4报告\" )", "?void @MFUNC 串口通信 发送换行符")),
    ("可视化矩阵键盘配置", ("?void @OPER ( *int32 @VAR 高队列最大长度 ) = ( ?int32 @WORD 10 )", "?void @OPER ( *int32 @VAR 中队列最大长度 ) = ( ?int32 @WORD 15 )", "?void @OPER ( *int32 @VAR 低队列最大长度 ) = ( ?int32 @WORD 20 )", "?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"KEYPAD RESET PARAM\" )")),
    (
        "可视化LCD2004状态显示",
        (
            "?void @MFUNC 信息显示器 清空",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 1 ) 行第 ( ?int32 @WORD 1 ) 列显示信息 ( ?Cstring @WORD \"ID:\" )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 1 ) 行第 ( ?int32 @WORD 4 ) 列向后显示数字 ( ?int32 @VAR 当前任务ID )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 1 ) 行第 ( ?int32 @WORD 10 ) 列显示信息 ( ?Cstring @WORD \"T:\" )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 1 ) 行第 ( ?int32 @WORD 12 ) 列向后显示数字 ( ?int32 @VAR 当前时间 )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 2 ) 行第 ( ?int32 @WORD 1 ) 列显示信息 ( ?Cstring @WORD \"Q:\" )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 2 ) 行第 ( ?int32 @WORD 4 ) 列向后显示数字 ( ?int32 @VAR 高队列长度 )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 2 ) 行第 ( ?int32 @WORD 8 ) 列向后显示数字 ( ?int32 @VAR 中队列长度 )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 2 ) 行第 ( ?int32 @WORD 12 ) 列向后显示数字 ( ?int32 @VAR 低队列长度 )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 2 ) 行第 ( ?int32 @WORD 15 ) 列显示信息 ( ?Cstring @WORD \"R:\" )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 2 ) 行第 ( ?int32 @WORD 17 ) 列向后显示数字 ( ?int32 @VAR 当前任务剩余时间 )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 3 ) 行第 ( ?int32 @WORD 1 ) 列显示信息 ( ?Cstring @WORD \"Done:\" )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 3 ) 行第 ( ?int32 @WORD 7 ) 列向后显示数字 ( ?int32 @VAR 吞吐量 )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 3 ) 行第 ( ?int32 @WORD 11 ) 列显示信息 ( ?Cstring @WORD \"Drop:\" )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 3 ) 行第 ( ?int32 @WORD 17 ) 列向后显示数字 ( ?int32 @VAR 丢弃数 )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 4 ) 行第 ( ?int32 @WORD 1 ) 列显示信息 ( ?Cstring @WORD \"WRR 3:2:1\" )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 4 ) 行第 ( ?int32 @WORD 11 ) 列显示信息 ( ?Cstring @WORD \"M:\" )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 4 ) 行第 ( ?int32 @WORD 13 ) 列向后显示数字 ( ?int32 @VAR 调度模式 )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 4 ) 行第 ( ?int32 @WORD 15 ) 列显示信息 ( ?Cstring @WORD \"S:\" )",
            "?void @MFUNC 信息显示器 在第 ( ?int32 @WORD 4 ) 行第 ( ?int32 @WORD 17 ) 列向后显示数字 ( ?int32 @VAR 系统状态 )",
        ),
    ),
    ("可视化周期报告", ("?void @MFUNC 串口通信 发送字符串 ( ?Cstring @WORD \"PERF 60000ms\" )", "?void @MFUNC 串口通信 发送换行符")),
)


def visual_blocks() -> tuple[str, str]:
    blocks: list[str] = []
    links: list[str] = []
    next_id = 100
    x = -710
    y = 520
    for index, (name, steps) in enumerate(VISUAL_FUNCS):
        func_id = 39 + index * 2
        end_id = func_id + 1
        blocks.append(block("UserFunctionIns", func_id, f"?void {name}", x + (index % 3) * 430, y + (index // 3) * 230))
        previous = func_id
        cursor_y = y + (index // 3) * 230 + 48
        for step in steps:
            if "如果" in name or "调度" in name:
                pass
            current = next_id
            next_id += 1
            blocks.append(block("FuncIns", current, step, x + (index % 3) * 430 + 35, cursor_y))
            links.append(f"//[指令链接] @{previous} NextIns -> @{current},")
            links.append(f"//[指令链接] @{current} PreIns -> @{previous},")
            previous = current
            cursor_y += 30
        blocks.append(block("CondiEndIns", end_id, "", x + (index % 3) * 430, cursor_y + 5))
        links.append(f"//[UserFunction结构链接] @{func_id} CondiEnd -> @{end_id},")
        links.append(f"//[指令链接] @{previous} NextIns -> @{end_id},")
        links.append(f"//[指令链接] @{end_id} PreIns -> @{previous},")
    blocks.extend(
        (
            block("EventIns", 80, "控制器_反复执行", -250, 230),
            block("CondiEndIns", 81, "", -250, 615),
            block("ForeverIns", 82, "", -225, 260),
            block("CondiEndIns", 83, "", -225, 585),
            block("FuncIns", 84, "?void @USER 可视化任务到达生成", -200, 292),
            block("IfElseIns", 85, "?bool @OPER ( ?int32 @VAR 调度模式 ) == ( ?int32 @WORD 0 )", -200, 324),
            block("FuncIns", 86, "?void @USER 可视化严格优先级调度", -175, 356),
            block("ElseIns", 87, "", -200, 388),
            block("FuncIns", 88, "?void @USER 可视化加权轮询调度", -175, 420),
            block("CondiEndIns", 89, "", -200, 452),
            block("LoopIns", 90, "?int32 @WORD 1", -200, 484),
            block("FuncIns", 91, "?void @USER 可视化LCD2004状态显示", -175, 516),
            block("FuncIns", 92, "?void @USER 可视化周期报告", -175, 548),
            block("CondiEndIns", 93, "", -200, 580),
        )
    )
    links.extend(
        (
            "//[指令链接] @80 NextIns -> @82,",
            "//[Event结构链接] @80 CondiEnd -> @81,",
            "//[指令链接] @81 PreIns -> @83,",
            "//[指令链接] @82 PreIns -> @80,",
            "//[指令链接] @82 NextIns -> @84,",
            "//[Forever结构链接] @82 CondiEnd -> @83,",
            "//[指令链接] @83 PreIns -> @93,",
            "//[指令链接] @83 NextIns -> @81,",
            "//[指令链接] @84 PreIns -> @82,",
            "//[指令链接] @84 NextIns -> @85,",
            "//[指令链接] @85 PreIns -> @84,",
            "//[指令链接] @85 NextIns -> @86,",
            "//[IfElse结构链接] @85 ElseIns -> @87,",
            "//[指令链接] @86 PreIns -> @85,",
            "//[指令链接] @86 NextIns -> @87,",
            "//[指令链接] @87 PreIns -> @86,",
            "//[指令链接] @87 NextIns -> @88,",
            "//[Else结构链接] @87 CondiEnd -> @89,",
            "//[指令链接] @88 PreIns -> @87,",
            "//[指令链接] @88 NextIns -> @89,",
            "//[指令链接] @89 PreIns -> @88,",
            "//[指令链接] @89 NextIns -> @90,",
            "//[指令链接] @90 PreIns -> @89,",
            "//[指令链接] @90 NextIns -> @91,",
            "//[Loop结构链接] @90 CondiEnd -> @93,",
            "//[指令链接] @91 PreIns -> @90,",
            "//[指令链接] @91 NextIns -> @92,",
            "//[指令链接] @92 PreIns -> @91,",
            "//[指令链接] @92 NextIns -> @93,",
            "//[指令链接] @93 PreIns -> @92,",
            "//[指令链接] @93 NextIns -> @83,",
        )
    )
    event_base = 200
    events = (
        ("控制器_初始化", "?void @USER 可视化初始化系统"),
        ("串口通信_接收缓冲区有数据时", "?void @USER 可视化串口命令"),
        ("四按钮_按钮1按下时", "?void @USER 可视化四按钮"),
        ("四按钮_按钮2按下时", "?void @USER 可视化四按钮"),
        ("四按钮_按钮3按下时", "?void @USER 可视化四按钮"),
        ("四按钮_按钮4按下时", "?void @USER 可视化周期报告"),
    )
    for offset, (name, call) in enumerate(events):
        event_id = event_base + offset * 3
        blocks.append(block("EventIns", event_id, name, 700, 520 + offset * 105))
        blocks.append(block("FuncIns", event_id + 1, call, 730, 558 + offset * 105))
        blocks.append(block("CondiEndIns", event_id + 2, "", 700, 595 + offset * 105))
        links.append(f"//[指令链接] @{event_id} NextIns -> @{event_id + 1},")
        links.append(f"//[指令链接] @{event_id + 1} PreIns -> @{event_id},")
        links.append(f"//[指令链接] @{event_id + 1} NextIns -> @{event_id + 2},")
        links.append(f"//[指令链接] @{event_id + 2} PreIns -> @{event_id + 1},")
        links.append(f"//[Event结构链接] @{event_id} CondiEnd -> @{event_id + 2},")
    return "".join(blocks), "\n".join(links) + "\n"


def config_text() -> str:
    parts = [
        "//-----------------------------------------------\n//[配置信息开始],\n//[工作台],\n//[语言] chinese,\n//[模块放缩] 1,\n//[软件加速] 0,\n//[VEX驱动周期] 10,\n//[动态内存] 30,\n//[RAM节约] 0,\n//[隐藏导线] 0,\n//[隐藏名称] False,\n//[连线拟合] 50,\n//[事件池] 16,\n//[EventVarStack] 300,\n//[EventFuncStack] 80,\n//[界面类型] 1,\n//[版本号] 5.56.250511,\n//[工作台结束],\n//[地图],\n//[背景图属性] 0 0 0 0,\n//[放大] 1,\n//[颜色] 245 245 245,\n//[CamMidX] 0,\n//[CamMidY] 0,\n//[CamAngle] 0,\n//[CamScale] 0,\n//[宽度] 0,\n//[高度] 0,\n//[地图结束],\n",
        "".join(component_text(component) for component in COMPONENTS),
        "".join(
            variable_text(name, 30 + (index % 3) * 135, -520 + (index // 3) * 42)
            for index, name in enumerate(
                (
                    "系统状态",
                    "调度模式",
                    "当前时间",
                    "任务ID数字",
                    "当前任务ID",
                    "当前任务剩余时间",
                    "高队列长度",
                    "中队列长度",
                    "低队列长度",
                    "高队列最大长度",
                    "中队列最大长度",
                    "低队列最大长度",
                    "轮询计数器",
                    "吞吐量",
                    "丢弃数",
                    "平均等待时间",
                    "串口命令",
                    "显示模式",
                )
            )
        ),
    ]
    blocks, instruction_links = visual_blocks()
    parts.append(blocks)
    parts.extend(f"//[链接] {link},\n" for link in LINKS)
    parts.append(instruction_links)
    parts.append("//[配置信息结束],\n")
    return "".join(parts)


def build_lab_text() -> str:
    return source_code().strip() + "\n\n" + config_text()


def missing_modules() -> list[str]:
    lib_dir = LINKBOY_DIR / "Lib"
    if not lib_dir.exists():
        return []
    return [module for module in MODULES if not (LINKBOY_DIR / "Lib" / module).exists()]


def write_gbk(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.strip().replace("\n", "\r\n").encode("gbk"))


def write_utf8(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")
