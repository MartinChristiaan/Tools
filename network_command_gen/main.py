import os

import yaml

with open("hosts.yml", "r") as file:
    hosts = yaml.safe_load(file)
os.makedirs("../cmds", exist_ok=True)
os.system("../cmds/*.sh")
for hostname, data in hosts.items():
    # Create the Bash script filename

    # Generate the Bash script contents
    port = data.get("port", 22)
    project = data.get("project", "")
    user = data["user"]
    gitpath = data["gitpath"]
    host = data["host"]
    script_contents = f"""#!/bin/bash
ssh  -p {port}  -t {user}@{host} "cd {gitpath} ; bash --login"
	"""

    script_contents_rsync = f"""#!/bin/bash
while sleep 0.1; do find ~/git  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP -e 'ssh -p {data.get('port', 22)}' --delete ~/git/projects/{project}/  {user}@{host}:{gitpath}/{project}/"; done
	"""

    script_contents_mount = f"""#!/bin/bash
cd /mnt && find . -maxdepth 1 -type d -empty -delete

mkdir -p /mnt/{hostname}/
sshfs -o allow_other -o identityfile=/home/leeuwenmcv/.ssh/id_rsa -o ServerAliveInterval=1 -o reconnect -p {port} {user}@{host}:/ /mnt/{hostname}/

	"""

    ssh_copy_key_contents = f"""
    ssh-copy-id -p {port} -i ~/.ssh/id_rsa.pub {user}@{host}
    """

    # Write the Bash script to a file
    script_ssh_filename = f"{hostname}-ssh.sh"
    script_rsync_filename = f"{hostname}-rsync.sh"
    script_mount_filename = f"{hostname}-mount.sh"
    script_copy_key_contents = f"{hostname}-keycopy.sh"

    for contents, filename in zip(
        [
            script_contents,
            script_contents_mount,
            script_contents_rsync,
            ssh_copy_key_contents,
        ],
        [
            script_ssh_filename,
            script_mount_filename,
            script_rsync_filename,
            script_copy_key_contents,
        ],
    ):
        with open(f"../cmds/{filename}", "w") as f:
            f.write(contents)
