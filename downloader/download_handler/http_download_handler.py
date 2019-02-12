# -*- coding:utf-8 -*-
# @Time     : 2019-01-15 22:47
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

import asyncio
import aiohttp

from quixote.protocol.response.html import HtmlResponse


class HTTPDownloadHandler(object):
    def __init__(self, settings):
        self.session = aiohttp.ClientSession()
        # print(settings['DOWNLOAD_HANDLERS']['http'])

    def download_request(self, request, spider):
        task = asyncio.ensure_future(self._download(request, spider))
        task.add_done_callback(self.downloaded)
        return task

    async def close(self):
        await self.session.close()

    @staticmethod
    def downloaded(future):
        print('Downloaded {}'.format(future.result().request.url))

    async def _download(self, request, spider):
        response = await self.session.request(request.method, request.url,
                                              **{'headers': request.headers.get_aiohttp_headers(),
                                                 'data': request.body})
        content = await response.read()
        await asyncio.sleep(1.8)
        return HtmlResponse(request.url, body=content, request=request)
