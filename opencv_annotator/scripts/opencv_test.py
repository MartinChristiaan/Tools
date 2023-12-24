import cv2
import numpy as np

img = np.zeros((2000, 2000, 3), dtype=np.uint8)
cv2.imshow("name", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
