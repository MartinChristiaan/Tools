# %%
%load_ext autoreload
%autoreload 2

import multiprocessing

import dlutils_ii as du
from annotator import BoundingBoxAnnotator
from cache_annotator import IOManager
from config.dataset import get_mantis
from torch import mul
from tqdm import tqdm

mantis = get_mantis()
from multiprocessing import Pool

from pre_annotation_writer import PreAnnotationWriter


def process_config(config):
	try:
		writer = PreAnnotationWriter(config, [0, -15, 15], source="tyolov8/tracks_tyolov8m-30112023.csv")
		writer.write()
	except Exception as e:
		print(e)

pool = Pool()
pool.map(process_config, mantis)
pool.close()
pool.join()
