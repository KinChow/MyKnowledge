# 图像文件格式

## 像素排列格式

像素排列的格式与色彩空间有关，每种色彩描述方式都对应了不同的排列格式。例如RGB888planar、GRB888packed、NV21、YUYV等等。

主要分为两类：

* planar：同类的像素排列在一起。比如YUV，先排完所有Y，再排列U，最后排列V
* packed：每个单元的像素排列一块。比如YUV，按照YUVYUVYUV的顺序去存储整张照片

通过FOURCC区分，有统一的编码，有时候为了方便会加上位宽。

排列格式有大小端的区别。



### 8bit像素排列

* RGB888、ARGB8888
  * 排列顺序
    * RGB888：RGBRGBRGB
    * ARGB8888：ARGBARGB
  * 这一类大同小异，但是在具体存储的时候会有排列顺序差异
* AYUV
  * 排列顺序：VUYAVUYAVUYA
  * YUV4:4:4格式，FOURCC码为AYUV。这是packed格式，其中每个像素都被编码为四个连续字节。
* UYVY
  * 排列顺序：UYVYUYVYUYVY
  * YUV4:2:2格式，可以看做两个小端字节，则第一个字节的LSB包含U值，MSB包含Y值，第二个字节的LSB包含V值，MSB包含Y值。
* NV12
  * 排列顺序：YYYUVUV
  * YUV4:2:0格式，组合的UV数组可以看做一个小端字节，LSB包含U值，MSB包含V值。NV21的U和V顺序与NV12相反。



### 10bit像素排列

这种格式一个字节存不下，一般会占用2个字节。一般在低位补0。这样可以使得不支持16bit的设备直接截断成10bit而仅仅需要损失少量细节。

还需要关注像素的大小端字节序。



## 图像存储格式

图像存储格式是一个盒子（Container）

* 可以存储一种或几种类型的像素格式。例如BMP里面存储的是RGB888或者RGBA8888。
* 可以采用有损或者无损的方式进行压缩。一般在文件头定义用于压缩的算法。
* 可以附带打包Exfi信息，例如JPEG、TIFF。



无损压缩格式

* BMP
* PNM（PPM/PGM/PBM）
* PNG



有损压缩格式

* JPEG
* JPEG2000
* GIF



既可以有损压缩又可以无损压缩格式

* TIFF
* DNG



### Exif

可交换图像文件格式（Exchangeable image file format），是专门为数码相机的照片设定的，可以记录数码相机的属性信息和拍摄数据。

Exif可以附加在JPEG、TIFF、RIFF等文件中，为其增加有关数码相机拍摄信息的内容和索引图或图像处理软件的版本信息。

Exif信息以0xFFE1作为开头标记，后两个字节表示为Exif信息的长度。

Exif信息最大为64KB。



常用Exif信息读取软件

* [ExifTool](https://github.com/exiftool/exiftool)



### RAW、TIFF、DNG

RAW文件包含创建一个可视图像所必须的相机传感器数据信息。一般存储Bayer Pattern和拍照时的所有参数。参数以Exif信息嵌入RAW内部。RAW文件包括ISO标准的RAW图像格式ISO 12234-2、TIFF-EP。

一般RAW格式的文件仅仅包含bayer格式的二进制图像数据，不包含Exif信息。



RAW格式没有统一的标准，每个厂商都针对自己的产品需求自定义RAW格式，其中包括3FR（Hasselblad）、DCR、K25、KDC（Kodak）、IIQ（Phase One）、CR2（Canon）、ERF（Epson）、MEF（Mamiya）、MOS（Leaf）、NEF（Nikon）、ORF（Olympus）、PEF（Pentax）、RW2（Panasonic）、ARW、SRF、SR2（Sony），都是基于TIFF格式。

为了统一不同厂商的RAW格式，Adobe开发了一种通用的RAW格式DNG（Digital Negative）。里面使用的tag基本定义在TIFF或TIFF-EP中，在DNG标准中只是定义或建议数据的组织方式、颜色空间的转换等等。手机的RAW文件是以DNG格式存储。



TIFF文件中的三个关键词

* 图像文件头（Image File Header）
* 图像文件目录（Image File Directory）
* 目录项（Directory Entry）

每幅图形都是以8字节的IFH开始的，这个IFH指向第一个IFD，IFD包含图像的各种信息，同时包含一个指向实际图像数据的指针。

一个TIFF/DNG里面可以存储多个指向实际图像的指针。通常用于存储不同分辨率的图像。还有一些RAW会存储一个用于预览的小JPEG图。



常用工具

* libtiff：解析TIFF
* libraw：解码DNG和进行后续处理



## 图像编解码工具

### [FFmpeg](https://ffmpeg.org/)

FFmpeg包含了各种图像以及视频的编解码以及编码转换工具。



