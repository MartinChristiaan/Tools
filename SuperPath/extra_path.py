import glob
from pathlib import Path
import os
import shutil

import tqdm

def find_leaf_directories(path):
	leaf_directories = []

	if os.path.isdir(path):
		has_subdirectories = False
		for item in os.listdir(path):
			item_path = os.path.join(path, item)
			if os.path.isdir(item_path):
				has_subdirectories = True
				break

		# If the directory doesn't have any subdirectories, add it to the leaf_directories list
		if not has_subdirectories:
			leaf_directories.append(path)

		# Recursively explore subdirectories
		for item in os.listdir(path):
			item_path = os.path.join(path, item)
			if os.path.isdir(item_path):
				leaf_directories.extend(find_leaf_directories(item_path))

	return leaf_directories

def rename_files_from_dir_to_numerical_sequence(directory):
	files = glob.glob(f"{directory}/*")
	files.sort()
	for i,file in enumerate(tqdm(files)):
		frame_no =  f"{i}".zfill(5)
		ext = file.split('.')[-1]
		new_name = f"{directory}/{frame_no}.{ext}"
		shutil.move(file,new_name)


class SPath(Path):
	def get_leaf_directories(self):
		return [SPath(x) for x in find_leaf_directories(str(self))]
	
	def copy_mkdir(self,dst:'SPath'):
		dst_dir = dst if dst.suffix == '' else dst.parent
		dst_dir.mk_dir(exist_ok=True)
		shutil.copy(self,dst)