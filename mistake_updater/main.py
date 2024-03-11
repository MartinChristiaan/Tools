# %%
from pathlib import Path
import pickle


model_dir = Path("/data/proposed")
mistake_files = list(model_dir.rglob("*.pkl"))
with open(mistake_files[0], "rb") as f:
    pickle.load(f)
