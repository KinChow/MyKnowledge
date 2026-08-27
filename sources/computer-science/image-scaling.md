---
archive_policy: text-only
confidentiality: public
domain: computer-science
extractor: utf8/1
id: image-scaling
local:
  file_sha256: sha256:d2a6d2fea0fcc2c184622a03bc5aa5c7cd75e0a986bec9b99ec9dac0af0cc7a3
  path_ref: local-sidecar:public/image-scaling
media_type: text/markdown
origin: external
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:d2a6d2fea0fcc2c184622a03bc5aa5c7cd75e0a986bec9b99ec9dac0af0cc7a3
source_type: local-file
vault_id: public
---
# 图像缩放

## 应用背景

改变图像的分辨率，以适应不同尺寸的显示设备和不同的图像使用场景。



## 实现方法

对缩放后的像素点在原图像中相对坐标点进行计算。



### 最近邻域插值



### 双线性插值



### 双三次插值



### 带边缘检测的图像放大算法



## 实现难度

### 锯齿

### 模糊

