# coding: utf-8
# 

def ou1(i1, i2):
    if i1 < i2:
        i1, i2 = i2, i1     # i1 和 i2交换
    if i2 == 0:     
        return i1
    i1 = i1 - i2
    return ou1(i1, i2)

print(ou1(90, 40))
print(ou1(121, 88))

