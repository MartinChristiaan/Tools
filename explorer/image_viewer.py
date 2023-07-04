
print('main')
import os
import cv2

from ImageLoader import ImageViewer
print('main')

def get_image_paths(directory):
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                image_paths.append(os.path.join(root, file))
    image_paths.sort()
    return image_paths


def get_next_different_image_index(filepaths, index, previous=False):
    base_folder = os.path.dirname(filepaths[index])

    if previous:
        for i in range(index - 1, -1, -1):
            current_folder = os.path.dirname(filepaths[i])
            if current_folder != base_folder:
                return i
    else:
        for i in range(index + 1, len(filepaths)):
            current_folder = os.path.dirname(filepaths[i])
            if current_folder != base_folder:
                return i

    # If no different folder image found, return -1 or raise an exception
    return -1


if __name__ == '__main__':
    print('main')
    import sys

    if len(sys.argv) != 2:
        print('Usage: python image_viewer.py <directory>')
    else:
        directory = sys.argv[1]
        if not os.path.isdir(directory):
            print('Invalid directory!')
        else:
            print('getting image paths')
            image_paths = get_image_paths(directory)
            if len(image_paths) == 0:
                print('No images found in the directory!')
            else:
                print('starting image viewer')
                image_viewer = ImageViewer(image_paths)
                print('starting showing')
                image_viewer.display_images()

