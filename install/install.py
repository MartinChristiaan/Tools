import os
from pathlib import Path
import shutil
import sys
home = os.path.expanduser('~')

toolpath = Path(f'{home}/git/tools')
if toolpath.exists():
	print('tool path exists, would you like to replace it?')
	if not input() == 'y':
		print('exiting')
		sys.exit()
	shutil.rmtree(toolpath)

os.makedirs(f'{home}/git',exist_ok=True)
os.system(f'git clone https://github.com/MartinChristiaan/Tools.git && mv Tools {home}/git/tools')
with open(f'{home}/.bashrc','r') as f:
	text = f.read()
if not 'bash_extension' in text:
	os.system('echo "source ~/git/tools/bash_extension/bash_extension.sh" >> ~/.bashrc')
	print('adding bash extension')
os.system(f'cd {toolpath/"install"};pip3 install -r requirements.txt')





