import math 
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:  # base case
        return n
    return fib(n-1) + fib(n-2)
  
def is_prime(n): 
    # Corner cases 
    if (n <= 1) : 
        return False
    if (n <= 3) : 
        return True
    if (n % 2 == 0 or n % 3 == 0) : 
        return False
  
    i = 5
    while(i * i <= n) : 
        if (n % i == 0 or n % (i + 2) == 0) : 
            return False
        i = i + 6
  
    return True


def solution(n):
    result = []
    for i in range(1,n+1):
        val = fib(i)
        if is_prime(val):
            result.append(val)
    return result

print(solution(11))