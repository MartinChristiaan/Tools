# %%

# class which runs several processes whcih share an input queue
import multiprocessing as mp
import random
import time
from typing import Dict


def example_process(
    input_queue: mp.Queue, output_queue: mp.Queue, val_dict: Dict, name="worker"
):
    while not val_dict["stop"]:
        if not input_queue.empty():
            item = input_queue.get()
            cnt, value = item
            sleeptime = random.randint(1, 20) / 100
            time.sleep(sleeptime)
            output_queue.put((cnt, name))
        time.sleep(0.001)
    print("stopping")


class SharedQueueProcessManager:
    def __init__(self, process, kwargs_list) -> None:
        self.process = process
        self.input_queue = mp.Queue()
        self.output_queue = mp.Queue()
        self.val_dict = mp.Manager().dict()
        self.val_dict["stop"] = False
        self.processes = []
        for kwargs in kwargs_list:
            self.add_worker(kwargs)
        self.start_workers()
        self._received_inputs = 0
        self._processed_items = {}
        self._input_id_to_return = 0
        self.results = []

    def add_worker(self, kwargs):
        process = mp.Process(
            target=self.process,
            args=(self.input_queue, self.output_queue, self.val_dict),
            kwargs=kwargs,
        )
        self.processes.append(process)

    def start_workers(self):
        for process in self.processes:
            process.start()

    def add_item(self, item):
        self.input_queue.put((self._received_inputs, item))
        self._received_inputs += 1

    def available_results(self):
        if self._input_id_to_return in self._processed_items:
            returnable = self._processed_items[self._input_id_to_return]
            del self._processed_items[self._input_id_to_return]
            self._input_id_to_return += 1
            return returnable
        else:
            return None

    def simulate(self):
        items = [i for i in range(100)]
        for item in items:
            self.add_item(item)

        while len(self._processed_items) < self._received_inputs:
            if not self.output_queue.empty():
                id, value = self.output_queue.get()
                self._processed_items[id] = value
            time.sleep(0.001)

        self.val_dict["stop"] = True
        for proc in self.processes:
            proc.join()


def main():
    man = SharedQueueProcessManager(
        example_process,
        [
            dict(name="worker1"),
            dict(name="worker2"),
            dict(name="worker3"),
            dict(name="worker4"),
        ],
    )
    man.simulate()
    for i in range(100):
        result = man.available_results()
        print(result)


if __name__ == "__main__":
    main()
