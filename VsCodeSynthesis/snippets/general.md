# argparse
parser = argparse.ArgumentParser(
                    prog = 'ProgramName',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
parser.add_argument('--filename',type=str,default=default)
parser.add_argument('-v', '--verbose',action='store_true')
args = parser.parse_args()

# folder read

${1:folder} = "${2:path}"
for filename in os.listdir(${1:folder}):
    with open(f'{${1:folder}}/{filename}', 'r') as f:
        text = f.read()

# Logger

import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

# videoshow

vid = cv2.VideoCapture(${1:0})
while(True):
    ret, frame = vid.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vid.release()
cv2.destroyAllWindows()

# rdamodule

#!/usr/bin/python3 -u
import os
import numpy as np
import rda
from rda_utils.basemodule import RDAModuleBase
from rda_utils.fifo import RDAOutputFiFo,PickleOutputFiFo
home = os.path.expanduser('~')
class v4r_${1:ModuleName}(RDAModuleBase):
	def __init__(self) -> None:
		self.input = "input"

	def init(self, h) -> None:
		self.output= PickleOutputFiFo()
		self.output.create(h)

	def update(self, h):
		item,attr = rda.getvarex(h,self.input)
		self.output.put(h,[item],attr)

if __name__ == "__main__":
    m = v4r_${1:ModuleName}
    rda.rda_module(m.arg, m.init, m.body, m.trigger, m.cleanup)

# engine

from typing import Dict, List
from engine_utils.engine_utils import AbstractEngineJsonOut,Output1DictListMixIn,AbstractEngine,Input1MixIn
import os

class ${1:EngineExample}(Input1MixIn,Output1DictListMixIn,AbstractEngine):
    def __init__(self, parameter1=0, parameter2=2.0):
        super().__init__()
        self._config["parameter1"] = parameter1 # int
        self._config["parameter2"] = parameter2 # float

    def init_sample(self, timestampdata, data): # optional!!
        self.something_to_intialize = some_fun(data[0][0]["data"])

    def process_sample(self, timestampdata, data):
        data = data[0][0]["data"]
        d = 1.0
        # when a list of dicts is returned, add timestamp!!!
        return [[{"timestamp": timestampdata["timestamp"], "some_value": d}]]

# bookmarks

import json

bookmarks = "/home/martin/.config/BraveSoftware/Brave-Browser/Default/Bookmarks"

with open(bookmarks,'r') as f:
	bookmarks = json.load(f)

top_level_items =bookmarks['roots']['bookmark_bar']['children']
for item in top_level_items:
	if "Spotify" in item['name']:
		for linkitem in item['children']:
			url = linkitem['url']
			print(url)
