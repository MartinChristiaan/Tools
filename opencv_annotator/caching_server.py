from pathlib import Path
from dlutils_ii import DatasetConfig
import termlit.selection as st
from termlit.videosets import (
    filter_items,
    videoset_selector,
    camera_selector,
    find_result_csv_in_mm_path,
    videosets,
)
import os
from pathlib import Path
from loguru import logger
from videosets_ii.videosets_ii import VideosetsII
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks, TrackUpdates
import pandas as pd


data_dir = Path("/diskstation/panoptes/sod/cache")

import dlutils_ii as du

# first select videosets/cameras
items = st.Menu([videoset_selector, camera_selector], "MM selector").run()
items_filtered = filter_items(videosets, items)
# for config in configs:

mm = videosets[items_filtered[0]["videoset"]].get_mediamanager(
    items_filtered[0]["camera"]
)
data_options = find_result_csv_in_mm_path(mm)
selected_options = st.Menu(st.MenuItemMultiStr("data", options=data_options))

for item in filter_items:




# then select
