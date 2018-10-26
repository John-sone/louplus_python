#!/usr/bin/env python3
import sys

# 设置税收起征点和社会保险金额

THRESHOLD = 3500

# SOCIAL_SECURITY = 0


def social_cecurity(salary):
    yanglao = salary * 8 / 100
    yiliao = salary * 2 / 100
    shiye = salary * 0.5 / 100
    gongshang = salary * 0 / 100
    shengyu = salary * 0 / 100
    gongjijin = salary * 6 / 100

    return (yanglao + yiliao + shiye + gongshang + shengyu + gongjijin)


def tax(salary):
    cecurity = social_cecurity(salary)

    if salary > 3500:
        tax_owned = salary - cecurity - THRESHOLD

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

        # print('{:.2f}'.format(tax))
        return tax

    else:
        return 0


if __name__ == '__main__':

    if len(sys.argv) > 2:
        for arg in sys.argv[1:]:
            a, b = arg.split(':')
            try:
                salary = int(b)
            except ValueError:
                print("Parameter Error")
                sys.exit()

            salary_tax = tax(salary)
            salary_security = social_cecurity(salary)
            print('{}:{:0.2f}'.format(a,
                                      salary - salary_security - salary_tax))

    else:
        print('error args')
