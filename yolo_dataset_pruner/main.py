import os
import sys

import cv2

dataset_path = r"\mnt\dl-11\data\leeuwenmcv\mantis\rotterdam_eo_yolo"
blacklist = os.path.join(dataset_path, "blacklist")


def determine_sequence_is_good(sequence_folder):
    image_folder = os.path.join(dataset_path, "images", sequence_folder)
    label_folder = os.path.join(dataset_path, "labels", sequence_folder)

    image_files = sorted(os.listdir(image_folder))
    sorted(os.listdir(label_folder))
    print(image_files)
    if len(image_files) < 5:
        return False
    while True:
        for label_file, image_file in zip(label_file, image_files):
            image_path = os.path.join(image_folder, image_file)

            image = cv2.imread(image_path)
            scale_factor = 1500 / image.shape[0]
            image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
            cv2.imshow("Sequence Images", image)
            key = cv2.waitKey(20)

            # Allow the user to draw bounding boxes...
            # Perform tracking on these bounding boxes

            # Write them to a csv file...
            # Perform downscaling using the camera model...
            # Tune the parameters using inputs from the keyboard.

            if key == ord("q"):  # Change delay (e.g., 100) as desired
                cv2.destroyAllWindows()
                sys.exit()
            elif key == ord("n"):
                cv2.destroyAllWindows()
                return False
            elif key == ord("y"):
                cv2.destroyAllWindows()
                return True


def process_sequences():
    sequence_folder = os.path.join(dataset_path, "images_debug")
    sequences = sorted(os.listdir(sequence_folder))

    for sequence in sequences:
        determine_sequence_is_good(sequence)


if __name__ == "__main__":
    process_sequences()
