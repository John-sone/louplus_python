#!/usr/bin/env python3


def compute(base, value):
    result = sum(base)
    print(result + value)


if __name__ == '__main__':
    testlist = [10, 20, 30]
    compute(testlist, 15)
    compute(testlist, 25)
    compute(testlist, 35)