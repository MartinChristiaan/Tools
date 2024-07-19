# %%
%load_ext autoreload
%autoreload 2


import os

from cache_annotator import IOManager
from config.dataset import get_mantis

IOManager(get_mantis()).run()
