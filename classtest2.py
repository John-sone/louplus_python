#!/usr/bin/env python3


class UserData:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '{}:{}'.format(self.id, self.name)


class NewUser(UserData):
    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def __repr__(self):
        return "{}'s id is {}".format(self.name, self.id)


if __name__ == '__main__':
    user1 = NewUser(101, 'Jack')
    user1.set_name('Jackie')
    user2 = NewUser(102, 'Louplus')
    print(user1)
    print(user2)