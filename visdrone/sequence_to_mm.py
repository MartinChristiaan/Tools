#%%
import os
from pathlib import Path
import shutil

import pandas as pd
data = '/data/VisDrone2019-VID-val/VisDrone2019-VID-val/'
mm_dir=  '/data/visdrone/'

from media_manager.core import MediaManager

sequences = list((Path(data)/'sequences').glob('*'))
annotation_files = list((Path(data)/'annotations').rglob('*.txt'))
sequences.sort()
annotation_files.sort()


for annotations_file,seq in zip(annotation_files,sequences):
	# convert video
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
	# convert annotations
	with open(annotations_file,'r') as f:
		text = f.read()
	lines= text.split("\n")
	out_data = []
	label_lut = {
		0:"ignored regions",
		1:"pedestrian",
		2:"people",
		3:"bicycle",
		4:"car",
		5:"van",
		6:"truck",
		7:"tricycle",
		8:"awning-tricycle",
		9:"bus",
		10:"motor",
		11:"others"
	}

	for line in lines:
		line_split =  line.split(',')
		if len(line_split) > 1:
			idx,frame_no,bbox_x,bbox_y,bbox_w,bbox_h,ignore,class_id,_,_ = line.split(',')
			label = label_lut[int(class_id)]	
			datadict = {
				"frame_no":frame_no,
				"bbox_x":bbox_x,
				"bbox_y":bbox_y,
				"bbox_w":bbox_w,
				"bbox_h":bbox_h,
				"ignore":ignore,
				"class_id":class_id,
				"label":label,
				"timestamp":int(frame_no)/25.9
			}
			out_data.append(datadict)
	# annotations_dir= Path(f"{resultsdir}/_annotations")
	# annotations_dir.mkdir(parents=True,exist_ok=True)

	mm.save_annotations(pd.DataFrame(out_data))
	# pd.DataFrame(out_data).to_csv(f"{annotations_dir}/{seq.stem}_annotations.csv",index=False)
	
		
	



	
 
	


	







