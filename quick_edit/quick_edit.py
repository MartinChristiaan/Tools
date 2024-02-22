#%%
from SFzfPrompt import prompt

# parse ssh hosts defined in user config
def get_ssh_hosts():
    ssh_hosts = []
    with open('/mnt/c/Users/leeuwenmcv/.ssh/config', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'Host ' in line:
                ssh_hosts.append(line.split()[1])
    return ssh_hosts

# parse ssh hosts defined in user config
hosts = get_ssh_hosts()
host = prompt(hosts,prompt_text="Select a host to connect to: ")
import paramiko

ssh = paramiko.SSHClient()
ssh.connect('yolo_docker_toren')
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)

