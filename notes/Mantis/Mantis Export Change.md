[[Work Ideas]]

Motivation: 
* int8 
* YOLOv8
* Clean up with config

Aproach
* Config files are available in work config
* Models user params defined there.
* Makefile contains trt Export
* Make command should start and stop containers
* Runs script in YOLO plugins
	* Should specify where the model should go.
	* Should specify configurations of models to process...

Took forever to debug, but you have to export onnx with fp16 for dla to work :/