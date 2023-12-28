* II Trainer
	* Change model architecture
	* Change data loader
	* Change plotting
* II Validator
	* Change validation dataloader
	* plotting


* II_Dataset (YOLO dataset using dl_utils), inject reader
	* Simple conversion of our detection format to YOLO
* Mosaicing Dataset, no building reader depends on h/w + params
	* Adds mosaicing. Needed to maintain balance Foreground background.

* YOLOManager
	* Collects / combines mosaicing datasets
	* 

