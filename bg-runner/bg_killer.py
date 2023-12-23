import os
from pathlib import Path

import psutil

home = os.path.expanduser("~")
runner_dir = Path(f"{home}/.bgrunner/")
id_dir = runner_dir / "ids"
log_dir = runner_dir / "logs"
for p in id_dir.glob("*"):
    with open(p, "r") as f:
        pid = int(f.read())
    if not psutil.pid_exists(pid):
        os.remove(p)
        logfile = str(p).replace(
            id_dir,
        )


#     print("a process with pid %d exists" % pid)
# else:
#     print("a process with pid %d does not exist" % pid)
