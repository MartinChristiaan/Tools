from typing import Any, List
from state import Observable

import os
from pathlib import Path
from loguru import logger

from videosets_ii.videosets_ii import VideosetsII
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks,TrackUpdates
import pandas as pd

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath= basedirpath)#basedirpath)
default_vset = 'drone_detection_dataset_2021'
default_cams=  videosets[default_vset].cameras
default_cam=  videosets[default_vset].cameras[5]

class Container:
	def __init__(self,name) -> None:
		self.name = name
	def get_observables(self) -> List[Observable]:
		observables = []
		for k,v in self.__dict__.items():
			print(k)
			if isinstance(v,Observable):
				observables.append(v)
		return observables

class MediaManagerSelection(Container):
	def __init__(self) -> None:
		self.videoset = Observable(default_vset,'videoset',uimode='selectbox',options=default_vset)
		self.camera = Observable(default_cam,'camera',uimode='selectbox',options=default_cams)
		self.videoset.subscribe(self.on_videoset_update)
		super().__init__('Media Manager Selection')

	def on_videoset_update(self):
		self.camera.options = (videosets[self.videoset.value].cameras)
	

 
class API:
	def __init__(self,containers:List[Container]) -> None:
		self.containers = containers
		self.container_lut = {x.name:x for x in self.containers}
	
	def get_ui_data(self):
		data = {}
		print(self.containers)
		for c in self.containers:
			data[c.name] = {x.name:x.get_ui_data() for x in  c.get_observables()}
		return data
	
	def set_ui_data(self,data):
		for k,container in self.container_lut.items():
			cdata = data[k] 
			for observable in container.get_observables():
				observable.set_value(cdata[observable.name])
		return self.get_ui_data()


		
		
from flask import Flask, request, jsonify
from typing import List

app = Flask(__name__)

# Create an instance of the Server class with some initial containers
media_manager_selection = MediaManagerSelection()
initial_containers = [media_manager_selection]  # Define your initial containers here
server = API(initial_containers)
# Endpoint to get UI data
@app.route('/get_ui_data', methods=['GET'])
def get_ui_data():
    data = server.get_ui_data()
    return jsonify(data)

# Endpoint to set UI data
@app.route('/set_ui_data', methods=['POST'])
def set_ui_data():
    data = request.json
    updated_data = server.set_ui_data(data)
    return jsonify(updated_data)

if __name__ == '__main__':
    app.run(debug=True)

