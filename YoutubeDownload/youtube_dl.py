import os
import time

import pyperclip


# f7 is download
# f8 is fzf to select from items
def grab_url():
    hotkey("ctrl", "l")
    time.sleep(1)
    hotkey("ctrl", "c")
    return pyperclip.paste()


with open("/tmp/youtube_category", "r") as f:
    path = f.read()
category = path.split("/")[-2]
datatype = path.split("/")[-3]
url = grab_url()
url = url.split("&")[0]
filename = f'"{path}%(title)s.%(ext)s"'
note = f"Downloading {url} into {datatype}/{category}"
from gi.repository import Notify

Notify.init("Youtube DL Hotkeys")
Notify.Notification.new(note).show()
if datatype == "Music":
    os.system(f"yt-dlp -o {filename} -f 140 {url}")
elif datatype == "Video":
    os.system(f"yt-dlp -o {filename} {url}")
