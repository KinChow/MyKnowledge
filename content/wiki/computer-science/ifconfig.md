---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: "IFCONFIG(8)        Linux System Administrator's Manual        IFCONFIG(8)\n
    \      ifconfig - configure a network interface\n       ifconfig [-v] [-a] [-s]
    [interface]\n       ifconfig [-v] interface [aftype] options | address ...\n       Ifconfig
    is used to configure the kernel-resident network\n       interfaces.  It is used
    at boot time to set up interfaces as\n       necessary.  After that, it is usually
    only needed when debugging\n       or when system tuning is needed."
  claim_id: ifconfig-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-5f0b8d621c23
    exact: "IFCONFIG(8)        Linux System Administrator's Manual        IFCONFIG(8)\n
      \      ifconfig - configure a network interface\n       ifconfig [-v] [-a] [-s]
      [interface]\n       ifconfig [-v] interface [aftype] options | address ...\n
      \      Ifconfig is used to configure the kernel-resident network\n       interfaces.
      \ It is used at boot time to set up interfaces as\n       necessary.  After
      that, it is usually only needed when debugging\n       or when system tuning
      is needed."
  targets:
  - evidence_id: evidence-5f0b8d621c23
    source_id: web-computer-science-ifconfig
id: ifconfig
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-ifconfig
- working-computer-science-ifconfig
status: published
tags:
- linux
- networking
- command-line
title: ifconfig
updated_at: '2026-09-06'
---
# ifconfig

## 详细章节

### ifconfig

#### 概要

功能：用来查看和配置网络设备。

命令：

```shell
ifconfig [网络设备] [参数]
```





#### 显示网络设备信息

```shell
ifconfig # 处于激活状态的网络接口
ifconfig -a # 所有配置的网络接口，不论其是否激活
ifconfig eth0 # 显示eth0的网卡信息
```

* 第一行：
  * Link encap：连接类型
  * HWaddr：物理地址
* 第二行：
  * inet addr：IP地址
  * Bcast：广播地址
  * Mask：掩码地址
* 第三行：状态
  * UP（代表网卡开启状态）
  * RUNNING（代表网卡的网线被接上）
  * MULTICAST（支持组播）
  * MTU:1500（最大传输单元）：1500字节
* 第四、五行：接收、发送数据包情况统计
* 第七行：接收、发送数据字节数统计信息





#### 启动关闭网卡

```shell
ifconfig eth0 up
ifconfig eht0 down
```





#### 配置删除网卡IPv6

```shell
ifconfig eth0 add 33ffe:3240:800:1005::2/64 # 为网卡eth0配置IPv6地址
ifconfig eth0 del 33ffe:3240:800:1005::2/64 # 为网卡eth0删除IPv6地址
```





#### 修改Mac地址

```shell
ifconfig eth0 hw ether 00:AA:BB:CC:DD:EE
```





#### 配置IP地址

```shell
ifconfig eth0 192.168.2.10 netmask 255.255.255.0 broadcast 192.168.2.255
```





#### 启动关闭arp协议

```shell
ifconfig eth0 arp # 开启网卡eth0 的arp协议
ifconfig eth0 -arp # 关闭网卡eth0 的arp协议
```





#### 设置最大传输单元

```shell
ifconfig eth0 mtu 1500 # 设置能通过的最大数据包大小为1500 bytes
```
