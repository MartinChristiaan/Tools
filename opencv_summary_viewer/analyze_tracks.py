# %%
from collections import defaultdict
from pathlib import Path

from videosets_ii.videosets_ii import VideosetsII
import pandas as pd
from functools import lru_cache

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)
classifications = pd.read_csv("classifications.csv")


# %%
@lru_cache
def get_tracks(videoset, camera):
    mm = videosets[videoset].get_mediamanager(camera)
    df = mm.load("tyolov8/tracks_proposed-20240326.csv")
    return df


tracks_per_label = defaultdict(list)


for i, row in classifications.iterrows():
    videoset = row["videoset"]
    camera = row["camera"]

    tracks = get_tracks(videoset, camera)
    track = tracks[tracks["track_id"] == row["track_id"]]
    tracks_per_label[row["label"]].append(track)

# %%
