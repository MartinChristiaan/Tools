[[Work Ideas]]

Goals
* Fast and efficient (annotating is expensive)
* Accurate for small object detection.
* Work effectively various video resolution

## Fast and Efficient
* Time of interest selector
	* Use pyqt gui (optionally with image), or streamlit
	* Ensure it is done in a non-blocking fashion
* Work on data that is locally cached.
	* Download selected timestamp locally using dlutils-ii
* Easily reject / accept tracks selection.
	* Streamlit show track images (Important context may be missing)
		* Accept track
		* Accept track until here
		* Accept track from here
		* Apply visual tracking towards past (Async)
			* Work on a tile?
		* Apply Visual tracking towards future (Async)
* Apply tracking between annotations of frames to provide suggestions.
	* Use a seperate process to do tracking towards the future.
	* Make sure the annotation process is not chronological to ensure that the tracking process has time to do work.
* Open using python script config.
## Accurate small object annotation
* Vizualize motion.
* Show ROI of annotated objects.
* Mouse
* Use model for cross validation
	* Cross validation training setup using yolo? Tyolo?
## Various image resolutions
* Support for tiling/scaling. 

Requirements
- Easily navigate between multiple camera’s / videosets
- (Visual) Tracking workflow (Make seperate tool?)
	- Press t for tracking -> Use cache or media manager for this? 
	- Better all at once due to needed time?
- Fast -> Smart Caching
	- Download subsequent frames in advance to avoid buffering
- Extensibility
- Image enhancements if needed + quick switching / adjustment
- Highlight likely missed annotations (Based on new prediction)
- Highlight difficult annotations
- Active learning using image embeddings (Use facebook segment anything)
- Ignore regions (with sequence / tracking capabilities)
- compatibility videosets
- tiling for large videos
- Keyboard shortcuts
	- Draw bbox for class based on keyboard shortcut
- Zooming
* bbox drawing

Tracking workflow

Detection -> Tracking (BBox) -> Tracking visual (Where are gaps?)

Why it can be improved
* Ignore / crop regions.
* How to better verify detections (Approve multiple detections at once / or make it easier to approve)
	* Accept track
	* Easy gui.
* How to choose / update class labels.
	* Easy gui where multiple frames at once are used.
	* Use a generic model to find correlations (like in CV90)
* How to use tracking
* Maintained zoom level.
* Switch/control image enhancements


Annotation manually is to much work and does not make sense given the quality of modern day detection algorithms. Even one shot detectors can do a good job???

Maybe initially, some frames need to be annotated, but ideally, it should be an iterative process. 

Drawing bounding boxes manually can take a lot of time. Ideally, the AI suggest images with bounding boxes, which a human can check.

Considerations
* We have a lot of video, so missing some samples is not a problem.
* Large frames are ok, but perhaps not necessary if a lot of false negatives.
* Ideally frames have little items -> not too busy, so that the chance of both false positive and false negative are small. To achieve this, we may crop around confirmed detections to help ensure no false negatives enter the dataset.

How to find good candidate frames
* Extrapolation of other tracks does not encroach area.
* Real Detections for tracks 
* Reasonable bounding box size.


Approach

1 Configure videoset/annotation/detections
2 Cache stuff!
3 Select timestamps (max-samples, etc) Based on tracks
4 Download timestamps locally -> csv file with videoset, camera, timestamp + frames
5 Annotate.
6 upload annotations

Auto timestamp selection
- Set max samples per track
- for every track 
	- it len > min
	- select samples at specified interval
- download bounding box for annotation...


Unfortunately, labels become more difficult with this approach. Also, i do not like current tools that are available for changing labels. I would like to create something which can be run from a server, so it can work from a deep learning pc. 

I want it to support detection proposals.

Current problems
* Cannot change labels/select labels easily enough (Good in matlab, bad in labelimg)
* Cannot see detections from network optimally (requires zooming) -> would prefer zoomed...
* There is no tracking yet to minimize errors.
* Timestamp selection is manual.
* Cannot run from dl machine, so cannot make use of the cache in there. 
* Cannot conveniently select ignore regions which carry over to the next frames. 
* No support for tracking, could be used to easily get more annotations.
* Cannot switch vizualization modes.


Maybe not one big program but separate programs
1. (maybe) Ignore timestamps by finding regions with camera movement / Create subsplits (Write csv file of seperate scenes). (Per camera define motion metrics?, global motion) Do I care?
2. Img viewer type app to show images / frame diff images / avg motion per camera? Be able to draw bounding boxes for ignore? maybe just labelimg? (delete images that should not be labeled?) Use config -> camera's to label -> extract some frames -> draw ignore masks / crops using labelimg.
3. Detection + Tracking using media manager. -> Skip ignore fn / or limit to crop fn
4. Timestamp selection using matlab/guitoolbox/personal tool / or certain interval
	1. Pre annotated (Be able to modify certain parameters such as object size / object confidence)
	2. raw
6. Labelimg for modifying bounding boxes.
7. Program for updating labels / (auto classifier based on unsupervised Clustering)
8. For tracking + Verifying annotated frames to create more frames

# Requirements
* User should*



















































