# %%
from math import inf

import cv2
from opencv_annotator.annotation import Annotation
from annotator import BoundingBoxAnnotator, ReturnMode
from media_manager.core import MediaManager
from trackertoolbox.detections import Detections

# import dlutils_ii as du

# pf = du.Pathfinder("mantis_drone_2023", "DJI_202309100220_001/wide_hd")
# print(pf.media_manager.result_dirpath)
# print(pf.media_manager.filepath)
mm = MediaManager(
    "/diskstation/mantis/Security/20230910_drone_recording/videosets/video/DJI_202309100220_001/wide_hd",
    result_dirpath="/diskstation/mantis/Security/20230910_drone_recording/videosets/results/DJI_202309100220_001/wide_hd",
    video_suffix=".mp4",
)
tracks = mm.load("tyolov8/tracks_tyolov8m-30112023.csv")
# %%


def get_sparse_annotations(annotations, dt=1):
    t_prev = -inf
    sparse_timestamps = []
    for t in annotations.timestamp.unique():
        if t > t_prev + dt:
            sparse_timestamps.append(t)
            t_prev = t
    return annotations[annotations.timestamp.isin(sparse_timestamps)]


sparse_tracks = get_sparse_annotations(tracks)
if not "label" in sparse_tracks:
    sparse_tracks["label"] = ["object"] * len(sparse_tracks)

j = 0
items = list(sparse_tracks.groupby("timestamp"))
# for  in item:
while True:
    timestamp, detections = items[j]
    detections = detections.sort_values(["bbox_y", "bbox_x"])
    detections = Annotation.from_pandas(detections)
    frame = cv2.cvtColor(mm.get_frame_nearest(timestamp)[0], cv2.COLOR_RGB2BGR)
    result = BoundingBoxAnnotator(frame, detections).run()
    if result == ReturnMode.NEXT:
        j += 1
    elif result == ReturnMode.PREV:
        j -= 1
    elif result == ReturnMode.STOP:
        break
