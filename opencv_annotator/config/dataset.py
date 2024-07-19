# %%
from pathlib import Path
from typing import List

import dlutils_ii as du
from tqdm import tqdm
from videosets_ii.videosets_ii import VideosetsII

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basoedirpath)


def drone_tracking_dataset(output_dir="/data/sod_cache"):
    vset_name = "drone-tracking"
    vset = videosets[vset_name]
    configs = []
    for c in vset.cameras:
        if "1280" in c or "cam1" in c:
            continue
        pathfinder = du.Pathfinder(videoset=vset_name, camera=c, cache_dir=output_dir)
        train_options = du.TrainOptions(
            val=False,
            offset_scales=[1],
            max_samples=20,
        )
        config = du.DatasetConfig(pathfinder, train_options)
        configs.append(config)
    return configs


def drone_detection_dataset(output_dir="/data/sod_cache"):
    vset_name = "drone_detection_dataset_2021"
    vset = videosets[vset_name]
    configs = []
    val_cameras = [
        "IR_DRONE_151",
        "IR_DRONE_155",
        "V_DRONE_039",
        "V_DRONE_050",
        "V_DRONE_069",
    ]
    for i, c in enumerate(vset.cameras):
        val = c in val_cameras
        pathfinder = du.Pathfinder(
            videoset=vset_name, camera=c, cache_dir=output_dir  # , crop=0
        )
        train_options = du.TrainOptions(
            val=val,
            offset_scales=[1],
            max_samples=20,
        )
        config = du.DatasetConfig(pathfinder, train_options)
        configs.append(config)
    return configs


def get_mantis():
    vsets = VideosetsII("/diskstation")
    configs = []
    for camera in vsets["mantis_drone_2023"].cameras:
        if not camera.endswith("wide_hd"):
            continue
        pf = du.Pathfinder(
            "mantis_drone_2023",
            camera,
            cache_dir="/data/sod_cache",
        )
        o = du.TrainOptions(
            False,
            [1],
            max_samples=300,
            annotations_suffix="smallObjectsCorrected",
            motion_models="compute",
        )
        cfg = du.DatasetConfig(pf, o)
        configs.append(cfg)
    return configs


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


def get_tie(output_dir="/data/sod_cache"):
    vset_name = "TIE_2023"
    configs = []
    vset = videosets[vset_name]
    # annotated_cameras = [
    #     x for x in du.get_cameras_with_annotations(vset) if "halfres" in x
    # ]
    annotated_cameras = [x for x in vset.cameras if "basler" in x and "halfres" in x]
    for i, cam in enumerate(annotated_cameras):
        is_val = i < 4
        pathfinder = du.Pathfinder(videoset=vset_name, camera=cam, cache_dir=output_dir)
        train_options = du.TrainOptions(
            val=is_val,
            offset_scales=[0.5],
            max_samples=30,
            min_temporal_spacing=10,
            annotations_suffix=None,
        )
        config = du.DatasetConfig(pathfinder, train_options)
        configs.append(config)
    return configs


all_configs = (
    get_mantis()
    + get_tie()
    + [get_marnehuizen()]
    + drone_detection_dataset()
    + drone_tracking_dataset()
)

# if __name__ == "__main__":
#     webcams = get_webcams_2023()
#     from dlutils_ii.dataset_cache.fo_vizualize import open_fiftyone
#     from scripts.pre_annotation_writer import PreAnnotationWriter
#     from yolo_plugins.defaults.inference import get_default_tyolo_processor
#     from yolo_plugins.processing import MMProcessSequence, Sequence

#     proc = get_default_tyolo_processor()
#     for sequence in tqdm(webcams):
#         print(sequence.pathfinder.name)
#         # break
#         pathfinder = sequence.pathfinder
#         seq = MMProcessSequence(videoset=pathfinder.videoset, camera=pathfinder.camera)
#         seq._media_manager = pathfinder.media_manager
#         proc.mm_process(seq, False, True, True)
#         PreAnnotationWriter(
#             sequence, [-15, 15, 0], source="tyolov8/tracks_tyolov8m-30112023.csv"
#         ).write()
#     open_fiftyone(webcams, "0").wait()
