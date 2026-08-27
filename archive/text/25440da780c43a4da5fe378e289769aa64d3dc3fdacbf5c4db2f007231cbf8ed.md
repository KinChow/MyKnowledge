# ADB

## 下载

* Windows版本：https://dl.google.com/android/repository/platform-tools-latest-windows.zip
* Mac版本：https://dl.google.com/android/repository/platform-tools-latest-darwin.zip
* Linux版本：https://dl.google.com/android/repository/platform-tools-latest-linux.zip





## 安装

1. 解压缩到自定义安装目录
2. 将安装目录添加到环境变量





## 基础用法

### 命令语法

```shell
adb [-d|-e|-s <serial|number>] <command>
```



### 为命令指令目标设备

如果有多个没备/模拟器连接，则需要为命令指定目标设备

| 参数                | 含义                                               |
| ------------------- | -------------------------------------------------- |
| `-d`                | 指定当前唯一通过 USB 连接的 Android 设备为命令目标 |
| `-e`                | 指定当唯一运行的模拟器为命令目标                   |
| `-s <serialNumber>` | 指定相应 serialNumber 号的设备/模拟器为命令目标    |

serialNumber 可以通过 `adb devices` 命令获取，



### 启动/停止 adb server

```shell
adb start-server # 启动，一般无需手动执行此命令，在运行 adb 命令时若发现 adb server 没有启动会自动调起
adb kill-server # 停止
```



### 查看 adb 版本

```shell
adb version
```



### 以 root 权限运行 adbd

```shell
adb root
```

adb 的运行原理是 PC 端的 adb server 与手机端的守护进程 adbd 建立连接，然后 PC 端口 adb client 通过 adb server 转发命令，adbd 接收命令后解析运行。

如果 adbd 以普通权限执行，有些需要 root 权限才能执行的命令无法直接用`adb xxx`执行，这时可以`adb shell` 然后 `su` 后执行命令，也可以让 adbd 以 root 权限执行，这样就能随便执行高权限命令了。



### 指定 adb server 的网络端口

```shell
adb -P <port> start-server
```

默认端口：5037





## 设备连接管理

### 查询已连接设备/模拟器

```shell
adb devices
```

输出格式为 `[serialNumber] [state]`，serialNumber 即我们常说的 SN，state 有如下几种：

- `offline` —— 表示设备未连接成功或无响应。
- `device` —— 设备已连接。注意这个状态并不能标识 Android 系统已经完全启动和可操作，在设备启动过程中设备实例就可连接到 adb，但启动完毕后系统才处于可操作状态。
- `no device` —— 没有设备/模拟器连接。





## 应用管理

### 查看应用列表

```shell
adb shell pm list packages [-f] [-d] [-e] [-s] [-3] [-i] [-u] [--user USER_ID] [FILTER]
```



| 参数       | 显示列表                   |
| ---------- | -------------------------- |
| 无         | 所有应用                   |
| -f         | 显示应用关联的 apk 文件    |
| -d         | 只显示 disabled 的应用     |
| -e         | 只显示 enabled 的应用      |
| -s         | 只显示系统应用             |
| -3         | 只显示第三方应用           |
| -i         | 显示应用的 installer       |
| -u         | 包含已卸载应用             |
| `<FILTER>` | 包名包含 `<FILTER>` 字符串 |



### 安装APK

```shell
adb install [-lrtsdg] <path_to_apk>
```



| 参数                 | 含义                                                         |
| -------------------- | ------------------------------------------------------------ |
| -l                   | 将应用安装到保护目录 /mnt/asec                               |
| -r                   | 允许覆盖安装                                                 |
| -t                   | 允许安装 AndroidManifest.xml 里 application 指定 `android:testOnly="true"` 的应用 |
| -s                   | 将应用安装到 sdcard                                          |
| -d                   | 允许降级覆盖安装                                             |
| -g                   | 授予所有运行时权限                                           |
| --abi abi-identifier | 为特定 ABI 强制安装 apk，abi-identifier 可以是 armeabi-v7a、arm64-v8a、v86、x86_64 等 |



`adb install` 实际是分三步完成：

1. push apk 文件到 /data/local/tmp。
2. 调用 pm install 安装。
3. 删除 /data/local/tmp 下的对应 apk 文件。



### 卸载应用

```shell
adb uninstall [-k] <packagename>
```

`<packagename>` 表示应用的包名，`-k` 参数可选，表示卸载应用但保留数据和缓存目录。



### 清除应用数据与缓存

```shell
adb shell pm clear <packagename>
```



### 查看前台 Activity

```shell
adb shell dumpsys activity activities | grep mResumedActivity
```



### 查看正在运行的 Services

```shell
adb shell dumpsys activity services [<packagename>]
```



### 与应用交互

```shell
adb shell am <command>
```



常用command

| command                           | 用途                            |
| --------------------------------- | ------------------------------- |
| `start [options] <INTENT>`        | 启动 `<INTENT>` 指定的 Activity |
| `startservice [options] <INTENT>` | 启动 `<INTENT>` 指定的 Service  |
| `broadcast [options] <INTENT>`    | 发送 `<INTENT>` 指定的广播      |
| `force-stop <packagename>`        | 停止 `<packagename>` 相关的进程 |



用于决定 intent 对象的选项如下：

| 参数             | 含义                                                         |
| ---------------- | ------------------------------------------------------------ |
| `-a <ACTION>`    | 指定 action，比如 `android.intent.action.VIEW`               |
| `-c <CATEGORY>`  | 指定 category，比如 `android.intent.category.APP_CONTACTS`   |
| `-n <COMPONENT>` | 指定完整 component 名，用于明确指定启动哪个 Activity，如 `com.example.app/.ExampleActivity` |





### 调起 Activity

```shell
adb shell am start [options] <INTENT>
```



### 调起 Services

```shell
adb shell am startservice [options] <INTENT>
```



### 发送广播

```shell
adb shell am broadcast [options] <INTENT>
```



### 强制停止应用

```shell
adb shell am force-stop <package_name>
```





## 文件管理

### 从设备复制文件到电脑

```shell
adb pull <设备文件路径> [电脑目录]
```



### 从电脑复制文件到设备

```shell
adb push <电脑文件路径> <设备目录>
```





## 模拟按键/输入

```shell
adb shell input [<source>] <command> [<arg>...]
```

source类型

* dpad
* keyboard
* mouse
* touchpad
* gamepad
* touchnavigation
* joystick
* touchscreen
* stylus
* trackball
* [keyevent](https://developer.android.com/reference/android/view/KeyEvent)



### 电源键

```shell
adb shell input keyevent 26
```



### 菜单键

```shell
adb shell input keyevent 82
```



### HOME 键

```shell
adb shell input keyevent 3
```



### 返回键

```shell
adb shell input keyevent 4
```



### 音量控制

```shell
adb shell input keyevent 24 # 增加音量
adb shell input keyevent 25 # 降低音量
adb shell input keyevent 164 # 静音
```



### 媒体控制

```shell
adb shell input keyevent 85 # 播放/暂停
adb shell input keyevent 86 # 停止播放
adb shell input keyevent 87 # 播放下一首
adb shell input keyevent 88 # 播放上一首
adb shell input keyevent 126 # 恢复播放
adb shell input keyevent 127 # 暂停播放
```



### 点亮/熄灭屏幕

```shell
adb shell input keyevent 224 # 点亮屏幕
adb shell input keyevent 223 # 熄灭屏幕
```



### 滑动解锁

```shell
adb shell input swipe 300 1000 300 500 # 300、1000、300、500分别表示起始点x坐标、起始点y坐标、结束点x坐标、结束点y坐标
```



### 输入文书

```shell
adb shell input text hello
```





## 查看日志

Android 系统的日志分为两部分

* 底层的 Linux 内核日志，输出到`/proc/kmsg`
* Android 日志，输出到`/dev/log`



### Android 日志

```shell
[adb] logcat [<option>] ... [<filter-spec>] ...
```



### 内核日志

```shell
adb shell dmesg
```





## 查看设备信息

### 型号

```shell
adb shell getprop ro.product.model
```



### 电池状况

```shell
adb shell dumpsys battery
```



### 屏幕分辨率

```shell
adb shell wm size
```



### 屏幕密度

```shell
adb shell wm density
```



### 显示屏参数

```shell
adb shell dumpsys window displays
```



### Android ID

```shell
adb shell settings get secure android_id
```



### Android 系统版本

```shell
adb shell getprop ro.build.version.release
```



### IP 地址

```shell
adb shell ifconfig
```



### MAC 地址

```shell
adb shell cat /sys/class/net/wlan0/address
```



### CPU 信息

```shell
adb shell cat /proc/cpuinfo
```



### 内存信息

```shell
adb shell cat /proc/meminfo
```



### 更多硬件与系统属性

```shell
adb shell cat /system/build.prop
```





## 实用功能

### 屏幕截图

```shell
adb exec-out screencap -p > sc.png
adb pull /sdcard/sc.png
```



### 屏幕录制

```shell
adb shell screenrecord /sdcard/filename.mp4 # 需要停止时按 ctrl + c ，默认录制时间和最长录制时间都是180秒
adb pull /sdcard/filename.mp4 
```



### 查看连接过的 WIFI 密码

```shell
adb shell
su
cat /data/misc/wifi/*.conf
```



### 设置系统日期和时间

```shell
adb shell
su
data -s 20240408.110300 # 设置时间为2024年4月8日11点03分
```



### 重启手机

```shell
adb reboot
```



### 查看设备是否已经 root

```shell
adb shell
su
```

* $：表示没有 root 权限
* #：表示已经 root



### 使用 Monkey 进行压力测试

Monkey 可以生成伪随机用户事件来模拟单击、触摸、手势等操作，可以对正在开发中的程序进行随机压力测试。

```shell
adb shell monkey -p <package_name> -v 500
```

表示向 package_name 指定的应用程序发送 500 个伪随机事件。



### 开启/关闭 WIFI

```shell
adb root
adb shell svc wifi enable # 开启
adb shell svcc wifi disable # 关闭
```





## 更多 adb shell 命令

### 查看进程

```shell
adb shell ps
```



### 查看实时资源占用情况

```shell
adb shell top
```



### 其他

| 命令  | 功能                        |
| ----- | --------------------------- |
| cat   | 显示文件内容                |
| cd    | 切换日录                    |
| chmod | 改变文件的存取模式/访问权限 |
| df    | 查着磁盘空间使用憜况        |
| grep  | 过滤输出                    |
| kill  | 杀死指定 PID 的进程         |
| ls    | 列举目录内容                |
| mount | 挂载目录的查看和管理        |
| mv    | 移动或重命名文件            |
| ps    | 查看正在运行的进程          |
| rm    | 删除文件                    |
| top   | 查看进程的资源占用情况      |





## 参考

https://juejin.cn/post/7158765693536731172
