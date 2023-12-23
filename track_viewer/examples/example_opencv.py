import sys

import cv2
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget


class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a label to display the image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Create a layout to hold the label
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image_label)
        self.central_widget.setLayout(self.layout)

        # Create a timer to update the image
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)

        # Load the initial image
        self.image = cv2.imread("./mpv-shot0001.jpg")
        self.update_image()

    def keyPressEvent(self, event):
        # Start the timer when a key is pressed
        self.timer.start(1000 / 30)  # Update image at 30 fps

    def update_image(self):
        # Process the image (e.g., apply filters, transformations, etc.)
        processed_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        # Convert the processed image to QImage
        height, width, channel = processed_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(
            processed_image.data, width, height, bytes_per_line, QImage.Format_RGB888
        )

        # Scale the image to fit the label
        scaled_image = q_image.scaled(
            self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio
        )

        # Update the label with the new image
        self.image_label.setPixmap(QPixmap.fromImage(scaled_image))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageWindow()
    window.show()
    sys.exit(app.exec_())
