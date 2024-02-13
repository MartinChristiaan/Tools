import numpy as np


from dataclasses import dataclass


@dataclass
class Project:
    name: str
    planned_hours: np.ndarray
    realised_hours: np.ndarray