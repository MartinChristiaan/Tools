import os
import sys
from datetime import datetime
from pathlib import Path

home = os.path.expanduser("~")
command = " ".join(sys.argv[1:])
runner_dir = Path(f"{home}/.bgrunner/")
log_dir = runner_dir / "logs"
id_dir = runner_dir / "ids"
log_dir.mkdir(exist_ok=True, parents=True)
id_dir.mkdir(exist_ok=True, parents=True)

datestr = datetime.now().strftime("%d%m%YT%H%M%S")
logname = sys.argv[1] + "_" + Path(sys.argv[2]).stem + f"_{datestr}"
logfile = str(log_dir / logname)
id_file = str(id_dir / logname)
os.system(
    f'bash {home}/git/tools/bg-runner/nohup_cmd.sh "{command}" {logfile} {id_file}'
)


# Store logfile somewhere based on arguments and filename
