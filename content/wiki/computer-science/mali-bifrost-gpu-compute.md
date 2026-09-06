---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: Mali 和 Immortalis 系列是 Arm Holdings 生产并授权给合作伙伴集成到 ASIC 设计中的 GPU 与多媒体处理器 IP。
  claim_id: mali-gpu-ip
  support: direct
  supporting_quotes:
  - evidence_id: evidence-8c0bde510fac
    exact: The Mali and Immortalis series of graphics processing units (GPUs) and
      multimedia processors are semiconductor intellectual property cores produced
      by Arm Holdings for licensing in various ASIC designs by Arm partners.
  targets:
  - evidence_id: evidence-8c0bde510fac
    source_id: wikipedia-mali-processor-v2
id: mali-bifrost-gpu-compute
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-mali-processor-v2
- working-computer-science-mali-bifrost-gpu-compute
status: published
tags:
- opencl
- mali
- gpu
- compute
- optimization
title: Mali Bifrost GPU计算
updated_at: '2026-09-06'
---
# Mali Bifrost GPU计算


## 一句话结论

以 Laplace 滤波为例，在 Mali Bifrost GPU 上用 OpenCL 做图像处理的核心优化是：边界单独处理、使用 128-bit 向量加载/存储（vload/vstore）、合并加载减少指令、利用 Bifrost 32-bit 数学向量化、并优化 local workgroup size。

## 核心概念

- **Laplace 滤波**：图像边缘检测/锐化的卷积算子，模板 {-1, -1, -1, -1, 9, -1, -1, -1, -1}。
- **128-bit 加载/存储**：Bifrost（原文“Mimir”）更偏好一次加载/存储 128 bits，最好一次覆盖 cache line（512 bits）。
- **边界处理三种方法**：每个 kernel 都做边界检查、用不同 kernel 处理边界数据、在输入输出内存加 padding buffer。
- **Bifrost 数学向量化**：数学运算无需超过 32-bit 向量化，32-bit 与 128-bit 数学性能相近。
- **local workgroup size**：基于 quad 架构，可整除 4 时性能更好；非整除图像用 `-cl-arm-non-uniform-work-group-size`。

## 工作机制

1. 基础版本：每个 work-item 处理一个像素，先做边界检查，再计算 Laplace 中心点并 clamp 到 [0,255]。
2. 128-bit 向量化版本：globalWorkSize = {height, width>>4}，用 vload16 一次加载 16 字节，uchar16/int16 向量计算，vstore16 存储。
3. 合并加载版本：只加载 6 个 vload16（src00/02/10/12/20/22），用 swizzle 拼出 src01/11/21，减少加载指令。
4. 32-bit 向量化：数学计算保持 32-bit 宽度即可。
5. local workgroup 大小在 4 到 64 之间的 4 倍数范围内性能差异不大；运行时驱动可能不选最优。

## 示例或代码

（三个版本的完整 kernel 代码见 ## 详细章节：基础版、128-bit 向量化版、合并加载版。）

## 常见误区

- 边界像素直接在 kernel 内计算导致越界访问——边界应单独处理。
- 用标量加载 `=pSrc[idx]` 逐个取像素，浪费带宽——用 vloadN/vstoreN。
- 误以为数学运算需要 128-bit 向量化——Bifrost 上 32-bit 数学即可。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| mali-gpu-ip | wikipedia-mali-processor-v2 | Mali/Immortalis 是 Arm Holdings 的 GPU/多媒体 IP，授权合作伙伴集成到 ASIC |

## 待验证项

- “Mimir” 疑为 Bifrost 一代引擎名笔误，待核对。
- local workgroup 4~64 范围内性能结论为经验值，需按实际内核验证。

## 关联知识

- [[mali-gpu-overview]] —— Mali GPU 架构概述。
- [[optimizing-opencl-for-mali-gpus]] —— Mali OpenCL 优化。
- [[opencl-optimizations-list]] —— OpenCL 优化清单。


## 详细章节

### Mali Bifrost GPU计算

以Laplace滤波为例子，使用OpenCL在Mali Bifrost计算。



#### Laplace滤波

Laplace滤波常用于图像处理中，对图像进行边缘检测或图像锐化。



#### 约束

* 只处理灰度图，真实场景处理RGB图像。

* local workgroup size为nullptr



#### 代码

```c
// globalWorkSize = {height, width};
__kernel void laplaceFilter(__global unsigned char *pDst, // destination buffer
                           __global unsigned char *pSrc, // source buffer
                           int width, // image width
                           int height) // image height
{
    int x = get_global_id(0);
    int y = get_global_id(1);
    int w = get_global_size(0);
    int h = get_global_size(1);
    int idx = x + w * y;
    int xBoundry = w - 2;
    int yBoundry = h - 2;
    // boundry check
    if (x >= xBoundry || y >= yBoundry) {
        pDst[idx] = pSrc[idx];
        return;
    }
    // laplace filer {-1, -1, -1, -1, 9, -1, -1, -1, -1}
    int center = (-pSrc[idx]) + (-pSrc[idx + 1]) + (-pSrc[idx + 2]) + (-pSrc[idx + w]) + (pSrc[idx + w + 1] * 9) + (-pSrc[idx + w + 2]) + (-pSrc[idx + w * 2]) + (-pSrc[idx + w * 2 + 1]) + (-pSrc[idx + w * 2 + 2]);
    unsigned char center_s8 = (unsigned char)clamp(center, 0, 255);
    pDst[idx + w + 1] = center_s8;
}
```





#### 优化

##### 单独处理边界

为了避免访问非法数据，边界应该单独被处理。



有多种方法处理边界

* 每个kernel都进行边界检查
* 使用不同kernel处理边界数据
* 在输入输出内存增加padding buffer





##### 128 bits加载和存储

Mimir更喜欢一次加载和存储128 bits数据，更喜欢一次性加载次数cache line（512 bits）

使用vload/vstore指令进行向量化加载/存储

* 使用`vloadN`代替`=pSrc[idx]`进行加载数据，使用`vstoreN`代替`pDst[idx]=`进行存储数据
* 算术计算通常由32bits指令完成
  * `(char16)a + (char16)b`是由4个`char4`相加而成
* 加载的数据多了，工作项减少，需要调整global work size



```c
// globalWorkSize = {height, width >> 4};
__kernel void laplaceFilter(__global unsigned char *pDst, // destination buffer
                           __global unsigned char *pSrc, // source buffer
                           int width, // image width
                           int height) // image height
{
    int x = get_global_id(0);
    int y = get_global_id(1);
    int w = get_global_size(0);
    int h = get_global_size(1);
    int idx = (x << 4) + w * y;
    uchar16 src00 = vload16(0, pSrc + idx);
    uchar16 src01 = vload16(0, pSrc + idx + 1);
    uchar16 src02 = vload16(0, pSrc + idx + 2);
    uchar16 src10 = vload16(0, pSrc + idx + w);
    uchar16 src11 = vload16(0, pSrc + idx + w + 1);
    uchar16 src12 = vload16(0, pSrc + idx + w + 2);
    uchar16 src20 = vload16(0, pSrc + idx + w * 2);
    uchar16 src21 = vload16(0, pSrc + idx + w * 2 + 1);
    uchar16 src22 = vload16(0, pSrc + idx + w * 2 + 2);
    // laplace filer {-1, -1, -1, -1, 9, -1, -1, -1, -1}
    int16 center = (-src00) + (-src01) + (-src02) + (-src10) + (src11 * (int16)9) + (-src12) + (-src20) + (-src21) + (-src22);
    uchar16 center_s8 = convert_uchar16(clamp(center, (int16)0, (int16)255));
    vstore16(center_s8, 0, pDst + idx + w + 1);
}
```





##### 合并加载

```c
// globalWorkSize = {height, width >> 4};
__kernel void laplaceFilter(__global unsigned char *pDst, // destination buffer
                           __global unsigned char *pSrc, // source buffer
                           int width, // image width
                           int height) // image height
{
    int x = get_global_id(0);
    int y = get_global_id(1);
    int w = get_global_size(0);
    int h = get_global_size(1);
    int idx = (x << 4) + w * y;
    uchar16 src00 = vload16(0, pSrc + idx);
    uchar16 src02 = vload16(0, pSrc + idx + 2);
    uchar16 src10 = vload16(0, pSrc + idx + w);
    uchar16 src12 = vload16(0, pSrc + idx + w + 2);
    uchar16 src20 = vload16(0, pSrc + idx + w * 2);
    uchar16 src22 = vload16(0, pSrc + idx + w * 2 + 2);
    uchar16 src01 = (uchar16)(src00.s12345678, src02.s789abcde);
    uchar16 src11 = (uchar16)(src10.s12345678, src12.s789abcde);
    uchar16 src21 = (uchar16)(src20.s12345678, src22.s789abcde);
    // laplace filer {-1, -1, -1, -1, 9, -1, -1, -1, -1}
    int16 center = (-src00) + (-src01) + (-src02) + (-src10) + (src11 * (int16)9) + (-src12) + (-src20) + (-src21) + (-src22);
    uchar16 center_s8 = convert_uchar16(clamp(center, (int16)0, (int16)255));
    vstore16(center_s8, 0, pDst + idx + w + 1);
}
```





##### 32bit向量化

Bifrost在数学运算上无需超过32bit向量化，尽管内存操作更喜欢更大的数据操作；

32bit数学运算应该和128bit数学运算性能相近。





##### 优化local workgroup size

local workgroup size可以影响缓存模式

* 基于quad架构，local workgroup大小可以整除4时，性能会更好
* 运行时驱动程序可能不是选择最优local workgroup大小



选择合适的workgroup大小

* 使用`-cl-arm-non-uniform-work-group-size`选项，因为某些图像大小不能被local workgroup大小整除
* 在4到64之间变化，只要是4的倍数，性能不会发生太大变化
