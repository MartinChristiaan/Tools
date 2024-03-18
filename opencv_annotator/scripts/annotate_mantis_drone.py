# %%
%load_ext autoreload
%autoreload 2


import dlutils_ii as du
from opencv_annotator.annotator import BoundingBoxAnnotator
from opencv_annotator.cache_annotator import IOManager
from yolo_plugins.training.yolo_experiment import SODExperiment, get_sod_label_config

from scripts.dataset_config import get_mantis


mantis = get_mantis()
du.Writer.export_multiprocessed(mantis,[0,-15,15],labelconfig=get_sod_label_config())
index =0 
print(mantis[index].pathfinder.name)
BoundingBoxAnnotator(mantis[index]).run()
