# %%
%load_ext autoreload
%autoreload 2

from annotator import BoundingBoxAnnotator
from cache_annotator import IOManager
from scripts.dataset_config import get_mantis

mantis = get_mantis()
import dlutils_ii as du

annotator = BoundingBoxAnnotator(mantis)
annotator.run()




# cv2.destroyWindow()
# %%
