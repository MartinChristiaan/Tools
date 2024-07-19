import os
import shutil
import subprocess
import sys
import threading
import time

import cv2

cache_size = 50


def resize_image(image, max_width, max_height):
    height, width = image.shape[:2]
    aspect_ratio = width / height

    if width > max_width or height > max_height:
        if aspect_ratio > 1:
            width = max_width
            height = int(width / aspect_ratio)
        else:
            height = max_height
            width = int(height * aspect_ratio)

        image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    elif width < max_width and height < max_height:
        if aspect_ratio > 1:
            width = max_width
            height = int(width / aspect_ratio)
        else:
            height = max_height
            width = int(height * aspect_ratio)

        image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)

    return image


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


class ImageLoader:
    def get_image_paths(self, directory):
        for root, _, files in os.walk(directory):
            if "quarantine" in root or "debug" in root:
                continue
            for file in files:
                if file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                    self.image_paths.append(os.path.join(root, file))
        self.image_paths.sort()

    def __init__(self, directory):
        self.image_paths = []
        # path_thread  = threading.Thread(target=self.get_image_paths,args=(directory,))
        self.get_image_paths(directory)
        # path_thread.start()
        self.index = 0
        self.step = 1
        self.cache_index = 9999999999
        self.cache_step = 9999999999
        self.key_actions = {
            ord("k"): self.next_image,
            ord("j"): self.previous_image,
            ord("f"): self.next_different_image,
            ord("a"): self.previous_different_image,
            ord("d"): self.delete_image,
            ord("e"): self.open_folder,
            ord("h"): self.decrease_step_size,
            ord("l"): self.increase_step_size,
            ord("q"): self.quarantine_images_in_directory,
            27: self.exit_viewer,
        }
        self.image_cache = {}
        self.stopped = False
        self.loader = threading.Thread(target=self.load_images)
        self.loader.start()
        for j in range(100):
            time.sleep(0.1)
            print(self.total_images)
            if self.total_images > 0:
                return
        sys.exit()

    @property
    def total_images(self):
        return len(self.image_paths)

    def next_image(self):
        self.index = (self.index + self.step) % self.total_images

    def previous_image(self):
        self.index = (self.index - self.step) % self.total_images

    def increase_step_size(self):
        self.step *= 10

    def decrease_step_size(self):
        self.step /= 10
        self.step = int(self.step)
        self.step = max(1, self.step)

    def quarantine_images_in_directory(self):
        image_directory = os.path.dirname(self.image_paths[self.index])
        print(image_directory)
        parent_folder = os.path.dirname(image_directory)
        quarantine_folder = f"{parent_folder}/quarantine_images"
        os.makedirs(quarantine_folder, exist_ok=True)
        shutil.move(image_directory, quarantine_folder)
        label_directory = image_directory.replace("images", "labels")
        if os.path.exists(label_directory):
            quarantine_folder_labels = f"{parent_folder}/quarantine_labels"
            os.makedirs(quarantine_folder_labels, exist_ok=True)
            shutil.move(label_directory, quarantine_folder_labels)

        # for i,p in enumerate(self.image_paths): if os.path.dirname(p) == image_directory:
        # 		print(f"removing {p}")
        # 		self.image_paths.remove(p)
        self.image_paths = [
            x for x in self.image_paths if os.path.dirname(x) != image_directory
        ]
        if self.index > len(self.image_paths):
            self.index = 0
        self.image_cache = {}
        self.cache_index = 999999999999

    def next_different_image(self):
        self.index = get_next_different_image_index(
            self.image_paths, self.index, previous=False
        )

    def previous_different_image(self):
        if self.index == 0:
            return
        self.index = get_next_different_image_index(
            self.image_paths, self.index, previous=True
        )

    def delete_image(self):
        image_path = self.image_paths[self.index]
        os.remove(image_path)
        del self.image_paths[self.index]
        self.total_images -= 1
        if self.total_images == 0:
            self.exit_viewer()
        else:
            self.index %= self.total_images

    def load_image(self, image_path):
        image = cv2.imread(image_path)
        image = resize_image(image, 1820, 980)
        # Add image path as text overlay
        cv2.putText(
            image,
            f"({self.step}):{image_path}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )
        return image

    def load_images(self):
        while not self.stopped:
            # if abs(self.cache_index - self.index) > cache_size//4 * self.step or self.cache_step!=self.step:
            # 	self.cache_index = self.index
            # 	self.cache_step = self.step
            # 	self.image_cache = {}
            # 	indices_to_load = [self.cache_index]
            # 	for i in range(1,cache_size//2):
            # 		indices_to_load.append(i)
            # 		indices_to_load.append(-i)
            # 	for i in indices_to_load:
            # 		im_index = (self.cache_index + i * self.step)%self.total_images
            # 		if abs(self.cache_index - self.index) > cache_size//4 * self.step or self.cache_step!=self.step or im_index in self.image_paths:
            # 			# skip ahead if index already changed again
            # 			print("skipping")
            # 			continue
            # 		print(f"loading {im_index}")
            # 		if im_index >= len(self.image_paths):
            # 			continue
            # 		image_path = self.image_paths[im_index]
            # 		if os.path.exists(image_path):
            # 			self.image_cache[im_index] = self.load_image(image_path)
            # 		else:
            # 			break
            # 		time.sleep(0.001)

            time.sleep(0.1)

    def open_folder(self):
        image_path = self.image_paths[self.index]
        folder_path = os.path.dirname(image_path)
        subprocess.Popen(f"explorer.exe {folder_path}")

    def exit_viewer(self):
        self.stopped = True
        cv2.destroyAllWindows()
        self.loader.join()
        sys.exit()

    def display_images(self):
        while True:
            if self.index not in self.image_cache:
                print(self.index)
                image_path = self.image_paths[self.index]
                print(self.image_paths[:10])
                if not os.path.exists(image_path):
                    print(self.index, image_path)
                    cv2.destroyAllWindows()
                    sys.exit()
                    continue

                image = self.load_image(image_path)
            else:
                image = self.image_cache[self.index]
            cv2.imshow("Image Viewer", image)
            key = cv2.waitKey(0)
            if key in self.key_actions:
                self.key_actions[key]()


def parse_yolo_annotations(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()

    annotations = []
    for line in lines:
        data = line.strip().split()
        if len(data) < 4:
            continue
        label = data[0]
        x_center = float(data[1])
        y_center = float(data[2])
        width = float(data[3])
        height = float(data[4])

        annotations.append(
            {
                "label": label,
                "x_center": x_center,
                "y_center": y_center,
                "width": width,
                "height": height,
            }
        )

    return annotations


def draw_bounding_boxes(image, annotations):
    for annotation in annotations:
        label = annotation["label"]
        x_center = int(annotation["x_center"] * image.shape[1])
        y_center = int(annotation["y_center"] * image.shape[0])
        width = int(annotation["width"] * image.shape[1])
        height = int(annotation["height"] * image.shape[0])

        x_min = int(x_center - width / 2)
        y_min = int(y_center - height / 2)
        x_max = int(x_center + width / 2)
        y_max = int(y_center + height / 2)

        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        cv2.putText(
            image,
            label,
            (x_min, y_min - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )

    return image


class YOLOImageLoader(ImageLoader):
    def load_image(self, image_path):
        img = super().load_image(image_path)
        ext = image_path.split(".")[-1]
        label_path = image_path.replace("images", "labels").replace(ext, "txt")
        print(label_path)
        if os.path.exists(label_path):
            annotations = parse_yolo_annotations(label_path)
            draw_bounding_boxes(img, annotations)
        return img
