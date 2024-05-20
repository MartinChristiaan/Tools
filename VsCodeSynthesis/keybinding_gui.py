# %%
# load settings json
from math import e
import os
import json
import shutil
from typing import List


def load_vscode_data():
	home = os.path.expanduser("~")
	vscode_path = f"{home}/.config/Code/User/settings.json"
	if not os.path.exists(vscode_path):
		vscode_path = "/mnt/c/Users/leeuwenmcv/AppData/Roaming/Code/User/settings.json"

	# backup vscode path
	shutil.copy(vscode_path, f"{vscode_path}.bak")

	with open(vscode_path, "r") as f:
		data = json.load(f)
	return data

def get_keybinds(data);
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
		self.keybindings= 
		
	def make_vscode_keybind(keybinds: List[dict]):
		command = get_vscode_command()
		current_keybinds = [x["before"] for x in keybinds]
		keybind = get_keybind()
		while keybind in current_keybinds:
			print("keybinding already exists")
			keybind = get_keybind()
		data = dict(before=keybind, commands=[dict(command=command)])
		keybindings.append(data)
		return keybindings


	def delete_keybind(keybinds: List[dict]):
		stringified = [str(x) for x in keybinds]
		command_to_remove = prompt(stringified)
		print("remove {command_to_remove} from keybindings? [y/n]?")
		char = click.getchar()
		if char == "y":
			keybinds = [x for x in keybinds if str(x) != command_to_remove]
		return keybinds

	menu_str = """
	a : add keybinding
	d : delete keybinding
	q : quit
	"""

	def save_keybinds():
		with open(vscode_path, "w") as f:
			json.dump(data, f, indent=4)

	def main():
		print(menu_str)
		# keybindings = make_vscode_keybind(keybindings)
		action_lut = {
			"a": make_vscode_keybind,
			"d": delete_keybind,
			"q": exit
		}
		char = click.getchar()
		action_lut[char]()

	if __name__ == "__main__":

