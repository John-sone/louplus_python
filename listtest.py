#!/usr/bin/env python3

import sys

long = []
short = []

for i in sys.argv[1:]:
    if len(i) > 3:
        long.append(i)
    else:
        short.append(i)

print(long)
print(short)
