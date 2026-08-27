---
archive_policy: text-only
confidentiality: public
domain: computer-science
extractor: utf8/1
id: device-frequency
local:
  file_sha256: sha256:4d71fb54952bb9999b72c409d3e3e6623738a76ba2088ee39a35458390c41259
  path_ref: local-sidecar:public/device-frequency
media_type: text/markdown
origin: external
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:4d71fb54952bb9999b72c409d3e3e6623738a76ba2088ee39a35458390c41259
source_type: local-file
vault_id: public
---
# 设备频率

## 获取设备频率

### CPU

#### little core

```shell
# available frequencies
cat /sys/devices/system/cpu/cpufreq/policy0/scaling_available_frequencies

# current frequencies
cat /sys/devices/system/cpu/cpufreq/policy0/cpuinfo_cur_freq
```



#### middle core

```shell
# available frequencies
cat /sys/devices/system/cpu/cpufreq/policy1/scaling_available_frequencies

# current frequencies
cat /sys/devices/system/cpu/cpufreq/policy1/cpuinfo_cur_freq
```



#### big core

```shell
# available frequencies
cat /sys/devices/system/cpu/cpufreq/policy2/scaling_available_frequencies

# current frequencies
cat /sys/devices/system/cpu/cpufreq/policy2/cpuinfo_cur_freq
```



### GPU
```shell
# available frequencies
cat /sys/class/devfreq/gpufreq/available_frequencies

# current frequencies
cat /sys/class/devfreq/gpufreq/cur_freq
```



### NPU

```shell
# available frequencies
cat /sys/class/devfreq/npufreq/available_frequencies

# current frequencies
cat /sys/class/devfreq/npufreq/cur_freq
```



### DDR

```shell
# available frequencies
cat /sys/class/devfreq/ddrfreq/available_frequencies

# current frequencies
cat /sys/class/devfreq/ddrfreq/cur_freq
```



### L3 cache

```shell
# available frequencies
cat /sys/class/devfreq/l3c_devfreq/available_frequencies

# current frequencies
cat /sys/class/devfreq/l3c_devfreq/cur_freq
```





## 设置设备频率

### CPU

#### little core

```shell
# max frequency
echo {} > /sys/devices/system/cpu/cpufreq/policy0/scaling_max_freq

# min frequency
echo {} > /sys/devices/system/cpu/cpufreq/policy0/scaling_min_freq
```


#### middle core

```shell
# max frequency
echo {} > /sys/devices/system/cpu/cpufreq/policy1/scaling_max_freq

# min frequency
echo {} > /sys/devices/system/cpu/cpufreq/policy1/scaling_min_freq
```


#### big core

```shell
# max frequency
echo {} > /sys/devices/system/cpu/cpufreq/policy2/scaling_max_freq

# min frequency
echo {} > /sys/devices/system/cpu/cpufreq/policy2/scaling_min_freq
```



### GPU

```shell
# max frequency
echo {} > /sys/devices/devfreq/gpufreq/max_freq

# min frequency
echo {} > /sys/devices/devfreq/gpufreq/min_freq
```



### NPU

```shell
# max frequency
echo {} > /sys/devices/devfreq/npufreq/max_freq

# min frequency
echo {} > /sys/devices/devfreq/npufreq/min_freq
```



### DDR

```shell
# max frequency
echo {} > /sys/devices/devfreq/ddrfreq/max_freq

# min frequency
echo {} > /sys/devices/devfreq/ddrfreq/min_freq
```



### L3 cache

```shell
# max frequency
echo {} > /sys/devices/devfreq/l3c_devfreq/max_freq

# min frequency
echo {} > /sys/devices/devfreq/l3c_devfreq/min_freq
```