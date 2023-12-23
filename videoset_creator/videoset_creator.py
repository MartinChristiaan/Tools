import os
from pathlib import Path

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


def generate_videoset(input_path: Path, datasetdir: Path):
    input_videos = input_path.glob("*")
    for vid in input_videos:
        cmd = f'scenedetect -i "{vid}" split-video -o scenes'
        os.system(cmd)

    # datasetdir = Path("/diskstation/datasets/webcams_2023")
    videodir = datasetdir / "video"
    resultsdir = datasetdir / "results"
    videos = Path("scenes").glob("*.mp4")
    # from generate_videosets import get_annotations_filename

    for v in videos:
        camera_video_dir = videodir / v.stem
        camera_video_dir.mkdir(exist_ok=True, parents=True)
        resultsdir / v.stem

        timestamps_string = generate_timestamps(v)
        with open(camera_video_dir / (v.stem + ".log"), "w") as f:
            f.write(timestamps_string)
        os.system(f'rsync -azP "{v}" "{camera_video_dir/v.name}"')
