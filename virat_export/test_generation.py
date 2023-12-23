VIDEOSETS_BASEDIR = "/diskstation"
from videosets_ii.videosets_ii import VideosetsII

videosets = VideosetsII(basedirpath=VIDEOSETS_BASEDIR)


# import yaml
# with open("configs/datasets.yaml") as f:
# 	ymldata = yaml.load(f, yaml.SafeLoader)

# datasets = list(ymldata.keys())
# for key in datasets:

videoset = videosets["virat_external"]
for cam in videoset.cameras:
    mm = videoset.get_mediamanager(camera=cam)
    print(mm.load_annotations())
