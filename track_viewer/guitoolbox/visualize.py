from typing import Dict, Optional

import seaborn as sns
from matplotlib.patches import Rectangle


class ColorMap:
    def __init__(self, color_count: int, palette: str = "colorblind"):
        self.color_map = sns.color_palette(palette, n_colors=color_count)

    def __getitem__(self, item: int):
        return self.color_map[item % len(self.color_map)]


class DetectionRectangle(Rectangle):
    def __init__(self, xy, width, height, metadata: Optional[Dict] = None, **kwargs):
        super().__init__(xy, width, height, **kwargs)

        if metadata is not None and not isinstance(metadata, dict):
            raise ValueError(f"Meta data should be a dict, but is a: {type(metadata)}")
        self.metadata = metadata
