from itertools import product
from multiprocessing import Process
import os

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
from pathlib import Path
import pickle
import sys
import time
from typing import List
import click

import fnmatch

try:
    from fzf_utils import prompt
except:
    pass


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


def print_grid(strings):
    try:
        # Get terminal width
        terminal_width = os.get_terminal_size().columns

        # Calculate number of columns based on terminal width
        num_columns = terminal_width // (
            max(len(s) for s in strings) + 2
        )  # +2 for padding

        # Pad shorter strings with spaces to ensure equal length
        padded_strings = [s.ljust(max(len(s) for s in strings) + 2) for s in strings]

        # Print grid
        for i in range(0, len(padded_strings), num_columns):
            row = padded_strings[i : i + num_columns]
            print("".join(row))
    except:
        print(strings)


@dataclass
class MenuItemSelectStr(MenuItem):
    options: List = None
    single_value: bool = True

    def select(self):
        print("selecting")
        self._selected = prompt(
            self.options, multi=not self.single_value, cachename="menu_cache"
        )
        return self._selected


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
                selected += fnmatch.filter(self.options, f"{sub_pattern}")

            click.clear()
            # print(",".join(selected))
            if len(selected) > 0:
                print_grid(selected)
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
        self.cache_file = self.cache_dir / f"{name}.pkl"
        self.load_cache_state()

    def load_cache_state(self):
        if self.cache_file.exists():
            with open(self.cache_file, "rb") as f:
                state = pickle.load(f)
            for k, v in state.items():
                menu_item = [x for x in self.menu_items if x.name == k]
                for item in menu_item:
                    item._selected = v

    def save_state(self):
        state = {item.name: item.selected for item in self.menu_items}
        with open(self.cache_file, "wb") as f:
            pickle.dump(state, f)

    def run(self, debug=False):
        pass

        selected_idx = 0
        configs = {x.name: x.selected for x in self.menu_items}
        while not debug:
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
                self.save_state()
            if c == "\x1b":  # esc
                configs = {x.name: x.selected for x in self.menu_items}
                break

            if c == "q":
                sys.exit()

        tasks = []
        list_values = []
        list_keys = []
        single_values = []

        for k, v in configs.items():
            if isinstance(v, list):
                list_values.append(v)
                list_keys.append(k)
                print(len(v))
            else:
                single_values.append((k, v))
        configs = []
        from icecream import ic

        for val_tuple in product(*list_values):
            config = {}
            for k, v in zip(list_keys, val_tuple):
                config[k] = v
            for k, v in single_values:
                config[k] = v
            configs.append(config)
        return configs


class TaskProcessor:
    def __init__(self, task) -> None:
        self.queue = []
        self.task = task
        self.config_in_progess = None
        self.p = Process(target=self.run)
        self.p.start()

    def run(self):
        while True:
            if not len(self.queue) == 0:
                self.config_in_progess = self.queue[0]
                self.task(self.config_in_progess)
                self.config_in_progess = None
                self.queue = self.queue[1:]
            else:
                print("sleeping")
                time.sleep(0.1)


@dataclass
class QueueControl(MenuItem):
    processer: TaskProcessor = None

    def select(self):
        while True:
            out_str = f"""
	Items in queue : {self.processor.queue.size()}
	currently processing : {self.processor.config_in_process}
			"""
            selected_idx = 0

            for i, t in enumerate(self.processer.queue):
                task_str = str(t)[:200]
                if selected_idx == i:
                    task_str = " > " + task_str
                out_str += task_str + "\n"
            print(out_str)
            c = click.getchar()
            if c == "j":
                selected_idx += 1
                if selected_idx >= len(self.menu_items):
                    selected_idx = 0
            if c == "k":
                selected_idx -= 1
                if selected_idx < 0:
                    selected_idx = len(self.menu_items) - 1
            if c == "d":
                del self.processer.queue[selected_idx]
            if c == "t":
                self.processer.queue = []
            if c == "\x1b":  # esc
                return


@dataclass
class MenuItemReturnGlob(MenuItem):
    options: List = None

    def select(self):
        print("selecting")
        current_pattern = ""
        while True:
            selected = []
            for sub_pattern in current_pattern.split("+"):
                selected += fnmatch.filter(self.options, f"{sub_pattern}")

            click.clear()
            # print(",".join(selected))
            if len(selected) > 0:
                print_grid(selected)
            print(f"Pattern : {current_pattern}")
            char = click.getchar()
            if char == "\x7f":
                current_pattern = current_pattern[:-1]
            elif char == " ":
                self._selected = current_pattern
                return
            else:
                current_pattern += char
