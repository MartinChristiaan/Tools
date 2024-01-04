# %%
%load_ext autoreload
%autoreload 2


import dlutils_ii as du
from annotator import BoundingBoxAnnotator
from cache_annotator import IOManager
from scripts.dataset_config import get_mantis

mantis = get_mantis()
BoundingBoxAnnotator(mantis[10]).run()
