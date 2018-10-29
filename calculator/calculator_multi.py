import sys
import csv
from multiprocessing import Process, Queue

THRESHOLD = 3500


class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]

    @property
    def configfile(self):
        try:
            index_c = self.args.index('-c')
            configfile = self.args[index_c + 1]
            return configfile
        except ValueError:
            print('Paremeter Error!')
            sys.exit(-1)

    @property
    def userdatafile(self):
        try:
            index_d = self.args.index('-d')
            userdatafile = self.args[index_d + 1]
            return userdatafile
        except ValueError:
            print('Paremeter Error!')
            sys.exit(-1)

    @property
    def outputfile(self):
        try:
            index_o = self.args.index('-o')
            outputfile = self.args[index_o + 1]
            return outputfile
        except ValueError:
            print('Paremeter Error!')
            sys.exit(-1)


class Config(object):
    def __init__(self):
        self.config = self._read_config()

    def _read_config(self):
        args_ = Args()
        config = {}
        try:
            path = args_.configfile
            with open(path) as f:
                for x in f:
                    # x = x.strip()
                    # print(x)
                    a, b = x.split('=')
                    config[a.strip()] = b.strip()
            # print(config['JiShuL'])
        except FileNotFoundError:
            print('No such file or directory!')
            sys.exit(-1)

        return config


class UserData(object):
    def __init__(self):
        # self.userdata = self._read_userdata()
        pass

    def _read_userdata(self, queue1):
        args_ = Args()

        userdata = []
        # path = args_.userdatafile
        try:
            with open(args_.userdatafile, 'r') as f:
                data = list(csv.reader(f))
                for i in data:
                    # print(i)
                    userdata.append(tuple(i))
            # print(userdata)
        except FileNotFoundError:
            print('No such file or directory!')
        queue1.put_nowait(userdata)


class IncomeTaxCalculator(object):
    def calc_for_all_userdata(self, queue1, queue2):
        # userdata_ = UserData()
        config_ = Config()
        userdata = queue1.get_nowait()
        outputdata = []

        for data in userdata:
            user = data[0]
            salary = data[1]
            taxdata = []
            taxdata.append(user)
            taxdata.append(salary)
            # print(salary, config_.config['JiShuL'])
            shebao = float(config_.config['YangLao']) + float(
                config_.config['YiLiao']) + float(
                    config_.config['ShiYe']) + float(
                        config_.config['GongJiJin'])
            if float(salary) < float(config_.config['JiShuL']):
                shebao = shebao * int(config_.config['JiShuL'])
                taxdata.append('%.2f' % shebao)
            elif float(salary) > float(config_.config['JiShuH']):
                shebao = float(config_.config['JiShuH']) * shebao
                taxdata.append('%.2f' % shebao)
                # taxdata.append(shebao)
            else:
                shebao = float(salary) * shebao
                # taxdata.append(shebao)
                taxdata.append('%.2f' % shebao)

            if float(salary) > 3500:
                tax_owned = float(salary) - shebao - THRESHOLD

                if tax_owned <= 1500:
                    tax = tax_owned * 3 / 100
                    taxdata.append(tax)
                elif 1500 < tax_owned <= 4500:
                    tax = tax_owned * 10 / 100 - 105
                    taxdata.append(tax)
                elif 4500 < tax_owned <= 9000:
                    tax = tax_owned * 20 / 100 - 555
                    taxdata.append(tax)
                elif 9000 < tax_owned <= 35000:
                    tax = tax_owned * 25 / 100 - 1005
                    taxdata.append(tax)
                elif 35000 < tax_owned <= 55000:
                    tax = tax_owned * 30 / 100 - 2755
                    taxdata.append(tax)
                elif 55000 < tax_owned <= 80000:
                    tax = tax_owned * 35 / 100 - 5505
                    taxdata.append(tax)
                else:
                    tax = tax_owned * 45 / 100 - 13505
                    taxdata.append(tax)
            else:
                tax = 0.00
                taxdata.append('%.2f' % tax)

            taxdata.append('%.2f' % (float(salary) - shebao - tax))
            outputdata.append(taxdata)
        # print(outputdata)
        # return outputdata
        queue2.put_nowait(outputdata)

    def export(self, queue2, default='csv'):
        args_ = Args()
        # result = self.calc_for_all_userdata()
        result = queue2.get()
        path = args_.outputfile
        with open(path, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(result)


if __name__ == '__main__':
    queue1 = Queue()
    queue2 = Queue()
    userdata = UserData()
    gongzi = IncomeTaxCalculator()
    Process(target=userdata._read_userdata, args=(queue1, )).start()
    Process(target=gongzi.calc_for_all_userdata, args=(queue1, queue2)).start()
    Process(target=gongzi.export, args=(queue2, )).start()
