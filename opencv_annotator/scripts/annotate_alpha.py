# %%
%load_ext autoreload
%autoreload 2

import os

from annotator import BoundingBoxAnnotator
from cache_annotator import IOManager
from config.dataset import get_mantis, get_webcams_2023

alpha = get_webcams_2023()[0]
import dlutils_ii as du

annotator = BoundingBoxAnnotator(alpha)
annotator.run()




# cv2.destroyWindow()
# %%
