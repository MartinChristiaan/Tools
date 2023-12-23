# %%
from pathlib import Path
from typing import List
import dlutils_ii as du
from tqdm import tqdm


def get_mantis():
    pf = du.Pathfinder(
        "mantis_drone_2023",
        "DJI_202309100220_001/wide_hd",
        # basedir=r"\\wsl.localhost\Ubuntu\diskstation",
        # cache_dir=r"c:/Data/dataset",
    )

    o = du.TrainOptions(
        False,
        [1],
        max_samples=300,
        # motion_models="motion_models.csv",
        annotations_suffix=None,
    )
    return du.DatasetConfig(pf, o)


def get_marnehuizen():
    pf = du.Pathfinder(
        "marnehuizen_2013",
        "",
        basedir=None,
        cache_dir="./dataset",
    )

    o = du.TrainOptions(
        False,
        [1],
        max_samples=300,
        motion_models="motion_models.csv",
        annotations_suffix=None,
    )
    return du.DatasetConfig(pf, o)


import yolo_plugins as yp


def get_webcams_2023() -> List[du.DatasetConfig]:
    from media_manager.core import MediaManager

    cameras = list(Path("/diskstation/webcams_2023/video").rglob("*"))
    cfgs = []
    for cam in cameras:
        try:
            if not "alpha" in cam.stem:
                continue

            pf = du.Pathfinder(
                "webcams_2023",
                cam.stem,
                basedir=None,
                cache_dir="/home/martin/dataset",
            )
            pf._media_manager = MediaManager(cam, video_suffix=".mp4")
            o = du.TrainOptions(
                False,
                [1],
                max_samples=30,
                annotations_suffix=None,
            )
            cfgs.append(du.DatasetConfig(pf, o))
        except Exception as e:
            print(e)
        break
    return cfgs


if __name__ == "__main__":
    webcams = get_webcams_2023()
    from yolo_plugins.processing import Sequence, MMProcessSequence
    from yolo_plugins.defaults.inference import get_default_tyolo_processor
    from scripts.pre_annotation_writer import PreAnnotationWriter
    from dlutils_ii.dataset_cache.fo_vizualize import open_fiftyone

    proc = get_default_tyolo_processor()
    for sequence in tqdm(webcams):
        print(sequence.pathfinder.name)
        # break
        pathfinder = sequence.pathfinder
        seq = MMProcessSequence(videoset=pathfinder.videoset, camera=pathfinder.camera)
        seq._media_manager = pathfinder.media_manager
        proc.mm_process(seq, False, True, True)
        PreAnnotationWriter(
            sequence, [-15, 15, 0], source="tyolov8/tracks_tyolov8m-30112023.csv"
        ).write()
    open_fiftyone(webcams, "0").wait()
