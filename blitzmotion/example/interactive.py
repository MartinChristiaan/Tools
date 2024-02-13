import time

# %%
# setup dataset
# %load_ext autoreload
# %autoreload 2
import cv2
import numpy as np
import streamlit as st
from blitzmotion.writer import MotionSADWriter
from datasets import get_mantis
from dlutils_ii import CacheReader

mantis = get_mantis()

dataset = mantis[-1]
reader = CacheReader(dataset, [0, -15, 15])
pipelines = [MotionSADWriter("fwd", dataset), MotionSADWriter("bwd", dataset)]
# for idx in tqdm(range(len(reader))):
idx = st.slider("frame index", 0, len(reader))
frames, annotations = reader.read(idx)
frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) for frame in frames]
t = annotations.timestamp[0]

forward = st.checkbox("forward", True)
refine = st.checkbox("refine", True)

apply_triple_median = st.checkbox("apply triple median", False)
start_time = time.time()
if forward:
    sad, mvf_image = pipelines[0].process(
        frames[0], frames[2], t, apply_triple_median=apply_triple_median, refine=refine
    )
else:
    sad, mvf_image = pipelines[1].process(
        frames[0], frames[1], t, apply_triple_median=apply_triple_median, refine=refine
    )
end_time = time.time()
fps = 1 / (end_time - start_time)
st.write(f"FPS: {fps:.2f}")

sad = sad.astype(np.uint8)
st.image(sad)
st.image(mvf_image)

# sad_bwd = pipelines[1].process(frames[0], frames[1], t)
