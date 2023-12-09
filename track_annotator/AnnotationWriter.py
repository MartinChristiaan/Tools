import dlutils_ii as du
import pandas as pd
from loguru import logger


class AnnotationWriter:
    def __init__(
        self, pathfinder: du.Pathfinder, load_existing=False, annotation_suffix="tmp"
    ) -> None:
        self.pathfinder = pathfinder
        self.annotations = None
        self.suffix = annotation_suffix
        if load_existing:
            self.annotations = pathfinder.media_manager.load_annotations(
                annotation_suffix
            )
            if self.annotations is None:
                logger.info(f"no pre existing annotations for {pathfinder.name}")

        if self.annotations is None:
            self.annotations = pd.DataFrame()

    def accept_detection(self, new_detections):
        self.annotations = pd.concat([self.annotations, new_detections])

    def save_to_diskstation(self):
        self.pathfinder.media_manager.save_annotations(
            self.annotations, self.suffix, drop_extra_columns=True
        )
