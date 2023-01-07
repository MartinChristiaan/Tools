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


user = current_host["user"]
host = current_host["host"]
port = current_host["port"]
datapath = current_host["datapath"]
gitpath = current_host["gitpath"]
project= current_host["project"]

ssh_command = f"ssh -p {port} -t {user}@{host} \"cd {gitpath}; bash --login\""
with open('ssh_to_host.sh','w') as f:
	f.write(ssh_command)

sync_git_command = f"while sleep 1; do find ~/git/{project} | entr -d bash -c \"rsync  -azP -e 'ssh -p {port}' --delete ~/git/{project}  {user}@{host}:{gitpath}/{project} \"; done"
with open('sync_git.sh','w') as f:
	f.write(sync_git_command)

sync_data_command = f"""while sleep 10;
	do rsync -azP -e  "ssh -p {port}" --exclude '*diskstation*' {user}@{host}:${datapath}/{project} /data/{project}; 
done
"""

with open('sync_data.sh','w') as f:
	f.write(sync_data_command)

