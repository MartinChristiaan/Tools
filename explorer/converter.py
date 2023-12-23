import glob
import os
import shutil

from tqdm import tqdm


def convert_paths(input_paths, output_root):
    converted_paths = []

    for input_path in input_paths:
        path_parts = input_path.split("/")
        file_name = path_parts[-1]

        category = path_parts[-2]
        file_name_parts = file_name.split("_")
        folder_name = file_name_parts[0]
        file_name = "_".join(file_name_parts[1:])
        if (
            file_name.endswith(".jpg")
            or file_name.endswith(".jpeg")
            or file_name.endswith(".png")
        ):
            output_path = os.path.join(
                output_root, "images", category, folder_name, file_name
            )
        else:
            output_path = os.path.join(
                output_root, "labels", category, folder_name, file_name
            )

        converted_paths.append(output_path)

    return converted_paths


def create_directories_and_copy_files(input_paths, converted_paths):
    for input_path, output_path in tqdm(zip(input_paths, converted_paths)):
        if output_path[-1] == "/":
            output_path = output_path[:-1]
        # print(input_path,output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        shutil.copyfile(input_path, output_path)


# Example usage
input_paths = glob.glob("/home/leeuwenmcv/data/CEGR/*/*")
output_root = "/home/leeuwenmcv/data/CEGR2/"
converted = convert_paths(input_paths, output_root)
create_directories_and_copy_files(input_paths, converted)
# for input_path, output_path in zip(input_paths, converted_paths):
# 	shutil.copy(input_path,output_path)
# print("Input:", input_path)
# print("Output:", output_path)
# print()
