# %%
import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from tqdm import tqdm

# set wide layout
st.set_page_config(layout="wide")


ourplan = pd.read_csv("./ourplan_januari_2024.csv")

plan_columns = [c for c in ourplan.columns if c.startswith("Plan ")]
real_columns = [c for c in ourplan.columns if c.startswith("Real ")]

planned_dates = [
    "x" + c.split(" ")[3] + " " + c.split(" ")[2].replace("*", "wk")
    for c in plan_columns
]
real_dates = [
    "x" + c.split(" ")[3] + " " + c.split(" ")[2].replace("*", "wk")
    for c in real_columns
]
print(planned_dates[0])

# add slider to control which dates are processed
start_date = st.slider("Start date", 0, len(plan_columns) - 1, 0)
end_date = st.slider("End date", 0, len(plan_columns) - 1, len(plan_columns) - 1)


os.makedirs("project_plots", exist_ok=True)

# streamlit selection
st.title("Project planner")
project = st.selectbox("Project", ourplan["Project name"].unique())


row = ourplan[ourplan["Project name"] == project].iloc[0]

planned = np.cumsum([row[c] for c in plan_columns[start_date:end_date]])
real = np.cumsum([row[c] for c in real_columns[start_date:end_date]])

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=planned_dates[start_date:end_date], y=planned, mode="lines", name="Planned"
    )
)
fig.add_trace(
    go.Scatter(x=real_dates[start_date:end_date], y=real, mode="lines", name="Real")
)
fig.update_layout(title="Planned vs Real", xaxis_title="Date", yaxis_title="Hours")
st.plotly_chart(fig, use_container_width=True)
