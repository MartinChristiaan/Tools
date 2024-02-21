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
	break
lines= text.split("\n")
out_data = []
for line in lines:
	line_split =  line.split(',')
	if len(line_split) > 1:
		idx,frame_no,bbox_x,bbox_y,bbox_w,bbox_h,ignore,class_id,_,_ = line.split(',')
		datadict = {
			"frame_no":frame_no,
			"bbox_x":bbox_x,
			"bbox_y":bbox_y,
			"bbox_w":bbox_w,
			"bbox_h":bbox_h,
			"ignore":ignore,
			"class_id":class_id
		}
		out_data.append(datadict)
pd.DataFrame(out_data).to_csv("annotations.csv",index=False)
	
 

