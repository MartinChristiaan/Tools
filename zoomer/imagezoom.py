#%%
import numpy as np
import cv2

# image = cv2.imread('/data/sod_cache/raw/drone-tracking/cam0_video_cam0_video/0/48631.jpg')
array = np.arange(2000)


zoom = 1
x = 200
y = 200

zoommult = 1.1
h,w=  image.shape[:2]

for zoomindex in range(8):
	zoom = zoom * zoommult














