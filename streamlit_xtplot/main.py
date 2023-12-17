

#%%
import pandas as pd
import glob
import streamlit as st
import os
import yaml
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio


@st.cache_resource()
def xt_plot(sequence, tracktype,fps):

	datas = []
	name, tracks_per_frame = sequence
	t_array = np.arange(len(tracks_per_frame)) * 1 / fps

	# print(tracks_per_frame)
	for t, tracks in zip(t_array, tracks_per_frame):
		for track in tracks:
			datadict = {
				"x1": track.bounding_box[0],
				"y1": track.bounding_box[1],
				"x2": track.bounding_box[2],
				"y2": track.bounding_box[3],
				"x": (track.bounding_box[2] + track.bounding_box[0]) // 2,
				"t": t,
				"vavg": track.v_avg,
				# "log": track.log,
				"mature": track.mature,
				"id": track.id,
				"source": name,
			}
			datas += [datadict]

	# }
	df = pd.DataFrame(datas)
	pio.templates.default = "plotly"

	return px.line(
		df,
		x="t",
		y="x",
		color="id",
		hover_data=list(datadict.keys()),
		facet_col="source",
		markers=True,
		color_discrete_sequence=[
		"#0068c9",
		"#83c9ff",
		"#ff2b2b",
		"#ffabab",
		"#29b09d",
		"#7defa1",
		"#ff8700",
		"#ffd16a",
		"#6d3fc0",
		"#d5dae5",
		],
		title=tracktype,
	)

import cv2

@st.cache_resource()#(hash_funcs={cv2.VideoCapture: lambda x:x})
def get_video_reader(path):

	mm = MediaManager(path,video_suffix='.mp4')
	return mm

def get_frame(reader,index):
	reader.set(cv2.CAP_PROP_POS_FRAMES, index)
	ret,frame = reader.read()
	if ret:
		frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
	return frame


from media_manager.core import MediaManager
import streamlit as st
import streamlit as st
import streamlit.components.v1 as components

path = '/diskstation/mantis/Security/20230910_drone_recording/videosets/video/DJI_202309100220_001/wide_hd'
mm = get_video_reader(path)
if 'timestamp_idx' not in st.session_state:
    st.session_state['timestamp_idx'] = 0

timestamps = mm.timestamps

def left_callback():
	global timestamp_idx
	st.session_state['timestamp_idx']-=1
	print('updated')

def right_callback():
	global timestamp_idx
	st.session_state['timestamp_idx']+=1
	print('updated',timestamp_idx)

timestamp_idx = st.session_state['timestamp_idx']

frame = mm.get_frame(timestamps[timestamp_idx])
st.image(frame,str(timestamps[timestamp_idx]))
left_col, right_col, _ = st.columns([1, 1, 3])

st.text(timestamp_idx)

with left_col:
	st.button('PREV', on_click=left_callback)

with right_col:
	st.button('NEXT', on_click=right_callback)

components.html(
	"""
<script>
const doc = window.parent.document;
buttons = Array.from(doc.querySelectorAll('button'));
const left_button = buttons.find(el => el.innerText === 'PREV');
const right_button = buttons.find(el => el.innerText === 'NEXT');
doc.addEventListener('keydown', function(e) {
	switch (e.keyCode) {
		case 37: // (37 = left arrow)
			left_button.click();
			break;
		case 39: // (39 = right arrow)
			right_button.click();
			break;
	}
});
</script>
""",
	height=0,
	width=0,
)

# 







	




# st.set_page_config(layout="wide")
# col1,col2,col3 = st.columns(3)
# with col1:
# 	runs =  modify_windows_paths(glob.glob("../data/offline/*/*/"))
# 	sequences = {x.split('/')[-2] for x in runs}
# 	configs = {x.split('/')[-3] for x in runs}

# 	base_dir = "../data/offline/"
# 	sequence_tuples = []
# 	# with col1:
# 	sequence = st.selectbox(
# 		'sequence',
# 		sequences)

# 	config = st.selectbox(
# 		'config',
# 		configs)

# 	# im_width = st.slider("Im_width")

# 	# print(track_maker)
# 	data_path = f'{base_dir}{config}/{sequence}/'
# 	config_file=f"./work/configs/{config}.yaml"
# 	tracks_dict,detection_dict = get_track_and_detection_data(data_path)

# 	detection_type = st.selectbox("detection",
# 		list(detection_dict.keys())
# 	)

# 	track_type = st.selectbox(
# 		'track_type',
# 		list(tracks_dict.keys()))

# 	if st.button("Re-Process Sequence"):
# 		sequence_file = f"../data/video/{sequence}.mp4"
# 		os.system('pwd')
# 		os.system(f"python3 -m core.offline_runner --config_sub {config_file} --source {sequence_file} --until cropper")

# 	with open(config_file, 'r') as file:
# 		config_dict = yaml.safe_load(file)
# 		if 'detector' in config_dict:

# 			fps= config_dict['detector']['fps_limit']
# 		else:
# 			fps = 3

# video_path  = f"../data/video_{fps}fps/{sequence}.mp4"
# reader = get_video_reader(video_path)
# num_frames = reader.get(cv2.CAP_PROP_FRAME_COUNT)
# # if os.path.exists(tracks_path):

# with col3:
# 	tracks = tracks_dict[track_type]
# 	if len(tracks) > num_frames:
# 		tracks = tracks[::10] # TODO add proper down convert
# 	# track_fps = fps * len(tracks)/num_frames
# 	# print(track_fps)
# 	fig = xt_plot((config,tracks),track_type,fps)

# 	selected_points = plotly_events(fig, click_event=True,override_height=400)
	
# 	if len(selected_points):
# 		with open('tmp_points.json','w') as f:
# 			json.dump(selected_points,f)


# with col2:
# 	# detections_per_frame = load_pickle(detections_path)
# 	# tracks_per_frame = load_pickle(tracks_path)
# 	cropper = Cropper(Config.from_yaml(BASE_CONFIG),data_path)
# 	# reader_cropped = get_video_reader(video_path_cropped)
# 	frame_index = 0 

# 	with open('tmp_points.json','r') as f:
# 		selected_points = json.load(f)

# 	frame_index = int(selected_points[0]['x'] * fps)

# 	vizualizer = DebugVizualizer(create_writer=False)
# 	frame = get_frame(reader,frame_index)
# 	detection_frame = vizualizer.create_detection_frame(frame,detection_dict[detection_type][frame_index],"")
# 	track_frame = vizualizer.create_tracker_frame(frame,tracks_dict[track_type][frame_index],"")

# 	crop_positions = tracks_dict['crop_positioner']
# 	realtime_factor = len(crop_positions)/num_frames # To go from low fps tracks to realtime tracks
# 	realtime_frame_index = int(frame_index * realtime_factor)
# 	cropped_frame = cropper(frame_index/3,frame,crop_positions[realtime_frame_index])

# 	st.image(detection_frame,detection_type)#,width=600)
# 	st.image(track_frame,track_type)#,width=600)
# with col1:
# 	st.image(cropped_frame,"cropped")#,width=600)
# # else:
# # 	with col2:
# # 		st.text("Sequence not yet available")