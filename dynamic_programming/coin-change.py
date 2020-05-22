#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'getWays' function below.
#
# The function is expected to return a LONG_INTEGER.
# The function accepts following parameters:
#  1. INTEGER n
#  2. LONG_INTEGER_ARRAY c
#

def getWays(n, c):
    combinations = [0 for k in range(n+1)]
    combinations[0] = 1 # there is only 1 way to return 0 cents
    # Pick all coins one by one and update the combinations[] values 
    # after the index greater than or equal to the value of the 
    # picked coin 
    for i in range(0,len(c)): # for each coin
        for j in range(c[i],n+1): # for each coin starting from j to the target amount
            reminder = j-c[i]
            combinations[j] += combinations[reminder]
    return combinations[n] 


if __name__ == '__main__':
    assert getWays(4, [1,2,3]) == 4
