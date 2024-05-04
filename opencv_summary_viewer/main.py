# %%
#
from pathlib import Path
import time
import cv2
import numpy as np


summaries = (
    "/mnt/dl-41/data/leeuwenmcv/general/ablation_tyolo/proposed-20240326/summaries"
)
summaries = Path(summaries).rglob("*.webm")

# %% Read summaries with opencv and show content to the user


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Clicked at coordinates:", x, y)


next_video = False
should_exit = False
for summary in summaries:
    if should_exit:
        break
    next_video = False
    while not next_video and not should_exit:
        print("opening video", summary)
        cap = cv2.VideoCapture(str(summary))
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()

            cv2.imshow("summary", frame)
            cv2.setMouseCallback("summary", mouse_callback)
            k = cv2.waitKey(1)

            if k == ord("n"):
                next_video = True
                break
            if k == ord("q"):
                should_exit = True
                break
            time.sleep(1 / 30)

cv2.destroyAllWindows()
