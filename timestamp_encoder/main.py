import ast
from itertools import product
import cv2
import numpy as np


def create_video(height, width):
	fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
	writer = cv2.VideoWriter('out.mp4', fourcc, 24, (width, height))

	blocksize =16
	spacing = 32
	colors = []
	for c1,c2,c3 in product(np.arange(0,255,spacing),repeat=3):
		colors.append((c1,c2,c3))
	print('total colors:',len(colors))

	for j in range(100):
		color =  colors[j]
		frame = np.random.randint(0,255,(height, width, 3)).astype(np.uint8)    

		meta_frame = np.zeros((height, blocksize, 3), dtype=np.uint8)
		num_blocks =height//blocksize
		[:16,:16]= np.array(color).astype(np.uint8)
		frame_no = frame.mean(axis=(0,1))
		print('encoded',j,frame_no)
		writer.write(frame)
	writer.release()

	reader = cv2.VideoCapture('out.mp4')

	#read frames and determine frame_no
	cnt = 0
	errors = 0
	while True:
		ret, frame = reader.read()
		if not ret:
			break
		color = frame[:8,:8].mean(axis=(0,1))
		deltas = np.abs(color - np.array(colors)).sum(axis=-1)
		frame_no = np.argmin(deltas)
		if not frame_no == cnt:
			errors+=1
		cnt+=1

	print(errors)

 


# %%
