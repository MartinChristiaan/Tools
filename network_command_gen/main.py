import os

import yaml

os.makedirs("../cmds", exist_ok=True)
# os.system("../cmds/*.sh")


def get_ssh_hosts():
    ssh_hosts = {}
    current_host = None

    with open("/mnt/c/Users/leeuwenmcv/.ssh/config", "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("Host "):
                current_host = line.split()[1]
                ssh_hosts[current_host] = {}
            elif line.startswith("HostName "):
                ssh_hosts[current_host]["host"] = line.split()[1]
            elif line.startswith("User "):
                ssh_hosts[current_host]["user"] = line.split()[1]
            elif line.startswith("Port "):
                ssh_hosts[current_host]["port"] = line.split()[1]

    return ssh_hosts


# Example usage
ssh_hosts = get_ssh_hosts()
print(ssh_hosts)


# parse ssh hosts defined in user config
hosts = get_ssh_hosts()

for hostname, data in hosts.items():
    # Create the Bash script filename

    # Generate the Bash script contents
    port = data.get("port", 22)
    project = data.get("project", "")
    user = data["user"]
    host = data["host"]
    script_contents = f"""#!/bin/bash
ssh  -p {port}  -t {user}@{host} "cd /home/{user}/git ; bash --login"
	"""
    #     script_contents_rsync = f"""#!/bin/bash
    # while sleep 0.1; do find ~/git  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP -e 'ssh -p {data.get('port', 22)}' --delete ~/git/projects/{project}/  {user}@{host}:{gitpath}/{project}/"; done
    # 	"""

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
    # script_rsync_filename = f"{hostname}-rsync.sh"
    script_mount_filename = f"{hostname}-mount.sh"
    script_copy_key_contents = f"{hostname}-keycopy.sh"

    for contents, filename in zip(
        [
            script_contents,
            script_contents_mount,
            # script_contents_rsync,
            ssh_copy_key_contents,
        ],
        [
            script_ssh_filename,
            script_mount_filename,
            # script_rsync_filename,
            script_copy_key_contents,
        ],
    ):
        with open(f"../cmds/{filename}", "w") as f:
            f.write(contents)
