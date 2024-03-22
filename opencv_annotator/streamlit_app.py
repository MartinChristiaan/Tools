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
from config.writers import writers, label_config
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
camera = st.selectbox("camera", list({x.pathfinder.camera for x in datasets}))
writer = st.selectbox("writer", list(writers.keys()))

config = [
    x
    for x in datasets
    if x.pathfinder.camera == camera and x.pathfinder.videoset == videoset
][0]


# Assuming paths is your list of Path objects
prev_annotations = config.pathfinder.media_manager.load_annotations(
    "smallObjectsCorrected"
)
if prev_annotations:
    # Create a Plotly scatter plot for the previous and new annotations
    trace_prev = go.Scatter(
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
        data = [trace_prev, trace_new]
    else:
        data = [trace_prev]

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

# action_lut = dict(export=export_fn, annotate=BoundingBoxAnnotator.annotate_config)
# for action in args.action.split(","):
#     for d in datasets[args.start_idx : args.num_items]:
#         action_lut[action](d)
