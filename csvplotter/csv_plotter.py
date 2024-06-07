import numpy as np
import scienceplots
from dataclasses import dataclass
import argparse

from matplotlib import pyplot as plt

plt.style.use("science")
import pandas as pd
import termlit.selection as s

# argparse with which selects the csv file

argparser = argparse.ArgumentParser(description="Plot a CSV file")
argparser.add_argument(
    "-p", "--csv_path", default="mantis_mist.csv", help="Path to the CSV file", type=str
)
args = argparser.parse_args()

df = pd.read_csv(args.csv_path)
columns = list(df.columns)


menu = [
    # s.MenuItemStr("csv_path",args.csv_path),
    s.MenuItemSelectStr("plot_type", "line", ["line", "scatter", "bar"]),
    s.MenuItemSelectStr("x", columns[0], columns),
    s.MenuItemSelectStr("y", columns[0], columns),
    s.MenuItemSelectStr("pivot_column", "", columns + [""]),
    s.MenuItemSelectStr("facet_row", "", columns + [""]),
    s.MenuItemStr("x_label", "auto"),
    s.MenuItemStr("y_label", "auto"),
    s.MenuItemInt("fig_size_x", 4),
    s.MenuItemInt("fig_size_y", 3),
    s.MenuItemFloat("x_min", 0),
    s.MenuItemFloat("x_max", 1.1),
    s.MenuItemFloat("y_min", 0),
    s.MenuItemFloat("y_max", 1.1),
]
while True:
    config = s.Menu(menu, "Plot CSV file").run(False)[0]

    @dataclass
    class PlotConfig:
        plot_type: str
        x: str
        y: str
        pivot_column: str
        facet_row: str
        x_label: str
        y_label: str
        fig_size_x: int
        fig_size_y: int
        x_min: float
        y_min: float
        x_max: float
        y_max: float

    configs = PlotConfig(**config)

    groups_facet = []
    if configs.facet_row == "" or configs.facet_row == None:
        groups_facet = [("", df)]
    else:
        groups_facet = df.groupby(configs.facet_row)

    fig, axs = plt.subplots(
        1,
        len(groups_facet),
        figsize=(configs.fig_size_x * len(groups_facet), configs.fig_size_y),
    )
    if len(groups_facet) == 1:
        axs = [axs]

    for (groupname, df_facet_group), ax in zip(groups_facet, axs):
        if groupname != "":
            ax.set_title(groupname)
        groups_pivot = []
        if configs.pivot_column == "" or configs.pivot_column == None:
            groups_pivot = [("", df_facet_group)]
        else:
            groups_pivot = df_facet_group.groupby(configs.pivot_column)

        for i, (groupname, group_df) in enumerate(groups_pivot):
            if configs.plot_type == "line":
                ax.plot(group_df[configs.x], group_df[configs.y], label=groupname)
            elif configs.plot_type == "scatter":
                ax.scatter(group_df[configs.x], group_df[configs.y], label=groupname)
            elif configs.plot_type == "bar":
                xpositions = np.arange(len(group_df[configs.x])) + 0.4 * i
                width = 0.8 / len(groups_pivot)
                ax.bar(xpositions, group_df[configs.y], width=width, label=groupname)

        if configs.plot_type == "bar":
            xpositions = np.arange(len(group_df[configs.x])) - 0.2  # * 0.5 * len(
            ax.set_xticks(xpositions + width / 2)
            ax.set_xticklabels(group_df[configs.x], rotation=45)

            # ax.plot(group_df[configs.x], group_df[configs.y], label=groupname)

        if configs.x_label == "auto":
            ax.set_xlabel(configs.x)
        else:
            ax.set_xlabel(configs.x_label)

        if configs.y_label == "auto":
            ax.set_ylabel(configs.y)
        else:
            ax.set_ylabel(configs.y_label)

        # plt.xlim(configs.x_min,configs.x_max)
        # plt.ylim(configs.y_min,configs.y_max)
        ax.set_ylim(configs.y_min, configs.y_max)
        ax.legend()
        ax.grid(1)
    plt.savefig(args.csv_path.replace(".csv", ".png"), dpi=500, transparent=True)
    plt.savefig(args.csv_path.replace(".csv", ".pdf"), dpi=500, transparent=True)
