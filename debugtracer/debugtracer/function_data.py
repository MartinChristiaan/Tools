import time
from dataclasses import dataclass


@dataclass
class FunctionData:
    args: list
    kwargs: dict
    result: any
    execution_time: float
    module: str
    name: str
    is_method: bool
    timestamp: float = time.time()
