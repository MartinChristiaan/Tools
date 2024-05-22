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
    print(source,destination)
    current_files = list(destination.rglob(include))
    current_file_subpaths = [str(f).replace(str(destination),"") for f in current_files]
    for file in source.rglob(include):
        subpath = str(file).replace(str(source),"")
        logger.info(f'syncing {subpath}')

        if subpath in current_file_subpaths or file.is_dir():
            continue
        else:
            file_dest = f'{destination}\\{subpath}'
            Path(file_dest).parent.mkdir(parents=True,exist_ok=True)
            print(destination,file_dest,subpath)
            shutil.copy(file,file_dest)

def main():

    import click

    items = tv.Menu(menu_items, "processing_app").run(True)
    for item in items:
        mm = tv.videosets[item["videoset"]].get_mediamanager(item["camera"])
        for p in [mm.filepath, mm.result_dirpath]:
            p = str(p)
            if os.name == 'nt':
                newp = "\\".join(p.split("\\")[2:])
            else:
                newp = "/".join(p.split("/")[2:])
            dest = local_diskstation + newp
            sync_directory(Path(p),Path(dest))
            

if __name__ == "__main__":
    main()