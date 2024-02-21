import os
from pathlib import Path
home = os.path.expanduser('~')
annotation_dir = Path(f"{home}/annotations")
annotation_files = annotation_dir.rglob('*.txt')
for fil in annotation_files:
	with open(fil,'r') as f:
		text = f.read()
	print(text)