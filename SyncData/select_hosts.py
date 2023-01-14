import os
import yaml
import json
from pyfzf.pyfzf import FzfPrompt
with open("hosts.yml") as stream:
	configs = yaml.safe_load(stream)
config_names=list(configs.keys())
fzf = FzfPrompt()
config_name= fzf.prompt(config_names)[0]
current_host = configs[config_name]
with open('current_host.json','w') as f:
	json.dump(current_host,f)
if "port" not in current_host:
	current_host["port"] = 22

print(current_host)

user = current_host["user"]
host = current_host["host"]
port = current_host["port"]
datapath = current_host["datapath"]
gitpath = current_host["gitpath"]
project= current_host["project"]

host_source = "\n".join([f"{key.upper()}={value}" for key,value in current_host.items()])
with open("host.sh",'w') as f:
	f.write(host_source)

ssh_command = f"ssh -p {port} -t {user}@{host} \"cd {gitpath}/{project}; bash --login\""
with open('ssh_to_host.sh','w') as f:
	f.write(ssh_command)

sync_git_command = f"while sleep 1; do find ~/git/{project} | entr -d bash -c \"rsync  -azP -e 'ssh -p {port}' --delete ~/git/{project}/  {user}@{host}:{gitpath}/ \"; done"
with open('sync_git.sh','w') as f:
	f.write(sync_git_command)

sync_data_command = f"""while sleep 5;
	do rsync -azP -e  "ssh -p {port}" --exclude '*diskstation*' {user}@{host}:{datapath}/ /data/{project}; 
done
"""

with open('sync_data.sh','w') as f:
	f.write(sync_data_command)

