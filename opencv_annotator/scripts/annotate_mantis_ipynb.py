# %%
%load_ext autoreload
%autoreload 2


import os
from cache_annotator import CacheAnnotator
from dataset_config import get_mantis


CacheAnnotator(get_mantis()).run()
