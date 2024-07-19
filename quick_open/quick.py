import argparse
import glob
import os
import socket

import pyfzf

pc_hostname = socket.gethostname()
home = os.path.expanduser("~")

parser = argparse.ArgumentParser(
    prog="quick",
    description="What the program does",
    epilog="Text at the bottom of help",
)
parser.add_argument("-e", "--explore", action="store_true")
parser.add_argument("-c", "--clip", action="store_true")
parser.add_argument("-r", "--rsync", action="store_true")
args = parser.parse_args()

import yaml


def get_folders():
    with open(f"quick_folders.{pc_hostname}", "r") as f:
        folders = f.readlines()

    with open("../network_command_gen/hosts.yml", "r") as f:
        hosts = yaml.safe_load(f)
    mnt_path = "/mnt/"
    for hostname, hostdata in hosts.items():
        if hostname not in os.listdir(mnt_path):
            continue
        folders.append(f"/mnt/{hostname}/{hostdata['gitpath']}/*/")
        folders.append(f"/mnt/{hostname}/{hostdata['datapath']}/*/")

    combined_dirs = []
    for folder in folders:
        folder = folder.replace("\n", "")
        # print(folder)
        # print(os.listdir(folder))
        folder = folder + "/*"
        combined_dirs += [x for x in glob.glob(folder) if os.path.isdir(x)]
    return combined_dirs

    # with open('/tmp/interesting_dirs','w') as f:
    #     f.write("\n".join(combined_dirs))


def select_folder(folders):
    prompt = pyfzf.FzfPrompt()
    return prompt.prompt(folders)[0]


def open_explorer():
    dirs = get_folders()
    target_dir = select_folder(dirs)
    if pc_hostname == "PC-42089":
        cmd = f"cd {target_dir} && explorer.exe . "
    else:
        cmd = f"nautilus {target_dir}"
    os.system(cmd)


def to_clipboard():
    dirs = get_folders()
    target_dir = select_folder(dirs)
    if pc_hostname == "PC-42089":
        cmd = f"echo {target_dir} | clip.exe "
    else:
        cmd = f"xclip -sel clip {target_dir} "
    os.system(cmd)


def rsync():
    dirs = get_folders()
    source_dir = select_folder(dirs)
    target_dir = select_folder(dirs)
    command = f"rsync -azP {source_dir} {target_dir}"
    print(command)
    isok = input("Run this command? [y/n]")
    if isok == "y":
        os.system(command)
        print(source_dir)
        print(target_dir)
    else:
        print("canceled")


if __name__ == "__main__":
    if args.explore:
        open_explorer()
    if args.clip:
        to_clipboard()
    if args.rsync:
        rsync()
