# %%
from pathlib import Path
from loguru import logger
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.io import loadmat
import os

import streamlit as st
from tqdm import tqdm

from Project import Project
from typing import List

st.set_page_config(layout="wide")


def get_data(years):
    matdir = Path(
        r"\\tsn.tno.nl\data\sv\sv-091547\kluis\algemeen_intern\planning\ourplan\dailydump\matfolder"
    )
    mat_dict = {}
    for year in years:
        year = str(year)

        mats_year = list((matdir / year).rglob("*.mat"))
        # print(year, mats_year)
        if len(mats_year) == 0:
            continue
        mats_year.sort()
        latest_mat_year = mats_year[-1]
        mat_dict[year] = latest_mat_year

    # Start by getting active projects
    for year, matfile in mat_dict.items():
        data = loadmat(matfile)
        mat_dict[year] = data
    return mat_dict


# data = get_data()


# %%
def get_employee_index(employee, data):

    employees = [x[0][0] for x in data["Employees"]]
    employee_index = 0
    for i, e in enumerate(employees):
        if not employee in e.lower():
            continue
        employee_index = i
        break
    return employee_index


def extract_projects(mat_dict) -> List[Project]:

    total_num_weeks = 0
    all_active_projects = []
    employee = "m.c. van leeuwen"
    for year, data in mat_dict.items():

        employee_index = get_employee_index(employee, data)
        projects = [x[1][0] for x in data["WBS"]]

        planned_hours = data["PlannedHours"][:, :, employee_index]
        realised_hours = data["RealisedHours"][:, :, employee_index]
        # get project ids with planned or realised hours
        combined_hours = planned_hours + realised_hours
        combined_hours = combined_hours.sum(axis=0)
        active_projects = np.argwhere(combined_hours > 0)

        all_active_projects += [projects[i[0]] for i in active_projects]
        total_num_weeks += planned_hours.shape[0]

    all_active_projects = list(set(all_active_projects))
    project_objects = []
    logger.info(f"{total_num_weeks} weeks considered")
    for project in all_active_projects:
        project_cls = Project(
            project, np.zeros(total_num_weeks), np.zeros(total_num_weeks)
        )
        week_0 = 0
        for year, data in mat_dict.items():
            employee_index = get_employee_index(employee, data)
            projects = [x[1][0] for x in data["WBS"]]
            num_weeks = data["PlannedHours"].shape[0]
            if not project in projects:
                print(f"continueing for {year}")
                week_0 += num_weeks
                continue
            project_id = projects.index(project)

            project_cls.planned_hours[week_0 : week_0 + num_weeks] = data[
                "PlannedHours"
            ][:, project_id, employee_index]
            # print(project, project_cls.planned_hours)
            # print(data["RealisedHours"][:, project_id, employee_index])

            project_cls.realised_hours[week_0 : week_0 + num_weeks] = data[
                "RealisedHours"
            ][:, project_id, employee_index]
            week_0 += num_weeks
            # break
        project_objects.append(project_cls)
    return project_objects


@st.cache_data
def get_projects(years):
    return extract_projects(get_data(years))


# %%
from datetime import datetime

st.title("Hourplan viewer")
current_year = datetime.now().year
start_year = st.slider(
    "starting year", current_year - 1, current_year, current_year - 1
)

end_year = st.slider("end_year", current_year, current_year + 4, current_year)
years = list(range(start_year, end_year + 1))


projects = get_projects(years)
active_project_names = [x.name for x in projects]


project = st.selectbox("Project", active_project_names)


def select_project(project, active_project_names) -> Project:
    project_index = active_project_names.index(project)
    project = projects[project_index]
    return project


startingpoint = st.slider("starting week", 0, len(projects[0].planned_hours) - 2)
project = select_project(project, active_project_names)
planned = np.cumsum(project.planned_hours[startingpoint:])
real = np.cumsum(project.realised_hours[startingpoint:])

hours_spent = real.max()
hours_remaining = planned.max() - hours_spent
budget_percent_remaining = hours_remaining / planned.max() * 100

date_range = pd.date_range(start="2023-01-01", end="2024-12-31", freq="W")[
    startingpoint:
]
# %%
print(len(date_range))

fig = go.Figure()
fig.add_trace(go.Scatter(x=date_range, y=planned, mode="lines", name="Planned"))

fig.add_trace(go.Scatter(x=date_range, y=real, mode="lines", name="Real"))
fig.update_layout(title="Planned vs Real", xaxis_title="Date", yaxis_title="Hours")
st.plotly_chart(fig, use_container_width=True)
st.write(
    f"{hours_spent}hrs used, {hours_remaining}hrs remaining. {budget_percent_remaining:.0f}% of total budget for this period"
)

# TODO add hours remaining in total
# TODO add ahead or behind planning
