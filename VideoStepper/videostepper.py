import glob
import os

import click
import cv2
import pandas as pd
from media_manager.core import MediaManager
from media_manager.media_readers import CSVReader, VideoReader2, VideoReaderMJPG

# rda_directory = sys.argv[1]
path = "/mnt/toren/data/leeuwenmcv/mantis/pipeline/badplanner3"
rda_directory = path
avi_files = glob.glob(f"{rda_directory}/**/*.avi", recursive=True)
log_files = [x.replace(".avi", ".log") for x in avi_files]
print(log_files)
for log_file in log_files:
    with open(log_file, "r") as f:
        text = f.read().split("\n")
    out_text = ""
    for line in text:
        items = line.split(" ")
        if len(items) > 1 and items[-2] == "0":
            out_text += line + "\n"
    with open(log_file, "w") as f:
        f.write(out_text)

        # print(text)


csv_files = glob.glob(f"{rda_directory}/**/*.csv", recursive=True)


mm = MediaManager(
    f"{rda_directory}/video/EO_overview_temporal",
    result_dirpath=f"{rda_directory}/results/",
    video_suffix=".avi",
    log_column_to_use=1,
    videoreader=VideoReader2(),
)
dfs = []
for csv_file in csv_files:
    # readers.append(CSVReader(csv_file))
    df = pd.read_csv(csv_file)
    # print(df['timestamp'])
    dfs.append(df)

idx = 100
while True:
    timestamp = mm.timestamps[idx]
    frame = mm.get_frame(timestamp)
    os.system("cls")
    for df in dfs:
        print(df[df["timestamp"] == timestamp].to_markdown())

    cv2.imshow("frame", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    key = cv2.waitKey(0)
    if key == ord("q"):
        break
    elif key == ord("j"):
        idx -= 1
    elif key == ord("k"):
        idx += 1
# log_files = glob.glob(f"{rda_directory}/**/*.log",recursive=True)

cv2.destroyAllWindows()
