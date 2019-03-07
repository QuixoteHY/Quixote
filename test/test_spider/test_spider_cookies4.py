# -*- coding: utf-8 -*-

from os.path import dirname, abspath
import time

import quixote
from quixote.test.test_spider.test_item import TestItem
from quixote.starter import Starter


class TestCookiesSpider(quixote.Spider):
    name = 'test_cookies'
    # host = 'localhost'
    # host = '127.0.0.1'
    host = 'www.huyuan.com'
    # host = '192.168.31.142'
    # host = 'www.quixotehy.xyz'
    # host = '119.29.152.194'
    port = 8000
    allowed_domains = [host]
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "HOST": host,
        "Referer": "http://"+host+':'+str(port)+"/login",
        "Connection": "keep-alive",
    }
    logs_path = dirname(dirname(dirname(abspath(__file__))))+'/logs/'
    _xsrf = ''
    i = 0
    j = 0

    def before_start_requests(self):
        print('before_start_requests 4: ')
        yield quixote.Request('http://'+self.host+':8000/login', headers=self.header, callback=self.do_login)
        login_url = 'http://'+self.host+':8000/login'
        login_data = {"username": "huyuan", "password": "hy195730", '_xsrf': self._xsrf}
        yield quixote.FormRequest(url=login_url, method='POST', formdata=login_data, headers=self.header,
                                  callback=self.is_login)

    def start_requests(self):
        print('start_requests: ')
        while True:
            self.i += 1
            url = 'http://'+self.host+':8000/test_cookies/test_cookies_'+str(self.i)
            # yield quixote.Request(url, dont_filter=True, headers=self.header, callback=self.parse)
            yield quixote.Request(url, dont_filter=True, headers=self.header)
            if self.i > 2000:
                break

    def do_login(self, response):
        print(response)
        self._xsrf = response.xpath(".//form/input[1]/@value").extract()[0]
        print(self._xsrf)
        yield b'do_login......'
        # return 100

    def is_login(self, response):
        print(response)
        if "welcome" in response.url:
            print("登录成功")
            yield b'is_login......'
        else:
            print("登录失败")
            import sys
            sys.exit(1)

    def parse(self, response):
        # with open(self.logs_path+'html01/mm.html', 'a') as f:
        #     f.write(response.text)
        self.j += 1
        if self.j in [100, 1500, 20000, 25000]:
            url = 'http://' + self.host + ':8000/test_cookies/PARSE_RECORD_%s' + 'W'*3000
            yield quixote.Request(url % self.j, dont_filter=True, headers=self.header)
            yield quixote.Request(url % (self.j+1), dont_filter=True, headers=self.header)
            yield quixote.Request(url % (self.j+2), dont_filter=True, headers=self.header)
            yield quixote.Request('http://' + self.host + ':8000/test_cookies/OOOOOOOOOOO_PARSE_RECORD_%s' % (self.j+3),
                                  dont_filter=True, headers=self.header)
            yield quixote.Request(url % (self.j+4), dont_filter=True, headers=self.header)
            yield quixote.Request('http://' + self.host + ':8000/aaa/HttpErrorMiddleware_%s' % (self.j+8),
                                  dont_filter=True, headers=self.header)
            yield quixote.Request('http://' + self.host + ':8000/bbb/HttpErrorMiddleware%s' % (self.j+9),
                                  dont_filter=True, headers=self.header)
        time.sleep(0.05)
        item = TestItem()
        item['status'] = response.status
        item['url'] = response.url
        item['pipeline'] = list()
        item['q'] = ''
        yield item


def main():
    s = Starter('quixote.test.test_spider.test_spider_cookies4.TestCookiesSpider', is_check_emmory=False)
    s.start()


if __name__ == '__main__':
    main()
