---
domain: computer-science
legacy_first_commit_at: '2025-07-06T20:30:14+08:00'
legacy_path: docs/computer-science/applied-computer-science/multimedia/camera/algorithm/image-processing/image-reconstruction/green-balance-correction.md
snapshot_sha256: sha256:5270c4956f99741f00abf07707f6e502e69fe266deea830ad95d001a037d14c1
title: 绿平衡校正
---
# 绿平衡校正

## 绿平衡背景

由于：

*   半导体制造工艺限制
*  微透镜

导致Gr和Gb两个绿色分量存在偏差。



## 影响

迷宫格 出现在平坦区域



## 绿平衡难点

绿平衡、噪声、细节



## 绿平衡校正方法

### 静态校正

根据sensor模组决定，使用较少



### 动态校正

根据图像中像素之间的差值等关系动态决定

优化：阈值可以是动态的

1. 分别计算Gr和Gb平均值
2. 取Gr和Gb平均值的差值diff
3. diff < 阈值
    * 如果为False，无需校正处理
    * 如果为True，校正G分量