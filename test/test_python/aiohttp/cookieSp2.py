
import asyncio
import aiohttp
from lxml import etree

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "HOST": "localhost",
    "Referer": "http://localhost:8000/login",
}

header_remote = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "HOST": "119.29.152.194",
    "Referer": "http://119.29.152.194:8000/login",
}


async def fetch_one():
    async with aiohttp.ClientSession() as session:
        login_url = 'http://localhost:8000/test_cookies/test_cookies_99999'
        async with session.get(login_url, headers=header) as res:
            print(await res.text())
            print(res.status)


async def fetch():
    async with aiohttp.ClientSession() as session:
        login_url = 'http://localhost:8000/login'
        async with session.get(login_url, headers=header) as res:
            print('begin_login: ' + str(res.url))
            text = await res.text()
            # html = etree.parse(text, etree.HTMLParser())
            html = etree.HTML(text)
            _xsrf = html.xpath(".//form/input[1]/@value")
            print(_xsrf)
        login_url = "http://localhost:8000/login"
        login_data = {"username": "huyuan", "password": "hy195730", '_xsrf': _xsrf}
        async with session.post(login_url, headers=header, data=login_data) as res:
            text = await res.text()
            # html = etree.parse(text, etree.HTMLParser())
            html = etree.HTML(text)
            _xsrf = html.xpath(".//form/input[1]/@value")
            print(_xsrf)

            res_url = str(res.url)
            print('do_login: ' + res_url)
            if "welcome" in res_url:
                print('登录成功')
            else:
                print("登录失败")
                # return
        for i in range(10):
            url = 'http://localhost:8000/test_cookies/test_cookies_' + str(i)
            res2 = await session.get(url, headers=header)
            print('is_login: ' + str(res2.url))
            text = await res2.text()
            with open('/Users/muyichun/PycharmProjects/socialpeta/quixote/logs/html/nn.html', 'w',
                      encoding=res2.charset) as f:
                f.write(text)
            res2.close()


async def fetch11():
    async with aiohttp.ClientSession() as session:
        login_url = 'http://119.29.152.194:8000/login'
        async with session.get(login_url, headers=header_remote) as res_remote:
            print('begin_login: ' + str(res_remote.url))
            text = await res_remote.text()
            html = etree.HTML(text)
            _xsrf = html.xpath(".//form/input[1]/@value")
            print(_xsrf)
        login_url = "http://119.29.152.194:8000/login"
        login_data = {"username": "quixote", "password": "123456789", '_xsrf': _xsrf}
        # login_data = {"username": "quixote", "password": "123456789"}
        async with session.post(login_url, headers=header_remote, data=login_data) as res_remote:
            text = await res_remote.text()
            html = etree.HTML(text)
            _xsrf = html.xpath(".//form/input[1]/@value")
            print(_xsrf)

            res_url = str(res_remote.url)
            print('do_login: ' + res_url)
            if "welcome" in res_url:
                print('登录成功')
            else:
                print("登录失败")
                return
        for i in range(10):
            url_remote = 'http://119.29.152.194:8000/test_cookies/test_cookies_remote_' + str(i+99999000)
            res2 = await session.get(url_remote, headers=header_remote)
            print('is_login: ' + str(res2.url))
            text = await res2.text()
            with open('/Users/muyichun/PycharmProjects/socialpeta/quixote/logs/html/jj.html', 'w',
                      encoding=res2.charset) as f:
                f.write(text)
            res2.close()


async def fetch2():
    async with aiohttp.ClientSession() as session:
        login_url = 'http://localhost:8000/login'
        async with session.get(login_url, headers=header) as res:
            print('begin_login: ' + str(res.url))
            text = await res.text()
            # html = etree.parse(text, etree.HTMLParser())
            html = etree.HTML(text)
            _xsrf = html.xpath(".//form/input[1]/@value")
            print(_xsrf)
        login_url = "http://localhost:8000/login"
        login_data = {"username": "huyuan", "password": "hy195730", '_xsrf': _xsrf}
        async with session.post(login_url, headers=header, data=login_data) as res:
            res_url = str(res.url)
            print('do_login: ' + res_url)
            if "welcome" in res_url:
                print('登录成功')
            else:
                print("登录失败")
                return
        print('*************************************************************************************')
        login_url = 'http://119.29.152.194:8000/login'
        async with session.get(login_url, headers=header_remote) as res_remote:
            print('begin_login: ' + str(res_remote.url))
            text = await res_remote.text()
            html = etree.HTML(text)
            _xsrf = html.xpath(".//form/input[1]/@value")
            print(_xsrf)
        login_url = "http://119.29.152.194:8000/login"
        login_data = {"username": "huyuan", "password": "hy195730", '_xsrf': _xsrf}
        async with session.post(login_url, headers=header_remote, data=login_data) as res_remote:
            res_url = str(res_remote.url)
            print('do_login: ' + res_url)
            if "welcome" in res_url:
                print('登录成功')
            else:
                print("登录失败")
                return
        print('*************************************************************************************')
        for i in range(10):
            url = 'http://localhost:8000/test_cookies/test_cookies_' + str(i)
            res2 = await session.get(url, headers=header)
            print('is_login: ' + str(res2.url))
            text = await res2.text()
            with open('/Users/muyichun/PycharmProjects/socialpeta/quixote/logs/html/nn.html', 'w',
                      encoding=res2.charset) as f:
                f.write(text)
            res2.close()
            print('********************************')
            url_remote = 'http://119.29.152.194:8000/test_cookies/test_cookies_remote_' + str(i+99999000)
            res2 = await session.get(url_remote, headers=header_remote)
            print('is_login: ' + str(res2.url))
            text = await res2.text()
            with open('/Users/muyichun/PycharmProjects/socialpeta/quixote/logs/html/jj.html', 'w',
                      encoding=res2.charset) as f:
                f.write(text)
            res2.close()
        print('*************************************************************************************')


loop = asyncio.get_event_loop()
tasks = [fetch(), ]
# tasks = [fetch11(), ]
# tasks = [fetch2(), ]
# tasks = [fetch_one(), ]
loop.run_until_complete(asyncio.wait(tasks))

loop.run_until_complete(asyncio.sleep(1))
loop.close()
