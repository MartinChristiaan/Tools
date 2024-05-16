from pathlib import Path
from dlutils_ii import DatasetConfig
import termlit.selection as st
from termlit.videosets import videoset_selector, camera_selector

data_dir = Path("/diskstation/panoptes/sod/cache")

import dlutils_ii as du

# first select videosets/cameras
menu = [videoset_selector, camera_selector]
