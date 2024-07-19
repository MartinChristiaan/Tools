# %%
import termlit.selection as st
from pathlib import Path


import dlutils_ii as du

# import pandas as pd
from opencv_annotator.annotator import BoundingBoxAnnotator

# from opencv_annotator.cache_annotator import IOManager
# from yolo_plugins.training.yolo_experiment import SODExperiment, get_sod_label_config


dataset_cache = Path("/data/sod_cache/")
cameras = [str(x) for x in list(dataset_cache.glob("raw/*/*/")) if x.is_dir()]
# print(cameras)

debug = False
items = st.Menu(
    [st.MenuItemMultiStr("camera", options=cameras)], "annotation_camera"
).run(debug)

# camera = fzf_utils.prompt(cameras, prompt_text="choose_camera")
for item in items:
    camera = Path(item["camera"])

    pathfinder = du.Pathfinder(
        videoset=camera.parent.name, camera=camera.name, cache_dir=dataset_cache
    )
    train_options = du.TrainOptions(
        val=False,
        offset_scales=[1],
        max_samples=1000,
    )
    config = du.DatasetConfig(pathfinder, train_options)

    data_dir = Path("/diskstation/panoptes/sod/cache")
    # first select videosets/cameras
    for item in items:
        BoundingBoxAnnotator(config).run()

    # mantis = get_mantis()
    # # du.Writer.export_multiprocessed(mantis[:1],[0,-15,15],labelconfig=get_sod_label_config())

    # index =0

    # # x = mantis[index]

    # # tmp_path = x.pathfinder.annotations_path.with_suffix(".tmp.csv")
    # # annotations = pd.read_csv(tmp_path)
    # # x.pathfinder.media_manager.save_annotations(annotations, "smallObjectsCorrected", True)
    # # # print('uploaded')
