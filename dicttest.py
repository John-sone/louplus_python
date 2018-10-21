#!/usr/bin/env python3

import sys

dict_test = {}

for i in sys.argv[1:]:
    a, b = i.split(':')
    dict_test[a] = b

# print(dict_test)

for key, value in dict_test.items():
    print('ID:{} Name:{}'.format(key, value))
