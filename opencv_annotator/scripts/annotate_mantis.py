# %%
%load_ext autoreload
%autoreload 2

from annotator import BoundingBoxAnnotator
from cache_annotator import IOManager
from scripts.dataset_config import get_mantis

mantis = get_mantis()
from pre_annotation_writer import PreAnnotationWriter

for config in mantis:
	writer  = PreAnnotationWriter(config,[0,-15,15],source="tyolov8/tracks_tyolov8m-30112023.csv")
import dlutils_ii as du

annotator = BoundingBoxAnnotator(mantis)
annotator.run()




# cv2.destroyWindow()
# %%
