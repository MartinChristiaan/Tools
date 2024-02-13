# %%
# setup dataset
# %load_ext autoreload
# %autoreload 2
import cv2
import numpy as np
import streamlit as st
from blitzmotion.writer import MotionSADWriter
from dlutils_ii import CacheReader
from example.datasets import get_mantis

mantis = get_mantis()
# for c in mantis:
MotionSADWriter.export_multiprocessed(mantis)


# sad_bwd = pipelines[1].process(frames[0], frames[1], t)
