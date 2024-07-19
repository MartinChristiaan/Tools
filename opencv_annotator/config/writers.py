from functools import partial
from dlutils_ii import Writer, LabelConfig
from opencv_annotator.pre_annotation_writer import PreAnnotationWriter


label_config = LabelConfig(
    {
        "object": 0,
        "ignore_area": 1,
    },
    ["object", "ignore_area"],
    ["ignore_frame"],
)

writers = dict(tyolo_writer=PreAnnotationWriter, annotation_writer=Writer)
