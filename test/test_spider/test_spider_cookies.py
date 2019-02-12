# -*- coding: utf-8 -*-
from quixote import Spider, Request, FormRequest
from quixote.starter import Starter


class DongmengSpider(Spider):
    name = 'dongmeng'
    allowed_domains = ['www.dongmengdai.com']
    start_urls = ['https://www.dongmengdai.com/view/Investment_list_che.php?page=1']

    # 根据浏览器Network返回值来构造header，这是比较简单的header，复杂的还会有很多信息
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "HOST": "www.dongmengdai.com",
        "Referer": "https://www.dongmengdai.com/index.php?user&q=action/login",
    }

    def parse(self, response):
        """ 正式进入爬取区域 """
        print('parse: '+str(response))
        with open('/Users/muyichun/PycharmProjects/socialpeta/quixote/logs/html/bb.html', 'w',
                  encoding=response.encoding) as f:
            text = response.text
            f.write(text)
        yield b'parsed...'

    def start_requests(self):
        """重载start_requests方法 待登录成功后，再进入parse进行数据爬取
            访问登录页面 并调用do_login方法进行登录
        """
        print('start_requests: ')
        return [Request('https://www.dongmengdai.com/index.php?user&q=action/login', headers=self.header,
                        callback=self.do_login)]

    def do_login(self, response):
        """根据Network的信息 向登录地址发送请求
            携带用户名和密码 如果需要token或者其他标识则需要用正则进行匹配，然后放到login_data中
            调用is_login方法判断是否登录成功
        """
        print('do_login: '+str(response))
        login_url = "https://www.dongmengdai.com/index.php?user&q=action/login"
        login_data = {
            "keywords": "15972920500",
            "password": "hy195730"
        }
        return [FormRequest(url=login_url, formdata=login_data, headers=self.header, callback=self.is_login)]

    def is_login(self, response):
        """这个网站登陆后会自动跳转到用户中心 可根据返回的url判断是否登录成功
            其他网站可以依靠状态码进行判断
            如果登录成功则从 start_urls中抽取url进行爬取
            这里不用设置callback回调parse 因为它默认调用parse
                如果是在crawl模板的爬虫，可能需要设置callback调用
        """
        if "index.php?user" in response.url:
            print('is_login: '+str(response))
            for url in self.start_urls:
                yield Request(url, dont_filter=True, headers=self.header, callback=self.parse)
        else:
            print("登录失败")


def main():
    s = Starter('quixote.test.test_spider.test_spider_cookies.DongmengSpider')
    s.start()


if __name__ == '__main__':
    main()
