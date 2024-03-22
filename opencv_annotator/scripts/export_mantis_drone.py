# %%
%load_ext autoreload
%autoreload 2

import multiprocessing

import dlutils_ii as du
from config.dataset import get_mantis
from torch import mul
from tqdm import tqdm

mantis = get_mantis()
from multiprocessing import Pool

from opencv_annotator.pre_annotation_writer import PreAnnotationWriter
from config.dataset import get_tie

def process_config(config):
	try:
		writer = PreAnnotationWriter(config, [0, -15, 15], source="tyolov8/tracks_proposed.csv")
		writer.write()
	except Exception as e:
		print(e)

pool = Pool()
pool.map(process_config, get_tie())
pool.close()
pool.join()
