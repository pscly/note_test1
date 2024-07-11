# coding: utf-8
# sum尝试

def sum1(l1:list):
    r1 = 0
    for i in l1:
        r1 += i
    return r1

def sum2(l1:list):
    if l1:
        return l1[0] + sum2(l1[1::])
    return 0

print(sum2([2,4,6]))


