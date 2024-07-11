
def a1(i):
    print(i)
    if i == 0:  # 到达0的时候就不在继续了(基准条件)
        return
    else:   # 递归条件
        a1(i-1)

a1(10)


