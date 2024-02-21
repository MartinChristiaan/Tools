#%%
import os
from pathlib import Path
import shutil
data = '/data/VisDrone2019-VID-val/VisDrone2019-VID-val/'
mm_dir=  '/data/visdrone/'

from media_manager.core import MediaManager

sequences = (Path(data)/'sequences').glob('*')
for seq in sequences:
	videodir = Path(f"{mm_dir}/video/{seq.stem}")
	videodir.mkdir(parents=True,exist_ok=True)
	resultsdir=  Path(f"{mm_dir}/results/{seq.stem}")
	resultsdir.mkdir(parents=True,exist_ok=True)
	imgdir = videodir / 'images'
	logfile = videodir/"images.log"
	# os.system(f'rsync -azP {seq}/ {imgdir}')
	images = list(seq.glob('*.jpg'))
	images.sort()

	for i,img in enumerate(images):
		filename = str(i).zfill(5) + '.jpg'
		shutil.copy(img,imgdir/filename)
	num_images = len(list(imgdir.glob('*.jpg')))
	logstr = ""
	for i in range(num_images):
		timestamp = i/25
		logstr += f"{timestamp}\n"
	with open(logfile,'w') as f:
		f.write(logstr)
	
	mm = MediaManager(videodir,video_suffix='.jpg')
	frame = mm.get_frame(1)


	







