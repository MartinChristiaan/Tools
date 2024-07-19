# %%
#
from pathlib import Path
import pickle
import time
import cv2


# summaries = (
#     "/mnt/dl-41/data/leeuwenmcv/general/mantis_mist/multi-frame-adv-mist-aug/summaries"
# )

summaries = (
    "/mnt/dl-41/data/leeuwenmcv/general/ablation_tyolo/proposed-20240326/summaries"
)
summaries = sorted(list(Path(summaries).rglob("*.pkl")))
summaries = [
    x
    for x in summaries
    if "drone-tracking" in x.stem or "drone_detection" in x.stem or "TIE" in x.stem
]
for x in summaries:
    print(x)
# %%
from pathlib import Path

from videosets_ii.videosets_ii import VideosetsII
import pandas as pd

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)
names = list(videosets.to_pandas()["name"])
# mantis = [x for x in names if "mantis" in x]


# %% Read summaries with opencv and show content to the user

next_video = False
should_exit = False

video_idx = 0

label = "false_pos"
# for summary in list(summaries)[::-1]:
while True:
    summary = summaries[video_idx]
    metadata = pickle.load(open(summary, "rb"))
    summary_video = summary.with_suffix(".webm")
    name = f"{metadata['videoset']}_{metadata['camera'].replace('/', '_')}"
    track_ids = metadata["track_ids"]

    if should_exit:
        break
    next_video = False
    while not next_video and not should_exit:
        print("opening video", summary.stem, video_idx)
        cap = cv2.VideoCapture(str(summary_video))
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()
            # print(frame.shape)
            if frame is None:
                next_video = True
                continue

            def mouse_callback(event, x, y, flags, param):
                if event == cv2.EVENT_LBUTTONDOWN:
                    # print("Clicked at coordinates:", x, y)
                    h, w = frame.shape[:2]
                    rows = w // 200
                    x_idx = x // 200
                    y_idx = y // 200
                    idx = x_idx + y_idx * rows
                    print(idx)
                    if idx < len(track_ids):
                        track_id = track_ids[idx]
                        data = dict(
                            videoset=metadata["videoset"],
                            camera=metadata["camera"],
                            track_id=track_id,
                            comment="",
                            label=label,
                        )
                        print(data)
                        interesting_path = Path("interesting_moments.csv")

                        pd.DataFrame([data]).to_csv(
                            interesting_path,
                            header=not interesting_path.exists(),
                            mode="a",
                            index=False,
                        )

            cv2.imshow("summary", frame)
            cv2.setMouseCallback("summary", mouse_callback)
            k = cv2.waitKey(1)

            if k == ord("n"):
                next_video = True
                video_idx += 1
                break
            if k == ord("q"):
                should_exit = True
                break
            time.sleep(1 / 30)

cv2.destroyAllWindows()

# %%
