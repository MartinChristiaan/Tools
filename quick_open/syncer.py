import glob
import os

import pyfzf

home = os.path.expanduser("~")

with open(f"quick_folders", "r") as f:
    folders = f.readlines()
combined_dirs = []
for folder in folders:
    print(folder)
    folder = folder.replace("\n", "")
    folder = folder + "/*"
    combined_dirs += [x for x in glob.glob(folder) if os.path.isdir(x)]

prompt = pyfzf.FzfPrompt()
source_dir = prompt.prompt(combined_dirs)[0]
target_dir = prompt.prompt(combined_dirs)[0]

command = f"rsync -azP {source_dir} {target_dir}"
print(command)
isok = input("Run this command? [y/n]")
if isok == "y":
    os.system(command)
    print(source_dir)
    print(target_dir)

# os.system(command)

# print(result)
