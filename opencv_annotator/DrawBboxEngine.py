import cv2
from trackertoolbox.detections import Detections


class DrawBboxEngine:
    def __init__(
        self,
        line_thickness=2,
        color_key="track_id",
        label_keys=["track_id"],
        colors=[
            (0, 0, 255),
            (255, 255, 255),
            (255, 0, 0),
            (0, 255, 255),
            (255, 0, 255),
            (255, 255, 0),
            (255, 255, 255),
        ],
    ) -> None:
        self.line_thickness = line_thickness
        self.color_key = color_key
        self.label_keys = label_keys
        self.colors = colors

    def color_id(self, id):
        return self.colors[id % len(self.colors)]

    def write_bbox(self, image, detection, color, label=None):
        x = int(detection["bbox_x"])
        y = int(detection["bbox_y"])
        w = int(detection["bbox_w"])
        h = int(detection["bbox_h"])
        x2 = x + w
        y2 = y + h

        new_image = cv2.rectangle(image, (x, y), (x2, y2), color, self.line_thickness)

        if label is not None:
            tf = max(self.line_thickness - 1, 1)  # font thickness
            t_size = cv2.getTextSize(
                label, 0, fontScale=self.line_thickness / 3, thickness=tf
            )[0]
            c2 = x + t_size[0], y - t_size[1] - 3
            cv2.rectangle(new_image, (x, y), c2, color, -1, cv2.LINE_AA)  # filled
            cv2.putText(
                new_image,
                label,
                (x, y - 2),
                0,
                self.line_thickness / 3,
                [225, 255, 255],
                thickness=tf,
                lineType=cv2.LINE_AA,
            )

        return new_image

    def __call__(self, timestampdata, data):
        image = data[0][0]["data"]
        bboxs = data[1][0]["data"]
        frame = self.draw(image, bboxs)
        return [frame]

    def draw(self, image, bboxs):
        if isinstance(bboxs, Detections):
            bboxs = bboxs.to_pandas().to_dict(orient="records")
        # Copy image and draw bounding boxes on the final image
        bbox_image = image.copy()
        for bbox in bboxs:
            # set color for bounding box
            if self.color_key not in bbox:  # if key does not exist in dictionary
                color_id = 1  # set bounding box to default color
            else:
                color_id = bbox[self.color_key]
            color = self.color_id(color_id)

            # set label for bounding box
            labels = []
            for key in self.label_keys:
                if key in bbox:
                    labels.append(str(bbox[key])[:5])
            if len(labels) == 0:
                label = None
            else:
                label = " ".join(labels)  # add spaces

            # burn bboxes on image
            bbox_image = self.write_bbox(bbox_image, bbox, color=color, label=label)
        return bbox_image
