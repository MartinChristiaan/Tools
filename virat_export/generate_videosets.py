import argparse
import glob
import os
import shutil
from dataclasses import dataclass

##
# ouptut = logfile videos
from datetime import datetime
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import yaml
from videosets_ii.videosets_ii import VideosetII


@dataclass
class VideoInfo:
    path: str = ""
    annotations: str = ""
    camera: str = ""
    quality: str = ""


def find_video_file_extensions(directory):
    video_extensions = [
        ".mp4",
        ".avi",
        ".mkv",
        ".mov",
        ".wmv",
        ".flv",
        ".tiff",
        ".tif",
        ".jpg",
    ]
    video_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            _, extension = os.path.splitext(file)
            if extension.lower() in video_extensions:
                video_files.append(extension)

    return list(set(video_files))


import datetime
import os


def find_appropriate_timestamp_col(video_dir, annotations):
    # t0_tracks = tracks[0].timestamp[0]
    t0_annotations = pd.read_csv(annotations)["timestamp"].min()
    # print(t0_tracks)
    best_log_col = 0
    min_dist = 1e20
    logfile = [x for x in glob.glob(f"{video_dir}/*") if x.endswith(".log")][0]
    with open(logfile, "r") as f:
        text = f.read().split("\n")[1]
        columns = [(i, x) for i, x in enumerate(text.split(" ")) if len(x) > 0]
        for i, x in columns:
            try:
                value = float(x)
            except:
                continue
            delta = abs(value - t0_annotations)
            # print(value,delta,i)
            if delta < min_dist:
                min_dist = delta
                best_log_col = i

    return best_log_col


# Specify the path to the file you want to check
def get_last_modified(file_path):
    timestamp = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(timestamp)


def get_annotations_filename(file_path):
    return "annotations_" + get_last_modified(file_path).strftime("%Y%m%dT%H%M%S")


def create_videoset_files(videoset_name, videos: List[VideoInfo]):
    dataset_path = Path(f"/diskstation/datasets/{videoset_name}/")
    if dataset_path.exists():
        # raise Exception(f"{dataset_path} already exists")
        print(f"{dataset_path} already exists")
        # if input('contine y/n : ') == 'n':
        # 	sys.exit()

    for v in videos:
        vpath = dataset_path / f"video/{v.camera}/{v.quality}/"
        vpath.mkdir(parents=True, exist_ok=True)
        os.system(f"rsync -azP {v.path} {vpath}")
        annotations_filename = get_annotations_filename(v.annotations)
        annotations_path = (
            dataset_path
            / f"results/{v.camera}/{v.quality}/_annotations/{annotations_filename}.csv"
        )
        annotations_path.parent.mkdir(exist_ok=True, parents=True)
        shutil.copy(v.annotations, annotations_path)


def get_suffix(videoset_name):
    dataset_path = Path(f"/diskstation/datasets/{videoset_name}/")
    return find_video_file_extensions(dataset_path)[0]


def generate_yaml_file(videoset_name, videos: List[VideoInfo], dataset):
    cams = list(set([v.camera for v in videos if v.camera != ""]))
    cams.sort()
    qs = list(set([v.quality for v in videos if v.quality != ""]))
    qs.sort()
    obj = VideosetII(
        "\\diskstationii1",
        "",
        videoset_name,
        f"datasets/{videoset_name}",
        cams,
        qualities=qs,
        video_suffix=get_suffix(videoset_name),
        log_column=find_appropriate_timestamp_col(
            videos[0].path, videos[0].annotations
        ),
        objects=dataset["objects"],
        contact=dataset["contact"],
    )

    with open(f"../datasets/{type}/{videoset_name}.yml", "w") as yaml_file:
        d = obj.__dict__
        out_d = {}
        for k, v in d.items():
            if not isinstance(v, list) or not len(v) == 0:
                out_d[k] = v
        yaml.dump(out_d, yaml_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Video Config Generator",
        description="What the program does",
        epilog="Text at the bottom of help",
    )
    parser.add_argument("--config", type=str, default="configs/datasets.yaml")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    import yaml

    with open(args.config) as f:
        ymldata = yaml.load(f, yaml.SafeLoader)
    for name, data in ymldata.items():
        video_infos = []
        for d in data["videoInfos"]:
            if "*" in d["path"]:
                paths = glob.glob(d["path"])
                paths.sort()
                annotations = glob.glob(d["annotations"])
                annotations.sort()
                print(annotations)
                print(paths)
                paths = paths[: len(annotations)]
                # assert len(paths) == len(annotations)
                cameras = [""] * len(annotations)
                qualities = [""] * len(annotations)
                if "camera" in d:
                    cameras = [Path(x).parts[d["camera"]] for x in paths]

                if "quality" in d:
                    qualities = [Path(x).parts[d["quality"]] for x in paths]

                for x in zip(paths, annotations, cameras, qualities):
                    video_infos.append(VideoInfo(*x))
            else:
                video_infos.append(**d)
        create_videoset_files(name, video_infos)
        generate_yaml_file(name, video_infos, data["type"])
