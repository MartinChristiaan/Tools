
# class which runs several processes whcih share an input queue
import multiprocessing as mp
import random
import time
from typing import Dict

def example_process(input_queue:mp.Queue, output_queue:mp.Queue,val_dict:Dict):

	while not val_dict['stop']:
		if not input_queue.empty():
			item = input_queue.get()
			timestamp,value = item
			sleeptime = random.randint(1, 5)/1000
			time.sleep(sleeptime)
			output_queue.put((timestamp, value))

class SharedQueueProcessManager():
	def __init__(self,process) -> None:
		self.process = process
		self.input_queue = mp.Queue()
		self.output_queue = mp.Queue()
		self.val_dict = mp.Manager().dict()
		self.val_dict['stop'] = False
	
	def start(self,kwargs):
		process = mp.Process(target=self.process, args=(self.input_queue, self.output_queue,self.val_dict),kwargs=kwargs)
		
    
	
