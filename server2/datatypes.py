import os
import pickle
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Source:
    name: str
    url: str
    last_update: datetime
    id: int
    weight: int
    child_sources: List[int] = field(default_factory=list)
    type: str = ""
    parent_sources: List[int] = field(default_factory=list)
    rel_weight = 0
    favorite = False

    def attach_to_parent(self, parent: "Source"):
        parent.child_sources.append(self.id)
        self.parent_sources.append(parent.id)
        update_time = datetime.now()
        self.last_update = update_time
        parent.last_update = update_time


def write(sources):
    with open("data.pickle", "wb") as f:
        pickle.dump(sources, f)


def readSources() -> List[Source]:
    if not os.path.exists("data.pickle"):
        return []
    with open("data.pickle", "rb") as f:
        sources = pickle.load(f)
    return sources
