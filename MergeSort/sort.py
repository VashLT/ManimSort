#!Python 3

# Implementation of MergeSort algorithm in Python 3.7.4
import sys
import time
import logging
import numpy as np
from Modules.Screen.Screen import Screen

logging.basicConfig(
    filename="merge.log", format="%(asctime)s | %(funcName)s : %(message)s", level=logging.DEBUG
)
# logging.disable(logging.DEBUG)


def mergeSort(array, start_index, end_index):
    """ divide and conqueror algorithm"""
    if start_index < end_index:
        split = int(np.floor((start_index + end_index) / 2))

        logging.debug(f"Merging {array[start_index:end_index + 1]}")

        # divide input array till one-element arrays
        mergeSort(array, start_index, split)
        mergeSort(array, split + 1, end_index)
        # re-build splitted sub-arrays
        merge(array, start_index, split, end_index)


def merge(array, start_index, split, end_index):
    n1 = split - start_index + 1
    n2 = end_index - split
    left_side = []
    right_side = []
    logging.debug(f"Sorting {array[start_index: end_index + 1]}")
    for i in range(n1):
        left_side.append(array[start_index + i])
    for j in range(n2):
        right_side.append(array[split + j + 1])
    left_side.append(float('inf'))
    right_side.append(float('inf'))
    i = 0
    j = 0
    logging.debug(f"""
    R = {right_side}
    L = {left_side}
    """)
    for k in range(start_index, end_index + 1):
        if left_side[i] <= right_side[j]:
            array[k] = left_side[i]
            i += 1
        else:
            array[k] = right_side[j]
            j += 1
    logging.debug(f"""
    mod array = {array}
    """)


def start_sort(array, desc=False):
    """ intermedius function to keep track of execution time """
    a = array.copy()
    start_time = time.perf_counter_ns()
    n = len(array)
    mergeSort(a, 0, n - 1)

    return a, start_time


def main(args):
    screen = Screen("Merge Sort")
    screen.display()
    n = 20  # input size
    to_sort = np.random.randint(1, 10000, size=n, dtype=np.int64)
    print(f"[IN PROCESS] Processing input: {to_sort}")
    result, start_time = start_sort(to_sort)
    exec_time = time.perf_counter_ns() - start_time
    print(f"[INFO] Input successfully proccessed. Time spent: {exec_time}ns")
    print(f"""
    INPUT: {to_sort}
    OUTPUT: {result}
    """)


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


if __name__ == "__main__":
    main(sys.argv)
