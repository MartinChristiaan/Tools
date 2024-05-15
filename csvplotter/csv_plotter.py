
import scienceplots
from dataclasses import dataclass
import argparse

from matplotlib import pyplot as plt
plt.style.use("science")
import pandas as pd
import termlit.selection as s

#argparse with which selects the csv file

argparser = argparse.ArgumentParser(description="Plot a CSV file")
argparser.add_argument("-p","--csv_path", default="/mnt/dl-41/data/leeuwenmcv/general/mantis_mist/mist_combined_prcurve_roc_data.csv",help="Path to the CSV file", type=str)
args = argparser.parse_args()

df = pd.read_csv(args.csv_path)
columns = list(df.columns)

menu = [
	# s.MenuItemStr("csv_path",args.csv_path),
	s.MenuItemSelectStr("x",columns[0],columns),
	s.MenuItemSelectStr("y",columns[1],columns),
	s.MenuItemSelectStr("pivot_column",columns[2],columns),
	s.MenuItemStr("x_label", "auto"),
	s.MenuItemStr("y_label", "auto"),
	s.MenuItemInt('fig_size_x',4),
	s.MenuItemInt('fig_size_y',3),
	s.MenuItemFloat('x_min',0),
	s.MenuItemFloat('x_max',1.1),
	s.MenuItemFloat('y_min',0),
	s.MenuItemFloat('y_max',1.1),
]

config = s.Menu(menu, "Plot CSV file").run(True)[0]

@dataclass
class PlotConfig:
	x: str
	y: str
	pivot_column: str
	x_label: str
	y_label: str
	fig_size_x: int
	fig_size_y: int
	x_min : float
	y_min : float
	x_max : float
	y_max : float

configs = PlotConfig(**config)


groups = []
if configs.pivot_column == "":
	groups = [("",df)]
else:
	groups = df.groupby(configs.pivot_column)


plt.figure()
for groupname,group_df in groups:
	plt.plot(group_df[configs.x],group_df[configs.y],label=groupname)

if configs.x_label == "auto":
	plt.xlabel(configs.x)
else:
	plt.xlabel(configs.x_label)

if configs.y_label == "auto":
	plt.ylabel(configs.y)
else:
	plt.ylabel(configs.y_label)
plt.xlim(configs.x_min,configs.x_max)
plt.ylim(configs.y_min,configs.y_max)
plt.legend()
plt.grid(1)
plt.show()









