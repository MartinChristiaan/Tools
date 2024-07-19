import os
import shutil

import cv2
import pandas as pd
from tqdm import tqdm

video_folder = r"\\diskstationii1.tsn.tno.nl\deeplearning\datasets\Singapore_Maritime_Dataset\VIS_Onshore\VIS_Onshore\Videos"
tracks_folder = r"\\diskstationii1.tsn.tno.nl\deeplearning\datasets\Singapore_Maritime_Dataset\VIS_Onshore\VIS_Onshore\tracks"
output_dir = "/data/onshore"
video_output_dir = f"{output_dir}/video"
results_dir = f"{output_dir}/results/"

downscales = [1, 2, 4]
# Copy video and generate logfile
for video in tqdm(os.listdir(video_folder)):
    name = video.split(".")[0]
    for downscale in downscales:
        # try:

        video_output_path = f"{video_output_dir}/{name}_{downscale}x"
        tracks_output_path = f"{results_dir}/{name}_{downscale}x/tracks/"
        os.makedirs(video_output_path, exist_ok=True)
        os.makedirs(tracks_output_path, exist_ok=True)
        processed_video_path = f"{video_output_path}/{name}_{downscale}x.avi"
        cmd = f"ffmpeg -i {video_folder}/{video} -vf scale=iw/{downscale}:ih/{downscale} -c:v libx264 -preset veryslow -crf 0 temp.avi"
        os.system(cmd)
        shutil.move("tmp.avi", processed_video_path)

        # cap = cv2.VideoCapture()
        # fps=  cap.get(cv2.CAP_PROP_FPS)

        # num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # logfile = "\n".join([f"{i/fps} {i/fps}" for i in range(num_frames)])
        # with open(f"{video_output_path}/{name}.log",'w') as f:
        # 	f.write(logfile)

        # track_file = f"{tracks_folder}/{name}.csv"
        # df = pd.read_csv(track_file)
        # df['timestamp'] = df['frame_id']/fps
        # # columns_to_downscale= [f'bbox_{x}' for x in 'xywh']
        # for x in 'xywh':
        # 	df[f'bbox_{x}'] /= downscale

        # df.to_csv(f"{tracks_output_path}/tracks_gt.csv",index=False)
        break
    break

    # except:
    # 	pass

    # except:
    # 	print(f"{video} failed")

    # shutil.rmtree(video_output_path)
    # shutil.rmtree(tracks_output_path)
