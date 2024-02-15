# %%
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy.io import loadmat
import os

import streamlit as st
from tqdm import tqdm

# set wide layout
st.set_page_config(layout="wide")

home = os.path.expanduser("~")


matdir = Path(
    r"\\tsn.tno.nl\data\sv\sv-091547\Kluis\Algemeen_intern\Planning\ourplan\DailyDump\\"
)
print(list(matdir.glob('*')))
#%%


data = loadmat(f"{home}/OurPlanDump_II_2024_240126.mat")
# %%
print(data.keys())
for key in data.keys():
    try:
        print(key, data[key].shape)
    except:
        pass

# %%
# locate employee
employees = [x[0][0] for x in data["Employees"]]
employee = "m.c. van leeuwen"

employee_index = 0
for i, e in enumerate(employees):
    if not employee in e.lower():
        continue
    employee_index = i
    print(e)
    break

# %% get projects

# streamlit selection
st.title("Project planner")


projects = [x[1][0] for x in data["WBS"]]

planned_hours = data["PlannedHours"][:, :, employee_index]
realised_hours = data["RealisedHours"][:, :, employee_index]


# get project ids with planned or realised hours
combined_hours = planned_hours + realised_hours
combined_hours = combined_hours.sum(axis=0)
active_projects = np.argwhere(combined_hours > 0)
active_projects_labels = [projects[i[0]] for i in active_projects]
project = st.selectbox("Project", active_projects_labels)
project_index = projects.index(project)

planned = np.cumsum(planned_hours[:, project_index])
real = np.cumsum(realised_hours[:, project_index])

fig = go.Figure()
fig.add_trace(
    go.Scatter(x=np.arange(len(planned)), y=planned, mode="lines", name="Planned")
)
fig.add_trace(go.Scatter(x=np.arange(len(planned)), y=real, mode="lines", name="Real"))
fig.update_layout(title="Planned vs Real", xaxis_title="Date", yaxis_title="Hours")
st.plotly_chart(fig, use_container_width=True)

# TODO add hours remaining in total
# TODO add ahead or behind planning
