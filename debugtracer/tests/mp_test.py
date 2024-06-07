# multiprocessing queue test scripts
from multiprocessing import Queue


def function_to_ignore(queue):
    queue.put("Hello, World!")
    return 0


def main():
    q = Queue()
    v = function_to_ignore(q)
    print("completed")
