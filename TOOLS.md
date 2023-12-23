[home](README.md)

# Tools

This folder contains tools to visualise & convert datasets using FiftyOne. These tools also support the used video dataset formats.

## Visualise

FiftyOne can be used to load datasets in various formats and visualise the ground truth or detections in the browser. This browser window is available at the port defined in the [docker Makefile](../docker/Makefile). Currently, the following formats are supported:

* MS COCO
* YOLOv5
* COCO-VID

To visualise your data, use the following command:

```bash
python tools/fiftyone_visualise.py \
    --dataset_dir /path/to/dataset/root \
    --type coco \
    --name optional_name
```

The dataset will now be visible in the browser at http://pc-11393:12015/.

### COCO-VID

COCO-VID is a video version of the MS-COCO JSON formatting following [mmtracking](https://github.com/open-mmlab/mmtracking/blob/master/docs/en/dataset.md#2-convert-annotations). The format is as follows:

```json
{
  "videos": [video],
  "images": [image],
  "annotations": [annotation],
  "categories": [category],
}

video{
  "id": int,
  "name": str,
}

image{
  "id": int,
  "frame_id": int,
  "video_id": int,
  "width": int,
  "height": int,
  "file_name": str,
}

annotation{
  "id": int,
  "image_id": int,
  "video_id": int,
  "category_id": int,
  "area": float,
  "bbox": [x,y,width,height],
  "iscrowd": 0 or 1,
}

category{
  "id": int,
  "name": str,
  "supercategory": str,
}
```

A COCO-VID dataset can be loading using the following command:

```bash
python tools/fiftyone_visualise.py \
    --dataset_dir /path/to/coco-vid-dataset/root \
    --type coco-vid \
    --name optional_name \
    --fps video_fps \
```

This will generate `mp4` videos from the dataset frames to visualise the dataset in video format instead of separate frames.

## Convert

FiftyOne can be used to convert datasets between various formats. This tool allow for the conversion between COCO-VID & YOLO-VID format. Use the following command:

```bash
python tools/fiftyone_convert.py \
    --dataset_dir path/to/coco-vid/root \
    --out_dir path/to/output/root \
    --input_type coco-vid \
    --output_type yolo-vid \
```

## Bbox Eval F1

A script to calculate F1 score using MS COCO style labels & predictions. The tool generates a F1-score curve to find the maximum F1 score over various confidence values. The True Positive threshold is calculated by pixel distance between bounding box middle coordinates and can be set using the `--tp-distance` flag:

```bash
python bbox_eval_f1.py \
    --gt-json path/to/coco/labels.json
    --pred-json path/to/coco/predictions.json
    --output-dir path/to/output/dir
    --tp-distance <int>                         # Pixel distance threshold for TP
```

Note that the `predictions.json` must be in [MS COCO format](https://cocodataset.org/#format-results), where the `image_id` field corresponds with the `image_id` field in the `labels.json`. YOLOv5 returns predictions with `image_id=image_file_name.png` format. This can be converted using the TNO tool [here](https://gitlab.tsn.tno.nl/intelligent_imaging/python/object_detection/dataset_utilities/-/blob/main/docs/README_tiny_object_det_eval.md).
