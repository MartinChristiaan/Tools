# %%
import json
import os
from dataclasses import dataclass
from typing import List

from black import NewLine
from icecream import ic
from loguru import logger

# goal easily add keybindings using python file
# read current settings vscode
# for keybinding, check if exists, if not, add it...


class BaseCommand:
    def get_dict(self):
        return {}


@dataclass
class terminalCommand(BaseCommand):
    cmd: str
    newTerminal: bool = False
    saveAllFiles: bool = True
    showTerminal: bool = True
    focus: bool = False

    def get_dict(self):
        return {
            "command": "terminalCommandKeys.run",
            "args": {
                "cmd": self.cmd,
                "newTerminal": self.newTerminal,
                "saveAllFiles": self.saveAllFiles,
                "showTerminal": self.showTerminal,
                "focus": self.focus,
            },
        }


@dataclass
class vscodeCommand(BaseCommand):
    cmd: str

    def get_dict(self):
        return {
            "command": self.cmd,
        }


@dataclass
class keybinding:
    key: str
    commands: List[BaseCommand]

    @property
    def binding(self):
        return self.key.split("+")

    def get_data(self):
        return dict(
            before=self.key.split("+"), commands=[x.get_dict() for x in self.commands]
        )


def add_bashrc(new_bindings: List[keybinding]):
    home = os.path.expanduser("~")
    bashrc_path = f"{home}/.bashrc"
    with open(bashrc_path, "r") as f:
        text = f.read()
    lines = text.split("\n")
    new_lines = []
    aliases = []

    for binding in new_bindings:
        keys = "".join(binding.key.split("+")).replace("<leader>", "")
        alias = f"alias {keys}"
        aliases.append(alias)

    for i, line in enumerate(lines):
        keep = True
        for alias in aliases:
            if alias in line:
                keep = False
                logger.debug(f"detected {keys}")
        if keep:
            new_lines.append(line)
    for binding, alias in zip(new_bindings, aliases):
        new_lines.append(f"{alias}='{binding.commands[0].cmd}'")
    with open(bashrc_path, "w") as f:
        f.write("\n".join(new_lines))


def add_keybindings(new_bindings: List[keybinding]):
    home = os.path.expanduser("~")
    vscode_path = f"{home}/.config/Code/User/settings.json"
    if not os.path.exists(vscode_path):
        vscode_path = "/mnt/c/Users/leeuwenmcv/AppData/Roaming/Code/User/settings.json"
        logger.info("Windows path")

    with open(vscode_path, "r") as f:
        data = json.load(f)

    key = "vim.normalModeKeyBindingsNonRecursive"
    keybindings = data[key]
    current_keys = [str(x["before"]) for x in keybindings]
    current_idxs = list(range(len(current_keys)))
    idx_lut = dict(zip(current_keys, current_idxs))
    for binding in new_bindings:
        if str(binding.binding) in current_keys:
            del data[key][idx_lut[str(binding.binding)]]
        logger.info(f"adding {binding}")
        keybindings.append(binding.get_data())

    data[key] = keybindings
    with open(vscode_path, "w") as f:
        json.dump(data, f, indent=4)

    # return keybindings


# %%
