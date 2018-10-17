#!/usr/bin/env python3
import sys

# 设置税收起征点和社会保险金额

THRESHOLD = 3500
SOCIAL_SECURITY = 0

if len(sys.argv) == 2:
    try:
        salary = int(sys.argv[1])
    except ValueError:
        print("Parameter Error")
        sys.exit()

    if salary > 3500:
        tax_owned = salary - SOCIAL_SECURITY - THRESHOLD

        if tax_owned <= 1500:
            tax = tax_owned * 3 / 100
        elif 1500 < tax_owned <= 4500:
            tax = tax_owned * 10 / 100 - 105
        elif 4500 < tax_owned <= 9000:
            tax = tax_owned * 20 / 100 - 555
        elif 9000 < tax_owned <= 35000:
            tax = tax_owned * 25 / 100 - 1005
        elif 35000 < tax_owned <= 55000:
            tax = tax_owned * 30 / 100 - 2755
        elif 55000 < tax_owned <= 80000:
            tax = tax_owned * 35 / 100 - 5505
        else:
            tax = tax_owned * 45 / 100 - 13505

        print('{:.2f}'.format(tax))

    else:
        print(0.00)
else:
    print('error args')
