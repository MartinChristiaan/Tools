# %%
%load_ext autoreload
%autoreload 2


import os

from cache_annotator import IOManager
from scripts.dataset_config import get_mantis

IOManager(get_mantis()).run()
