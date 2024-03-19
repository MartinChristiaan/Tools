# %%
from pathlib import Path
import os
from loguru import logger

from videosets_ii.videosets_ii import VideosetsII

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)
names = list(videosets.to_pandas()["name"])
for name in names:
    print(name)
    vpath = Path(f"/configs/{name}")
    vpath.mkdir(exist_ok=True, parents=True)
    for camera in videosets[name].cameras:
        out_file = vpath / f"{camera}___{name}"
        os.system("touch {out_file}")
