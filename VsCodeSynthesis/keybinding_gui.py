# %%
# load settings json
from math import e
import os
import json
import random
import shutil
from typing import List

KEYBIND_KEY = "vim.normalModeKeyBindingsNonRecursive"


def get_vscode_path():
    home = os.path.expanduser("~")
    vscode_path = f"{home}/.config/Code/User/settings.json"
    if not os.path.exists(vscode_path):
        vscode_path = "/mnt/c/Users/leeuwenmcv/AppData/Roaming/Code/User/settings.json"
    return vscode_path


def load_vscode_data():
    vscode_path = get_vscode_path()
    shutil.copy(vscode_path, f"{vscode_path}.bak")
    with open(vscode_path, "r") as f:
        data = json.load(f)
    return data


def get_keybinds(data):
    key = "vim.normalModeKeyBindingsNonRecursive"
    keybindings = data[key]
    return keybindings
    # effects = []
    # for item in keybindings:
    # 	effect = ""
    # 	if "after" in item:
    # 		effect += ",".join(item["after"])
    # 	if "commands" in item:
    # 		for command in item["commands"]:
    # 			if "command" in command:
    # 				effect += command["command"]
    # 			if "args" in command:
    # 				effect += str(command["args"])
    # 	effects += [effect]


# %%
from fzf_utils import prompt

# selected = prompt(effects)

import click


def get_vscode_command():
    home = os.path.expanduser("~")
    with open(f"{home}/git/tools/VsCodeSynthesis/vscode_commands", "r") as f:
        commands = f.read().split("\n")
    command = prompt(commands)
    return command


def get_keybind() -> List[str]:
    keybind = ""
    while True:
        keybind_list = []
        for x in keybind:
            if x == " ":
                keybind_list += ["<leader>"]
            else:
                keybind_list += [x]
        print(f"current_keybinding : {keybind_list}")
        char = click.getchar()
        # check if char == escape
        if char == "\x1b":
            break
        keybind += char
    return keybind_list


class KeybindManager:
    def __init__(self) -> None:
        self.data = load_vscode_data()
        self.keybinds = get_keybinds(self.data)

    def make_vscode_keybind(self):
        command = get_vscode_command()
        current_keybinds = [x["before"] for x in self.keybinds]
        keybind = get_keybind()
        while keybind in current_keybinds:
            print("keybinding already exists")
            keybind = get_keybind()
        data = dict(before=keybind, commands=[dict(command=command)])
        self.keybinds.append(data)
        self.save_keybinds()

    def delete_keybind(self):
        stringified = [str(x) for x in self.keybinds]
        command_to_remove = prompt(stringified)
        print("remove {command_to_remove} from keybindings? [y/n]?")
        char = click.getchar()
        if char == "y":
            self.keybinds = [x for x in self.keybinds if str(x) != command_to_remove]
        self.save_keybinds()

    def save_keybinds(self):
        self.data[KEYBIND_KEY] = self.keybinds
        with open(get_vscode_path(), "w") as f:
            json.dump(self.data, f, indent=4)

    def trainer(self):
        while True:
            random_keybind = random.choice(self.keybinds)
            effect = ""
            if "after" in random_keybind:
                effect += ",".join(random_keybind["after"])
            if "commands" in random_keybind:
                effect += random_keybind["commands"][0]["command"]
                if "args" in random_keybind["commands"][0]:
                    effect += str(random_keybind["commands"][0]["args"])

            print(effect)
            guessed_keybind = get_keybind()
            if str(guessed_keybind) == str(random_keybind["before"]):
                print("correct")
            else
                print(f"{guessed_keybind}=incorrect", random_keybind["before"])
            click.getchar()

    def run(self):

        menu_str = """
a : add keybinding
d : delete keybinding
q : quit
t : trainer
		"""
        while True:
            print(menu_str)
            action_lut = {
                "a": self.make_vscode_keybind,
                "d": self.delete_keybind,
                "q": exit,
                "t": self.trainer,
            }
            char = click.getchar()
            action_lut[char]()


def main():
    manager = KeybindManager()
    manager.run()


if __name__ == "__main__":
    main()
