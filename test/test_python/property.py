
class Goods(object):
    _price = None

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @price.deleter
    def price(self):
        self._price = None


obj = Goods()
obj.price = 50
print(obj.price)
del obj.price
