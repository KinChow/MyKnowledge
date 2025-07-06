# fastboot

fastboot是一种特殊的启动模式，主要用于Android设备。它允许用户与设备的引导程序（Bootloader）进行通信，以便执行系统级别的操作，而无需完全启动Android操作系统。fastboot模式提供了一个命令行界面，通过这个界面，用户可以刷写固件、解锁引导程序、安装自定义Recovery等





## 分区

在Android设备上，使用Fastboot可以操作不同的分区，每个分区都有其特定的作用和用途。以下是一些常见的分区及其作用：

* **boot分区**：

  - 包含设备的引导加载程序（Bootloader）和内核。

  - 当设备启动时，首先加载的分区，用于启动操作系统。

* **recovery分区**：

  - 包含一个小型的操作系统，用于恢复和维护设备。

  - 可以用于执行如系统更新、清除数据、刷入新的ROM等操作。

- **system分区**：
  - 包含Android系统的核心文件和应用程序。
  - 包括系统库、框架、设置应用和系统服务等。

- **userdata分区**：
  - 存储用户数据和应用程序数据。
  - 包括用户安装的应用、用户账户信息、应用数据等。

- **cache分区**：
  - 用于存储临时文件和缓存数据。
  - 清理此分区可以帮助释放存储空间，但通常不会影响系统功能。

- **vendor分区**：
  - 包含供应商特定的系统文件和二进制文件。
  - 通常包括设备制造商的专有软件和驱动程序。

- **modemst1和modemst2分区**：
  - 包含基带（调制解调器）固件。
  - 负责处理无线通信和网络连接。

- **efs分区**：
  - 包含加密文件系统，用于存储敏感信息，如Wi-Fi密码、蓝牙配置文件等。

- **misc分区**：
  - 用于存储杂项数据，如设备标识符、序列号等。

- **vendor_ext分区**：
  - 扩展的供应商分区，用于存储额外的供应商数据。

- **odm分区**：
  - 原始设备制造商（ODM）用于存储特定于其硬件的文件和数据。

- **product分区**：
  - 包含产品特定的文件和数据。

请注意，不同的设备和Android版本可能会有不同的分区结构。在进行分区操作时，应该非常小心，因为错误的操作可能会导致设备无法启动或其他问题。在进行任何分区操作之前，建议备份重要数据，并确保了解每个分区的作用。





## 指令

### 设备管理指令

- `fastboot devices`：显示连接到计算机的所有fastboot设备。
- `fastboot getvar all`：获取手机相关信息，如设备状态。



### 重启指令

- `fastboot reboot`：重启手机（退出fastboot模式）。
- `fastboot reboot-bootloader`：重启到Bootloader模式。



### 擦除分区指令

- `fastboot erase system`：擦除system分区。
- `fastboot erase boot`：擦除boot分区。
- `fastboot erase cache`：擦除cache分区。
- `fastboot erase userdata`：擦除userdata分区。



### 写入分区指令

- `fastboot flash system system.img`：将system.img文件刷写到system分区。
- `fastboot flash boot boot.img`：将boot.img文件刷写到boot分区。
- `fastboot flash recovery recovery.img`：将recovery.img文件刷写到recovery分区。
- `fastboot flash bootloader bootloader.img`：刷写bootloader引导文件。



### 上锁/解锁指令

- `fastboot oem unlock`：解锁命令。
- `fastboot oem lock`：上锁命令。





## 参考

https://blog.csdn.net/weixin_37738083/article/details/62429992

https://blog.csdn.net/m0_66587877/article/details/134807972

https://blog.csdn.net/ByteKnight/article/details/133414756