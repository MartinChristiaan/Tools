from dataclasses import dataclass
from typing import List


@dataclass
class Processedpath:
    full_path: str
    shorthand: str


@dataclass
class Combination:
    path: Processedpath
    keybind: str


@dataclass
class State:
    current_folder: str
    combinations: List[Combination]
    path_to_copy: str
    mode: str
    curkey: str
    cur_selection: List[Combination]


class MODES:
    OPEN = "open"
    COPY = "copy"
    MOVE = "move"
    DELETE = "delete"
    BOOKMARK = "bookmark"
    SEARCH = "search"
    HISTORY = "history"
