# Start a OpenCL project on Visual Studio using Nvidia GPU

## cuda

下载地址：https://developer.nvidia.com/cuda-downloads



## Visual Studio配置

项目->属性

配置属性->C/C++->常规->附加包含目录

`C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\include`

配置属性->链接器->常规->附加包含目录

x86：`C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\lib\Win32`

x64：`C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\lib\x64`

配置属性->链接器->输入->附加依赖项

`OpenCL.lib`





