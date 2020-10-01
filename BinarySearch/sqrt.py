#! Python3
# This script compute a square root with certain precition using binary search
import numpy as np

EPSILON = 1e-10

def binary_sqrt(value):
    #compute mid = L + (R-L)2
    l = 0 #left side interval
    r = value #right side interval
    while r - l > EPSILON:
        mid = l + (r-l)/2
        if mid * mid < value:
            l = mid
        else:
            r = mid
    return l + (r-l)/2

def main():
    try:
        value = input("Enter the square root to compute: ")
        sq = binary_sqrt(float(value))
        print(f"The square root of {value} is {sq}")
    except ValueError:
        print("[ERROR] A number is expected.")

if __name__ == "__main__":
    main()
