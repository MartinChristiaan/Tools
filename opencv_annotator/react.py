# TODO
# %%
import cv2
import os
import json
import enum
import time
import logging
from termcolor import colored


class ReturnType(enum.Enum):
    UNDEFINED = 0
    IMG = 1
    FEATURE = 2
    KERNEL = 3
    TENSORFEATURE = 4
    MOTIONVECTOR = 5


# Source = outer Array = branch (Execute independently), inner array = Merge (Combine outputs as arguments)
# outputs = select item from iterable (if some observable returns an iterable)


class Observable:
    def __init__(
        self,
        fun,
        source=[[]],
        outputs=[],
        branches=[],
        return_type=ReturnType.UNDEFINED,
        _arg_is_list=False,
        is_sink=False,
        _always_execute=False,
    ):
        if not isinstance(source, list):
            source = [source]
        if not isinstance(source[0], list):
            source = [source]
        self._arg_is_list = _arg_is_list
        self._active = True
        self.subscribers = []
        self._return_type = return_type
        self._is_sink = is_sink
        self._always_execute = _always_execute
        if not isinstance(self._return_type, list):
            self._return_type = [self._return_type]

        if not isinstance(branches, list):
            branches = [branches]
        if not isinstance(outputs, list):
            outputs = [outputs]

        if len(source) > 0:
            needed_length = sum([len(x) for x in source])
            if len(branches) < needed_length:
                branches = [0] * needed_length

        self.branches = branches
        cnt = 0
        for branch_idx, branch in enumerate(source):
            if len(outputs) != len(branch):
                outputs = [None] * len(branch)
                # (outputs)
            for inp_idx, (s, arg_idx) in enumerate(zip(branch, outputs)):
                s.subscribe(self, branch_idx, inp_idx, arg_idx, branches[cnt])
                cnt += 1

        self.args = [[None for _ in range(len(outputs))] for _ in range(len(source))]
        self.fun = fun
        self.__execution_needed = True
        self.sources = source
        self.outputs = outputs

    def build_call_stack(self, call_stack):
        if self in call_stack:
            call_stack.remove(self)
        if self._active or self._always_execute:
            call_stack.append(self)
            for sub, _, _, _, _ in self.subscribers:
                sub.build_call_stack(call_stack)

    def update_args(self, arg, inp_index, branch_index):
        self.args[branch_index][inp_index] = arg

    def run(self):
        results = []
        for branch_idx, branch in enumerate(self.args):
            # print(f"{self} {branch_idx}")
            if self._arg_is_list:
                results += [self.fun(branch)]
            else:
                if not isinstance(branch, list):
                    branch = [branch]
                results += [self.fun(*branch)]

        for ob, branch_idx, inp_idx, arg_idx, branch_source_idx in self.subscribers:
            if arg_idx != None:
                ob_result = results[branch_source_idx][arg_idx]
            else:
                ob_result = results[branch_source_idx]
            ob.update_args(ob_result, inp_idx, branch_idx)

    def execute(self, timeit=False):
        if timeit:
            start = time.time()

        call_stack = []
        self.build_call_stack(call_stack)
        index = len(call_stack) - 1
        sinks = []

        while index >= 0:
            obs = call_stack[index]
            if not obs.__execution_needed:
                call_stack.remove(obs)
            elif obs._is_sink:
                sinks += [obs]
                call_stack.remove(obs)
            index -= 1

        for sink in sinks:
            call_stack += [sink]

        call_stack = [x.run for x in call_stack]
        # print(call_stack)
        if timeit:
            call_stack_time = time.time() - start
            times = [call_stack_time]
            labels = ["build_call_stack"]
            for func in call_stack:
                start = time.time()
                func()
                times += [time.time() - start]
                label = str(func).split(".")[-1].split(" ")[0]
                labels += [label]
            total_time = sum(times) + 1e-10

            logstring = f"\ntotal execution time          : {total_time} \n"

            for label, exectime in zip(labels, times):
                spaces = (30 - len(label)) * " "
                percent = exectime / total_time * 100
                text_color = "green" if exectime < 0.1 else "red"
                logstring += colored(
                    f"{label}" + spaces + f" : {exectime:.2f} ({percent:.2f}%) \n",
                    text_color,
                )
            logging.warning(logstring)

        else:
            for func in call_stack:
                func()

    def activate(self):
        if not self._active:
            self._active = True
            for source in self.sources:
                for s in source:
                    s.activate()
            # if not self._is_sink:
            #     print(self)
            #     self.run()

    def subscribe(self, subscriber, branch_idx, inp_idx, arg_idx, branch_source_idx):
        self.subscribers.append(
            [subscriber, branch_idx, inp_idx, arg_idx, branch_source_idx]
        )

    def unsubscribe(self, subscriber, branch_idx, inp_idx, arg_idx, branch_source_idx):
        self.subscribers.remove(
            [subscriber, branch_idx, inp_idx, arg_idx, branch_source_idx]
        )


class TestClass(Observable):
    def __init__(
        self,
        source=[[]],
    ):
        super().__init__(
            self.f,
            source,
        )

    def f(self, x):
        return x * 5


class TestClassMerge(Observable):
    def __init__(
        self,
        source=[[]],
    ):
        super().__init__(
            self.f,
            source,
        )

    def f(self, x, y):
        time.sleep(0.5)
        return x * 5 + y


t1 = Observable(lambda: 3)
t2a = Observable(lambda x: x * 3, t1)
t2b = Observable(lambda x: x * 2, t1)
# t3 = Observable(lambda x: x * 2, t1)

t4 = TestClassMerge([t2a, t2b])
t5 = Observable(lambda x: print(x), t4)
t1.execute(timeit=True)
