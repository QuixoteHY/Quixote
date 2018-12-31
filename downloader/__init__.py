# -*- coding:utf-8 -*-
# @Time     : 2018-12-31 22:55
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 下载器

import aiohttp


class Downloader(object):

    @staticmethod
    async def get(url, headers=None, cookies=None, proxy=None, timeout=10):
        if cookies:
            session = aiohttp.ClientSession(cookies=cookies)
        else:
            session = aiohttp.ClientSession()
        if proxy:
            response = await session.get(url, headers=headers, proxy=proxy, timeout=timeout)
        else:
            response = await session.get(url, headers=headers, timeout=timeout)
        await session.close()
        return response

    @staticmethod
    async def post(url, headers=None, data=None, cookies=None, proxy=None, timeout=10):
        if cookies:
            session = aiohttp.ClientSession(cookies=cookies)
        else:
            session = aiohttp.ClientSession()
        if proxy:
            response = await session.post(url, headers=headers, data=data, proxy=proxy, timeout=timeout)
        else:
            response = await session.post(url, headers=headers, data=data, timeout=timeout)
        await session.close()
        return response
