Future idea
* Moor zoom variation. (Should be able to downscale a lot!)
* Bigger mosaic tiles? (640x640) -> Find balance.
* Even Weight distribution -> Automatic rebalancing with a curve
* Smart scaling? No, should be in aug
* Require improved annotation
	* Spar with Jan -> Imenhancement to make visible movementinfo
* Annotation workflow
	* Use images in cache -> Preprocess to boost visibility movement (Calculate noise?)
	* Use viewer to determine sample in need of reannotation.

Strategy  
* Multi scale mosaicing! 1280x1280 (Full res) (640x640) Half res (320x320) QRes
* Multi scale export -> (more complexity...)
	* Export at multiple resolutions? apply scaling beforehand...
		* Multiple (crop/tile)_sizes ensure more scales available.
			* Configure
			* Handle scale automatically? 
				* Use median object sizes to see what is appropriate -> scale so size is max 100px?
* Use raw cache, so read full size images... -> To heavy for noise augs



PR strategy
* Employ Ella -> Find better architectures, but mostly training
* Talk with anca -> (Should talk to Hugo first!) 
	* Discuss Ella
	* Discuss Panoptes.
	* Discuss opportunities.
	* Show few images and video!
* Christophe Empower
	* Talk about small object detection
	* Coaching
	* Training Ella
* Coach gesprek
	* Moeilijk om als overwinning te zien
	* Nogal veel variatie





