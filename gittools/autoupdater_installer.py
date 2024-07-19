# Installs autoupdater as a service assuming SystemD is used.
import os
import subprocess
import sys
from pathlib import Path

from loguru import logger

updater_file = Path(__file__).parent.absolute() / "autoupdater.py"
# check if the updater file exists
if not updater_file.exists():
    logger.error(f"Updater file {updater_file} does not exist.")
    sys.exit(1)

if os.environ["USER"]:  # == 'root':
    user = "leeuwenmcv"
else:
    user = os.environ["USER"]

# create the contents of the service file
SERVICE_CONTENTS = f"""[Unit]
Description=Auto Updater Service
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User={user}
ExecStart={sys.executable} {updater_file}
WorkingDirectory={Path(__file__).parent.absolute()}

[Install]
WantedBy=multi-user.target
"""

SERVICE_PATH = "/etc/systemd/system/autoupdater.service"

# create the service file
with open(SERVICE_PATH, "w") as f:
    f.write(SERVICE_CONTENTS)

# enable the service
subprocess.check_output(
    "systemctl enable autoupdater", shell=True, stderr=subprocess.STDOUT
)

# start the service
subprocess.check_output(
    "systemctl restart autoupdater", shell=True, stderr=subprocess.STDOUT
)

# start the service
subprocess.check_output(
    "sudo systemctl daemon-reload", shell=True, stderr=subprocess.STDOUT
)

# check the status of the service
status = subprocess.check_output(
    "systemctl status autoupdater", shell=True, stderr=subprocess.STDOUT
).decode()
logger.info(status)
