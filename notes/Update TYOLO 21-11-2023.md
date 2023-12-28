## Experiments

* Increased resolution -> Many false positive detections (Why?) + But birds are detected!
* Dilation on diff map -> Improved bird recall

* Added new data (Many drones + birds) + Very small 
* Made bounding boxes bigger during validation -> Improved validation metrics (Overlap needed to compute recall/precision)
* Resulting model had poor precision and recall was not yet satisfactory for smaller objects
	* Cause : Crop background ratio poor (Model could not recognize background well)
* Trained model with dilated diff feature -> Same performance as regular diff model.


Major Challenge :
How to get good model performance for both background and very small objects
* Base resolution may contain unannotated objects
* Downscaling / Median blur can be used to remove these objects. But this may affect model performance on base resolution.

### Annotation

I found that annotation for very small objects is very difficult because they these objects are hard to see. I have two strategies in mind to improve this

Training pipeline adaptations





