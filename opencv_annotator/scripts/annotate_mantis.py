# %%
# %load_ext autoreload
# %autoreload 2

import os
import sys

import cv2
import loguru
from cache_annotator import CacheAnnotator

from dataset_config import get_mantis

# loguru.logger.add(sys.stdout, level="INFO")

mantis = get_mantis()
# mantis.pathfinder.annotations_path.with_suffix(".tmp")
# try:
#     os.remove(CacheAnnotator(mantis).tmp_annotation_path)
# except:
#     pass

annotator = CacheAnnotator(mantis)
# if annotator.tmp_annotation_path.exists():
#     os.remove(annotator.tmp_annotation_path)
annotator.run()

# cv2.destroyWindow()
# %%
