# Mali Bifrost GPU计算

以Laplace滤波为例子，使用OpenCL在Mali Bifrost计算。



## Laplace滤波

Laplace滤波常用于图像处理中，对图像进行边缘检测或图像锐化。



## 约束

* 只处理灰度图，真实场景处理RGB图像。

* local workgroup size为nullptr



## 代码

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





## 优化

### 单独处理边界

为了避免访问非法数据，边界应该单独被处理。



有多种方法处理边界

* 每个kernel都进行边界检查
* 使用不同kernel处理边界数据
* 在输入输出内存增加padding buffer





### 128 bits加载和存储

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





### 合并加载

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





### 32bit向量化

Bifrost在数学运算上无需超过32bit向量化，尽管内存操作更喜欢更大的数据操作；

32bit数学运算应该和128bit数学运算性能相近。





### 优化local workgroup size

local workgroup size可以影响缓存模式

* 基于quad架构，local workgroup大小可以整除4时，性能会更好
* 运行时驱动程序可能不是选择最优local workgroup大小



选择合适的workgroup大小

* 使用`-cl-arm-non-uniform-work-group-size`选项，因为某些图像大小不能被local workgroup大小整除
* 在4到64之间变化，只要是4的倍数，性能不会发生太大变化