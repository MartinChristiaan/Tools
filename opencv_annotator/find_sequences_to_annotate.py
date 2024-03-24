# %%
# load import shutil



from config.dataset import get_tie

from config.writers import PreAnnotationWriter

datasets = get_tie()
for config in datasets:
    prewriter = PreAnnotationWriter(config, [0, -15, 15])
    source_detections = prewriter.load_annotation_source()
    prev_annotations = config.pathfinder.media_manager.load_annotations(
        "smallObjectsCorrected"
    )
    print(len(prev_annotations), print(len(source_detections)))
    ratio = len(source_detections) / len(prev_annotations)
    print(ratio)

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
