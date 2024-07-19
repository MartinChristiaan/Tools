from dataclasses import dataclass


@dataclass
class ExampleArgClass:
    name: str
    age: int
    number: float
    number_2: float

    @staticmethod
    def from_df(df):
        return [ExampleArgClass(**row) for i, row in df.iterrows()]
