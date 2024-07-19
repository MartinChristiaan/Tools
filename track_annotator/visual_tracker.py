import glob
import os
from multiprocessing import pool

import cv2
import numpy as np
import pandas as pd
from media_manager.core import MediaManager
from skimage.transform import resize
from tqdm import tqdm

basedir = r"/diskstation/v2119/data/20221011_VustCo_tharde/2022101"
videodirs = glob.glob(f"{basedir}*/video/EO_lq/")
annotations_dirs = glob.glob(f"{basedir}*/results/EO_lq/_annotations/")
videodirs.sort()
annotations_dirs.sort()
# print(len(annotations_dir))
print(videodirs)
print(annotations_dirs)
# print(len(videodirs))
out_annotations_folder = "/home/user/data/converted/tharde/"
os.makedirs(out_annotations_folder, exist_ok=True)

items = []
for i, (annotation_dir, videodir) in enumerate(zip(annotations_dirs, videodirs)):
    items.append((i, annotation_dir, videodir))


def process(args):
    i, annotation_dir, videodir = args
    out_annotations = []
    out_annotations_path = os.path.join(out_annotations_folder, f"annotations_{i}.csv")
    annotations = glob.glob(f"{annotation_dir}/*")
    annotations = [x for x in annotations if x.endswith(".csv")]
    annotations.sort()
    annotation_file = annotations[-1]
    videodir.split("/")[-1] + f"{i}"
    mm = MediaManager(videodir, result_dirpath="", video_suffix=".mp4")
    # print(annotation_file)
    annotations_df = pd.read_csv(annotation_file)
    timestamps = np.unique(annotations_df["timestamp"])
    frame_timestamps = mm.timestamps
    fps = 1 / np.median(np.diff(frame_timestamps))
    print(fps)

    for i, timestamp in enumerate(tqdm(timestamps)):
        frame_df = annotations_df[annotations_df["timestamp"] == timestamp]
        frame = mm.get_frame(timestamp)
        frame_index = frame_timestamps.index(timestamp)

        trackers_fwd = []
        trackers_bwd = []

        for j, row in frame_df.iterrows():
            bbox = [int(row[f"bbox_{x}"]) for x in "xywh"]
            detection_dict = {"bbox_" + k: v for k, v in zip("xywh", bbox)}
            detection_dict["timestamp"] = timestamp
            detection_dict["label"] = "object"
            detection_dict["class_index"] = 0
            out_annotations.append(detection_dict)
            for trackerlist in [trackers_fwd, trackers_bwd]:
                try:
                    tracker = cv2.TrackerKCF_create()
                    ret = tracker.init(frame, bbox)
                    trackerlist.append(tracker)
                except Exception as e:
                    print(f"failed {bbox}, {e}")

        for is_bwd, trackerlist in enumerate([trackers_fwd, trackers_bwd]):
            for t_index, delta_t in enumerate(range(60)):
                if is_bwd == 1:
                    delta_t = -delta_t
                new_index = frame_index + delta_t
                if new_index < 0 or new_index >= len(frame_timestamps):
                    break

                timestamp_new = frame_timestamps[new_index]
                frame_next = mm.get_frame(timestamp_new)
                bboxes = []
                # print(timestamp,timestamp_new)

                for tracker in trackerlist:
                    ret, bbox = tracker.update(frame_next)
                    if ret:
                        bboxes.append(bbox)

                if len(bboxes) != len(trackerlist):
                    break

                for bbox in bboxes:
                    detection_dict = {"bbox_" + k: v for k, v in zip("xywh", bbox)}
                    detection_dict["timestamp"] = timestamp_new
                    detection_dict["label"] = "object"
                    detection_dict["class_index"] = 0
                    out_annotations.append(detection_dict)

        df = pd.DataFrame(out_annotations)
        df.sort_values("timestamp")
        df.to_csv(out_annotations_path, index=False)


if __name__ == "__main__":
    with pool.Pool(4) as p:
        p.map(process, items)
    # for x in items:
    # 	process(x)
