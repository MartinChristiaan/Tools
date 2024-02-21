from pathlib import Path
data = ''
mm_dir=  '/data/VisDrone2019-VID-val/VisDrone2019-VID-val/'
sequences = (Path(data)/'sequences').glob('*')
for seq in sequences:
	videodir = Path(f"{mm_dir}/video/{seq.stem}")
	videodir.mkdir(parents=True,exist_ok=True)
	resultsdir=  Path(f"{mm_dir}/results/{seq.stem}")
	resultsdir.mkdir(parents=True,exist_ok=True)




