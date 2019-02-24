
from quixote import Item, Field


class TestItem(Item):
    status = Field()
    url = Field()
    pipeline = Field()
    q = Field()
