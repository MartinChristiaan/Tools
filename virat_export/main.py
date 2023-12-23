# for video in videos
import os
from pathlib import Path

import pandas as pd

sourcedir = Path(
    r"\mnt\dl-41\data\leeuwenmcv\mantis\VIRAT Ground Dataset".replace("\\", "/")
)
videos = (sourcedir / "videos_original").rglob("*")
import cv2


def generate_timestamps(videofile):
    # Open the video file
    cap = cv2.VideoCapture(str(videofile))
    if not cap.isOpened():
        return "Error: Unable to open video file"
    # Get frames per second (fps) of the video
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Get total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the timestamps
    timestamps = ""
    for frame_number in range(total_frames):
        # Calculate the timestamp in seconds
        timestamp = frame_number / fps
        timestamps += (
            f"{timestamp:.3f}\n"  # Format timestamp as a float with 3 decimal places
        )

    # Release the video capture object
    cap.release()

    return timestamps


# Example usage:

datasetdir = Path("/diskstation/datasets/virat-external")
videodir = datasetdir / "video"
resultsdir = datasetdir / "results"


def parse_annotations(text, timestamps, csv_path):
    lines = text.split("\n")
    detections = []
    for line in lines:
        if len(line.split(" ")) < 7:
            continue
        track_id, _, frame_id, x, y, w, h, class_id = line.split(" ")
        data_dict = {
            "timestamp": timestamps[int(frame_id)],
            "bbox_x": int(x),
            "bbox_y": int(y),
            "bbox_w": int(w),
            "bbox_h": int(h),
            "class_id": int(class_id),
            "track_id": int(track_id),
        }
        detections.append(data_dict)
    return pd.DataFrame(detections).to_csv(csv_path, index=False)


from generate_videosets import get_annotations_filename

for v in videos:
    camera_video_dir = videodir / v.stem
    camera_video_dir.mkdir(exist_ok=True, parents=True)
    camera_results_dir = resultsdir / v.stem

    timestamps_string = generate_timestamps(v)
    with open(camera_video_dir / (v.stem + ".log"), "w") as f:
        f.write(timestamps_string)

    camera_annotations_dir = camera_results_dir / "_annotations"
    camera_annotations_dir.mkdir(exist_ok=True, parents=True)
    annotations = sourcedir / f"annotations/{v.stem}.viratdata.objects.txt"
    try:
        with open(annotations, "r") as f:
            text = f.read()
        annot_filename = camera_annotations_dir / (
            get_annotations_filename(annotations) + ".csv"
        )
        os.system(f'rsync -azP "{v}" {camera_video_dir/v.name}')
        parse_annotations(text, timestamps_string.split("\n"), annot_filename)
    except:
        pass
