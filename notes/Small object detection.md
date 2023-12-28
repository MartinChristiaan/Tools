Tiny objects cannot be detected by YOLO
* First prognose was lack of annotations, but new experiments appear to uncover an inherent flaw in the architecture.
* Should experiment more.. (What happens with upscaling?) Dilated inputs?
* Do simulated 1px experiments. (Ella) Model with no pooling, or fully connected ?
* Many frame needed (1px over time causes lots of frame differences, so perceivable?)

* Diff summing preproc -> normalize (exposes trajectories, more detectable by neural nets)
* Pipeline using plightning + segmentation.
* I need a good reader test....
* I need to improve annotation workflow
	* 




