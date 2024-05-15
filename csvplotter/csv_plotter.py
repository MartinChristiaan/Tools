
from dataclasses import dataclass
import argparse

from matplotlib import pyplot as plt
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
	s.MenuItemStr("y_label", "auto")
]

config = s.Menu(menu, "Plot CSV file").run(True)[0]

@dataclass
class PlotConfig:
	x: str
	y: str
	pivot_column: str
	x_label: str
	y_label: str

configs = PlotConfig(**config)




# plt.figure()
# plt.plot(df[configs["x"]],df[configs["y"]])

# for config in configs:









