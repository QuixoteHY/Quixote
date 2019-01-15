
from quixote.utils.httpobj import urlparse_cached

from quixote.protocol.request import Request


def parse():
    print('parse')


print(urlparse_cached(Request(url='http://www.baidu.com', callback=parse)))


