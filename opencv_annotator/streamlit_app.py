import plotly.graph_objs as go

import streamlit as st

import pandas as pd

from pathlib import Path

# %%
# %load_ext autoreload
# %autoreload 2
# Require


# Streamlit, select config + show xt_plot?

import argparse
import pickle
from pathlib import Path

from loguru import logger
import pandas as pd
from config.dataset import all_configs
import fnmatch
import dlutils_ii as du

from opencv_annotator.annotator import BoundingBoxAnnotator
from config.writers import writers, label_config, PreAnnotationWriter

import streamlit as st


# parser = argparse.ArgumentParser(prog="ProgramName", description="Description")
# parser.add_argument("-c", "--config", type=str, default="*TIE*")
# parser.add_argument("-a", "--action", type=str, default="annotate")
# parser.add_argument("-w", "--writer", type=str, default="tyolo_writer")

# parser.add_argument("-s", "--start_idx", type=int, default=1)
# parser.add_argument("-n", "--num_items", type=int, default=5)
# args = parser.parse_known_args()[0]


datasets = all_configs


videoset = st.selectbox("videoset", list({x.pathfinder.videoset for x in datasets}))
cameras = list(
    {
        x.pathfinder.camera
        for x in datasets
        if len(x.pathfinder.camera) > 0 and x.pathfinder.videoset == videoset
    }
)
cameras.sort()
camera = st.selectbox("camera", cameras)
writer = st.selectbox("writer", list(writers.keys()))

config = [
    x
    for x in datasets
    if x.pathfinder.camera == camera and x.pathfinder.videoset == videoset
][0]

prewriter = PreAnnotationWriter(config, [0, -15, 15])
source_detections = prewriter.load_annotation_source()
import plotly.express as px

fig = px.scatter(source_detections, x="timestamp", y="bbox_x", color="track_id")
st.plotly_chart(fig)


# Assuming paths is your list of Path objects
prev_annotations = config.pathfinder.media_manager.load_annotations(
    "smallObjectsCorrected"
)
print(prev_annotations)
if not prev_annotations is None:
    # Create a Plotly scatter plot for the previous and new annotations
    trace_tracks_yolo = go.Scatter(
        x=prev_annotations.timestamp,
        y=prev_annotations.bbox_x,
        mode="markers",
        name="prev",
    )

    tmp_path = config.pathfinder.annotations_path.with_suffix(".tmp.csv")
    if tmp_path.exists():
        annotations = pd.read_csv(tmp_path)

        trace_new = go.Scatter(
            x=annotations.timestamp, y=annotations.bbox_x, mode="markers", name="new"
        )
        data = [trace_tracks_yolo, trace_new]
    else:
        data = [trace_tracks_yolo]

    # Create layout
    layout = go.Layout(
        title="Scatter Plot of Annotations",
        xaxis=dict(title="timestamp"),
        yaxis=dict(title="bbox_x"),
        hovermode="closest",
    )
    # Create a Plotly figure
    fig = go.Figure(data=data, layout=layout)

    # Display Plotly figure using Streamlit
    st.plotly_chart(fig)


if st.button("write"):
    writer = writers[writer]
    writer(config, [0, -15, 15], label_config).write()

if st.button("annotate"):
    BoundingBoxAnnotator.annotate_config(config)
if st.button("save"):
    BoundingBoxAnnotator.save(config)


# action_lut = dict(export=export_fn, annotate=BoundingBoxAnnotator.annotate_config)
# for action in args.action.split(","):
#     for d in datasets[args.start_idx : args.num_items]:
#         action_lut[action](d)
