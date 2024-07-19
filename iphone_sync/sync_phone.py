# %%
import os
import time

from gtts import gTTS
from playsound import playsound

home = os.path.expanduser("~")


def say(text):
    tts = gTTS(text)
    tts.save("tmp.mp3")
    playsound("tmp.mp3")


import logging

os.makedirs(f"{home}/logs/", exist_ok=True)
logging.basicConfig(
    filename=f"{home}/logs/Sync.log", encoding="utf-8", level=logging.DEBUG
)
logging.debug("This message should go to the log file")


def get_all_files(path):
    files = []
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    return files


phone_location_audio = "/run/user/1000/gvfs/afc:host=00008110-001460D41145801E,port=3/com.foobar2000.mobile"
phone_location_video = (
    "/run/user/1000/gvfs/afc:host=00008110-001460D41145801E,port=3/org.videolan.vlc-ios"
)
phone_location_obsidian = (
    "/run/user/1000/gvfs/afc:host=00008110-001460D41145801E,port=3/md.obsidian/Notes/"
)
phone_location_voide_notes = "/run/user/1000/gvfs/afc:host=00008110-001460D41145801E,port=3/com.TapMediaLtd.VoiceRecorderFREE/"
last_sync_time = 0

computer_location_music = "/mnt/HardDrive/Media/Music"
computer_location_voice_notes = "/mnt/HardDrive/Media/VoiceNotes/"


def look_for_transfer():
    all_files = get_all_files(phone_location_audio)
    all_files_computer = get_all_files(computer_location_music)
    # %%
    raw_paths_phone = {x.replace(phone_location_audio, "") for x in all_files}
    # raw_paths_computer = [x.replace(computer_location_music,"") for x in all_files_computer]
    files_to_transfer = []
    for p in all_files_computer:
        p_raw = p.replace(computer_location_music, "")
        if p_raw not in raw_paths_phone:
            files_to_transfer.append(p)

    from tqdm import tqdm

    for p in tqdm(files_to_transfer):
        dest = p.replace(computer_location_music, phone_location_audio)
        out_dir = "/".join(dest.split("/")[:-1])
        os.makedirs(out_dir, exist_ok=True)
        os.system(f'cp "{p}" "{dest}"')


# print(raw_paths_phone)
while True:
    if os.path.isdir(phone_location_audio) and time.time() - last_sync_time > 60 * 10:
        logging.info("syncing phone")
        # say("Master, I am syncing your phone")
        cmd = f"unison -auto -batch -fat -fastcheck true /home/martin/Documents/NotesObsidian/ {phone_location_obsidian}"
        os.system(cmd)
        os.system(
            f"rsync -azP {phone_location_voide_notes} {computer_location_voice_notes}"
        )
        look_for_transfer()
        last_sync_time = time.time()

# 	else:

# 		logging.info("phone not found")
# 		time.sleep(60)
