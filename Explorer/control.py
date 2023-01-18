import os
import sys
import click
from view import command_message
from state import MODES, State

def get_parent_directory(directory):
	return "/".join(directory.split("/")[:-1]) or "/"
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
	if char == "n":
		os.system(f"nautilus {state.current_folder}")
		
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
	if char == "t":
		with open('/tmp/dest','w') as f:
			f.write(state.current_folder)
		# os.system(f"{current_folder} > /tmp/dest")
		sys.exit()
	if char == "p":
		if state.mode == MODES.MOVE:
			os.system(f"mv {state.path_to_copy} {state.current_folder}")
		elif state.mode == MODES.COPY:
			os.system(f"cp {state.path_to_copy} {state.current_folder}")
		return True
