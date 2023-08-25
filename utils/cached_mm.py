import os
from pathlib import Path
from media_manager.core import MediaManager
from dtypes import ProcessingConfig

class ProcessedMediaManager(ProcessingConfig):
	def load_media_manager(self):
		pass
	
 
		

	def update_available(self):
		if not self.local_path.exists():
			return True
		t_local = os.path.getmtime(self.local_path)
		t_video = os.path.getmtime(self.args_base_mm['filepath'])
		t_procfile = os.path.getmtime(self.procfile)
		if t_video > t_local or t_procfile > t_local:
			return True
	
	def run_processing():
		# cropping
		# scaling
		# sampling

	
	
		


		# if os.path.exists(local_path):


			# check if it should be updatad





		# super().__init__(
		#     filepath,
		#     logfilepath,
		#     log_column_to_use,
		#     result_dirpath,
		#     video_suffix,
		#     videoreader,
		# )
