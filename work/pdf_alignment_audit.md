# PDF 逐项对齐审查报告

- PDF 文本：`D:\linkboy\work\pdf_extract.txt`
- LinkBoy 工程：`D:\linkboy\work\port_sort.lab`
- 桌面副本：`C:\Users\cyc20\Desktop\port_sort.lab`
- 桌面副本一致性：通过
- PDF 标题命中：通过

## 汇总

- 通过: 32
- 等价通过: 1
- 冲突取舍: 2
- 选做未做: 3

## 逐项审查

| PDF 章节 | 要求 | 结论 | 证据/说明 |
| --- | --- | --- | --- |
| 二/实验目的 | 硬件覆盖：控制器、屏幕、矩阵键盘、无线遥控、点阵、串口、湿度、PPM、灯带、称重、舵机、四按钮均出现在图形化工程 | 通过 | `port_sort.lab:1282` `//[名称] 控制器`<br>`port_sort.lab:1311` `//[名称] 液晶屏`<br>`port_sort.lab:1337` `//[名称] 矩阵键盘`<br>`port_sort.lab:1362` `//[名称] 无线遥控器`<br>`port_sort.lab:1408` `//[名称] 点阵屏`<br>另 7 项关键词已检查 |
| 二/实验目的 | 数据结构覆盖：数组、队列、随机数用于任务调度 | 通过 | `port_sort.lab:201` `历史时间[10]`<br>`port_sort.lab:202` `历史重量[10]`<br>`port_sort.lab:207` `队列编号[20]`<br>`port_sort.lab:215` `队列长度`<br>`port_sort.lab:247` `取随机数(` |
| 三/3.1.1 | 环境监测：湿度采集、80% 阈值、红色报警/绿色正常、点阵图标、串口报警/解除 | 通过 | `port_sort.lab:801` `湿度传感器.湿度()`<br>`port_sort.lab:805` `当前湿度 > 80s`<br>`port_sort.lab:807` `ALARM HUMIDITY HIGH`<br>`port_sort.lab:818` `ALARM CLEAR`<br>`port_sort.lab:570` `设置灯带颜色(255s, 0s, 0s)`<br>另 3 项关键词已检查 |
| 三/3.1.2 | 货物称重与三档分拣：0-5000g 限制、轻/中/重阈值、舵机 0/90/180、历史保存、串口发送 | 通过 | `port_sort.lab:258` `称重传感器.数值()`<br>`port_sort.lab:262` `临时重量 > 5000s`<br>`port_sort.lab:857` `临时重量 < 轻货阈值`<br>`port_sort.lab:860` `临时重量 <= 重货阈值`<br>`port_sort.lab:859` `角度 = 0s`<br>另 4 项关键词已检查 |
| 三/3.1.3 | 无线遥控：A 启动、B 暂停、C 复位、D 灯带测试，按 6.1 具体主流程落地 | 冲突取舍 | `port_sort.lab:949` `无线遥控器.按键A按下`<br>`port_sort.lab:538` `启动系统()`<br>`port_sort.lab:957` `无线遥控器.按键B按下`<br>`port_sort.lab:547` `暂停系统()`<br>`port_sort.lab:965` `无线遥控器.按键C按下`<br>另 3 项关键词已检查<br>PDF 3.1 同时写到无线紧急停止；PDF 6.1 的 A/B/C/D 具体映射写 B=暂停。本工程按更具体的 6.1 执行，紧急停止保留在串口 E 与矩阵键盘 10。 |
| 三/3.1.3 | PPM 手动控制舵机：手动模式下读取 1000-2000us 并映射到 0-180 度 | 通过 | `port_sort.lab:981` `PPM遥控器.读取第_通道数据((1s))`<br>`port_sort.lab:982` `手动模式 == 1s`<br>`port_sort.lab:984` `临时PPM宽度 < 1000s`<br>`port_sort.lab:987` `临时PPM宽度 > 2000s`<br>`port_sort.lab:990` `(临时PPM宽度 - 1000s) * 180s / 1000s` |
| 三/3.1.4 | 人机交互：屏幕显示湿度、重量、队列长度、状态、阈值 | 通过 | `port_sort.lab:167` `液晶屏.打开背光()`<br>`port_sort.lab:407` `信息显示器.在第_行第_列向后显示数字_((1s),(5s),(当前湿度))`<br>`port_sort.lab:419` `信息显示器.在第_行第_列向后显示数字_((2s),(6s),(最新重量))`<br>`port_sort.lab:409` `信息显示器.在第_行第_列向后显示数字_((1s),(12s),(队列长度))`<br>`port_sort.lab:412` `信息显示器.在第_行第_列显示信息_((1s),(16s),(`<br>另 2 项关键词已检查 |
| 三/3.1.4 | 矩阵键盘修改轻/重阈值并可启动暂停、急停、复位、灯带测试 | 通过 | `port_sort.lab:898` `矩阵键盘.按键值 == 1s`<br>`port_sort.lab:903` `矩阵键盘.按键值 == 2s`<br>`port_sort.lab:908` `矩阵键盘.按键值 == 3s`<br>`port_sort.lab:913` `矩阵键盘.按键值 == 4s`<br>`port_sort.lab:934` `矩阵键盘.按键值 == 9s`<br>另 3 项关键词已检查 |
| 三/3.1.4 | 四按钮：手动称重、清空队列、切换点阵图片、发送队列数据 | 通过 | `port_sort.lab:993` `四按钮.按钮1按下`<br>`port_sort.lab:629` `手动称重一次()`<br>`port_sort.lab:996` `四按钮.按钮2按下`<br>`port_sort.lab:597` `清空队列并反馈()`<br>`port_sort.lab:999` `四按钮.按钮3按下`<br>另 3 项关键词已检查 |
| 三/3.1.5 | 串口双向通信：上传传感器/队列/报警信息，接收 GET/THRES/HIST/RESET 等命令 | 通过 | `port_sort.lab:24` `const int32 串口通信_波特率 = 115200`<br>`port_sort.lab:434` `发送状态到串口()`<br>`port_sort.lab:501` `发送队列到串口()`<br>`port_sort.lab:807` `ALARM HUMIDITY HIGH`<br>`port_sort.lab:458` `GET THRES 1000 3000 HIST RESET`<br>另 3 项关键词已检查 |
| 三/3.1.6 | 任务调度与缓冲：20 项队列缓存 ID/重量/时间戳，随机到达和重量 | 通过 | `port_sort.lab:207` `队列编号[20]`<br>`port_sort.lab:208` `队列重量[20]`<br>`port_sort.lab:209` `队列时间[20]`<br>`port_sort.lab:210` `队列时[20]`<br>`port_sort.lab:211` `队列分[20]`<br>另 3 项关键词已检查 |
| 三/3.2 | 湿度数据采集周期为 2 秒 | 通过 | `port_sort.lab:800` `(当前时间 - 上次湿度时间) >= 2000s`<br>`port_sort.lab:827` `上次湿度时间 = 当前时间` |
| 三/3.2 | 舵机分拣动作 0.5 秒 + 归中 0.2 秒，总动作约 0.7 秒，小于 1 秒 | 通过 | `port_sort.lab:583` `延时器.延时_毫秒((500s))`<br>`port_sort.lab:531` `舵机.设置角度为_((90s))`<br>`port_sort.lab:376` `延时器.延时_毫秒((200s))` |
| 三/3.2 | 队列容量 20；溢出策略按 5.2/6.2 丢弃新任务并报警 | 冲突取舍 | `port_sort.lab:280` `队列长度 >= 20s`<br>`port_sort.lab:282` `QUEUE FULL DROP NEW ID=`<br>`port_sort.lab:281` `报警灯橙色闪烁()`<br>`port_sort.lab:287` `return 0s`<br>PDF 3.2 写丢弃最旧任务，但 5.2 与 6.2.2 明确写丢弃新任务；本工程按数据结构和伪代码章节执行。 |
| 三/3.2 | 串口通信波特率 115200bps | 通过 | `port_sort.lab:24` `const int32 串口通信_波特率 = 115200`<br>`port_sort.lab:1300` `//[参数] baud = 115200` |
| 三/3.2 | 系统连续运行无死机时间 >=30 分钟 | 通过 | `D:\linkboy\work\simulation_probe_30min.log` 记录 `MAX_SECONDS=1800`、`TICK=1800`、`EXITING_OK`，运行期未见异常关键词；`EXITING_OK` 之后出现 WinForms BufferedGraphics/WmPaint 退出重绘异常，已按退出阶段噪声单独记录 |
| 三/3.3 | 操作员通过键盘、遥控器、按钮控制；管理员通过串口监控参数 | 通过 | `port_sort.lab:895` `处理遥控与按钮()`<br>`port_sort.lab:176` `处理串口命令()`<br>`port_sort.lab:434` `发送状态到串口()`<br>`port_sort.lab:447` `发送阈值到串口()` |
| 四/硬件设计 | 核心引脚映射：LCD A4/A5、键盘 D2-D9、无线 A 路 D10、点阵 D11-D13、湿度 A0、PPM D19、灯带 D20、称重 A1/D18、舵机 D21、四按钮 D22-D25 | 等价通过 | `port_sort.lab:29` `液晶屏.driver.SDA = 控制器.A4`<br>`port_sort.lab:30` `液晶屏.driver.SCL = 控制器.A5`<br>`port_sort.lab:42` `矩阵键盘.driver.IN1 = 控制器.D2`<br>`port_sort.lab:49` `矩阵键盘.driver.OUT4 = 控制器.D9`<br>`port_sort.lab:54` `无线接收器.driver.OUTA = 控制器.D10`<br>另 7 项关键词已检查<br>PDF 注明 LinkBoy 支持虚拟引脚映射；无线模块实际为四路 OUTA-D，A 路贴 D10，其余三路使用 D26-D28。 |
| 五/5.1 | 历史数组固定 10 项，记录时间、重量、类别，循环覆盖并跟踪写入位置 | 通过 | `port_sort.lab:201` `历史时间[10]`<br>`port_sort.lab:202` `历史重量[10]`<br>`port_sort.lab:203` `历史类别[10]`<br>`port_sort.lab:204` `历史写位置`<br>`port_sort.lab:350` `历史时间[历史写位置] = 时间 / 1000s`<br>另 2 项关键词已检查 |
| 五/5.2 | 任务队列最大 20，包含编号、重量、到达时间，入队/出队/清空/长度均实现 | 通过 | `port_sort.lab:207` `队列编号[20]`<br>`port_sort.lab:208` `队列重量[20]`<br>`port_sort.lab:210` `队列时[20]`<br>`port_sort.lab:296` `队尾索引 = (队尾索引 + 1s) % 20s`<br>`port_sort.lab:310` `队首索引 = (队首索引 + 1s) % 20s`<br>另 2 项关键词已检查 |
| 五/5.3 | 随机数：固定种子、到达间隔 500-3000ms、重量 200-4500g、湿度 60±10 | 通过 | `port_sort.lab:1241` `随机种子 = 20260604s`<br>`port_sort.lab:844` `下次间隔 = 取随机数(500s, 3000s)`<br>`port_sort.lab:260` `取随机数(200s, 4500s)`<br>`port_sort.lab:803` `当前湿度 = 60s + 取随机数(0s, 20s) - 10s` |
| 五/5.4 | 其他变量：系统状态 0/1/2、阈值 1000/3000、灯带红绿蓝橙、点阵正常/报警图标 | 通过 | `port_sort.lab:188` `int32 系统状态`<br>`port_sort.lab:528` `系统状态 = 0s`<br>`port_sort.lab:549` `系统状态 = 1s`<br>`port_sort.lab:810` `系统状态 = 2s`<br>`port_sort.lab:1218` `轻货阈值 = 1000s`<br>另 4 项关键词已检查 |
| 六/6.1 | 启动初始化：硬件、随机种子、清空队列/历史、运行状态、时间戳、首次随机间隔、舵机归中 | 通过 | `port_sort.lab:140` `void main0()`<br>`port_sort.lab:166` `OS_VarInit()`<br>`port_sort.lab:1241` `随机种子 = 20260604s`<br>`port_sort.lab:526` `清空队列();`<br>`port_sort.lab:527` `清空历史();`<br>另 5 项关键词已检查 |
| 六/6.1 | 无限循环：湿度、键盘/无线/PPM/按钮、串口、货物生成、分拣、屏幕、10ms 延时均被调度 | 通过 | `port_sort.lab:171` `forever {`<br>`port_sort.lab:176` `处理串口命令();`<br>`port_sort.lab:181` `主循环任务();`<br>`port_sort.lab:1013` `检测湿度();`<br>`port_sort.lab:1014` `处理遥控与按钮();`<br>另 4 项关键词已检查 |
| 六/6.2.1 | 湿度监测子程序按伪代码实现 | 通过 | `port_sort.lab:798` `void 检测湿度()`<br>`port_sort.lab:800` `(当前时间 - 上次湿度时间) >= 2000s`<br>`port_sort.lab:805` `当前湿度 > 80s`<br>`port_sort.lab:810` `系统状态 = 2s`<br>`port_sort.lab:818` `ALARM CLEAR`<br>另 1 项关键词已检查 |
| 六/6.2.2 | 队列操作伪代码对应入队/出队/失败返回 | 通过 | `port_sort.lab:278` `int32 入队(`<br>`port_sort.lab:280` `if( 队列长度 >= 20s )`<br>`port_sort.lab:287` `return 0s`<br>`port_sort.lab:298` `return 1s`<br>`port_sort.lab:301` `int32 出队()` |
| 六/6.2.3 | 随机货物生成子程序按独立计时器生成编号、重量、时间并刷新下一间隔 | 通过 | `port_sort.lab:833` `void 生成货物()`<br>`port_sort.lab:411` `系统状态 == 0s`<br>`port_sort.lab:632` `货物编号 = 货物编号 + 1s`<br>`port_sort.lab:633` `最新重量 = 读取称重重量()`<br>`port_sort.lab:634` `入队(货物编号, 最新重量, 当前时间)`<br>另 1 项关键词已检查 |
| 六/6.2.4 | 分拣处理子程序按空闲标志、出队、分类、舵机动作、历史、串口完成信息实现 | 通过 | `port_sort.lab:849` `void 处理分拣()`<br>`port_sort.lab:854` `舵机空闲标志 == 1s`<br>`port_sort.lab:855` `出队() == 1s`<br>`port_sort.lab:856` `舵机空闲标志 = 0s`<br>`port_sort.lab:872` `保存历史(临时时间, 临时重量, 类别)`<br>另 3 项关键词已检查 |
| 六/6.2.5 | 串口命令解析覆盖 GET/THRES/HIST/RESET | 通过 | `port_sort.lab:710` `void 处理串口命令()`<br>`port_sort.lab:719` `串口命令 == ('G')`<br>`port_sort.lab:725` `串口命令 == ('T')`<br>`port_sort.lab:733` `串口命令 == ('H')`<br>`port_sort.lab:738` `串口命令 == ('R')`<br>另 3 项关键词已检查 |
| 七/7.1 | 考核 1：图形化界面连接硬件模块 | 通过 | `port_sort.lab:1280` `//[组件]`<br>`port_sort.lab:3423` `//[链接]`<br>`port_sort.lab:1430` `//[名称] 舵机`<br>`port_sort.lab:1442` `//[名称] 四按钮` |
| 七/7.1 | 考核 2：流程图/积木块实现伪代码功能 | 通过 | `port_sort.lab:3097` `//[ForeverIns]`<br>`port_sort.lab:3127` `//[IfElseIns]`<br>`port_sort.lab:1963` `//[LoopIns]`<br>`port_sort.lab:1466` `//[UserFunctionIns]`<br>`port_sort.lab:1475` `//[FuncIns]` |
| 七/7.1 | 考核 3：随机货物流与队列调度 | 通过 | `port_sort.lab:833` `生成货物()`<br>`port_sort.lab:260` `取随机数(200s, 4500s)`<br>`port_sort.lab:215` `队列长度`<br>`port_sort.lab:637` `处理分拣()` |
| 七/7.1 | 考核 4：串口观察数据上传并发送阈值指令 | 通过 | `port_sort.lab:434` `发送状态到串口()`<br>`port_sort.lab:501` `发送队列到串口()`<br>`port_sort.lab:666` `THRES OK`<br>`port_sort.lab:447` `发送阈值到串口()` |
| 七/7.1 | 考核 5：实验报告需要分析数组和队列作用 | 通过 | `D:\linkboy\work\port_sort_experiment_report.md` 已分析数组和队列在缓解物流波动中的作用 |
| 七/7.2 | 选做：Wi-Fi/MQTT 上传云平台 | 选做未做 | PDF 标为选做，本轮未实现。 |
| 七/7.2 | 选做：点阵屏动态显示货物 ID 条形码 | 选做未做 | PDF 标为选做，本轮未实现。 |
| 七/7.2 | 选做：轻/中/重多级队列优先级调度 | 选做未做 | PDF 标为选做，本轮未实现。 |

## 审查口径

- `通过`：当前 `.lab` 中有直接代码/图形元数据证据。
- `等价通过`：LinkBoy 模块形态或 PDF 注释允许虚拟引脚调整，功能等价且证据存在。
- `冲突取舍`：PDF 不同章节互相冲突，已按更具体的数据结构/主流程伪代码实现。
- `未验证`：需要运行时长测或独立文档产物，当前证据不足，不能算完成。
- `选做未做`：PDF 7.2 明确为选做项。
