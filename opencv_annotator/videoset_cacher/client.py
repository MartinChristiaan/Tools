# %%
from loguru import logger
from itertools import product
import shutil
import os
from pathlib import Path
import termlit.selection as ts
import termlit.videosets as tv
from icecream import ic

menu_items = [
    tv.videoset_selector,
    tv.camera_selector,
]
local_diskstation = "/data/local_diskstation"
queue_file = Path("processing_app_queue.csv")

def sync_directory(source:Path,destination:Path,exclude="",include="*"):
    current_files = list(destination.rglob(include))
    current_file_subpaths = [str(f).replace(str(destination),"") for f in current_files]
    for file in source.rglob(include):
        subpath = str(file).replace(str(source),"")
        logger.info(f'syncing {subpath}')
        if subpath in current_file_subpaths:
            continue
        else:
            file_dest = destination/subpath
            file_dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy(file,file_dest)

def main():

    import click

    items = tv.Menu(menu_items, "processing_app").run(True)
    for item in items:
        mm = tv.videosets[item["videoset"]].get_mediamanager(item["camera"])
        for p in [mm.filepath, mm.result_dirpath]:
            p = str(p)
            # newp = "/".join(p.split("/")[2:])
            newp = "\\".join(p.split("\\")[2:])
            dest = local_diskstation + newp
            sync_directory(Path(p),Path(dest))
            

if __name__ == "__main__":
    main()