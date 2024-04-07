# %%
import pandas as pd
from mm_io_manager import IOData
from pathlib import Path


def track_classification_plot(
    detections: pd.DataFrame,
    annotations: pd.DataFrame,
    experiment="yolov8m",
    camera="cam",
    timestamp=0,
):
    # if "confidence" in detections.columns:
    #     detections = detections[detections.confidence > 0.15]

    # Set up the figure with two subplots
    annotations = annotations.fillna(3000)
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True, sharey=True)

    # Calculate the min and max values of color_axis_values across both subplots

    vmin, vmax = 0, 3500

    for i_source, source_df in enumerate([detections, annotations]):
        source_df.track_classification = [
            x.split("_0m")[0].split("_300m")[0].split("_600m")[0].split("_1200m")[0]
            for x in source_df.track_classification
        ]
        dim = "x"

        axs[i_source].set_title(
            camera + " : " + (experiment if i_source == 0 else "annotations")
        )
        for classification, class_df in source_df.groupby("track_classification"):

            x_axis_values = class_df[f"timestamp"]
            y_axis_values = class_df[f"bbox_{dim}"]
            color_lut = {
                "succesfull_encounter": "green",
                "failed_encounter": "red",
                "false_alarm": "red",
                "partial": "orange",
                "ignored": "gray",
            }
            scatter = axs[i_source].scatter(
                x_axis_values,
                y_axis_values,
                s=2,
                vmin=vmin,
                vmax=vmax,
                label=classification,
                color=color_lut[classification],
            )
        axs[i_source].plot([timestamp, timestamp], [0, max(source_df.bbox_x)])
        axs[i_source].set_ylabel(f"{dim}_center")
        axs[i_source].set_xlabel(f"timestamp")
        axs[i_source].grid(1)
        axs[i_source].legend()

    plt.savefig(
        f"/data/l3_harris/{experiment}/{camera.replace('/','_')}_classifications.png"
    )


saves = list(Path("saves").glob("*.pkl"))
saves.sort()
for save in saves:
    recent = IOData.load(saves[-1])

    import matplotlib.pyplot as plt

    data = recent.detections
    num_subplots = len(recent.selected_sources)
    fig, axs = plt.subplots(num_subplots, 1, figsize=(10, 6 * num_subplots))

    if num_subplots == 1:
        axs = [axs]

    dfs = []
    for i, (source, df_s) in enumerate(data.groupby("source")):
        dfs.append(df_s)

    track_classification_plot(
        dfs[1], dfs[0], "yolov8s_precision_20240301", recent.camera, recent.timestamp
    )

    # def plot_datadict_subplots(datadicts):
    #     num_subplots = len(datadicts)

    #     if num_subplots == 1:
    #         axs = [axs]

    #     for i, datadict in enumerate(datadicts):
    #         print(datadict)
    #         if datadict["mode"] == "markers":
    #             if "markers" in datadict:
    #                 axs[i].scatter(
    #                     datadict["x"],
    #                     datadict["y"],
    #                     c=datadict["marker"]["color"],
    #                     cmap="magma",
    #                     ms=1,
    #                 )
    #             else:
    #                 axs[i].scatter(datadict["x"], datadict["y"], s=2)
    #         else:
    #             axs[i].plot(datadict["x"], datadict["y"], label=datadict["name"])
    #         axs[i].set_xlabel("timestamp")
    #         axs[i].set_ylabel("bbox_x")
    #         axs[i].legend()

    #     plt.tight_layout()
    #     plt.show()

    # datadicts = []

    # for source in recent.selected_sources:
    #     datadicts_source = recent.get_xt_plot(source)
    #     for d in datadicts_source:
    #         d["source"] = source
    #     datadicts += datadicts_source
    # plot_datadict_subplots(datadicts)
