# %%
import os
from pathlib import Path
import shutil
import cv2
import pandas as pd
from tqdm import tqdm

mm_dir = "/diskstation/datasets/visdrone_2019/"
# shutil.rmtree(mm_dir)
modes = ["val", "train", "test"]
for data, mode in zip(
    [
        "/data/VisDrone2019-VID-val/",
        "/data/VisDrone2019-VID-train/",
        "/data/VisDrone2019-VID-test-dev/",
    ],
    modes,
):

    from media_manager.core import MediaManager

    sequences = list((Path(data) / "sequences").glob("*"))
    print(f"{len(sequences)} sequences found")
    annotation_files = list((Path(data) / "annotations").rglob("*.txt"))
    sequences.sort()
    annotation_files.sort()
    for annotations_file, seq in zip(annotation_files, sequences):
        # convert video
        videodir = Path(f"{mm_dir}/video/{seq.stem}")
        videodir.mkdir(parents=True, exist_ok=True)
        resultsdir = Path(f"{mm_dir}/results/{seq.stem}")
        resultsdir.mkdir(parents=True, exist_ok=True)
        imgdir = videodir / "images"
        logfile = videodir / "images.log"
        imgdir.mkdir(parents=True, exist_ok=True)

        # os.system(f'rsync -azP {seq}/ {imgdir}')
        images = list(seq.glob("*.jpg"))
        images.sort()

        for i, img in enumerate(tqdm(images)):
            filename = str(i).zfill(5) + ".jpg"
            shutil.copy(img, imgdir / filename)
        num_images = len(list(imgdir.glob("*.jpg")))
        logstr = ""
        for i in range(num_images):
            timestamp = i / 25
            logstr += f"{timestamp:.2f}\n"
        with open(logfile, "w") as f:
            f.write(logstr)
        mm = MediaManager(videodir, video_suffix=".jpg", result_dirpath=resultsdir)
        # convert annotations
        with open(annotations_file, "r") as f:
            text = f.read()
        lines = text.split("\n")
        out_data = []
        label_lut = {
            0: "ignore_area",
            1: "pedestrian",
            2: "people",
            3: "bicycle",
            4: "car",
            5: "van",
            6: "truck",
            7: "tricycle",
            8: "awning-tricycle",
            9: "bus",
            10: "motor",
            11: "others",
        }

        for line in lines:
            line_split = line.split(",")
            if len(line_split) > 1:
                (
                    frame_no,
                    track_id,
                    bbox_x,
                    bbox_y,
                    bbox_w,
                    bbox_h,
                    ignore,
                    class_id,
                    _,
                    _,
                ) = line.split(",")
                label = label_lut[int(class_id)]
                datadict = {
                    "frame_no": frame_no,
                    "bbox_x": bbox_x,
                    "bbox_y": bbox_y,
                    "bbox_w": bbox_w,
                    "bbox_h": bbox_h,
                    "track_id": track_id,
                    # "ignore":ignore,
                    "class_id": class_id,
                    "label": label,
                    "timestamp": f"{(int(frame_no)-1)/25:.2f}",
                    "mode": mode,
                }
                out_data.append(datadict)
        print(mm.result_dirpath)

        mm.save_annotations(pd.DataFrame(out_data))
        annotations = mm.load_annotations()
        from dlutils_ii.tools.drawer import DrawBboxEngine
        from trackertoolbox.detections import Detections

        t = mm.timestamps
        drawer = DrawBboxEngine(color_key="class_id", label_keys=["label"])
        for i in range(10):
            frame = mm.get_frame(t[i])
            annotations_frame = annotations[annotations["timestamp"] == t[i]]
            f_out = drawer.draw(frame, Detections(annotations_frame))
            os.makedirs(f"/data/test/", exist_ok=True)
            cv2.imwrite(
                f"/data/test/{annotations_file.stem}_test_{i}.jpg",
                cv2.cvtColor(f_out, cv2.COLOR_RGB2BGR),
            )

        # # pd.DataFrame(out_data).to_csv(f"{annotations_dir}/{seq.stem}_annotations.csv",index=False)
