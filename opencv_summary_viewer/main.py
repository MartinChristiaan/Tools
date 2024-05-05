# %%
#
from math import pi
from pathlib import Path
import pickle
import time
import cv2
import numpy as np


summaries = (
    "/mnt/dl-41/data/leeuwenmcv/general/ablation_tyolo/proposed-20240326/summaries"
)
summaries = Path(summaries).rglob("*.pkl")
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


for summary in list(summaries)[::-1]:
    metadata = pickle.load(open(summary, "rb"))
    summary_video = summary.with_suffix(".webm")
    name = f"{metadata['videoset']}_{metadata['camera'].replace('/', '_')}"
    track_ids = summary.stem.replace(name, "")[1:].split("_")

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # print("Clicked at coordinates:", x, y)
            x_idx = x // 200
            y_idx = y // 200
            idx = x_idx + y_idx * 6
            if idx < len(track_ids):
                track_id = track_ids[idx]
                data = dict(
                    videoset=metadata["videoset"],
                    camera=metadata["camera"],
                    track_id=track_id,
                    comment="",
                )
                print(data)
                interesting_path = Path("interesting_moments.csv")

                pd.DataFrame([data]).to_csv(
                    interesting_path,
                    header=not interesting_path.exists(),
                    mode="a",
                    index=False,
                )

    if should_exit:
        break
    next_video = False
    while not next_video and not should_exit:
        print("opening video", summary.stem)
        cap = cv2.VideoCapture(str(summary_video))
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
