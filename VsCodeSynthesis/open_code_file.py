# %%
# Collect all python files
import os
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from icecream import ic
from loguru import logger
from PIL import Image
from tqdm import tqdm

home = os.path.expanduser("~")
gitpath = Path(f"{home}/git")
python_files = list(gitpath.rglob("*.py"))
# %%
from pyfzf import FzfPrompt


class SFzfPrompt(FzfPrompt):
    def prompt(self, choices=[], multi=False, prompt_text=None, return_idx=False):
        fzf_options = ""
        if multi:
            fzf_options += "--multi "
        if not prompt_text is None:
            fzf_options += f'--prompt "{prompt_text}"'
        if return_idx:
            return self.prompt_index(choices, fzf_options)
        else:
            return super().prompt(choices, fzf_options)

    def prompt_index(self, choices, fzf_options=""):
        choices_str = [str(x) for x in choices]
        selection = self.prompt(choices_str, fzf_options)
        indices = []
        for x in selection:
            indices.append(choices_str.index(x))
        return indices


prompt = SFzfPrompt()
path_to_edit = prompt.prompt(list(python_files), prompt_text="choose file")[0]
os.system(f"code {path_to_edit}")
