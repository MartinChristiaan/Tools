# %%
%load_ext autoreload
%autoreload 2


import dlutils_ii as du
from opencv_annotator.annotator import BoundingBoxAnnotator
from opencv_annotator.cache_annotator import IOManager
from scripts.dataset_config import get_mantis

mantis = get_mantis()
BoundingBoxAnnotator(mantis[0]).run()
