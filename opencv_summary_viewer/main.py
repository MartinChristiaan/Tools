# %%
#
from pathlib import Path


summaries = (
    "/mnt/dl-41/data/leeuwenmcv/general/ablation_tyolo/proposed-20240326/summaries"
)
summaries = Path(summaries).rglob("*.webm")

for summary in summaries:
    print(summary)

# %% Read summaries with opencv and show content to the user
import cv2
import numpy as np

next_video = False
should_exit = False
for summary in summaries:
    if should_exit:
        break
    next_video = False
    while not next_video and not should_exit:
        cap = cv2.VideoCapture(str(summary))
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()

            cv2.imshow("summary", frame)
            k = cv2.waitKey(1)

            if k == ord("n"):
                next_video = True
            if k == ord("q"):
                should_exit = True

cv2.destroyAllWindows()
