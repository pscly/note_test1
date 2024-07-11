def is_narcissistic_number(n):
    """
    判断一个数是否是水仙花数

    Args:
      n: 要判断的数

    Returns:
      True 如果是水仙花数，False 如果不是
    """

    digits = list(str(n))
    n_digits = len(digits)
    sum_of_powers = 0
    for digit in digits:
        sum_of_powers += int(digit) ** n_digits

    return sum_of_powers == n


def main():
    """
    主函数
    """

    for i in range(100, 1000):
        if is_narcissistic_number(i):
            print(i)


if __name__ == "__main__":
    main()
