import os
import click
import sys
from state import State,Combination,MODES,Processedpath
from view import get_output_string
from control import get_parent_directory, handle_control_keys
home = os.path.expanduser('~')

state = State(os.getcwd(),[],"",MODES.OPEN,"",[])

while True:
	
	if state.current_folder.startswith("//"):
		state.current_folder = state.current_folder[1:]
	## Prepare keybinds
	subpaths = os.listdir(state.current_folder)
	if state.mode == MODES.BOOKMARK:
		with open(f'{home}/git/tools/explorer/bookmarks','r') as f:
			subpaths = f.read().split('\n')
	subpaths.sort()


	starting_char = []
	starting_charpairs = []

	identifier_chars = [x for x in "asdfjkl;qweruiopzsxcvnm,."]
	processed_paths = []

	for path in subpaths:
		full_path = f"{state.current_folder}/{path}"
		if path.endswith('/'):
			path = path[:-1]
		if len(path) < 2:
			continue
		path = path.split('/')[-1].replace("\n","")
		processed_paths.append(Processedpath(full_path,path))
		starting_char.append(path[0])
		starting_charpairs.append(path[:2])

	final_keybind_char_lookup = {charpair:identifier_chars.copy() for charpair in starting_charpairs}
	# Get combinations

	combinations = []
	for path in processed_paths:
		c1,c2 = path.shorthand[:2]
		if len([x for x in starting_char if x == c1]) == 1: # unique starting char
			combination = Combination(path,c1)
			combinations.append(combination)
		elif len([x for x in starting_charpairs if x == c1+c2]) == 1: # unique starting char
			combinations.append(Combination(path,c1+c2))
		else:
			identifier_list = final_keybind_char_lookup[path.shorthand[:2]]
			if len(identifier_list) == 0:
				continue
			identifier = identifier_list.pop(0)
			combinations.append(Combination(path,c1+c2+identifier))
	state.combinations = combinations

	# UI loop

	get_output_string(state)
	final_result = False
	state.cur_selection = []
	state.curkey = ""
	while True:
		char = click.getchar()
		# input(f"u pressed {char} with {len(char)}")
		if char == " " and handle_control_keys(state):
			break

		elif char == "\x1b":
			state.current_folder = get_parent_directory(state.current_folder)
			os.system("clear")
			break

		os.system("clear")
		state.curkey+=char
		state.cur_selection = [x for x in state.combinations if x.keybind.startswith(state.curkey)]
		if len(state.cur_selection) == 1:
			path = state.cur_selection[0].path.full_path
			if state.mode == MODES.BOOKMARK:
				path = path.replace(state.current_folder,"")
				state.mode = MODES.OPEN
			final_result = True
			break
		elif len(state.cur_selection) == 0:
			state.cur_selection = state.combinations
			state.curkey = ""
		get_output_string(state)

	if final_result :
		if os.path.isfile(path):
			if state.mode == MODES.OPEN:
				os.system(f'xdg-open "{path}"')
				break
			elif state.mode == MODES.COPY or state.mode == MODES.MOVE:
				# os.system(f'clip.exe "{filepath}"')
				state.path_to_copy = path
				state.curkey = ""
			elif state.mode == MODES.DELETE:
				os.system(f"rm {path}")
				# state.current_folder = path
		else:
			state.curkey = ""
			state.current_folder = path
			
