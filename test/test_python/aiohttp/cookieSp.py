
import asyncio
import aiohttp

start_urls = ['https://www.dongmengdai.com/view/Investment_list_che.php?page=1',
              'https://www.dongmengdai.com/view/Investment_list_che.php']
header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "HOST": "www.dongmengdai.com",
    "Referer": "https://www.dongmengdai.com/index.php?user&q=action/login",
}


async def fetch():
    async with aiohttp.ClientSession() as session:
        login_url = 'https://www.dongmengdai.com/index.php?user&q=action/login'
        async with session.get(login_url, headers=header) as res:
            print('begin_login: ' + str(res.url))
        login_data = {
            "keywords": "15972920500",
            "password": "hy195730"
        }
        async with session.post(login_url, headers=header, data=login_data) as res:
            res_url = str(res.url)
            print('do_login: ' + res_url)
            if "index.php?user" in res_url:
                print('登录成功')
            else:
                print("登录失败")
                return
        for start_url in start_urls:
            async with session.get(start_url, headers=header) as res2:
                print('is_login: ' + str(res2.url))
                text = await res2.text()
                with open('/Users/muyichun/PycharmProjects/socialpeta/quixote/logs/html/zz.html', 'w',
                          encoding=res2.charset) as f:
                    f.write(text)


async def fetch2():
    async with aiohttp.ClientSession() as session:
        login_url = 'https://www.dongmengdai.com/index.php?user&q=action/login'
        async with session.get(login_url, headers=header) as res:
            print('begin_login: ' + str(res.url))
        login_data = {
            "keywords": "15972920500",
            "password": "hy195730"
        }
        async with session.post(login_url, headers=header, data=login_data) as res:
            res_url = str(res.url)
            print('do_login: ' + res_url)
            if "index.php?user" in res_url:
                print('登录成功')
            else:
                print("登录失败")
                return
        for start_url in start_urls:
            res2 = await session.get(start_url, headers=header)
            print('is_login: ' + str(res2.url))
            text = await res2.text()
            with open('/Users/muyichun/PycharmProjects/socialpeta/quixote/logs/html/zz.html', 'w',
                      encoding=res2.charset) as f:
                f.write(text)
            res2.close()


loop = asyncio.get_event_loop()
# tasks = [fetch(), ]
tasks = [fetch2(), ]
loop.run_until_complete(asyncio.wait(tasks))

loop.run_until_complete(asyncio.sleep(1))
loop.close()
