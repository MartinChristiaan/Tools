import os
from pathlib import Path

import argparse_enhanced as argparse

parser = argparse.ArgumentParser(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)
parser.add_argument("--filename", type=str, default="test")
parser.add_argument("-v", "--verbose", action="store_true")
args = parser.parse_args()
print(args)
home = os.path.expanduser("~")
argparse_dir = Path(f"{home}/.argparse/")
for x in argparse_dir.glob("*.csv"):
    print(x)
    with open(x, "r") as f:
        text = f.read()
    print(text)
# with open(argparse_dir,'r') as f:
# 	text = f.read()
