# -*- coding: utf-8 -*-

import scrapy
from scrapy import cmdline

# scrapy runspider test_cookies.py
# scrapy runspider test_cookies.py --nolog


class TestCookiesSpider(scrapy.Spider):
    name = 'test_cookies'
    # host = 'localhost'
    # host = '127.0.0.1'
    host = '192.168.31.142'
    # host = '119.29.152.194'
    port = 8000
    allowed_domains = [host]
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "HOST": host,
        "Referer": "http://"+host+str(port)+"/login",
    }

    def parse(self, response):
        print('parse: '+response.url)
        with open('/Users/muyichun/PycharmProjects/socialpeta/quixote/logs/html/mm.html', 'w') as f:
            f.write(response.text)

    def start_requests(self):
        print('start_requests: ')
        return [scrapy.Request('http://'+self.host+':8000/login', headers=self.header, callback=self.do_login)]

    def do_login(self, response):
        print('do_login: '+response.url)
        _xsrf = response.xpath(".//form/input[1]/@value").extract()[0]
        print(_xsrf)
        login_url = 'http://'+self.host+':8000/login'
        login_data = {"username": "huyuan", "password": "hy195730", '_xsrf': _xsrf}
        return [scrapy.FormRequest(url=login_url, formdata=login_data, headers=self.header, callback=self.is_login)]

    def is_login(self, response):
        if "welcome" in response.url:
            print('is_login: '+response.url)
            for i in range(10):
                url = 'http://'+self.host+':8000/test_cookies/test_cookies_'+str(i)
                yield scrapy.Request(url, dont_filter=True, headers=self.header)
        else:
            print("登录失败")


if __name__ == '__main__':
    cmdline.execute("scrapy runspider test_cookies.py --nolog".split())
    # cmdline.execute("scrapy runspider test_cookies.py".split())
