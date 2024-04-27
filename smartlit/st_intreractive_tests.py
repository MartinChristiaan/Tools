import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_plotly_events import plotly_events

if not "xpos" in st.session_state:
    st.session_state["xpos"] = []


@st.cache_data
def get_data():
    timestamps = np.arange(1000)
    x = np.random.random(1000)
    track_id = np.ones(1000, dtype=np.int32)
    df = pd.DataFrame(dict(timestamps=timestamps, x=x, track_id=track_id))
    return df


data = get_data()


def create_plot(
    _df,
    x_axis_label,
    y_axis_label,
    color_column,
    _plotting_fn,
    cameara="",
    videoset="",
    data_name="",
):
    fig = _plotting_fn(
        _df,
        x_axis_label,
        y_axis_label,
        color_column,
        color_discrete_sequence=[
            "#0068c9",
            "#83c9ff",
            "#ff2b2b",
            "#ffabab",
            "#29b09d",
            "#7defa1",
            "#ff8700",
            "#ffd16a",
            "#6d3fc0",
            "#d5dae5",
        ],
        title="XT Plot",
    )

    return fig


fig = create_plot(data, "timestamps", "x", "track_id", px.line)
for x in st.session_state["xpos"]:
    fig.add_vline(x)
selected_points = plotly_events(fig)
if len(selected_points) > 0:
    st.session_state["xpos"] += [selected_points[0]["x"]]
