---
archive_policy: text-only
attachments:
- filename: web-multimedia-highgui.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:7e3eb0631240c15568b04777635dadd550460b6f8f0b7ee28dd6f9313377383f
confidentiality: public
domain: multimedia
evidence_items:
- evidence_id: evidence-842d5b04eeae
  position:
    end: 319
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:a907548b6ade9900c3c03f8e267f4619db91322941cd3cf2863d026f4a9a579d
  selector:
    exact: While OpenCV was designed for use in full-scale applications and can be
      used within functionally rich UI frameworks (such as Qt*, WinForms*, or Cocoa*)
      or without any UI at all, sometimes there it is required to try functionality
      quickly and visualize the results. This is what the HighGUI module has been
      designed for.
    prefix: ''
    suffix: "\n      \n \n#include <opencv2/high"
    type: TextQuoteSelector
  selector_sha256: sha256:780c98deed2a67b3099982408dea19a8b3628e702e4a5691af639dabcdd3103b
  snapshot_sha256: sha256:593c75d03c74d764b8f6860ed54be10cf86b0d0fdcb998c78ed18a11b89cbd0c
extractor: trafilatura/2.2.0
id: web-multimedia-highgui
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/7e3eb0631240c15568b04777635dadd550460b6f8f0b7ee28dd6f9313377383f.html
  sha256: sha256:7e3eb0631240c15568b04777635dadd550460b6f8f0b7ee28dd6f9313377383f
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://docs.opencv.org/4.13.0/d7/dfc/group__highgui.html
  url: https://docs.opencv.org/4.x/d7/dfc/group__highgui.html
schema_version: source/v1
snapshot_sha256: sha256:593c75d03c74d764b8f6860ed54be10cf86b0d0fdcb998c78ed18a11b89cbd0c
source_type: doc
vault_id: public
---
While OpenCV was designed for use in full-scale applications and can be used within functionally rich UI frameworks (such as Qt*, WinForms*, or Cocoa*) or without any UI at all, sometimes there it is required to try functionality quickly and visualize the results. This is what the HighGUI module has been designed for.
      
 
#include <opencv2/highgui.hpp>
Creates a trackbar and attaches it to the specified window. 
The function createTrackbar creates a trackbar (a slider or range control) with the specified name and range, assigns a variable value to be a position synchronized with the trackbar and specifies the callback function onChange to be called on the trackbar position change. The created trackbar is displayed in the specified window winname.
- Note
- [Qt Backend Only] winname can be empty if the trackbar should be attached to the control panel.
Clicking the label of each trackbar enables editing the trackbar values manually.
- Parameters
- 
  
  
- Note
- If the value pointer isnullptr , the trackbar position must be manually managed. Call the callback function manually with the desired initial value to avoid runtime warnings.
- See also
- Adding a Trackbar to our applications! 
 
 
      
 
#include <opencv2/highgui.hpp>
Gets the mouse-wheel motion delta, when handling mouse-wheel events cv::EVENT_MOUSEWHEEL and cv::EVENT_MOUSEHWHEEL. 
For regular mice with a scroll-wheel, delta will be a multiple of 120. The value 120 corresponds to a one notch rotation of the wheel or the threshold for action to be taken and one such action should occur for each delta. Some high-precision mice with higher-resolution freely-rotating wheels may generate smaller values.
For cv::EVENT_MOUSEWHEEL positive and negative values mean forward and backward scrolling, respectively. For cv::EVENT_MOUSEHWHEEL, where available, positive and negative values mean right and left scrolling, respectively.
- Note
- Mouse-wheel events are currently supported only on Windows and Cocoa.
- Parameters
- 
  
  
 
 
      
 
#include <opencv2/highgui.hpp>
Displays an image in the specified window. 
The function imshow displays an image in the specified window. If the window was created with the cv::WINDOW_AUTOSIZE flag, the image is shown with its original size, however it is still limited by the screen resolution. Otherwise, the image is scaled to fit the window. The function may scale the image, depending on its depth:
- If the image is 8-bit unsigned, it is displayed as is.
- If the image is 16-bit unsigned, the pixels are divided by 256. That is, the value range [0,255*256] is mapped to [0,255].
- If the image is 32-bit or 64-bit floating-point, the pixel values are multiplied by 255. That is, the value range [0,1] is mapped to [0,255].
- 32-bit integer images are not processed anymore due to ambiguouty of required transform. Convert to 8-bit unsigned matrix using a custom preprocessing specific to image's context.
If window was created with OpenGL support, cv::imshow also support ogl::Buffer , ogl::Texture2D and cuda::GpuMat as input.
If the window was not created before this function, it is assumed creating a window with cv::WINDOW_AUTOSIZE.
If you need to show an image that is bigger than the screen resolution, you will need to call namedWindow("", WINDOW_NORMAL) before the imshow.
- Note
- This function should be followed by a call to cv::waitKey or cv::pollKey to perform GUI housekeeping tasks that are necessary to actually show the given image and make the window respond to mouse and keyboard events. Otherwise, it won't display the image and the window might lock up. For example, waitKey(0) will display the window infinitely until any keypress (it is suitable for image display). waitKey(25) will display a frame and wait approximately 25 ms for a key press (suitable for displaying a video frame-by-frame). To remove the window, use cv::destroyWindow.
- 
[Windows Backend Only] Pressing Ctrl+C will copy the image to the clipboard. Pressing Ctrl+S will show a dialog to save the image. 
- 
[Wayland Backend Only] Supoorting format is extended.
  - If the image is 8-bit signed, the pixels are biased by 128. That is, the value range [-128,127] is mapped to [0,255].
  - If the image is 16-bit signed, the pixels are divided by 256 and biased by 128. That is, the value range [-32768,32767] is mapped to [0,255].
- Parameters
- 
  
  
 
 
      
 
#include <opencv2/highgui.hpp>
Creates a window. 
The function namedWindow creates a window that can be used as a placeholder for images and trackbars. Created windows are referred to by their names.
If a window with the same name already exists, the function does nothing.
You can call cv::destroyWindow or cv::destroyAllWindows to close the window and de-allocate any associated memory usage. For a simple program, you do not really have to call these functions because all the resources and windows of the application are closed automatically by the operating system upon exit.
- Note
- Qt backend supports additional flags:
  - WINDOW_NORMAL or WINDOW_AUTOSIZE: WINDOW_NORMAL enables you to resize the window, whereas WINDOW_AUTOSIZE adjusts automatically the window size to fit the displayed image (see imshow ), and you cannot change the window size manually.
  - WINDOW_FREERATIO or WINDOW_KEEPRATIO: WINDOW_FREERATIO adjusts the image with no respect to its ratio, whereas WINDOW_KEEPRATIO keeps the image ratio.
  - WINDOW_GUI_NORMAL or WINDOW_GUI_EXPANDED: WINDOW_GUI_NORMAL is the old way to draw the window without statusbar and toolbar, whereas WINDOW_GUI_EXPANDED is a new enhanced GUI. By default, flags == WINDOW_AUTOSIZE | WINDOW_KEEPRATIO | WINDOW_GUI_EXPANDED
- Parameters
- 
  
  
 
 
      
 
#include <opencv2/highgui.hpp>
Waits for a pressed key. 
The function waitKey waits for a key event infinitely (when \(\texttt{delay}\leq 0\) ) or for delay milliseconds, when it is positive. Since the OS has a minimum time between switching threads, the function will not wait exactly delay ms, it will wait at least delay ms, depending on what else is running on your computer at that time. It returns the code of the pressed key or -1 if no key was pressed before the specified time had elapsed. To check for a key press but not wait for it, use pollKey.
- Note
- The functions waitKey and pollKey are the only methods in HighGUI that can fetch and handle GUI events, so one of them needs to be called periodically for normal event processing unless HighGUI is used within an environment that takes care of event processing.
- 
The function only works if there is at least one HighGUI window created and the window is active. If there are several HighGUI windows, any of them can be active.
- Parameters
-