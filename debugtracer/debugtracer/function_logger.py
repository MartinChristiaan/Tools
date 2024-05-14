from loguru import logger
from dataclasses import dataclass
import importlib
import os
import types
import pickle
from pathlib import Path
import time

from zmq import has


# from function_data import FunctionData
import library
import library.sub_library
import inspect
import sys

exec_data = {}


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
        self.function_logger_lut = {}
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
                            self.debug_trace_decorator(method, True),
                        )
                        print(obj, name, method)

                if isinstance(obj, types.FunctionType) or isinstance(
                    obj, types.MethodType
                ):
                    setattr(module, name, self.debug_trace_decorator(obj))

    def debug_trace_decorator(self, f, is_method=False):
        def wrapper(*args, **kwargs):
            fnname = f.__name__
            if fnname not in self.function_logger_lut:
                self.function_logger_lut[fnname] = FunctionLogger(
                    fnname, self.data_path, is_method
                )
            return self.function_logger_lut[fnname].log_function(f, *args, **kwargs)

        return wrapper


@dataclass
class FunctionLogger:
    name: str
    data_path: str
    is_method: bool
    iteration: int = 0

    def get_getpath(self, name="input", ext=".pkl", cross_iter=False):
        if cross_iter:
            path = Path(f"{self.data_path}/{self.name}/{name}{ext}")
        else:
            path = Path(f"{self.data_path}/{self.name}/{self.iteration}_{name}{ext}")
        path.parent.mkdir(exist_ok=True, parents=True)
        return path

    # def serialize(self,name,value,path):
    # def get_extention(self,name,value):

    def serialize(self, data, name="input", ext=".pkl", cross_iter=False):
        path = self.get_getpath(name, ext, cross_iter)
        with open(path, "wb") as f:
            pickle.dump(data, f)
        # primitives = []
        # primitive_types = [int, str, float, bool]
        # for key, value in items.items():
        #     if type(value) in primitive_types:
        #         primitives.append((key, value))

    def log_function(self, fn, *args, **kwargs):
        inputs = kwargs.copy()
        for i, arg in enumerate(args):
            inputs[f"arg{i}"] = arg

        function_data = dict(
            module=fn.__module__,
            name=fn.__name__,
            is_method=self.is_method,
        )
        self.serialize(function_data, "meta", cross_iter=True)
        self.serialize(inputs, "inputs")
        t0 = time.time()
        result = fn(*args, **kwargs)
        t1 = time.time()
        logger_result = dict(fn_output=result, dt=t1 - t0)
        self.serialize(logger_result, "outputs")
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


def main():
    python_module_path = sys.argv[1]
    from debugtracer.reloader import ModuleReloader

    module = importlib.import_module(python_module_path)
    reloader = ModuleReloader()
    modules = reloader.get_imported_modules()
    tracer = TestTracer(modules)
    print(tracer.function_logger_lut)
    module.main()


if __name__ == "__main__":
    main()
