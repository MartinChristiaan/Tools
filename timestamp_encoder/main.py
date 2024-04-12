#%%
import cv2
import numpy as np
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
writer = cv2.VideoWriter('out.mp4', fourcc, 24, (1920, 1080))

def frame_no_to_color(frame_no):
	return (frame_no*8) % 255

for j in range(5):
	color =  frame_no_to_color(j)
	print(color)
	frame = np.ones((1080, 1920, 3), np.uint8) * color
	writer.write(frame)
writer.release()


reader = cv2.VideoCapture('output.mp4')

#read frames and determine frame_no
cnt = 0
while True:
	ret, frame = reader.read()
	if not ret:
		break
	frame_no = frame[0][0][0]
	print(frame_no,cnt)
	cnt+=1



 

