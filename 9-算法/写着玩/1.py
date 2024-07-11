"""
水仙花数

一个n(3)位数，如果 每个位上的数字的立方和等于这个数，那么这个数就是水仙花数。

"""

import time

def calculate_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to run.")
        return result
    return wrapper

@calculate_time
def is_hua(n) -> list:
    """
    args:
        是一个几位数
    return: []
    """    
    r_list = []
    for i in range(10**(n-1), 10**n-1):
        l2 = [int(ii)**3 for ii in str(i)]
        if sum(l2) == i:
            r_list.append(i)
    return r_list

if __name__ == '__main__':
    x = is_hua(3)
    print(x)
    
