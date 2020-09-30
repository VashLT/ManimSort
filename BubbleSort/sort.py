#!Python 3

# Implementation of BubbleSort algorithm in Python 3.7.4
# Computational complexity O(n^2)
import sys
import time
import numpy as np
from Modules.Screen.Screen import Screen


def bubbleSort(array, desc=False):
    a = array.copy()
    start_time = time.time()
    n = len(array)
    for i in range(n):
        for j in range(i + 1, n, 1):
            temp = a[j]
            if a[i] >= a[j]:
                a[j] = a[i]
                a[i] = temp
            else:

                if desc:
                    a[j] = a[i]
                    a[i] = temp

    return a, start_time


def main(args):
    screen = Screen("Bubble Sort")
    screen.display()
    n = np.random.randint(1, 100)
    to_sort = np.random.randint(1, 10000, size=n, dtype=np.int64)
    print(f"[IN PROCESS] Processing input: {to_sort}")
    result, start_time = bubbleSort(to_sort)
    exec_time = time.time() - start_time
    print(f"[INFO] Input successfully proccessed. Time spent: {exec_time}s")
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
