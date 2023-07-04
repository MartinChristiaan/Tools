import time
import cv2
import os
import subprocess
import sys
import threading
cache_size = 50
def resize_image(image, max_width, max_height):
    height, width = image.shape[:2]
    aspect_ratio = width / height

    if width > max_width or height > max_height:
        if aspect_ratio > 1:
            width = max_width
            height = int(width / aspect_ratio)
        else:
            height = max_height
            width = int(height * aspect_ratio)

        image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    elif width < max_width and height < max_height:
        if aspect_ratio > 1:
            width = max_width
            height = int(width / aspect_ratio)
        else:
            height = max_height
            width = int(height * aspect_ratio)

        image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)

    return image

class ImageViewer:
	def __init__(self, image_paths):
		self.image_paths = image_paths
		self.index = 0
		self.step = 1
		self.total_images = len(image_paths)
		self.cache_index = 9999999999
		self.cache_step = 9999999999
		self.key_actions = {
			ord('k'): self.next_image,
			ord('j'): self.previous_image,
			ord('f'): self.next_different_image,
			ord('a'): self.previous_different_image,
			ord('d'): self.delete_image,
			ord('e'): self.open_folder,
			ord("h"):self.decrease_step_size,
			ord('l'):self.increase_step_size,
			27: self.exit_viewer
		}
		self.image_cache = {}
		self.stopped = False
		self.loader = threading.Thread(target=self.load_images)
		self.loader.start()

	def next_image(self):
		self.index = (self.index + self.step) % self.total_images
	def previous_image(self):
		self.index = (self.index - self.step) % self.total_images
	def increase_step_size(self):
		self.step*=10
	def decrease_step_size(self):
		self.step/=10
		self.step = int(self.step)
	def next_different_image(self):
		self.index = self.get_next_different_image_index(previous=False)
	def previous_different_image(self):
		if self.index == 0:
			return
		self.index = self.get_next_different_image_index(previous=True)
	def delete_image(self):
		image_path = self.image_paths[self.index]
		os.remove(image_path)
		del self.image_paths[self.index]
		self.total_images -= 1
		if self.total_images == 0:
			self.exit_viewer()
		else:
			self.index %= self.total_images
	def load_images(self):
		while not self.stopped:
			if abs(self.cache_index - self.index) > cache_size//4 * self.step or self.cache_step!=self.step:
				self.cache_index = self.index
				self.cache_step = self.step
				self.image_cache = {}
				indices_to_load = [self.cache_index]
				for i in range(1,cache_size//2):
					indices_to_load.append(i)
					indices_to_load.append(-i)
				for i in indices_to_load:
					if abs(self.cache_index - self.index) > cache_size//4 * self.step or self.cache_step!=self.step:
						# skip ahead if index already changed again 
						continue
					im_index = (self.cache_index + i * self.step)%self.total_images
					print(f"loading {im_index}")
					image_path = self.image_paths[im_index]
					image = cv2.imread(image_path)
					image = resize_image(image, 1920, 1080)
					# Add image path as text overlay
					cv2.putText(image, f"({self.step}):{image_path}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
					self.image_cache[im_index] = image
					time.sleep(0.01)
			
			time.sleep(0.2)

	def open_folder(self):
		image_path = self.image_paths[self.index]
		folder_path = os.path.dirname(image_path)
		subprocess.Popen(f'explorer.exe {folder_path}')

	def exit_viewer(self):
		self.stopped = True
		cv2.destroyAllWindows()
		self.loader.join()
		sys.exit()

	def display_images(self):
		err_cnt = 0
		while True:
			if self.index not in self.image_cache:
				print(f"index {self.index} not yet loaded")
				time.sleep(0.1)
				err_cnt +=1
				if err_cnt == 20:
					self.exit_viewer()
					sys.exit()
				continue
			err_cnt = 0

			image = self.image_cache[self.index]
			cv2.imshow('Image Viewer', image)
			key = cv2.waitKey(0)
			if key in self.key_actions:
				self.key_actions[key]()