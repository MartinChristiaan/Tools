import os


def summarize_dataset(folder):
    summary = {}

    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            directory = os.path.relpath(root, folder)

            if directory not in summary:
                summary[directory] = []
            if len(summary[directory]) < 2:
                summary[directory].append(file_path)

    return summary


def print_summary(summary):
    for directory, files in summary.items():
        for file in files:
            print(file)
        print()


# Example usage
dataset_folder = "/home/leeuwenmcv/data/CEGR"
summary = summarize_dataset(dataset_folder)
print_summary(summary)
