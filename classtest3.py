#!/usr/bin/env python3


class UserData:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    def __repr__(self):
        return '{}:{}'.format(self._id, self._name)


class NewUser(UserData):
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


if __name__ == '__main__':
    user1 = NewUser(101, 'Jack')
    user1.name = 'Lou'
    user1.name = 'Jackie'
    user2 = NewUser(102, 'Louplus')
    print(user1.name)
    print(user2.name)