# 频域降噪

## 背景

什么是频域

图像作为二维信号，对于某一点的灰度级，就是图像信号上这一点的幅度，根据信号的概念，频率就是信号变化的快慢，所谓的频率也就是在图空间上的灰度变换的快慢。



频域的基本性质：什么是低频，什么是高频？

频域：频率变量（u,v）定义的空间。

图像频率分量（u,v）和空间变量（×, y）（灰度变化模式）之间的联系：

1.   变化最慢的频率成分（u=v=0）对应一幅图像的平均灰度级
2.   当从变换的原点移开时，低频对应着图像的慢变化分量，如图像的平滑部分。
3.   进一步离开原点时，高频对应图像中变化越来越快的灰度级



什么地方灰度级变化越来越快？

*  图像边缘的灰度值变化快，对应着频率高，即高频显示图像边缘。
*  图像的细节处也是属于灰度值急剧变化的区域。
*  图像噪声（即噪点），在一个像素所在的位置，之所以是噪点，就是因为它与正常的点颜色不一样，也就是灰度有快速地变化，所以也是高频部分。



## 方法

### 频域降噪方法

思想：利用信号在空间上的连续性，将图像信号变换到频率域，在频率域将信号和噪声分离，进而完成降噪



### 傅里叶变换

空域-频域变换方法 图像的傅里叶变换 （Fourier Tranform）

*  任何周期函数，都可以看作是不同振幅，不同相位正弦波的叠加。



### 高通高斯滤波器

* 高频通过，低频衰减。
* 图像减少了灰度级的平滑过渡而突出了边缘等细节部分，使图像变得锐化。



### 低通高斯滤波器

* 低频通过，高频衰诚。
* 图像丢失尖锐的细节部分而突出了平滑过波部分，使图像变得模糊。



### DCT变换

* DCT变换（Discrete Cosine Transform）、离散余弦变换。类似于离散傅里叶变换。
*   离散佛里叶变换需要进行复数运算在实时处理中非常不便，根据离散傅里叶变换的性质，实偶函数的傅里叶变换只含实的余弦项，因此构造了一种实数域的变换-离散余弦变换（DCT）
* 利用DCT进行降噪的主要思路其实比较简单，对图像进行DCT变换，然后在变换后的频率域通过设置阈值，过滤掉高频部分（证常认为噪声都是高频部分），然后再用DCT反变换变换为图像。



### 小波变换

图像小波变换（Wavelet Transform）

*   将傅里叶变换中无限长的三角函数基换成有限长的会衰减的小波基。
*  对于M*N的二维图像先经过水平滤波器组分解成低频和高频分量：然后再通过垂直滤波器组
最终分解成为4个子带图像数据（M/2）×（N/2）.变换后的3个高频分量LH,HL和HH，而低烦分量LL送到下一级滤波器组中进行第二级变换，依次类推，最终完成二维Haar小波变换。



小波变换可以很好地保存有效的信号的尖峰和突变部分。



结论：在小波域，利用噪声的小波系数相对较小。

所以经常采用将较小的小波系数丢掉的方法降噪。



阈值去噪

1. 原始图像
2. 小波变换，得到各维度系数
3. 进行阈值处理
4. 小波重构，得到去噪后的图像
5. 最终图像



* 阈值门限选取
    * 固定阈值估计
    * 极值阈值估计
* 阈值函数处理
    * 硬阈值去噪：硬阈值法获得的重构信号具有更好的逼近性，但有附加振荡。
    * 软阈值去噪：软阈值获得的重构信号具有更好的光滑性，但误差相对较大。



## 应用

BM3D