import os
import sys
from pathlib import Path

import argparse_enhanced as argparse
from pyfzf import pyfzf

home = os.path.expanduser("~")
argparse_dir = Path(f"{home}/.argparse/")
filename = sys.argv[1]
argparse_file = argparse_dir / (filename.split(".py")[0] + ".csv")
if not os.path.exists(argparse_file):
    print(f"{argparse_file} not found")
    sys.exit()
import pandas as pd

df = pd.read_csv(argparse_file)
rows = [(row.to_dict()) for i, row in df.iterrows()]
str_rows = [str(x) for x in rows]
prompt = pyfzf.FzfPrompt()
choice = prompt.prompt(rows)[0]
row_idx = str_rows.index(choice)
choice = rows[row_idx]
command = f"python3 {sys.argv[1]}"
for k, v in choice.items():
    if type(v) == bool:
        if v:
            command += f" --{k}"
    else:
        command += f" --{k} {v}"
os.system(command)
# print(choice)
