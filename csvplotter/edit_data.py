import pandas as pd


path = "/mnt/dl-41/data/leeuwenmcv/general/mantis_mist/mist_combined_prcurve_roc_data.csv"
df = pd.read_csv(path)
changed_data = []

for model,dfm in df.groupby("model"):
	if 'single' in model:
		dfm['model_name'] = [x.replace('single-frame-','') for x in dfm['model']]
		dfm['model_type'] = 'single-frame'
	else:
		dfm['model_name'] = [x.replace('multi-frame-','') for x in dfm['model']]
		dfm['model_type'] = 'multi-frame'
	changed_data.append(dfm)
pd.concat(changed_data).to_csv('mantis_mist.csv',index=False)

	
	
