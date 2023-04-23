import os
import time
import glob
from dataclasses import dataclass

category_files = glob.glob("./categories/*/*",recursive=True)

channels = []
@dataclass
class ChannelInfo:
    category:str
    isVideo:bool
    url:str
    min_views:int

for fi in category_files:
    category = fi.split('/')[-1]
    with open(fi,'r') as f:
        text = f.read()
    for channel_info in text.split('\n'):
        channel_url,min_views = channel_info.split(',')
        channels.append(ChannelInfo(category,"video" in fi,channel_url.split('&')[0],int(min_views)))

base_path_video = "/mnt/HardDrive/Media/Video/Youtube/"
base_path_audio = "/mnt/HardDrive/Media/Audio/Youtube/"
base_path_video = "./Video/Youtube/"
for channel in channels:
    if channel.isVideo:
        cat_path = f"{base_path_video}/{channel.category}"
    else:
        continue
        cat_path = f"{base_path_audio}/{channel.category}"
    name_out = f'"{cat_path}/%(title)s.%(ext)s"'
    # note = f"Downloading {channel.url} into {cpathat_path}"
    from gi.repository import Notify
    # Notify.init("Youtube DL ")
    # Notify.Notification.new(note).show()
    print(cat_path)
    cmd = f"yt-dlp -o {name_out} {channel.url} --match-filter \"view_count>={channel.min_views}\" -I :30"
    if not channel.isVideo:
        cmd+=" -f 140"
    os.system(cmd)

