from bson import Timestamp
import cv2
from trackertoolbox.detections import Detections
from trackertoolbox.detections import Detections
from DrawBboxEngine import DrawBboxEngine

class BoundingBoxSelector:
    def __init__(self, image_path, detections=None):
        self.image = cv2.imread(image_path)
        self.new_bbox_coords = []
        self.is_button_down = False
        # self.bounding_boxes = []
        self.detections = Detections()
        self.drawer = DrawBboxEngine(color_key="class_id", label_keys=["label"])
        self.cur_image = self.image.copy()
        self.dirty = False

        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.draw_rectangle)

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE and self.is_button_down:
            cv2.rectangle(
                self.cur_image, self.new_bbox_coords[0], (x, y), (0, 255, 0), 2
            )

        elif event == cv2.EVENT_LBUTTONDOWN:
            self.new_bbox_coords = [(x, y)]
            self.is_button_down = True

        elif event == cv2.EVENT_LBUTTONUP:
            self.new_bbox_coords.append((x, y))
            self.is_button_down = False

            # Store the bounding box
            new_detection = [
                dict(
                    bbox_x=self.new_bbox_coords[0][0],
                    bbox_y=self.new_bbox_coords[0][1],
                    bbox_w=self.new_bbox_coords[1][0] - self.new_bbox_coords[0][0],
                    bbox_h=self.new_bbox_coords[1][1] - self.new_bbox_coords[0][1],
                    class_id=0,
                    label="object",
                    timestamp=0,
                )
            ]
            self.detections.append(Detections(new_detection))
            self.dirty = True

    def run(self):
        print("running")
        while True:
            if self.dirty:
                self.cur_image = self.drawer.draw(
                    self.image, self.drawer.draw(self.image, self.detections)
                )
                self.dirty = False
            cv2.imshow("image", self.cur_image)
            key = cv2.waitKey(0)
            if key == ord("q"):
                break

        cv2.destroyAllWindows()


if __name__ == "__main__":
    # Example usage
    impath = "./mpv-shot0001.jpg"
    bounding_box_selector = BoundingBoxSelector(impath)
    bounding_box_selector.run()
