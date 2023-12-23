import os

# import click
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from RSYNCER import RSYNCER

# from state import State,Combination,MODES,Processedpath
# from view import get_output_string
# from control import get_parent_directory, handle_control_keys,explorer_path,tools_path
from utils.charmenu import charmenu
from utils.SFzfPrompt import prompt

home = os.path.expanduser("~")
# state = State(os.getcwd(),[],"",MODES.OPEN,"",[])

explorer_path = f"{home}/git/tools/explorer2/"
image_viewer_path = f"{home}/git/tools/yolo_explorer/"
tools_path = f"{home}/git/tools/"
history_file = f"{explorer_path}/history"


def add_to_history_file(full_path):
    HISTORY_LEN = 100
    history_file = f"{explorer_path}/history"
    with open(history_file, "r") as f:
        paths = f.read().split("\n")[-HISTORY_LEN:]
    if full_path not in paths:
        paths.append(full_path)
        with open(history_file, "w") as f:
            f.write("\n".join(paths))


class MODES:
    TRAVEL = "travel"
    COMMAND = "command"


@dataclass
class FZFCMD:
    key: str
    action: any

    def get_bind(self):
        return f""" --bind="ctrl-{self.key}:execute(echo \'__{self.key}\')+abort" """


class App:
    def __init__(self) -> None:
        self.current_folder = Path(os.getcwd())
        self.mode = MODES.COMMAND
        self.rsyncer = RSYNCER(self)

    def exit(self):
        sys.exit()

    def open_path(self, subpath: str):
        mode, path = subpath.split(":")
        if mode == "r":
            target = self.current_folder / path
        else:
            target = Path(path)
        if not target.exists():
            return
        add_to_history_file(str(target))
        if target.is_file():
            os.system(f"xdg-open {target}")
        else:
            self.current_folder = target

    def to_command_mode(self):
        self.mode = MODES.COMMAND

    def go_to_parent_dir(self):
        self.current_folder = self.current_folder.parent

    def open_explorer(self):
        os.system(f"cd {self.current_folder} && explorer.exe .")

    def get_items(self):
        items_in_dir = ["r:" + x for x in os.listdir(self.current_folder)]
        items_in_dir.sort()

        with open(f"{explorer_path}/history", "r") as f:
            history_paths = ["h:" + h for h in f.read().split("\n")]
        history_paths.sort()
        paths = items_in_dir + history_paths
        return paths

    def explore(self):
        self.mode = MODES.TRAVEL
        fzf_actions = [
            FZFCMD("x", self.go_to_parent_dir),
            FZFCMD("e", self.open_explorer),
        ]
        action_lut = {"__" + a.key: a.action for a in fzf_actions}
        while self.mode == MODES.TRAVEL:
            paths = self.get_items()
            # print(items_in_dir)
            extra_options = "".join([x.get_bind() for x in fzf_actions])
            # print(extra_options)
            # break
            target = prompt(
                paths, prompt_text=f"{self.current_folder}", extra_options=extra_options
            )
            if not target:
                self.mode = MODES.COMMAND
                return
            if target in action_lut:
                action_lut[target]()
            else:
                self.open_path(target)

    def file_viewer(self):
        os.system(
            f"cd {image_viewer_path} && python.exe yolo_explorer.py {self.current_folder}"
        )

    # def set_rsync_source(self):
    # 	self.rsyncer.source = self.current_folder
    # def set_rsync_dest(self):
    # 	self.rsyncer.dest = self.current_folder
    # def execute_rsync(self):
    # 	self.rsyncer.execute()
    def open_terminal(self):
        with open("/tmp/dest", "w") as f:
            f.write(str(self.current_folder))
        self.exit()

    def __call__(self) -> Any:
        self.explore()
        while True:
            # os.system('clear')
            action_lut = {
                "x": self.explore,
                "q": self.exit,
                "e": self.open_explorer,
                "rs": self.rsyncer.rsync_set_source,
                "rd": self.rsyncer.rsync_set_dest,
                "re": self.rsyncer.rsync_execute,
                "t": self.open_terminal,
                "v": self.file_viewer,
            }
            charmenu(action_lut)


if __name__ == "__main__":
    App()()


# class TravelMode:
# 	def __init__(self) -> None:
# 		pass
# 	def __call__() -> Any:
# 		pass
