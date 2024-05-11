import types
import pickle
from math import pi
import os
from pathlib import Path
import time

from loguru import logger

# from function_data import FunctionData
import library
import library.sub_library
import inspect
import sys

exec_data = {}
fn_name_counter_lut = {}


# TODO manually specify functions to test!!! Use GUI???


class TestTracer:
    def __init__(
        self,
        modules,
        name=Path(sys.argv[0]).stem,
        data_path="/data/trace_data/",
    ) -> types.NoneType:
        self.name = name
        self.modules = modules
        # self.test_code_dir = test_code_dir
        # self.test_data_dir = test_data_dir
        exec_data[name] = []
        self.decorate_all_in_modules()

        self.data_path = Path(data_path) / (self.name)
        self.data_path.mkdir(parents=True, exist_ok=True)
        self.max_traced_executions = 5

    def decorate_all_in_modules(self):
        for module in self.modules:
            for name in dir(module):
                obj = getattr(module, name)
                if inspect.isclass(obj):
                    method_list = [
                        getattr(obj, func)
                        for func in dir(obj)
                        if callable(getattr(obj, func)) and not func.startswith("__")
                    ]
                    for method in method_list:
                        setattr(
                            obj,
                            method.__name__,
                            self.debug_trace_decorator(method, True, name=self.name),
                        )
                        print(obj, name, method)

                if isinstance(obj, types.FunctionType) or isinstance(
                    obj, types.MethodType
                ):
                    setattr(
                        module, name, self.debug_trace_decorator(obj, name=self.name)
                    )

    def debug_trace_decorator(self, f, is_method=False):
        def wrapper(*args, **kwargs):
            fnname = (f.__name__,)
            if fnname not in fn_name_counter_lut:
                fn_name_counter_lut[fnname] = 0
            elif fn_name_counter_lut[fnname] == self.max_traced_executions:
                return f(*args, **kwargs)
            else:
                fn_name_counter_lut[fnname] += 1

            t0 = time.time()

            result = f(*args, **kwargs)
            t1 = time.time()

            # function_data = FunctionData(
            #     args=args,
            #     kwargs=kwargs,
            #     result=result,
            #     execution_time=t1 - t0,
            #     module=f.__module__,
            #     name=f.__name__,
            #     is_method=is_method,
            # )
            # exec_data[name].append(function_data)
            return result

        return wrapper


if __name__ == "__main__":
    tracer = TestTracer([library, library.sub_library])
    library.sub_library.my_sum(2, 3)
    obj = library.sub_library.ObjectExample(6, 8)
    obj.do_sum()
    tracer.generate()
    import pickle

    os.system("pytest")
