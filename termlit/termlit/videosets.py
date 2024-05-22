from multiprocessing import Queue
import os
from pathlib import Path
from dataclasses import dataclass
import time
import click
from videosets_ii.videosets_ii import VideosetsII

from termlit.selection import (
	Menu,
	MenuItem,
	MenuItemBool,
	MenuItemMultiStr,
	MenuItemFloat,
	QueueControl,
	TaskProcessor,
)

basedirpath = Path(r"/diskstation")
# check if windows
if os.name == "nt":
	basedirpath = None
# basedirpath = Path(r"/data/local_diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)
videoset_names = list(videosets.to_pandas()["name"])


def find_result_csv_in_mm_path(mm):
	paths = list(mm.result_dirpath.rglob("*.csv"))
	# sorted_paths = sorted(paths, key=get_modified_date)
	# path_options = [f"{x.parent.stem}/{x.name}" for x in paths]
	return paths


def get_cameras(videoset_names):
	cameras = []
	for vset in videoset_names:
		cameras += videosets[vset].cameras
	return cameras


def get_videoset_cameras(videoset_names):
	cameras = []
	for vset in videoset_names:
		cameras += [vset + "|" + cam for cam in videosets[vset].cameras]
	return cameras


# camera_lut = []
# for vset in videoset_names:
#     camera_lut] += [vset + "|" + cam for cam in videosets[vset].cameras]
videoset_cameras = get_videoset_cameras(videoset_names)


@dataclass
class CameraSelector(MenuItemMultiStr):
	videoset_selector: MenuItemMultiStr = None

	def select(self):
		self.options = []
		for videoset in self.videoset_selector.selected:
			self.options += videosets[videoset].cameras
		return super().select()


videoset_selector = MenuItemMultiStr("videoset", _selected=[], options=videoset_names)
camera_selector = CameraSelector(
	"camera", _selected=[], options=None, videoset_selector=videoset_selector
)


def filter_items(videosets, items):
	items_filtered = []
	for item in items:
		if item["camera"] in videosets[item["videoset"]].cameras:
			items_filtered.append(item)
	return items_filtered


if __name__ == "__main__":
	# from termlit.selection import TaskProcessor

	# def task(config):
	#     print(f"running {config}")
	#     time.sleep(600)

	# processor = TaskProcessor(task)
	queue_file = Path("processing_app_queue.csv")
	menu_items = [
		videoset_selector,
		camera_selector,
		MenuItemMultiStr("experiment", _selected=[], options=["proposed", "clipped"]),
		MenuItemBool("use tensorrt", True),
		MenuItemFloat("confidence", 0.1),
		# QueueControl("queue", processer=processor),
	]
	while True:
		items = Menu(menu_items, "processing_app").run()
		items_filtered = filter_items(videosets, items)
		import pandas as pd

		df = pd.DataFrame(items_filtered)
		if not queue_file.exists():
			df.to_csv(queue_file, index=False)
		else:
			df.to_csv(queue_file, index=False, header=False, mode="a")
		print()
		print(f"added {len(df)} items, press any key to continue")
		click.getchar()
