---
archive_policy: text-only
confidentiality: public
domain: computer-science
extractor: utf8/1
id: calculate-mode
local:
  file_sha256: sha256:d876720adb8b30c5ea60b15b39e2d8290937dea2a819880ac7c12d689d42f1bc
  path_ref: local-sidecar:public/calculate-mode
media_type: text/markdown
origin: external
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:d876720adb8b30c5ea60b15b39e2d8290937dea2a819880ac7c12d689d42f1bc
source_type: local-file
vault_id: public
---
# 计算模式

## AI 三大范式流程

### 监督学习

### 非监督学习

### 强化学习



## 网络模型结构设计&演进

### 神经网络

### 主要计算：权重求和

#### 激活函数

##### tanh

##### ReLU

##### Sigmoid

##### Linear

### 主流的网络模型结构

* 全连接 Fully Connected Layer
  * Feed forward, fully connected
  * Multilayer Perceptron (MLP)
* 卷积层 Convolutional Layer
  * Feed forward, sparsely-connected, weight shading
  * Convolutional Neural Network (CNN)
  * Typically used for images
* 循环网络 Recurrent Layer
  * Feedback
  * Recurrent Neural Network (RNN/LSTM)
  * Typically used for sequential data (e.g., speech, language)
* 注意力机制 Attention Layer
  * Attention (matrix multiply) + Feed forward, fully connected
  * Foundation Models
  * Transformer



### 经典网络模型

模型越大越深



## 模型量化&网络剪枝

### 量化压缩 vs 网络剪枝

网络剪枝研究模型权重中

的冗余， 并尝试删除/修剪

冗余和非关键的权重。



模型量化是指通过减少权

重表示或激活所需的比特

数来压缩模型。



### 低比特量化特征

1. 参数压缩；
2. 提升速度；
3. 降低内存；
4. 功耗降低；
5. 提升芯片面积；