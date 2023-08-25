import os
from pathlib import Path
import shutil
import sys
import click
home = os.path.expanduser('~')

toolpath = Path(f'{home}/git/tools')
if toolpath.exists():
	print('tool path exists, would you like to replace it?')
	if not click.getchar() == 'y':
		print('exiting')
		sys.exit()
	shutil.rmtree(toolpath)

os.system(f'git clone https://github.com/MartinChristiaan/Tools.git && move Tools {home}/git/tools')
with open('.bashrc','r') as f:
	text = f.read()
os.makedirs(f'{home}/git',exist_ok=True)
if not 'bash_extension' in text:
	os.system('echo "source ~/git/tools/bash_extension/bash_extension.sh" >> ~/.bashrc')
	print('adding bash extension')



