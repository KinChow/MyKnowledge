# 锐化

## DE 概述

DE：Detail Enhancement 细节增强

RAWNF模块能够过滤掉图片中的噪声，并保留边缘信息；但是会导致一些纹理和高频的细节丢失。

DE模块就是用来恢复和提升细节信息用的。



## DE 原理

$$
FinalNoise = A*HF(noise) + B* MF(noise) + C*LF(noise) \\

Y' = Y + FinalNoise \\

noise = RAWNF_{input} - RAWNF_{output} \\
$$



* Y是上一级模块的输出，Y'是DE模块的输出。
* HF/MF/LF是从RAWNF输出的noise中提取的高频/中频/低频信息。
* A, B, C是HF/MF/LF的增益系数，用来控制加回的强度。



## Sharpen

### Sharpen概念

锐度：摄影媒介处理图像边缘反差的程度。

* 高锐度图像的边缘清晰而且边缘部分的反差较大，所以整个图像看上去清晰，引人注目。
* 低锐度图像的边缘模糊，不清哳。



锐化：增加图像边缘反差的过程。

普通的相机sensor和镜头出图不够清晰，通过做锐化，可以使图像升级到高端相机镜头的图像质量。

对于数码相机，这种不清晰是由相机传感器的抗锯齿滤镜和去马赛克处理引起的，此外跟相机的镜头也有关系。



### Sharpen原理

虽然锐化过程尤法重建上面的理想图像，但是它可以创建更明显的边缘外观。有效锐化的关键是在使边缘看起来足够明显之间达成微妙的平衡，同时还要使可见的under and overshoots（称为“锐化光晕”）最小化。



### Unsharp Mask

通过减去低通滤波的图像，得到Unsharp Mask（高频信息，边缘信息）。
通过高对比度图像、边缘信息、原始图像得到锐化后的图像。



## 算法原理

要想实现更好的sharpen效果，只做USM是不够的，还要做Clipping。
Clipping的作用是去除/降低overshoot和undershoot