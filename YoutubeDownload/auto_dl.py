# import os
# import time
# import glob
# from dataclasses import dataclass
# home = os.path.expanduser('~')

# import logging
# os.makedirs(f"{home}/logs/",exist_ok=True)
# logging.basicConfig(filename=f'{home}/logs/autodl.log', encoding='utf-8', level=logging.DEBUG)
# logging.debug('This message should go to the log file')


# category_files = glob.glob(f"{home}/git/tools/YoutubeDownload/categories/*/*",recursive=True)
# logging.debug(category_files)

# channels = []
# @dataclass
# class ChannelInfo:
#     name:str
#     category:str
#     isVideo:bool
#     url:str
#     min_views:int

# for fi in category_files:
#     category = fi.split('/')[-1]
#     with open(fi,'r') as f:
#         text = f.read()
#     for channel_info in text.split('\n'):
#         channel_url,min_views = channel_info.split(',')
#         name = channel_url.split("@")[-1]
#         channels.append(ChannelInfo(name,category,"video" in fi,channel_url.split('&')[0],int(min_views)))

# base_path_video = "/mnt/HardDrive/Media/Video/Youtube/"
# base_path_audio = "/mnt/HardDrive/Media/Audio/Youtube/"
# for channel in channels:
#     if channel.isVideo:
#         cat_path = f"{base_path_video}/{channel.category}/{channel.name}"
#     else:
#         continue
#         cat_path = f"{base_path_audio}/{channel.category}"
#     name_out = f'"{cat_path}/%(title)s.%(ext)s"'
#     # note = f"Downloading {channel.url} into {cpathat_path}"
#     from gi.repository import Notify
#     # Notify.init("Youtube DL ")
#     # Notify.Notification.new(note).show()
#     print(cat_path)
#     cmd = f"yt-dlp -o {name_out} {channel.url} --match-filter \"view_count>={channel.min_views}\" -I :5"
#     if not channel.isVideo:
#         cmd+=" -f 140"
#     os.system(cmd)
