#%%
import ast
import cv2
import numpy as np
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
writer = cv2.VideoWriter('out.mp4', fourcc, 24, (1920, 1080))

colors = [
    (255, 0, 0),     # Red
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (255, 255, 0),   # Yellow
    (255, 0, 255),   # Magenta
    (0, 255, 255),   # Cyan
    (255, 128, 0),   # Orange
    (128, 255, 0),   # Lime
    (0, 255, 128),   # Spring green
    (0, 128, 255),   # Azure
    (128, 0, 255),   # Violet
    (255, 0, 128),   # Rose
    (255, 128, 128), # Light red
    (128, 255, 128), # Light green
    (128, 128, 255), # Light blue
    (255, 255, 128), # Light yellow
    (255, 128, 255), # Light magenta
    (128, 255, 255), # Light cyan
    (255, 192, 128), # Peach
    (192, 255, 128), # Mint
    (128, 255, 192), # Pastel green
    (128, 192, 255), # Sky blue
    # (192, 128, 255), # Lavender
    # (255, 128, 192), # Light pink
    # (255, 192, 192), # Pale rose
    # (192, 255, 192), # Light mint
    # (192, 192, 255), # Light lavender
    # (255, 255, 192), # Pale yellow
    # (255, 192, 255), # Pale magenta
    # (192, 255, 255), # Pale cyan
    # (255, 224, 192), # Cream
    # (224, 255, 192), # Ivory
    # (192, 255, 224), # Light sea green
    # (192, 224, 255), # Light steel blue
    # (224, 192, 255), # Thistle
    # (255, 192, 224), # Carnation pink
    # (255, 224, 224), # Misty rose
    # (224, 255, 224), # Honeydew
    # (224, 224, 255), # Alice blue
    # (255, 255, 224), # Light yellow
    # (255, 224, 255), # Lavender blush
    # (224, 255, 255), # Light cyan
    # (255, 240, 224), # Papaya whip
    # (240, 255, 224), # Pale green
    # (224, 255, 240), # Light sea green
    # (224, 240, 255), # Light sky blue
    # (240, 224, 255), # Lavender blue
    # (255, 224, 240), # Pink
    # (255, 240, 240), # Light coral
    # (240, 255, 240), # Light green
    # (240, 240, 255), # Light blue
    # (255, 255, 240), # Light yellow
    # (255, 240, 255), # Plum
    # (240, 255, 255), # Light turquoise
    # (255, 248, 224), # Seashell
    # (248, 255, 224), # Light celery
    # (224, 255, 248), # Seafoam
    # (224, 248, 255), # Light cornflower blue
    # (248, 224, 255), # Light orchid
    # (255, 224, 248), # Cotton candy
    # (255, 248, 248), # Cherry blossom pink
    # (248, 255, 248), # Light celery
    # (248, 248, 255), # Light pastel purple
    # (255, 255, 248), # Light beige
    # (255, 248, 255), # Thistle
    # (248, 255, 255), # Light cyan
    # (255, 255, 255), # White
]


def frame_no_to_color(frame_no):
	return (frame_no*8) % 255

for j in range(5):
	color =  colors[j]
	frame = np.ones((1080, 1920, 3), np.uint8) * np.array(color).astype(np.uint8)
	frame_no = frame.mean(axis=(0,1))
	print(frame_no)
	writer.write(frame)
writer.release()


reader = cv2.VideoCapture('out.mp4')

#read frames and determine frame_no
cnt = 0
while True:
	ret, frame = reader.read()
	if not ret:
		break
	color = frame[0,0]
	deltas = np.abs(color - np.array(colors))
	print(deltas)
	print(np.argmin(deltas),cnt,color)
	cnt+=1



 

