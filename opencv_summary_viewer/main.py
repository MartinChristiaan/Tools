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
import os
from pathlib import Path
from loguru import logger

from videosets_ii.videosets_ii import VideosetsII
import pandas as pd

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)
names = list(videosets.to_pandas()["name"])
mantis = [x for x in names if "mantis" in x]


# %% Read summaries with opencv and show content to the user


next_video = False
should_exit = False
for summary in summaries:

    videoset_name = [x for x in names if x in str(summary.stem)][0]
    cameras = videosets[videoset_name].cameras
    camera_str = str(summary.stem).replace(videoset_name + "_", "")
    camera = [x for x in cameras if x.replace("/", "_") == camera_str][0]

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # print("Clicked at coordinates:", x, y)
            x_idx = x // 200
            y_idx = y // 200
            idx = x_idx + y_idx * 6
            # track_id = summary.stem
            track_ids = summary.stem.replace(videoset_name, "").replace(camera_str, "")
            print(track_ids)

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
