import os
import shutil
from pathlib import Path

from debugger import load_previous_state, Debugger

tests_dir = Path("./tests")
if tests_dir.exists():
    shutil.rmtree(tests_dir)


if __name__ == "__main__":
    debugger = load_previous_state()
    debugger.generate_test("example", "auto")
    os.system("pytest")
