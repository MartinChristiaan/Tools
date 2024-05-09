import numpy as np
import pandas as pd
from pathlib import Path

proposed = Path("./data_ppt/combo_combined_prcurve_proposed-0.csv")
df = pd.read_csv(proposed).iloc[::-1]
recalls = np.linspace(0, 1, 20)
print(recalls)
print(df)
precisions = np.interp(recalls, df["recall"], df["precision"])
print(precisions, recalls)
