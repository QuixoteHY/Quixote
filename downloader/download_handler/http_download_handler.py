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
        print(request.method.lower(), request.temp_body)
        print(request.headers.get_aiohttp_headers())
        response = await self.session.request(request.method.lower(), request.url,
                                              **{'headers': request.headers.get_aiohttp_headers(),
                                                 'data': request.temp_body})
        content = await response.read()
        await asyncio.sleep(1.8)
        print('********************', type(response.url), str(response.url))
        return HtmlResponse(str(response.url), body=content, request=request)
