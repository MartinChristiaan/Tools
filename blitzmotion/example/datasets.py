# %%

import dlutils_ii as du
from tqdm import tqdm
from videosets_ii.videosets_ii import VideosetsII


def get_mantis():
    vsets = VideosetsII("/diskstation")
    configs = []
    for camera in vsets["mantis_drone_2023"].cameras:
        if not camera.endswith("wide_hd"):
            continue
        pf = du.Pathfinder(
            "mantis_drone_2023",
            camera,
            cache_dir="/media/martin/DeepLearning/mantis_drone_2023",
        )
        o = du.TrainOptions(
            False,
            [1],
            max_samples=300,
            annotations_suffix=None,
        )
        cfg = du.DatasetConfig(pf, o)
        configs.append(cfg)
    return configs
