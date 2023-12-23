import os
import sys

current_folder = home = os.path.expanduser("~")
import sys

items = []
for line in sys.stdin:
    # sys.stdout.write(line)
    items.append(line.replace("\n", "").replace(" ", ""))

items.sort()

starting_char = []
starting_charpairs = []

identifier_chars = [x for x in "asdfjkl;qweruiopzsxcvnm,."]


for item in items:
    if item.endswith("/"):
        item = item[:-1]
    if len(item) < 2:
        continue
    print(item)

    item = item.split("/")[-1].replace("\n", "")
    c1 = item[0]
    c2 = item[1]
    starting_char.append(c1)
    starting_charpairs.append(c1 + c2)

next_identifier_char_lookup = {
    charpair: identifier_chars.copy() for charpair in starting_charpairs
}

combinations = []
for item in items:
    if item.endswith("/"):
        item = item[:-1]
    if len(item) < 2:
        continue
    itemk = item.split("/")[-1].replace("\n", "")
    c1 = itemk[0]
    c2 = itemk[1]
    if len([x for x in starting_char if x == c1]) == 1:  # unique starting char
        combinations.append(dict(keybind=c1, item=item))
    elif (
        len([x for x in starting_charpairs if x == c1 + c2]) == 1
    ):  # unique starting char
        combinations.append(dict(keybind=c1 + c2, item=item))
    else:
        print(itemk)
        identifier = next_identifier_char_lookup[itemk[:2]].pop(0)
        combinations.append(dict(keybind=c1 + c2 + identifier, item=item))

output_string = ""
for combo in combinations:
    keybind_label = f'{combo["keybind"]}'.rjust(4)
    output_string += f'{keybind_label} : {combo["item"]} \n'
print(output_string)
import click

cur_selection = []
cur_word = ""
while True:
    char = click.getchar()
    os.system("clear")
    cur_word += char
    cur_selection = [x for x in combinations if x["keybind"].startswith(cur_word)]
    if len(cur_selection) == 1:
        print(cur_selection[0]["item"])
        sys.exit()
    elif len(cur_selection) == 0:
        cur_selection = combinations
        cur_word = ""
    else:
        output_string = ""
        for combo in cur_selection:
            keybind_label = f'{combo["keybind"]}'.rjust(4)
            output_string += f'{keybind_label} : {combo["item"]} \n'
        print(output_string)
