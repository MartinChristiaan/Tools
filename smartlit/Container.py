from pathlib import Path
from state import Observable
from typing import List
import pickle


class Container:
    def __init__(self, name, ctype="control") -> None:
        self.name = name
        self.cache_file = Path(f"/data/container_caches/{self.name}")
        self.load_cache_state()
        self.ctype = ctype

    def get_observables(self) -> List[Observable]:
        observables = []
        for k, v in self.__dict__.items():
            if isinstance(v, Observable):
                print(k, "found as observable")
                observables.append(v)
        return observables

    def load_cache_state(self):
        if self.cache_file.exists():
            with open(self.cache_file, "rb") as f:
                state = pickle.load(f)
            observers = self.get_observables()
            for k, v in state.items():
                observer = [x for x in observers if x.name == k]
                for x in observer:
                    x._value = v

    def save_state(self):
        state = {obs.name: obs.value for obs in self.get_observables()}
        self.cache_file.parent.mkdir(exist_ok=True, parents=True)
        with open(self.cache_file, "wb") as f:
            pickle.dump(state, f)


# save to diskstation
# load from diskstation
