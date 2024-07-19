import subprocess

import yaml

# Open the YAML file and load the contents
with open("hosts.yml", "r") as f:
    data = yaml.safe_load(f)

# Loop over each section and print its contents
for section, config in data.items():
    ssh_cmd = (
        f"ssh {config['user']}@{config['host']} 'apt show nvidia-jetpack|grep version'"
    )
    output = subprocess.check_output(ssh_cmd, shell=True).decode().strip()

    # Print the output of the command
    print(f"{config['host']} Jetpack version: {output}")
