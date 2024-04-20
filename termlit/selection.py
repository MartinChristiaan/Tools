# import os
# from pathlib import Path
# from loguru import logger

# from videosets_ii.videosets_ii import VideosetsII
# from trackertoolbox.detections import Detections
# from trackertoolbox.tracks import Tracks,TrackUpdates
# import pandas as pd

# basedirpath = Path(r"/diskstation")
# videosets = VideosetsII(basedirpath= basedirpath)#basedirpath)


from dataclasses import dataclass
import enum
from pathlib import Path
import pickle
from typing import List
import click

import fnmatch
from loguru import logger


def flatten_list(list_of_lists):
    result = []
    for l in list_of_lists:
        for x in l:
            result.append(x)
    return result


from typing import List


@dataclass
class MenuItem:
    name: str
    _selected: any = None

    @property
    def selected(self):
        return self._selected

    def select(self):
        pass


@dataclass
class MenuItemFloat(MenuItem):
    _selected: float = None

    def select(self):
        self._selected = float(input(f"{self.name} (float) : "))


@dataclass
class MenuItemStr(MenuItem):
    _selected: str = None

    def select(self):
        self._selected = input(f"{self.name} (float) : ")


@dataclass
class MenuItemInt(MenuItem):
    _selected: int = None

    def select(self):
        self._selected = int(input(f"{self.name} (int) : "))


@dataclass
class MenuItemBool(MenuItem):
    _selected: bool = None

    def select(self):
        self._selected = not self.selected


@dataclass
class MenuItemMultiStr(MenuItem):
    options: List = None
    single_value: bool = False

    def select(self):
        print("selecting")
        current_pattern = ""
        while True:
            selected = []
            for sub_pattern in current_pattern.split("+"):
                selected += fnmatch.filter(self.options, f"*{sub_pattern}*")

            click.clear()
            print(",".join(selected))
            print(f"Pattern : {current_pattern}")
            char = click.getchar()
            if char == "\x7f":
                current_pattern = current_pattern[:-1]
            elif char == " ":
                if self.single_value:
                    self._selected = selected[0]
                    return
                else:
                    self._selected = selected
                    return
            else:
                current_pattern += char


class Menu:
    def __init__(
        self, menu_items: List[MenuItem], name: str, cache_dir="/data/menu_cache"
    ) -> None:
        self.menu_items = menu_items
        self.name = name
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        self.cache_file = self.cache_dir / "name.pkl"
        self.load_cache_state()

    def load_cache_state(self):
        if self.cache_file.exists():
            with open(self.cache_file, "rb"):
                state = pickle.load(f)
            for k, v in state.items():
                menu_item = [x for x in self.menu_items if x.name == k]
                for item in menu_item:
                    item._selected = v

    def save_state(self):

        state = {item.name: item.selected for item in self.menu_items}
        with open(self.cache_file, "rb"):
            for k, v in state.items():
                menu_item = [x for x in self.menu_items if x.name == k]
                for item in menu_item:
                    item._selected = v

    def run(self):
        selected_idx = 0
        while True:
            click.clear()
            print(self.name)
            print("")
            for i, item in enumerate(self.menu_items):
                printname = f"{item.name} = {str(item.selected)[:200]}"
                if i == selected_idx:
                    printname = f"> {item.name} {str(item.selected)[:200]}"
                print(printname)
            c = click.getchar()

            if c == "j":
                selected_idx += 1
                if selected_idx >= len(self.menu_items):
                    selected_idx = 0
            if c == "k":
                selected_idx -= 1
                if selected_idx < 0:
                    selected_idx = len(self.menu_items) - 1
            if c == " ":
                self.menu_items[selected_idx].select()

            if c == "\x7f":
                return {x.name: x.selected for x in self.menu_items}
