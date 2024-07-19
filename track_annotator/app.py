# %%
# Plan
# load track_updates
# Select current rows to use (Also maintain which tracks have been seen already) -> use some king of saved appstate
# drawer class for drawing
# app class for app things
# data management class for loading data (serve tracks to rate, save annotations?)

# %%

import cv2
import dlutils_ii as du
import numpy as np
import streamlit as st
from AnnotationWriter import AnnotationWriter
from config import get_example_dataset_configs
from detection_provider import DetectionProvider

st.set_page_config("Track Annotator", layout="wide")
NUM_COLS = 4


class App:
    def __init__(self) -> None:
        self.batch_id = 0


@st.cache_resource
def setup(config_index=0):
    # configs = get_example_dataset_configs()
    pf = du.Pathfinder("mantis_drone_2023", "DJI_202309100220_001/wide_hd")
    detection_provider = DetectionProvider(pf, "tyolov8/tracks_tyolov8m-30112023.csv")
    app = App()
    annotation_writer = AnnotationWriter(pf)
    return app, detection_provider, annotation_writer


app, detection_provider, annotation_writer = setup()


@st.cache_resource
def get_images_cached(batch_id):
    return detection_provider.get_images(app.batch_id)


updatedata = get_images_cached(app.batch_id)
columns = st.columns(NUM_COLS)
img_idx = 0

for i, update in enumerate(updatedata):
    with columns[i % NUM_COLS]:
        st.image(update.image, f"track_id:{update.track_id}")
        if i == len(updatedata) - 1 or update.track_id != updatedata[i + 1].track_id:
            if st.button("Accept all", key=f"{i}acceptall"):
                row_ids = [
                    d.row_id for d in updatedata if d.track_id == update.track_id
                ]
                detections = detection_provider.get_rows(row_ids)
                annotation_writer.accept_detection(detections)

# %%
