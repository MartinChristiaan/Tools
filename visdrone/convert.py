#%%
import os
from pathlib import Path
import pandas as pd
home = os.path.expanduser('~')
annotation_dir = Path(f"{home}/annotations")
annotation_files = annotation_dir.rglob('*.txt')
for fil in annotation_files:
	with open(fil,'r') as f:
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
	name = fil.stem
	pd.DataFrame(out_data).to_csv(f"{name}_annotations.csv",index=False)
		
	

