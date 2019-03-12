

class A(object):
    a = None
    b = 2


a1 = A()
print(id(a1.a))

a2 = A()
print(id(a2.a))



