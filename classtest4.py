#!/usr/bin/env python3


class UserData:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    def __repr__(self):
        return '{}:{}'.format(self._id, self._name)


class NewUser(UserData):

    group = 'shiyanlou-louplus'

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if len(value) > 3:
            self._name = value
        else:
            print('Error')

    def __repr__(self):
        return "{}'s id is {}".format(self._name, self._id)

    @classmethod
    def get_group(cls):
        return cls.group

    @staticmethod
    def format_userdata(id, name):
        return "{}'s id is {}".format(name, id)


if __name__ == '__main__':
    print(NewUser.get_group())
    print(NewUser.format_userdata(109, 'Lucy'))
