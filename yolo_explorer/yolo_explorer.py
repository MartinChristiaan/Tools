import os

import cv2
from core import ImageLoader, YOLOImageLoader

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python image_viewer.py <directory>")
        sys.exit()
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print("Invalid directory!")
    else:
        image_viewer = YOLOImageLoader(directory)
        image_viewer.display_images()
