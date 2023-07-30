import os
from datetime import datetime
import shutil
import json
home = os.path.expanduser('~')


snippet_path_code = f"{home}/.config/Code/User/snippets/python.json"
if not os.path.exists(snippet_path_code):
	snippet_path_code = "/mnt/c/Users/leeuwenmcv/AppData/Roaming/Code/User/snippets/python.json"

home = os.path.expanduser('~')
snippets_backup_folder = f"{home}/git/tools/VsCodeSynthesis/backups"
os.makedirs(snippets_backup_folder,exist_ok=True)
datestr = datetime.now().strftime("%d%m%YT%H%M%S")
shutil.copy(snippet_path_code,f'{snippets_backup_folder}/python_{datestr}.json')

example = f"""
home = os.path.expanduser('~')
snippets_backup_folder = f"{home}/git/tools/VsCodeSynthesis/backups"
os.makedirs(snippets_backup_folder,exist_ok=True)
datestr = datetime.now().strftime("%d%m%YT%H%M%S")
shutil.copy(snippet_path_code,f'{snippets_backup_folder}/python_{datestr}.json')
"""
with open(snippet_path_code,'r') as f:
	snippets_dict = json.load(f)
name_and_prefix = input("name/prefix : ")
snippets_dict[name_and_prefix] = {
	"scope" : "python",
	"prefix":name_and_prefix,
	"body" : [example]
}

with open(snippet_path_code,'w') as f:
	json.dump(snippets_dict,f,indent=4)

# print(json.dumps(snippets_dict,indent=4)






# cp current snippet file
# get clipboard content
# create snippet

