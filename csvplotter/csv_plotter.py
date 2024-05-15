
import argparse

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
	s.MenuItemMultiStr("x",[columns[0]],columns),
	s.MenuItemMultiStr("y",columns[1:],columns),
	s.MenuItemStr("x_label", "X-axis label"),
	s.MenuItemStr("y_label", "Y-axis label")
]

configs = s.Menu(menu, "Plot CSV file").run(True)
print(configs)








