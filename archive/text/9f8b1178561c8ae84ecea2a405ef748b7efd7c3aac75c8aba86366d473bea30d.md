# 去马赛克

## 去马赛克的背景

Sensor输出的bayer raw数据每个像素点只能感应一种颜色，需要还原成三通道的彩色图像，把bayer pattern插值转换成完整的RGB444（真彩色）图像的过程称为去马赛克过程。



彩色由R、G、B三通道组成，但CCD只能感受一种光强



### color sensing的方法

* three-CCD camera
* Foveon X3
* Bayer CFA
    * RGGB
    * BGGR
    * GBRG
    * GRBG



### Demosaic定义

从覆有滤色阵列(Color filter array，简称CFA）的感光元件所输出的不完全色彩取样中，重建出全彩影像。



### Demosaic的两大基本原则

*   Spectral correlation，谱相关
    *  相邻像素颜色色调一致，色调即色度和亮度的比例，可以理解为B/G、R/G
    *  相邻像素颜色色差一致，色差即色度和亮度的差，可以理解为B-G、R-G。
    *  第二种优于第一种，特别是特别是在红色或者蓝色分量比较饱和，而绿色分量比较不饱和的情況下。在这种情况下，红色或者蓝色的一点微小扰动都会对结果造成很大影响。
*   Spatial correlation，空间相关
    * 同质区内部，像素之间的颜色都是接近的；在非同质区则会有明显差异。



## 去马赛克的方法

### Nearest neighbor replication

最简单的方法

缺陷：分辨率降低，相当于downsample



### 双线性插值

缺点：模糊、伪彩色、拉链效应



插值的时候，还有什么信息有助于插值？

*  相邻像素，RGB颜色分量相关度很高。在对R括值的时候，G的信息能不能起到点作用？
* 边缘上的像素，边缘两侧像素值相差较大，可否考虑沿着边缘进行插值？



### MHC

*   Malvar-He-Cutler Linear Image Demosaicking谱相关原则
*   添加Laplacian cross-channel corrections

[Malvar-He-Cutler Linear Image Demosaicking](https://www.ipol.im/pub/art/2011/g_mhcd/article.pdf)



优缺点

* 优点：比双线性插值锐化
* 缺点：仍然会存在较明显的伪彩色



### 边缘自适应

* 谱相关
*   空间相关——边缘检测
*   Hamilton and Adams

[Adaptive color plane interpolation in single sensor color electronic camera](https://patents.google.com/patent/US5652621A/en)

## 去马赛克的难点

### 摩尔纹

*  出现原因：CCD中像素空间频率与景物中条纹空间频率接近，产生干涉。Bayer CFA的亚采样特性，在高频区域容易恢复出错误颜色从而产生细密的摩尔纹。
* 解决方法：思路：感光元件的采样空间分辨率要大大高于镜头景物分辨率。
    * 在彩色滤波阵列之前增加一个低通滤波器，滤除部分高频信号，通过降低图像锐度的方法减少摩尔纹的发生率
    * 提高CCD感光阵列像素密度来提高空间采样率



### 锯齿效应

*   出现原因：在图像边缘交界区域，Demosaic插值没有沿边缘进行，而是沿横跨边缘的方向插值；会产生像素点模糊以及颜色溢出；双线性插值会有大量的锯齿效应；
* 解决方法：空间相关原则-插值。



### 伪彩色

*  出现原因：图像重合错位；不恰当的领域插值常出现在色彩边缘处
* 解决方法：常使用中值滤波；对于包含较多点、线等细节的图像，则不适合使用，容易造成细节丢失。