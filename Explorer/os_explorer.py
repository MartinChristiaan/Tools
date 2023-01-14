
import os
import sys
import time
current_folder = os.getcwd()
import sys
from colorama import Fore,Style,Back
from colorama import init as colorama_init
colorama_init()
RESET = Style.RESET_ALL

def get_output_string(current_folder,combinations):

	num_cols = 4
	output_string = Back.BLUE + Fore.WHITE + Style.BRIGHT +  f"{current_folder}".center(25 * num_cols,"-") + f"{RESET}\n"
	get_full_path = lambda x: f"{current_folder}/{x['item']}"

	folder_combos = [x for x in combinations if os.path.isdir(get_full_path(x))]
	file_combos = [x for x in combinations if not os.path.isdir(get_full_path(x))]
	combinations = folder_combos + file_combos
	for i,combo in enumerate(combinations):
		keybind_label = f'{combo["keybind"]}'.rjust(4)

		item_path = f'{current_folder}/{combo["item"]}' 
		max_label_length = 20
		item_label = f'{combo["item"][:max_label_length]}'.rjust(20)

		if os.path.isdir(item_path):
			color = Fore.BLUE
		else:
			color = Fore.GREEN
		output_string += f'{Fore.RED}{keybind_label}{RESET} : {color}{item_label}{RESET} | '
		if i % num_cols == num_cols-1:
			output_string += "\n"
	if len(combinations) == 0:
		output_string += f"{Fore.RED} no items found {RESET} "

	print(output_string)

command_message = """
q : quit
t : terminal here
c : copy mode
"""

def get_parent_directory(directory):
	return "/".join(directory.split("/")[:-1])


while True:
	items = os.listdir(current_folder)
	# for line in sys.stdin:
	#     # sys.stdout.write(line)
	# 	items.append(line.replace('\n',"").replace(" ",""))

	items.sort()

	starting_char = []
	starting_charpairs = []

	identifier_chars = [x for x in "asdfjkl;qweruiopzsxxcvnm,."]

	# Scan for possible keybinds

	for item in items:
		if item.endswith('/'):
			item = item[:-1]
		if len(item) < 2:
			continue
		item = item.split('/')[-1].replace("\n","")
		c1 = item[0] 
		c2 = item[1] 
		starting_char.append(c1)
		starting_charpairs.append(c1+c2)

	next_identifier_char_lookup = {charpair:identifier_chars.copy() for charpair in starting_charpairs}
	# Get combinations

	combinations = []
	for item in items:
		if item.endswith('/'):
			item = item[:-1]
		if len(item) < 2:
			continue
		itemk = item.split('/')[-1].replace("\n","")
		c1 = itemk[0] 
		c2 = itemk[1] 
		if len([x for x in starting_char if x == c1]) == 1: # unique starting char
			combinations.append(dict(keybind=c1,item=item))
		elif len([x for x in starting_charpairs if x == c1+c2]) == 1: # unique starting char
			combinations.append(dict(keybind=c1+c2,item=item))
		else:
			identifier_list = next_identifier_char_lookup[itemk[:2]]
			if len(identifier_list) == 0:
				continue
			identifier = identifier_list.pop(0)
			combinations.append(dict(keybind=c1+c2+identifier,item=item))

	get_output_string(current_folder,combinations)
	import click
	cur_selection = []
	cur_word= ""
	final_result = False
	while True:
		char = click.getchar()
		if char == " ":
			os.system('clear')
			print(command_message)
			char = click.getchar()
			if char == "q":
				sys.exit()
			if char == "b":
				current_folder = get_parent_directory(current_folder)
				print(current_folder)
				break
			if char == "t":
				with open('/tmp/dest','w') as f:
					f.write(current_folder)
				# os.system(f"{current_folder} > /tmp/dest")
				sys.exit()

			





		os.system("clear")
		cur_word+=char
		cur_selection = [x for x in combinations if x["keybind"].startswith(cur_word)]
		if len(cur_selection) == 1:
			item = cur_selection[0]["item"]
			final_result = True
			break
		elif len(cur_selection) == 0:
			cur_selection = combinations
			cur_word = ""
		get_output_string(current_folder,cur_selection)
	if final_result :
		if os.path.isfile(f"{current_folder}/{item}"):
			os.system(f"xdg-open {current_folder}/{item}")
			break
		else:
			current_folder = f"{current_folder}/{item}"
