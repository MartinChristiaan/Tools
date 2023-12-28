Problems with caching media managers

* SQL LITE corruption may occur -> Difficult troubleshooting.
* Too many open files (Can be fixed by configuring linux).
* Slow load times for large videosets with many readers.
* Can not use FO directly with data-verification. 
* Data can change in between experiments.
* Need to rescale data








Solution Exporting videosets locally

Requirements
* config for specifying Videosets, Cameras and scaling
* Create a directory for each videoset
	* Each camera has a subdirectory
		* Each frame offset has a subdirectory
	* Each camera has a .log file containing line seperated timestamps associated with the exported jpgs
* 


Approach Exporter
2. Update/Create annotations
3. Get current timestamps
4. For each missing timestamp / frameoffset
	1. request frame.
	2. save frame
	3. update .log file

