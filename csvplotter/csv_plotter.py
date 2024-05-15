
import argparse
import termlit.selection as s

#argparse with which selects the csv file

argparser = argparse.ArgumentParser(description="Plot a CSV file")
argparser.add_argument("csv_path", help="Path to the CSV file",default="/mnt/dl-41/data/leeuwenmcv/general/mantis_mist/mist_combined_prcurve_roc_data.csv")
args = argparser.parse_args()

menu = [
	s.MenuItemStr("csv_path",args.csv_path),
	s.MenuItemStr("x_label", "X-axis label")
	s.MenuItemStr("y_label", "Y-axis label")
]

s.Menu(menu, "Plot CSV file")





