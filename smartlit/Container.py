from state import Observable


from typing import List


class Container:
    def __init__(self, name) -> None:
        self.name = name

    def get_observables(self) -> List[Observable]:
        observables = []
        for k, v in self.__dict__.items():
            print(k)
            if isinstance(v, Observable):
                observables.append(v)
        return observables
