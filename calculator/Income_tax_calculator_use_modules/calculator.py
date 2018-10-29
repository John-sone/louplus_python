# -*- coding: utf-8 -*-
import sys
import csv
from multiprocessing import Process, Queue
import queue
from getopt import getopt, GetoptError
from datetime import datetime
from collections import namedtuple
import configparser

# 税率表条目类
IncomeTaxQuickLookupItem = namedtuple(
    'IncomeTaxQuickLookupItem',
    ['income_tax_payable', 'tax_rate', 'quick_subtractor'])

# 起征点常量
INCOME_TAX_START_POINT = 3500

# 税率表
INCOME_TAX_QUICK_LOOKUP_TABLE = [
    IncomeTaxQuickLookupItem(80000, 0.45, 13505),
    IncomeTaxQuickLookupItem(55000, 0.35, 5505),
    IncomeTaxQuickLookupItem(35000, 0.30, 2755),
    IncomeTaxQuickLookupItem(9000, 0.25, 1005),
    IncomeTaxQuickLookupItem(4500, 0.20, 555),
    IncomeTaxQuickLookupItem(1500, 0.10, 105),
    IncomeTaxQuickLookupItem(0, 0.03, 0),
]


class Args(object):
    '''
    命令行参数处理
    '''

    def __init__(self):
        self.options = self._options()

    def _options(self):

        try:
            opts, _ = getopt(sys.argv[1:], "hC:c:d:o:", ['help'])
            # print(opts)
        except GetoptError:
            print('Parameter Error!')
            exit()

        options = dict(opts)
        # print(options)
        # print(len(options))

        if len(options) == 1 and ('-h' in options or '--help' in options):
            print(
                'Usage: calculator.py -C cityname -c configfile -d userdata \
                        -o resultdata'
            )
            exit()

        return options

    def _value_after_option(self, option):

        value = self.options.get(option)

        if value is None and option != '-C':
            print('Parameter Error!')
            exit()

        return value

    @property
    def city(self):

        return self._value_after_option('-C')

    @property
    def config_path(self):
        return self._value_after_option('-c')

    @property
    def userdata_path(self):
        return self._value_after_option('-d')

    @property
    def export_path(self):
        return self._value_after_option('-o')


args = Args()


class Config(object):
    def __init__(self):
        self.config = self._read_config()

    def _read_config(self):
        config = configparser.ConfigParser()
        config.read(args.config_path)
        # print(config)
        if args.city and args.city.upper() in config.sections():
            return config[args.city.upper()]
        else:
            return config['DEFAULT']

    def _get_config(self, key):

        try:
            return float(self.config[key])
        except (ValueError, KeyError):
            print('Parameter Error!')
            exit()

    @property
    def social_insurance_baseline_low(self):
        return self._get_config('JiShuL')

    @property
    def social_insurance_baseline_high(self):
        return self._get_config('JiShuH')

    @property
    def social_insurance_total_rate(self):
        return sum([
            self._get_config('YangLao'),
            self._get_config('YiLiao'),
            self._get_config('ShiYe'),
            self._get_config('GongShang'),
            self._get_config('ShengYu'),
            self._get_config('GongJiJin')
        ])


config = Config()


class UserData(Process):
    def __init__(self, userdata_queue):
        super().__init__()

        self.userdata_queue = userdata_queue

    def _read_userdata(self):

        userdata = []

        with open(args.userdata_path) as f:
            for line in f.readlines():
                employee_id, income_string = line.strip().split(',')
                try:
                    income = int(income_string)
                except ValueError:
                    print('Parameter Error!')
                    exit()
                userdata.append((employee_id, income))

        # print(userdata)
        return userdata

    def run(self):

        for item in self._read_userdata():
            self.userdata_queue.put(item)


class IncomeTaxCalculator(Process):
    def __init__(self, userdata_queue, export_queue):
        super().__init__()
        self.userdata_queue = userdata_queue
        self.export_queue = export_queue

    @staticmethod
    def calc_social_insurance_money(income):
        if income < config.social_insurance_baseline_low:
            return config.social_insurance_baseline_low * \
                    config.social_insurance_total_rate
        elif income > config.social_insurance_baseline_high:
            return config.social_insurance_baseline_high * \
                    config.social_insurance_total_rate
        else:
            return income * config.social_insurance_total_rate

    @classmethod
    def calc_income_tax_and_remian(cls, income):

        social_insurance_money = cls.calc_social_insurance_money(income)

        real_income = income - social_insurance_money
        taxable_part = real_income - INCOME_TAX_START_POINT

        for item in INCOME_TAX_QUICK_LOOKUP_TABLE:
            if taxable_part > item.income_tax_payable:
                tax = taxable_part * item.tax_rate - item.quick_subtractor
                return '{:.2f}'.format(tax), '{:.2f}'.format(real_income - tax)

        return '0.00', '{:.2f}'.format(real_income)

    def calculate(self, employee_id, income):

        social_insurance_money = '{:.2f}'.format(
            self.calc_social_insurance_money(income))

        tax, remain = self.calc_income_tax_and_remian(income)

        return [
            employee_id, income, social_insurance_money, tax, remain,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ]

    def run(self):

        while True:
            try:
                employee_id, income = self.userdata_queue.get(timeout=1)
            except queue.Empty:
                return

            result = self.calculate(employee_id, income)

            self.export_queue.put(result)


class IncomeTaxExport(Process):
    def __init__(self, export_queue):
        super().__init__()

        self.export_queue = export_queue

        self.file = open(args.export_path, 'w')
        self.writer = csv.writer(self.file)

    def run(self):

        while True:

            try:
                item = self.export_queue.get(timeout=1)
            except queue.Empty:
                self.file.close()
                return

            self.writer.writerow(item)


if __name__ == '__main__':
    userdata_queue = Queue()
    export_queue = Queue()

    userdata = UserData(userdata_queue)
    calculate = IncomeTaxCalculator(userdata_queue, export_queue)
    exporter = IncomeTaxExport(export_queue)

    userdata.start()
    calculate.start()
    exporter.start()

    userdata.join()
    calculate.join()
    exporter.join()
