#!/usr/bin/env python3


def count_str(str):
    countdict = {}
    for char in str:
        countdict[char] = countdict.setdefault(char, 0) + 1
    print(countdict)


if __name__ == '__main__':
    s = input('Enter a string: ')
    count_str(s)
