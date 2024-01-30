import pandas as pd
import os

home = os.path.expanduser("~")
df = pd.read_excel(f"{home}/2023_to_20240130.xls")
