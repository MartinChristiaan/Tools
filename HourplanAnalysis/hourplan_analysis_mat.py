# %%
from scipy.io import loadmat
import os

home = os.path.expanduser("~")
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

# get projects

projects = [x[0][0] for x in data["WBS"]]
print(projects)


# print(data["Employees"][0][0])


# print(data["RealisedHours"].shape)
