# %%
# load import shutil


import pandas as pd
from config.dataset import get_tie

from config.writers import PreAnnotationWriter

datasets = get_tie()
datas = []
for config in datasets:
    prewriter = PreAnnotationWriter(config, [0, -15, 15])
    source_detections = prewriter.load_annotation_source()
    prev_annotations = config.pathfinder.media_manager.load_annotations(
        "smallObjectsCorrected"
    )
    # if not prev_annotations is None and not source_detections is None:
    # ratio = len(source_detections) / len(prev_annotations)
    duration = max(config.pathfinder.media_manager.timestamps) - min(
        config.pathfinder.media_manager.timestamps
    )
    dout = dict(
        camera=config.pathfinder.camera,
        duration=duration,
        detections=len(source_detections) if not source_detections is None else 0,
        annotations=len(prev_annotations) if not prev_annotations is None else 0,
    )
    datas.append(dout)
pd.DataFrame(datas).to_csv("annotations.csv", index=False)

# print(ratio)

# if len()
# data = []
# if not prev_annotations is None:
# 	# Create a Plotly scatter plot for the previous and new annotations
# 	trace_tracks_yolo = go.Scatter(
# 		x=prev_annotations.timestamp,
# 		y=prev_annotations.bbox_x,
# 		mode="markers",
# 		name="prev",
# 	)
# 	data.append(trace_tracks_yolo)
