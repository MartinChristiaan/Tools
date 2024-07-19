import argparse
from pathlib import Path
from click import option
from fzf_utils import prompt
import yaml
import os


import argparse

parser = argparse.ArgumentParser(prog="namefinder", description="Description")
parser.add_argument("-m", "--mode", type=str, default="videoset")
args = parser.parse_known_args()[0]


home = os.path.expanduser("~")
videosets_path = Path(f"{home}/git/videosets_ii")
yaml_files = videosets_path.rglob("*.yml")
options = []
yml_data = {}

for yaml_file in yaml_files:
    if "git" in yaml_file.stem or "docker" in yaml_file.stem:
        continue
    # print(yaml_file)
    with open(yaml_file) as f:
        data = yaml.safe_load(f)
    if args.mode == "videoset":
        options.append(data["name"])
    if (args.mode == "camera" or args.mode == "detections") and "cameras" in data:
        for camera in data["cameras"]:
            repr_str = data["name"] + " : " + camera
            options.append(repr_str)
            yml_data[repr_str] = data

if args.mode == "videoset":
    print(prompt(options))
if args.mode == "camera":
    result = prompt(options).split(" : ")
    print(result[0])
    print(result[1])
if args.mode == "detections":
    result = prompt(options)
    camera = result.split(" : ")[-1]
    data = yml_data[result]
    path = Path("/diskstation") / data["relative_path"] / "results" / camera
    detections = path.rglob("*.csv")
    result = prompt([str(detection) for detection in detections])
    print(result)
