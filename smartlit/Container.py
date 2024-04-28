from state import Observable


from typing import List


class Container:
    def __init__(self, name) -> None:
        self.name = name

    def get_observables(self) -> List[Observable]:
        observables = []
        for k, v in self.__dict__.items():
            if isinstance(v, Observable):
                print(k, "found as observable")
                observables.append(v)
        return observables


# save to diskstation
# load from diskstation
