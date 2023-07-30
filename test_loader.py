import glob
import os
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks

# path = 
path = "/home/leeuwenmcv/track_test/tracks.csv"
tracks = Tracks.load(path)
print(tracks)

