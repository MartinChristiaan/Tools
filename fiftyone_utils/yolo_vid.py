import fiftyone.utils.yolo as fouy
import fiftyone.utils.data as foud

import eta.core.utils as etau
from pathlib import Path
import warnings

class YOLOv5VidDatasetExporter(
    fouy.YOLOv5DatasetExporter
):
    def setup(self):
        self._classes = {}
        self._labels_map_rev = {}
        self._images = []
        self._writer = YOLOVidAnnotationWriter()

        self._parse_classes()

        self._media_exporter = VidImageExporter(
            self.export_media,
            export_path=self.data_path,
            supported_modes=(True, False, "move", "symlink"),
            default_ext=self.image_format,
            ignore_exts=True,
        )
        self._media_exporter.setup()

    def export_sample(self, image_or_path, detections, vid_id, metadata=None):
        _, uuid = self._media_exporter.export(image_or_path)

        if detections is None:
            return

        if Path(image_or_path).parent.stem != "data":
            out_labels_path = Path(self.labels_path) / Path(image_or_path).parent.stem / (Path(image_or_path).stem + ".txt")
        else:
            out_labels_path = Path(self.labels_path) / (uuid + ".txt")

        self._writer.write(
            detections,
            vid_id,
            out_labels_path,
            self._labels_map_rev,
            dynamic_classes=self._dynamic_classes,
            include_confidence=self.include_confidence,
        )




class VidMediaExporter(foud.MediaExporter):
    def export(self, media_or_path, outpath=None):
        """Exports the given media.
        Args:
            media_or_path: the media or path to the media on disk
            outpath (None): a manually-specified location to which to export
                the media. By default, the media will be exported into
                :attr:`export_path`
        Returns:
            a tuple of:
            -   the path to the exported media
            -   the UUID of the exported media
        """
        
        if etau.is_str(media_or_path):
            media_path = media_or_path

            if outpath is not None:
                uuid = self._get_uuid(outpath)
            elif self.export_mode != False:
                # Place frames of videos in separate directories
                if Path(media_path).parent.stem != "data":
                    outpath = Path(self.export_path) / Path(media_path).parent.stem / Path(media_path).name
                else:
                    outpath = self._filename_maker.get_output_path(media_path)
                uuid = self._get_uuid(outpath)
            else:
                outpath = None
                uuid = self._get_uuid(media_path)

            # print(uuid, outpath)

            if self.export_mode == True:
                etau.copy_file(media_path, outpath)
            elif self.export_mode == "move":
                etau.move_file(media_path, outpath)
            elif self.export_mode == "symlink":
                etau.symlink_file(media_path, outpath)
            elif self.export_mode == "manifest":
                outpath = None
                self._manifest[uuid] = media_path
        else:
            media = media_or_path

            if outpath is None:
                outpath = self._filename_maker.get_output_path()

            uuid = self._get_uuid(outpath)

            if self.export_mode == True:
                self._write_media(media, outpath)
            elif self.export_mode != False:
                raise ValueError(
                    "Cannot export in-memory media when 'export_mode=%s'"
                    % self.export_mode
                )

        return outpath, uuid

class VidImageExporter(VidMediaExporter):
    pass


class YOLOVidAnnotationWriter(fouy.YOLOAnnotationWriter):
    def write(
        self,
        detections,
        vid_id,
        txt_path,
        labels_map_rev,
        dynamic_classes=False,
        include_confidence=False,
    ):
        """Writes the detections to disk.
        Args:
            detections: a :class:`fiftyone.core.labels.Detections` instance
            txt_path: the path to write the annotation TXT file
            labels_map_rev: a dictionary mapping class label strings to target
                integers
            dynamic_classes (False): whether to dynamically add new labels to
                ``labels_map_rev``
            include_confidence (False): whether to include confidences in the
                export, if they exist
        """
        rows = [str(vid_id)]
        for detection in detections.detections:
            label = detection.label

            if dynamic_classes and label not in labels_map_rev:
                target = len(labels_map_rev)
                labels_map_rev[label] = target
            elif label not in labels_map_rev:
                msg = (
                    "Ignoring detection with label '%s' not in provided "
                    "classes" % label
                )
                warnings.warn(msg)
                continue
            else:
                target = labels_map_rev[label]

            if include_confidence:
                confidence = detection.confidence
            else:
                confidence = None

            row = fouy._make_yolo_row(
                detection.bounding_box, target, confidence=confidence
            )
            rows.append(row)

        fouy._write_file_lines(rows, txt_path)
