import argparse

import fiftyone as fo
from fiftyone_utils.coco_vid import COCOtoVidDetectionDatasetExporter
from fiftyone_utils.yolo_vid import YOLOv5VidDatasetExporter
from fiftyone_utils.coco import COCOVidDetectionDatasetImporter

fo_type_dict = {
    'coco': fo.types.COCODetectionDataset,
    'voc': fo.types.VOCDetectionDataset,
    'yolov5': fo.types.YOLOv5Dataset,
    'coco-vid': None,
    'yolo-vid': None
}


def check_paths(args):

    if args.dataset_dir:
        assert args.data_path is None and args.labels_path is None
    elif not args.yaml_path:
        assert args.data_path is not None and args.labels_path is not None


def main(args):
    input_type = fo_type_dict[args.input_type]
    output_type = fo_type_dict[args.output_type]

    check_paths(args)

    print(f"Loading {args.input_type} dataset...")
  
    if args.input_type == "yolov5":
        dataset = fo.Dataset.from_dir(
            yaml_path=args.yaml_path,
            dataset_type=input_type,
            dataset_dir=args.dataset_dir,
            split=args.split,
            include_all_data=True,
            max_samples=args.max_samples,
        )
    elif args.input_type == "coco":
        importer = COCOVidDetectionDatasetImporter(
            dataset_dir=args.dataset_dir,
            data_path=args.data_path,
            labels_path=args.labels_path,
            max_samples=args.max_samples,
            extra_attrs=True,
            include_id=True,
        )
        dataset = fo.Dataset.from_importer(importer)
    else:
        dataset = fo.Dataset.from_dir(
            dataset_type=input_type,
            dataset_dir=args.dataset_dir,
            data_path=args.data_path,
            labels_path=args.labels_path,
            max_samples=args.max_samples,
            extra_attrs=True,
            include_id=True,
        )

    print(f"Exporting dataset to {args.out_dir}...")


    if args.export_media == 'True':
        export_media = True
    elif args.export_media == 'False':
        export_media = False
    else:
        export_media = args.export_media
    
    if args.output_type == "yolov5":
        split = args.split

        print(dataset.default_classes)
    
        # Convert test-dev, test-challenge, etc to test
        if split.startswith("test"):
            split = "test"
            
        dataset.export(
            export_dir=args.out_dir,
            dataset_type=output_type,
            split=split,
            yaml_path=args.yaml_path,
            export_media=export_media,
            classes=dataset.default_classes,
        )
    elif args.output_type == "coco-vid":
        exporter = COCOtoVidDetectionDatasetExporter(
            export_dir=args.out_dir,
            export_media=export_media,)
        exporter.export_dataset(dataset)
    elif args.output_type == "yolo-vid":
        split = args.split
        # Convert test-dev, test-challenge, etc to test
        if split.startswith("test"):
            split = "test"
        print(dataset.default_classes)
        exporter = YOLOv5VidDatasetExporter(
            export_dir=args.out_dir,
            export_media=export_media,
            split=split,
            yaml_path=args.yaml_path,
            classes=dataset.default_classes,
        )
        # dataset.export(
        #     dataset_exporter=exporter,
        # )
        with exporter:
            exporter.log_collection(dataset)
            for sample in dataset:

                image_path = sample.filepath
                try:
                    vid_id = sample.video_id
                except AttributeError:
                    vid_id = -1

                # print(sample.filepath)
               
                # print(sample)
                detections = sample.detections
                exporter.export_sample(image_path, detections, vid_id)
    else:
        dataset.export(
            export_dir=args.out_dir,
            dataset_type=output_type,
            export_media=export_media,
            classes=dataset.default_classes,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Convert datasets using FiftyOne")
    parser.add_argument("--dataset_dir",
                        help="Dataset directory. Needed for yolov5 loading")
    parser.add_argument("--data_path", help="Image data to convert")
    parser.add_argument("--labels_path", help="Labels to convert")
    parser.add_argument("--out_dir", required=True, help="Output directory")
    parser.add_argument("--input_type",
                        required=True,
                        choices=['coco', 'voc', 'yolov5'],
                        help="Dataset type of input dataset")
    parser.add_argument("--output_type",
                        required=True,
                        choices=['coco', 'voc', 'yolov5', 'coco-vid', 'yolo-vid'],
                        help="Dataset type of output dataset")
    parser.add_argument("--fraction", type=float, default=None, help="Extract fraction of dataset and export")
    parser.add_argument("--export_media", default=None, choices=['True', 'False', 'move', 'symlink', 'manifest'],
                        help="How to export media files, see: https://voxel51.com/docs/fiftyone/api/fiftyone.core.collections.html#fiftyone.core.collections.SampleCollection.export. Default is auto")
    parser.add_argument("--split", help="Split to export")
    parser.add_argument("--yaml_path", default=None, help="Location of yolov5 yaml dataset file")
    parser.add_argument("--max_samples", type=int, default=None, help="Max number of samples to export")
    args = parser.parse_args()

    main(args)
