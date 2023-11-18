import fiftyone.utils.coco as fouc
import os
import fiftyone.core.metadata as fom


class COCOVidDetectionDatasetImporter(
    fouc.COCODetectionDatasetImporter
):
    def __next__(self):
        filename = next(self._iter_filenames)

        if os.path.isabs(filename):
            image_path = filename
        else:
            image_path = self._image_paths_map[filename]

        image_dict = self._image_dicts_map.get(filename, None)

        if image_dict is None:
            image_metadata = fom.ImageMetadata.build_for(image_path)
            return image_path, image_metadata, None

        image_id = image_dict["id"]
        width = image_dict["width"]
        height = image_dict["height"]

        image_metadata = fom.ImageMetadata(width=width, height=height)

        label = {}

        if self._annotations is not None:
            coco_objects = self._annotations.get(image_id, [])
            frame_size = (width, height)

            if self.classes is not None and self.only_matching:
                coco_objects = fouc._get_matching_objects(
                    coco_objects, self.classes, self._classes
                )

            if "detections" in self._label_types:
                detections = fouc._coco_objects_to_detections(
                    coco_objects,
                    frame_size,
                    self._classes,
                    self._supercategory_map,
                    False,  # no segmentations
                )
                if detections is not None:
                    label["detections"] = detections

            if "segmentations" in self._label_types:
                if self.use_polylines:
                    segmentations = fouc._coco_objects_to_polylines(
                        coco_objects,
                        frame_size,
                        self._classes,
                        self._supercategory_map,
                        self.tolerance,
                    )
                else:
                    segmentations = fouc._coco_objects_to_detections(
                        coco_objects,
                        frame_size,
                        self._classes,
                        self._supercategory_map,
                        True,  # load segmentations
                    )

                if segmentations is not None:
                    label["segmentations"] = segmentations

            if "keypoints" in self._label_types:
                keypoints = fouc._coco_objects_to_keypoints(
                    coco_objects, frame_size, self._classes
                )

                if keypoints is not None:
                    label["keypoints"] = keypoints

        if "coco_id" in self._label_types:
            label["coco_id"] = image_id

        if "license" in self._label_types:
            license_id = image_dict.get("license", None)
            label["license"] = self._license_map.get(license_id, None)

        label['video_id'] = image_dict.get('video_id', -1)

        if self._has_scalar_labels:
            label = next(iter(label.values())) if label else None

        return image_path, image_metadata, label