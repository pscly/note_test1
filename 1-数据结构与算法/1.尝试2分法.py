# coding: utf-8

l1 = [i for i in range(100)]
# l1 = [1,2,3,4,5]
count = 0

answer = 99  # 答案

now_l1 = l1
while 1:
    count += 1
    # left_num = now_l1[0]
    # right_num = now_l1[-1]
    center = now_l1[len(now_l1) // 2]   # 取中位数

    if answer == center:
        break
    elif answer > center:   # 如果答案大于中位数
        now_l1 = now_l1[(len(now_l1) // 2):len(now_l1)]
    elif answer < center:
        now_l1 = now_l1[0: (len(now_l1) // 2)]

print(count)
