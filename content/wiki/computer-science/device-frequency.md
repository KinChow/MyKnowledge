---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: 现代处理器可以在多种时钟频率和电压配置（P-state）下运行。
  claim_id: device-frequency-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-c613c087b5a0
    exact: The majority of modern processors are capable of operating in a number
      of different clock frequency and voltage configurations, often referred to as
      Operating Performance Points or P-states (in ACPI terminology).
  targets:
  - evidence_id: evidence-c613c087b5a0
    source_id: linux-cpufreq-v2
id: device-frequency
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- linux-cpufreq-v2
- working-computer-science-device-frequency
status: published
tags:
- device
- frequency
- performance
- sysfs
title: 设备频率
updated_at: '2026-09-06'
---
# 设备频率

## 详细章节

### 设备频率

#### 获取设备频率

##### CPU

###### little core

```shell
# available frequencies
cat /sys/devices/system/cpu/cpufreq/policy0/scaling_available_frequencies

# current frequencies
cat /sys/devices/system/cpu/cpufreq/policy0/cpuinfo_cur_freq
```



###### middle core

```shell
# available frequencies
cat /sys/devices/system/cpu/cpufreq/policy1/scaling_available_frequencies

# current frequencies
cat /sys/devices/system/cpu/cpufreq/policy1/cpuinfo_cur_freq
```



###### big core

```shell
# available frequencies
cat /sys/devices/system/cpu/cpufreq/policy2/scaling_available_frequencies

# current frequencies
cat /sys/devices/system/cpu/cpufreq/policy2/cpuinfo_cur_freq
```



##### GPU
```shell
# available frequencies
cat /sys/class/devfreq/gpufreq/available_frequencies

# current frequencies
cat /sys/class/devfreq/gpufreq/cur_freq
```



##### NPU

```shell
# available frequencies
cat /sys/class/devfreq/npufreq/available_frequencies

# current frequencies
cat /sys/class/devfreq/npufreq/cur_freq
```



##### DDR

```shell
# available frequencies
cat /sys/class/devfreq/ddrfreq/available_frequencies

# current frequencies
cat /sys/class/devfreq/ddrfreq/cur_freq
```



##### L3 cache

```shell
# available frequencies
cat /sys/class/devfreq/l3c_devfreq/available_frequencies

# current frequencies
cat /sys/class/devfreq/l3c_devfreq/cur_freq
```





#### 设置设备频率

##### CPU

###### little core

```shell
# max frequency
echo {} > /sys/devices/system/cpu/cpufreq/policy0/scaling_max_freq

# min frequency
echo {} > /sys/devices/system/cpu/cpufreq/policy0/scaling_min_freq
```


###### middle core

```shell
# max frequency
echo {} > /sys/devices/system/cpu/cpufreq/policy1/scaling_max_freq

# min frequency
echo {} > /sys/devices/system/cpu/cpufreq/policy1/scaling_min_freq
```


###### big core

```shell
# max frequency
echo {} > /sys/devices/system/cpu/cpufreq/policy2/scaling_max_freq

# min frequency
echo {} > /sys/devices/system/cpu/cpufreq/policy2/scaling_min_freq
```



##### GPU

```shell
# max frequency
echo {} > /sys/devices/devfreq/gpufreq/max_freq

# min frequency
echo {} > /sys/devices/devfreq/gpufreq/min_freq
```



##### NPU

```shell
# max frequency
echo {} > /sys/devices/devfreq/npufreq/max_freq

# min frequency
echo {} > /sys/devices/devfreq/npufreq/min_freq
```



##### DDR

```shell
# max frequency
echo {} > /sys/devices/devfreq/ddrfreq/max_freq

# min frequency
echo {} > /sys/devices/devfreq/ddrfreq/min_freq
```



##### L3 cache

```shell
# max frequency
echo {} > /sys/devices/devfreq/l3c_devfreq/max_freq

# min frequency
echo {} > /sys/devices/devfreq/l3c_devfreq/min_freq
```
