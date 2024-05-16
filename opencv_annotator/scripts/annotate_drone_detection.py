# %%
%load_ext autoreload
%autoreload 2


import dlutils_ii as du
import pandas as pd
from opencv_annotator.annotator import BoundingBoxAnnotator
from opencv_annotator.cache_annotator import IOManager
from yolo_plugins.training.yolo_experiment import SODExperiment, get_sod_label_config

from config.dataset import drone_detection_dataset,drone_tracking_dataset


datasets =  drone_detection_dataset()
du.Writer.export_multiprocessed(datasets,[0,-15,15],labelconfig=get_sod_label_config())
#%%
index =11
# print(datasets[index].pathfinder.name)
BoundingBoxAnnotator(datasets[index]).run()
#%%
x = datasets[index]
tmp_path = x.pathfinder.annotations_path.with_suffix(".tmp.csv")
annotations = pd.read_csv(tmp_path)
# x.pathfinder.media_manager.save_annotations(annotations, "smallObjectsCorrected", True)
	# print('uploaded')





