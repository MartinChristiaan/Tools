import json
import os
import re
import shutil
import sys
from datetime import datetime

import click
import pyperclip

from utils.SFzfPrompt import SFzfPrompt

# %%


def extract_words(input_string):
    pattern = r"\b\w+\b"  # Word boundary followed by one or more word characters
    words = re.findall(pattern, input_string)
    return words


data = pyperclip.paste()
home = os.path.expanduser("~")
snippet_path_code = f"{home}/.config/Code/User/snippets/python.json"
if not os.path.exists(snippet_path_code):
    snippet_path_code = (
        "/mnt/c/Users/leeuwenmcv/AppData/Roaming/Code/User/snippets/python.json"
    )

home = os.path.expanduser("~")
snippets_backup_folder = f"{home}/git/tools/VsCodeSynthesis/backups"
os.makedirs(snippets_backup_folder, exist_ok=True)
datestr = datetime.now().strftime("%d%m%YT%H%M%S")
shutil.copy(snippet_path_code, f"{snippets_backup_folder}/python_{datestr}.json")

with open(snippet_path_code, "r") as f:
    snippets_dict = json.load(f)
print(data)


# Example usage
word_list = set(extract_words(data))
print(word_list)

# overwrite_existing
print("Overrwite existing? y/n")
overwrite_existing = click.getchar() == "y"

prompter = SFzfPrompt()
if overwrite_existing:
    existing_snippets = list(snippets_dict.keys())
    name_and_prefix = prompter.prompt(
        existing_snippets, prompt_text="Overwrite existing"
    )[0]
else:
    name_and_prefix = input("name/prefix : ")

var_words = prompter.prompt(word_list, True, "select varwords")
for i, var_word in enumerate(var_words):
    data = data.replace(var_word, r"${" + str(i) + ":" + var_word + "}")

print(data)
print("is this ok? y/n ")
is_ok = click.getchar() == "y"
if not is_ok:
    print("exiting")
    sys.exit()

snippets_dict[name_and_prefix] = {
    "scope": "python",
    "prefix": name_and_prefix,
    "body": [data],
}

with open(snippet_path_code, "w") as f:
    json.dump(snippets_dict, f, indent=4)

print(f"added/changed {name_and_prefix}")


# print(json.dumps(snippets_dict,indent=4)
