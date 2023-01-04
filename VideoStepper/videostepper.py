import sys
import glob
# rda_directory = sys.argv[1]
rda_directory = r"\mnt\pc-11393\data\leeuwenmcv\data\mantis\output__home_user_data_video_12_00.avi_20230104T113333".replace("\\","/")
avi_files = glob.glob(f"{rda_directory}/**/*.avi",recursive=True)
print(avi_files)

#TODO picker from data directories
# video_files = 

import cv2
import numpy as np
arr = np.zeros((20,20),dtype=np.uint8)
cv2.imshow(arr,"x")