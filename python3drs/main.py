import time

# %%
# setup dataset
# %load_ext autoreload
# %autoreload 2
import cv2
import numpy as np
import streamlit as st
from datasets import get_mantis
from dlutils_ii import CacheReader, DatasetConfig
from motion_estimation import MotionEstimator, OutSadComputer
from motion_refinement import mvf_refine
from motion_upscaling import (
    nearest_neighbours_upscale,
    perform_per_direction,
    triple_median,
)
from motion_vizualization import apply_colormap, flow_to_color, get_mixing_image
from tqdm import tqdm

mantis = get_mantis()

dataset = mantis[-1]
# estimator_bwd = MotionEstimator()
# estimator_fwd = MotionEstimator()
# estimators = [MotionEstimator(), MotionEstimator()]


class MotionPipeline:
    def __init__(self, name="fwd", config=DatasetConfig, write_output=False) -> None:
        self.name = name
        self.estimator = MotionEstimator()
        self.sad_computer = OutSadComputer()
        self.config = config
        self.write_output = write_output

    def write_image(self, image, name, timestamp):
        if not self.write_output:
            return
        pathfinder = self.config.pathfinder
        path = pathfinder.frame_filename(f"{self.name}_{name}", timestamp)
        cv2.imwrite(path, image)

    def process(self, frame_center, frame_offset, timestamp):
        sad = None
        self.estimator.downscale = st.slider("downscale", 1, 16)
        self.estimator.block_size = int(st.selectbox("block_size", [4, 8, 16], 1))
        self.estimator.actual_updates = st.slider("updates per candidate", 1, 16)
        time.t
        mvf = self.estimator.compute(frame_center, frame_offset)

        mvf = perform_per_direction(mvf, lambda x: cv2.medianBlur(x, 5))
        mvf = perform_per_direction(mvf, lambda x: cv2.blur(x, (5, 5)))

        # apply_triple_median = st.checkbox("apply tiple median")
        # if apply_triple_median:
        #     mvf_hr = triple_median(mvf)
        # else:
        mvf_hr = nearest_neighbours_upscale(mvf)
        sad = self.sad_computer.compute_out_sad(mvf_hr, frame_center, frame_offset)
        mvf_image = get_mixing_image(frame_center, flow_to_color(mvf_hr))
        self.write_image(mvf_image, "mvf", timestamp)
        self.write_image(sad, "sad", timestamp)
        return sad, mvf_image


reader = CacheReader(dataset, [0, -15, 15])
pipelines = [MotionPipeline("fwd", dataset), MotionPipeline("bwd", dataset)]
# for idx in tqdm(range(len(reader))):
idx = st.slider("frame index", 0, len(reader))
frames, annotations = reader.read(idx)
frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) for frame in frames]
t = annotations.timestamp[0]

forward = st.checkbox("forward")
start_time = time.time()

if forward:
    sad, mvf_image = pipelines[0].process(frames[0], frames[2], t)
else:
    sad, mvf_image = pipelines[1].process(frames[0], frames[1], t)

end_time = time.time()
fps = 1 / (end_time - start_time)

st.write(f"FPS: {fps:.2f}")

sad = sad.astype(np.uint8)
st.image(sad)
st.image(mvf_image)

# sad_bwd = pipelines[1].process(frames[0], frames[1], t)
