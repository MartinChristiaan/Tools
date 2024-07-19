import os
import pickle
from pathlib import Path

import click


class RSYNCER:
    def __init__(self, app) -> None:
        self.source = ""
        self.dest = ""
        self.delete = False
        self.app = app
        self.cache = Path("/tmp/rsync.pkl")
        if self.cache.exists():
            with open(self.cache, "rb") as f:
                d = pickle.load(f)
                self.source = d["source"]
                self.dest = d["dest"]

    def rsync_execute(self):
        print(f"will execute rsync from {self.source} to {self.dest}, ok? [y/n]")
        if click.getchar() == "y":
            if os.path.isdir(self.dest):
                self.dest = str(self.dest) + "/"
            os.system(f"nohup rsync -azP {self.source} {self.dest} > tmp.log &")

    def write_cache(self):
        with open(self.cache, "wb") as f:
            d = {"source": self.source, "dest": self.dest}
            pickle.dump(d, f)

    def rsync_set_source(self):
        self.source = self.app.current_folder
        self.write_cache()

    def rsync_set_dest(self):
        self.dest = self.app.current_folder
        self.write_cache()
