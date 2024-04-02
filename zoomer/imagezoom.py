# %%
import numpy as np
import cv2


import cv2
import numpy as np


def mouse_callback(event, x, y, flags, param):
    global zoom_factor
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags < 0:
            zoom_factor += 0.1
        else:
            zoom_factor -= 0.1
        if zoom_factor < 0.1:
            zoom_factor = 0.1

    if event == cv2.EVENT_MOUSEMOVE:
        global img
        h, w = img.shape[:2]
        x = int(x / zoom_factor)
        y = int(y / zoom_factor)
        start_x = max(x - w // 2, 0)
        start_y = max(y - h // 2, 0)
        end_x = min(start_x + w, img.shape[1])
        end_y = min(start_y + h, img.shape[0])
        resized_img = img[start_y:end_y, start_x:end_x]
        cv2.imshow("Zoomed Image", resized_img)


zoom_factor = 1.0

img = cv2.imread("/data/sod_cache/raw/drone-tracking/cam0_video_cam0_video/0/48631.jpg")

cv2.namedWindow("Zoomed Image")
cv2.setMouseCallback("Zoomed Image", mouse_callback)

cv2.imshow("Zoomed Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
