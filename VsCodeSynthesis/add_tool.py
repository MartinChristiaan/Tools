import os
from pathlib import Path

toolname = input("enter toolname : ")
home = os.path.expanduser("~")

toolbase = Path(f"{home}/git/tools/{toolname}")
toolbase.mkdir()
filepath = toolbase / f"{toolname}.py"
os.system(f"touch {filepath}")
os.system(f"code {toolbase}")
