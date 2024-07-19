from pathlib import Path

import cv2
import cv2 as cv
import numpy as np

drawing = False  # true if mouse is pressed
mode = False  # if True, draw rectangle. Press 'm' to toggle to curve
ix, iy = -1, -1
radius = 80


# mouse callback function
def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, mode
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)
            else:
                cv.circle(img, (x, y), radius, (255, 0, 0), -1)
                cv.circle(mask, (x, y), radius, (255, 255, 255), -1)

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)
        else:
            cv.circle(img, (x, y), radius, (255, 0, 0), -1)
            cv.circle(mask, (x, y), radius, (255, 255, 255), -1)


# images=  os.listdir('dirty')
#
# for filepath in images:
# cap =  cv2.VideoCapture(f"/home/leeuwenmcv/data/4person_test_video.mp4")

img_dir = r"\mnt\dl-41\data\leeuwenmcv\mantis\cv90\mantis_2023".replace("\\", "/")
img_dir = Path(img_dir)
cameras = list([x for x in img_dir.glob("*") if x.is_dir()])
for camera in cameras:
    img_path = list((camera / "0").glob("*.jpg"))[0]
    out_path = camera.stem + ".png"
    img = cv2.imread(str(img_path))
    orig_shape = img.shape[:2]
    img = cv2.resize(img, (1920, 1080))
    h, w = img.shape[:2]
    mask = np.zeros((h, w, 3), dtype=np.uint8)
    cv.namedWindow("image")
    cv.setMouseCallback("image", draw_circle)
    while 1:
        cv.imshow("image", img)
        k = cv.waitKey(1) & 0xFF
        if k == ord("m"):
            mode = not mode
        elif k == 27:
            break
    mask = cv2.resize(mask, orig_shape[::-1])
    cv2.imwrite(out_path, mask)

# cv.destroyAllWindows()
