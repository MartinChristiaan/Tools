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


@dataclass
class MenuItem:
    name: str
    options: List
    selected: List = None
    single_value: bool = False

    def select(self):
        if self.options is None:
            if type(self.selected) == bool:
                self.selected = not self.selected
                return self.selected
            if type(self.selected) == float:
                self.selected = float(input("enter your input : "))
        if len(self.options) == 0:
            logger.warning(f"no options available for {self.name}")
            return None
        return self.select_stringlist()

    def select_stringlist(self):
        current_pattern = ""
        while True:
            selected = []
            for sub_pattern in current_pattern.split("+"):
                selected += fnmatch.filter(self.options, f"*{sub_pattern}*")
            # if len(selected) == 0:
            #     current_pattern = ""
            #     continue

            click.clear()
            print(",".join(selected))
            print(f"Pattern : {current_pattern}")
            char = click.getchar()
            if char == "\x7f":
                current_pattern = current_pattern[:-1]
            elif char == " ":
                if self.single_value:
                    self.selected = selected[0]
                    return selected[0]
                else:
                    self.selected = selected
                    return selected
            else:
                current_pattern += char


def menu(menu_items: List[MenuItem], name: str):

    selected_idx = 0
    while True:
        click.clear()
        print(name)
        print("")
        for i, item in enumerate(menu_items):
            printname = f"{item.name} = {str(item.selected)[:200]}"
            if i == selected_idx:
                printname = f"> {item.name} {item.selected}"
            print(printname)
        c = click.getchar()

        if c == "j":
            selected_idx += 1
            if selected_idx >= len(menu_items):
                selected_idx = 0
        if c == "k":
            selected_idx -= 1
            if selected_idx < 0:
                selected_idx = len(menu_items) - 1
        if c == " ":
            menu_items[selected_idx].select()
        if c == "\x7f":
            return {x.name: x.selected for x in menu_items}
