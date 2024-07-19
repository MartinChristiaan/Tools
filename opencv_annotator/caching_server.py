# %%
from pathlib import Path
from dlutils_ii import DatasetConfig
import termlit.selection as st
from termlit.videosets import (
    filter_items,
    videoset_selector,
    camera_selector,
    find_result_csv_in_mm_path,
    videosets,
)
import os
from pathlib import Path
from loguru import logger
from videosets_ii.videosets_ii import VideosetsII
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks, TrackUpdates
import pandas as pd


import dlutils_ii as du


def get_sod_label_config():
    """standard label config for SOD experiments which involve only an object class."""
    sod_label_config = du.LabelConfig(
        {"object": 0, "ignore_area": 1, "ignore": 1, "ignore_area_seq": 2},
        ["object", "ignore_area", "ignore_area_seq"],
        ["ignore_frame"],
    )
    return sod_label_config


def main():
    debug = False
    data_dir = Path("/diskstation/panoptes/sod/cache")
    # first select videosets/cameras
    items = st.Menu([videoset_selector, camera_selector], "MM_selector").run(debug)
    items_filtered = filter_items(videosets, items)
    # for config in configs:

    mm = videosets[items_filtered[0]["videoset"]].get_mediamanager(
        items_filtered[0]["camera"]
    )

    data_options = list(map(str, find_result_csv_in_mm_path(mm)))
    additional_options = st.Menu(
        [
            st.MenuItemReturnGlob("data_glob", options=data_options),
            st.MenuItemInt("max_samples", 1000),
            st.MenuItemFloat("min_temporal_spacing", 2),
        ],
        "additional caching options",
    ).run(debug)[0]
    from opencv_annotator.pre_annotation_writer import MixedSourceWriter

    for item in items_filtered:
        # pathfinder = du.Pathfinder(
        #     **item, basedir="/local_diskstation", cache_dir=data_dir
        # )

        pathfinder = du.Pathfinder(**item, cache_dir=data_dir)
        train_config = du.TrainOptions(
            False,
            [0, -15, 15],
            max_samples=additional_options["max_samples"],
            min_temporal_spacing=additional_options["min_temporal_spacing"],
        )
        dataset_config = du.DatasetConfig(pathfinder, train_config)
        # raise Exception()
        writer = MixedSourceWriter(
            dataset_config,
            additional_options["data_glob"],
            [0, -15, 15],
            get_sod_label_config(),
        )
        writer.write()


if __name__ == "__main__":
    main()
