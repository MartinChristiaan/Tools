import argparse
import json
from pathlib import Path

import fiftyone as fo
import fiftyone.utils.annotations as foua
import fiftyone.utils.coco as fouc
from fiftyone import ViewField as F
from fiftyone.core.fields import EmbeddedDocumentField
from fiftyone.core.labels import Detections
from fiftyone_utils.coco_vid import COCOVidDetectionDatasetImporter
from fiftyone_utils.extract_clips import split_vid_datasets

fo_type_dict = {
    "coco": fo.types.COCODetectionDataset,
    "yolov5": fo.types.YOLOv5Dataset,
    "coco-vid": None,
}


def load_dataset_by_name(name):
    dataset = fo.load_dataset(name)
    return dataset


def load_dataset_from_disk(args):
    input_type = fo_type_dict[args.type]

    if args.type == "coco":
        dataset = fo.Dataset.from_dir(
            dataset_type=input_type,
            dataset_dir=args.dataset_dir,
            data_path=args.data_path,
            labels_path=args.labels_path,
            label_field="ground_truth",
            include_id=True,
            max_samples=args.max_samples,
            name=args.name,
            extra_attrs=True,
        )
    elif args.type == "yolov5":
        dataset = fo.Dataset.from_dir(
            dataset_type=input_type,
            dataset_dir=args.dataset_dir,
            yaml_path=args.yaml_path,
            split=args.split,
            max_samples=args.max_samples,
            name=args.name,
            include_all_data=True,
        )
    elif args.type == "coco-vid":
        importer = COCOVidDetectionDatasetImporter(
            dataset_dir=args.dataset_dir,
            as_video=True,
            max_samples=args.max_samples,
            calculate_bbox_stats=True,
            vid_fps=args.fps,
        )
        dataset = importer.get_dataset(name=args.name)

    if args.name is not None:
        dataset.persistent = True

    return dataset


def load_dataset(args):
    if (
        args.name
        and not args.dataset_dir
        and not args.data_path
        and not args.labels_path
    ):
        return load_dataset_by_name(args.name), True

    if args.predictions_paths and not args.type in ["coco", "coco-vid"]:
        raise ValueError("Predictions are only available for coco datasets atm")

    try:
        return load_dataset_from_disk(args), False
    except ValueError:
        print(
            f"Dataset with name {args.name} already exists. Loading existing dataset."
        )
        return load_dataset_by_name(args.name), True


def get_draw_config():
    config = foua.DrawConfig(
        {
            "show_object_names": False,
            "show_object_labels": False,
            "show_object_confidences": True,
            "show_object_attrs": False,
            "bbox_linewidth": 1,
            "show_event_boxes": False,
        }
    )
    return config


def main(args):
    print(f"Loading dataset {args.name}")
    dataset, by_name = load_dataset(args)

    if not by_name:
        print(dataset)
        dataset.compute_metadata()

        for sample in dataset.select_fields("filepath"):
            sample["filename"] = Path(sample["filepath"]).name
            sample.save()

        bbox_area = (
            F("$metadata.width")
            * F("bounding_box")[2]
            * F("$metadata.height")
            * F("bounding_box")[3]
        )

        try:
            frames = dataset.to_frames()
        except ValueError:
            frames = dataset

        for sample in frames:
            img_width = sample["metadata"]["width"]
            img_height = sample["metadata"]["height"]
            for field_name, value in dataset.get_field_schema().items():
                if (
                    isinstance(value, EmbeddedDocumentField)
                    and value.document_type is Detections
                    and "segmentation" not in field_name
                ):
                    if sample[field_name] is not None:
                        for det in sample[field_name]["detections"]:
                            det["width"] = img_width * det["bounding_box"][2]
                            det["height"] = img_height * det["bounding_box"][3]
                            det["area"] = int(det["width"] * det["height"])
            sample.save()
        print(dataset.default_classes)
        if args.predictions_paths:
            assert args.type in ["coco", "coco-vid"]

            for i, pred_path in enumerate(args.predictions_paths):
                prediction_name = (
                    args.predictions_names[i]
                    if len(args.predictions_names) > i
                    else f"{Path(pred_path).parents[1].name}_{Path(pred_path).parent.stem}"
                )

                if Path(pred_path).exists():
                    print(
                        f"Adding predictions from {pred_path} for model {prediction_name}..."
                    )

                    if args.type == "coco":
                        fouc.add_coco_labels(
                            sample_collection=dataset,
                            label_field=prediction_name,
                            labels_or_path=pred_path,
                            coco_id_field="ground_truth_coco_id",
                            classes=args.classes,
                        )
                    else:
                        with open(pred_path, "r") as f:
                            predictions = json.load(f)
                        COCOVidDetectionDatasetImporter.add_coco_labels(
                            dataset, predictions, prediction_name
                        )
                else:
                    print(f"Predictions file {pred_path} does not exist")

    if args.file_names:
        dataset = dataset.match(F("filename").is_in(args.file_names))

    if args.bbox_size is not None and args.bbox_size > 0:
        small_boxes = bbox_area < args.bbox_size**2

        for field_name, value in dataset.get_field_schema().items():
            if (
                isinstance(value, EmbeddedDocumentField)
                and value.document_type is Detections
            ):
                dataset = dataset.filter_labels(field_name, small_boxes)

    if args.export_path and not Path(args.export_path).exists():
        config = get_draw_config()
        high_conf = dataset

        for pred_path in args.predictions_paths:
            file_name = Path(pred_path).parents[1].name
            high_conf = dataset.filter_labels(
                file_name,
                F("confidence") > 0.3,
            )

        high_conf.draw_labels(args.export_path, config=config)

    # Split video dataset to prevent fiftyone errors
    if args.type == "coco-vid" and args.split_size > 0:
        print(f"Splitting videos with split size {args.split_size}...")
        dataset = split_vid_datasets(dataset, split_size=args.split_size)

    print(dataset)

    session = fo.launch_app(dataset, address="0.0.0.0", port=args.port)
    session.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Visualise datasets using FiftyOne")
    parser.add_argument(
        "--dataset_dir", help="Dataset directory. Needed for yolov5 loading"
    )
    parser.add_argument(
        "--yaml_path", help="Dataset yaml file path. Used for yolov5 loading"
    )
    parser.add_argument("--data_path", help="Image data to visualise")
    parser.add_argument("--labels_path", help="Labels to visualise")
    parser.add_argument(
        "--predictions_paths", nargs="*", help="Predictions to visualise"
    )
    parser.add_argument(
        "--predictions_names",
        nargs="*",
        default=[],
        help="Prediction names. if None use filenames",
    )
    parser.add_argument("--split", help="Split to visualise. Used for yolov5 loading")
    parser.add_argument(
        "--type",
        required=True,
        choices=["coco", "yolov5", "coco-vid"],
        help="Dataset type of input dataset",
    )
    parser.add_argument(
        "--max_samples",
        type=int,
        default=None,
        help="How many samples to visualise, None -> all samples",
    )
    parser.add_argument("--name", help="Dataset name")
    parser.add_argument(
        "--bbox_size",
        type=int,
        default=None,
        help="Max size of bbox to show, None -> all sizes",
    )
    parser.add_argument("--export_path", help="Path to export folder")
    parser.add_argument("--port", type=int, default=5151, help="Port to use")
    parser.add_argument(
        "--classes",
        nargs="*",
        default=None,
        help="Classes used by coco predictions. Used when predictions_paths is used",
    )
    parser.add_argument(
        "--file_names", type=str, nargs="*", default=None, help="file names to show"
    )
    parser.add_argument(
        "--split_size", type=int, default=-1, help="Split size for coco-vid"
    )
    parser.add_argument("--fps", type=float, default=30, help="FPS for coco-vid")
    args = parser.parse_args()

    print(args.classes)
    main(args)
