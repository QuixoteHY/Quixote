
from time import time


class A(object):
    state = 404

    @staticmethod
    def pp():
        print('A pp...')

    @staticmethod
    def pp2():
        return 'A pp...'


res = eval('A.state')
print(res)

res = eval('A.pp2()')
print(res)

res = eval('time()')
print(res)
