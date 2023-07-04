import os
import sys
import click
from view import command_message
from state import MODES, State

home = os.path.expanduser('~')
def get_parent_directory(directory):
	return "/".join(directory.split("/")[:-1]) or "/"
explorer_path = f"{home}/git/tools/explorer/"


def add_bookmark(folder):
	with open(f"{explorer_path}/bookmarks",'r') as f:
		bookmarks = f.read().split('\n')
	if folder not in bookmarks:
		bookmarks.append(folder)
	with open(f"{explorer_path}/bookmarks",'w') as f:
		f.write("\n".join(bookmarks))

def handle_control_keys(state:State):
	"""
	Returns bool which indicates a break out of the while loop
	"""
	os.system('clear')
	print(command_message)
	char = click.getchar()
	if char == "q":
		sys.exit()
	# if char == "b":
	# 	state.current_folder = get_parent_directory(state.current_folder)
	# 	os.system("clear")
	# 	return True
	if char == "a":
		add_bookmark(state.current_folder)
	if char == "n":
		os.system(f"nautilus {state.current_folder}")
	if char == "b":
		os.system('clear')
		state.mode = MODES.BOOKMARK
		return True
	if char == "e":
		os.system(f"cd {state.current_folder} && explorer.exe .")
	if char == "o":
		state.mode = MODES.OPEN
	if char == "c":
		state.mode = MODES.COPY
	if char == "m":
		state.mode = MODES.MOVE
	if char == "d":
		state.mode = MODES.DELETE
	if char == "v":
		os.system(f"python.exe {explorer_path}/image_viewer.py {state.current_folder}")
	if char == "t":
		with open('/tmp/dest','w') as f:
			f.write(state.current_folder)
		sys.exit()
	if char == "p":
		if state.mode == MODES.MOVE:
			os.system(f"mv {state.path_to_copy} {state.current_folder}")
		elif state.mode == MODES.COPY:
			os.system(f"cp {state.path_to_copy} {state.current_folder}")
		return True
