#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the reverseArray function below.
def reverseArray(a):
    l = len(a)
    middle = int(len(a) / 2)
    for i in range(middle):
        a[i],a[l-1-i] = a[l-1-i],a[i]
    return a

if __name__ == '__main__':
   res = reverseArray([1,4,3,2])
   print(res)
   assert res == [2,3,4,1]
