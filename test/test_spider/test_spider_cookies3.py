# -*- coding: utf-8 -*-

from os.path import dirname, abspath
import time

import quixote
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

    def start_requests(self):
        print('start_requests: ')
        yield quixote.Request('http://'+self.host+':8000/login', headers=self.header, callback=self.do_login)
        login_url = 'http://'+self.host+':8000/login'
        login_data = {"username": "huyuan", "password": "hy195730", '_xsrf': self._xsrf}
        yield quixote.FormRequest(url=login_url, method='POST', formdata=login_data, headers=self.header,
                                  callback=self.is_login)
        i = 0
        while True:
            i += 1
            # if i > 10:
            #     break
            url = 'http://'+self.host+':8000/test_cookies/test_cookies_'+str(i)
            print(url)
            yield quixote.Request(url, dont_filter=True, headers=self.header, callback=self.parse)

    def do_login(self, response):
        print(response)
        self._xsrf = response.xpath(".//form/input[1]/@value").extract()[0]
        print(self._xsrf)
        # login_url = 'http://'+self.host+':8000/login'
        # login_data = {"username": "huyuan", "password": "hy195730", '_xsrf': _xsrf}
        # return [quixote.FormRequest(url=login_url, method='POST', formdata=login_data, headers=self.header,
        #                             callback=self.is_login)]
        yield b'do_login......'

    def is_login(self, response):
        print(response)
        if "welcome" in response.url:
            print("登录成功")
            # for i in range(100):
            # i = 0
            # while True:
            #     i += 1
            #     if i > 100000:
            #         break
            #     url = 'http://'+self.host+':8000/test_cookies/test_cookies_'+str(i)
            #     yield quixote.Request(url, dont_filter=True, headers=self.header, callback=self.parse)
            yield b'is_login......'
        else:
            print("登录失败")
            import sys
            sys.exit(1)

    def parse(self, response):
        # print(response)
        # with open(self.logs_path+'html/mm.html', 'w') as f:
        #     f.write(response.text)
        time.sleep(0.05)
        yield bytes(str(response), encoding='utf8')


def main():
    s = Starter('quixote.test.test_spider.test_spider_cookies2.TestCookiesSpider', is_check_emmory=False)
    s.start()


if __name__ == '__main__':
    main()
