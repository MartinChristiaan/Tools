import traceback
from click import getchar
from icecream import ic
from loguru import logger
from dataclasses import dataclass
import importlib
import os
import types
import pickle
from pathlib import Path
import time

from pytest import fail
from zmq import has


# from function_data import FunctionData
from debugtracer.debugger import Debugger
from debugtracer.reloader import ModuleReloader
import library
import library.sub_library
import inspect
import sys

exec_data = {}
reloader = ModuleReloader()

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
        exec_data[name] = []
        self.data_path = Path(data_path) / (self.name)
        self.data_path.mkdir(parents=True, exist_ok=True)
        self.function_logger_lut = {}
        self.max_traced_executions = 5
        self.active = True
        self.decorate_all_in_modules()

    def decorate_all_in_modules(self):
        for module in self.modules:
            for name in dir(module):
                obj = getattr(module, name)
                if inspect.isclass(obj):
                    if obj.__module__ not in self.modules:
                        continue
                    method_list = [
                        getattr(obj, func)
                        for func in dir(obj)
                        if callable(getattr(obj, func)) and not func.startswith("__")
                    ]
                    for method in method_list:
                        setattr(
                            obj,
                            method.__name__,
                            debug_trace_decorator(self, method, True),
                        )

                        ic(obj, name, method, module)

                if isinstance(obj, types.FunctionType) or isinstance(
                    obj, types.MethodType
                ):
                    setattr(module, name, debug_trace_decorator(self, obj))


def debug_trace_decorator(tracer: TestTracer, f, is_method=False):
    def wrapper(*args, **kwargs):
        if tracer.active:
            fnname = f.__name__
            ic(fnname, f.__module__)
            if fnname not in tracer.function_logger_lut:
                tracer.function_logger_lut[fnname] = FunctionLogger(
                    fnname, tracer.data_path, is_method
                )
            return tracer.function_logger_lut[fnname].log_function(f, *args, **kwargs)
        return f(*args, **kwargs)

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
            iteration=self.iteration,
        )
        serialization_failed = False
        try:
            self.serialize(function_data, "meta", cross_iter=True)
            self.serialize(inputs, "inputs")
        except Exception as e:
            logger.warning(f"serialization failed for {fn.__name__}")
            serialization_failed = True
        t0 = time.time()
        try:
            result = fn(*args, **kwargs)
        except Exception as e:
            if serialization_failed:
                logger.error(
                    "serialization failed and error in function, unfortunately cannot debug :("
                )
                raise e
            traceback.print_exc()
            debugger = Debugger(self.data_path, self.data_path / f"{fn.__name__}")
            debugger.reloader = reloader
            debugger.iteration = self.iteration
            while True:
                logger.error(
                    f"An error occured during execution of {fn.__name__}, please enter key to try and fix the function"
                )
                getchar()
                result = debugger.run_function()
                if not result == "error":
                    break

        t1 = time.time()
        logger_result = dict(fn_output=result, dt=t1 - t0)
        if not serialization_failed:
            try:
                self.serialize(logger_result, "outputs")
            except:
                logger.warning(f"Failed to serialize {fn.__name__} output")

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
        self.iteration += 1
        return result


def main():
    python_module_path = sys.argv[1]
    sys.path.append(os.getcwd())

    module = importlib.import_module(python_module_path)
    modules = [
        x
        for x in reloader.get_imported_modules()
        if not x.__name__.endswith("tracer")
        and not "reloader" in str(x)
        and not "debugger" in str(x)
        and not "fzf_utils" in str(x)
        and not "testcode_generator" in str(x)
    ]
    name = python_module_path.split(".")[-1]
    tracer = TestTracer(modules, name=name)
    # return
    failed = False
    t0 = time.time()
    module.main()
    t1 = time.time()
    dt = t1 - t0

    # if not failed:
    #     logger.info(f"Tracing completed succesfully in {dt:.2f} sec, starting debugger")

    tracer.active = False
    from debugtracer.debugger import Debugger

    # print(tracer.function_logger_lut.keys())

    # last_function = tracer.function_logger_lut[
    #     list(tracer.function_logger_lut.keys())[-1]
    # ]

    debugger = Debugger(
        tracer.data_path,
        tracer.data_path / f"main",
    )
    debugger.reloader = reloader
    debugger.run()


if __name__ == "__main__":
    main()
