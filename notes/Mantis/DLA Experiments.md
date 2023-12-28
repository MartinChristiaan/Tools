
31-8

* Did advanced performance analysis of all models- Failed, something was wrong with the export causing most layers to be exported to the GPU.
* Multiprocessing performance analysis
* 








Why
DLA's are advertised to have great potential
Compiling YOLO to DLA does not yield great results, DLA should be especially effective for certain operations.

Goal 
1. To figure out under what circumstances/Configurations the DLA is effective and when it is not. 
2. Find ways to employ DLA such that YOLO throughput can be improved on the Jetson Orin.

Considerations
* The DLA may have different sizes for local caches and thus may have different performance characteristics. 
* Not all layers are supported on the DLA, so GPU fallback may be needed to support the DLA. 

How to employ DLA to its highest effectiveness.
Methods
* Limit GPU Fallback
* Employ Layers where DLA is effective

### Strategy 1, replace SWISH with RELU
Results, only a slight performance increase could be observed

### Strategy 2, YOLO Backbone with DLA, rest with GPU.
Why -> All layers can be executed on the DLA...
Result. DLA still bottlenecks gpu...
At first it appeared as if the DLA's memory transfers where to blame. But this turned out to be a bug in the profiler that was fixed after updating tensorRT to the newest version. But in the end, it turned out that the DLA could simply not keep up with the GPU. 
### Strategy 3, Layer experiments on the DLA.
To figure out how to most efficiently use the DLA we need to understand which types of layers it can effectively run and how these layers compare to the GPU. 
During these experiments I varied
* convolution dimensions
* kernel sizes
* precision 8bit vs 16bit
* Device (GPU vs DLA)
* number of consequtive convolution layers

* I found that the DLA was much faster (5-20x) when running int8 instead of fp16
* The speedup was at its largest when multiple layers where run consequtively

Experiment 4

So how quantized Yolo and TYOLO perform on the DLA, see if we can retain detection quality



	





Other

Tried to get nsys to work, but failed





Panoptes future
* More frames? 
* Investigate TYOLO vs T2YOLO vs v8 variant
* Investigate 2D UNET
* Investigate augmentations
* Collect even more data / Optimized data collection
* Local Caching system for the media manager 

Mantis proposals
Try to get into detector work

Schrijf proposal voor experiment
* 
* 