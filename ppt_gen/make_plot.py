# %%
# python script which loads png images from a directory and creates a powerpoint slide for every two images. In the powerpoint slide, the two images are placed side by side.


import os
import pptx
from pathlib import Path

image_dir = "/mnt/dl-41/data/leeuwenmcv/general/l3harris/yolov8l_dist_est_03022024"
images = list(Path(image_dir).rglob("*wdist.png"))
images.sort()

prs = pptx.Presentation()
for i in range(0, len(images), 2):
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    left = slide.shapes.add_picture(str(images[i]), 0, 0, 5000000, 5000000)
    if i + 1 < len(images):
        right = slide.shapes.add_picture(
            str(images[i + 1]), 5000000, 0, 5000000, 5000000
        )

prs.save("output.pptx")
