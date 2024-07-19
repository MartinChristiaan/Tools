import glob
import os
import sys

import click
import pyfzf
from guitoolbox.app import MainGUI, SyncMode
from media_manager.core import MediaManager
from pyfzf.pyfzf import FzfPrompt
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks

path = sys.argv[1]
# path = "/home/leeuwenmcv/data/vlucht"
# find video directories
# find suffix
import os


def find_leaf_directories_with_substring(path, substring):
    leaf_directories = []

    if os.path.isdir(path):
        print(path)
        # Check if the current directory contains the substring
        if substring in path:
            # Check if the directory has any subdirectories
            has_subdirectories = False
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    has_subdirectories = True
                    break

            # If the directory doesn't have any subdirectories, add it to the leaf_directories list
            if not has_subdirectories:
                leaf_directories.append(path)

        # Recursively explore subdirectories
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                leaf_directories.extend(
                    find_leaf_directories_with_substring(item_path, substring)
                )

    return leaf_directories


# Open the file and load the file


def find_video_file_extensions(directory):
    video_extensions = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".tiff"]
    video_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            _, extension = os.path.splitext(file)
            if extension.lower() in video_extensions:
                video_files.append(extension)

    return list(set(video_files))


def find_files_with_string(folder_path, substring):
    matching_files = []
    for root, dirs, files in os.walk(folder_path):
        print(root, dirs, files)
        for file in files:
            if file.endswith(".csv") and substring in file:
                file_path = os.path.join(root, file)
                matching_files.append(file_path)

    return matching_files


import pandas as pd


def find_appropriate_timestamp_col(videodir, tracks):
    t0_tracks = tracks[0].timestamp[0]
    print(t0_tracks)
    best_log_col = 0
    min_dist = 1e20
    logfile = [x for x in glob.glob(f"{video_dir}/*") if x.endswith(".log")][0]
    with open(logfile, "r") as f:
        text = f.read().split("\n")[1]
        columns = [x for x in text.split(" ") if len(x) > 0]
        for i, x in enumerate(columns):
            value = float(x)
            delta = abs(value - t0_tracks)
            # print(value,delta,i)
            if delta < min_dist:
                min_dist = delta
                best_log_col = i
    return best_log_col


video_dirs = find_leaf_directories_with_substring(path, substring="video")
fzf = FzfPrompt()
print(len(video_dirs), "video dirs")
video_dir = video_dirs[0]
if len(video_dirs) > 1:
    video_dir = fzf.prompt(video_dirs)[0]
file_ext = find_video_file_extensions(video_dir)[0]
track_files = find_files_with_string(path, "track")
print(len(track_files), "track files")


fzf = FzfPrompt()
track_file = track_files[0]
if len(track_files) > 1:
    track_file = fzf.prompt(track_files)[0]
# print(track_files)
print(f"loading tracks {track_file}")

tracks = Tracks.load(track_file)
print(tracks)
log_col = find_appropriate_timestamp_col(video_dir, tracks)
print(f"using log col {log_col}")
mm = MediaManager(video_dir, video_suffix=file_ext, log_column_to_use=log_col)
print(mm.timestamps)


gui = MainGUI(
    videos=[mm],
    tracks=[tracks],
    sync_mode=SyncMode.ALL,
)
