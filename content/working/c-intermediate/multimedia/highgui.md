---
domain: multimedia
legacy_first_commit_at: '2025-07-06T20:30:14+08:00'
legacy_path: docs/computer-science/applied-computer-science/multimedia/camera/software/opencv/highgui.md
snapshot_sha256: sha256:194d0e1fe528d442e58be7cb88393b493441e0d22e854404f3fdde4dce69cee9
title: highgui
---
# highgui

## interface

HighGUI（High-level GUI）是 OpenCV 的高层用户界面与媒体输入输出模块，提供跨平台的窗口显示、鼠标/键盘事件、图像与视频读写接口。它屏蔽了底层平台差异（Windows/Linux/macOS），让开发者用几行代码就能完成"读图 → 处理 → 显示"的闭环，常用于算法调试、Demo 演示与原型验证。

核心接口：

- `imread(filename)` / `imwrite(filename, img)`：读取/保存图像
- `namedWindow(name)` / `imshow(name, img)` / `destroyWindow(name)`：创建窗口并显示
- `waitKey(delay)`：等待按键（配合 imshow 刷新窗口，delay≤0 表示一直等待）
- `setMouseCallback(window, callback)`：鼠标事件回调
- `VideoCapture` / `VideoWriter`：视频与相机捕获/写入
- `createTrackbar`：创建滑块用于参数实时调节（调参利器）

## application

### image

图像读写与显示是 HighGUI 最常用的功能：

读取图像

- `cv::Mat img = cv::imread("lena.jpg");` 读入图像为 BGR 的 Mat；路径错误时返回空 Mat，需用 `img.empty()` 判断。

显示图像

- `cv::namedWindow("win", cv::WINDOW_AUTOSIZE); cv::imshow("win", img); cv::waitKey(0);` 显示并等待按键；`WINDOW_NORMAL` 允许缩放窗口。

保存图像

- `cv::imwrite("out.png", img);` 按扩展名选择编码（PNG 无损、JPEG 有损、BMP 等）。

### video

HighGUI 的 VideoCapture/VideoWriter 负责视频输入输出：

从相机录制视频

- `cv::VideoCapture cap(0);` 打开默认相机（0 为第一个摄像头）；`cap.read(frame)` 逐帧读取；可设置 `CAP_PROP_FRAME_WIDTH/HEIGHT/FPS` 等属性。

播放视频

- `cv::VideoCapture cap("video.mp4");` 打开视频文件，逐帧 `cap.read` + `imshow` + `waitKey(30)`（按帧率延时）播放；`cap.get(CAP_PROP_POS_FRAMES)` 定位。

保存视频

- `cv::VideoWriter writer("out.mp4", cv::VideoWriter::fourcc('M','P','4','V'), fps, size);` 指定编码器/帧率/尺寸；`writer.write(frame)` 逐帧写入，结束后 `release()`。

### drawing

HighGUI 依赖 imgproc 的绘图函数在图像上叠加标注（调试/可视化常用）：

- 线段：`cv::line(img, pt1, pt2, color, thickness)`
- 矩形：`cv::rectangle(img, rect, color, thickness)`
- 圆：`cv::circle(img, center, radius, color, thickness)`
- 椭圆：`cv::ellipse(img, center, axes, angle, startAngle, endAngle, color, thickness)`
- 多边形：`cv::polylines(img, pts, isClosed, color, thickness)`
- 文字：`cv::putText(img, text, org, fontFace, fontScale, color, thickness)`

## 参考

- OpenCV HighGUI 官方文档：https://docs.opencv.org/4.x/d7/dfc/group__highgui.html
- OpenCV 图像/视频读写：https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html
